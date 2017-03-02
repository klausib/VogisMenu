# -*- coding: utf-8 -*-
#!/usr/bin/python


from PyQt4 import QtGui, QtCore, QtSql


from qgis.core import *
from qgis.gui import *
from gui_blattschnitte import *
from gui_adresssuche_pg import *
from doVermessung import *
from ladefortschritt import *
from osgeo import ogr

#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import sys, re


class AdrDialogPG(QtGui.QDialog, Ui_frmAdresssuche):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_adressuche,pfad = None, db = None, schema = '', table = ''):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmAdresssuche.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.Gemeinde = ""

        self.Adresscode = []
        self.Rechtswert = []
        self.Hochwert = []
        self.Strasselist = []
        self.Hausnummer = []


        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        self.speicheradressen_adressuche = speicheradressen_adressuche

        self.buttonGroup.setExclusive(True)
        self.db = db
        self.table = table
        self.schema = schema
        self.tablename = schema + '.' + table

        self.db.open()

        self.abfrage = object()
        self.abfrageNummer = object()

        self.FlagTreeWahl = ''



        #Abfragen instanzieren
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrageNummer = QtSql.QSqlQuery(self.db)

        # Das Model
        self.ModelTree = QtGui.QStandardItemModel()



        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)



        # Die Nötigen Signale einbinden
        QtCore.QObject.connect(self.leStrasse, QtCore.SIGNAL("textEdited (const QString&)"),self.strassensuche)
        QtCore.QObject.connect(self.treeAdressen, QtCore.SIGNAL("clicked (const QModelIndex&)"),self.TreeClicked)
        QtCore.QObject.connect(self.btnEinklappen, QtCore.SIGNAL("clicked ()"),self.einklappen)


        # Focus auf der Eingabefeld für die Strassensuche
        self.leStrasse.setFocus()
        self.strassensuche()


        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)



    # Tree View Elemente zuklappen
    def einklappen(self):
        self.treeAdressen.collapseAll()


    # Wenn auf 'im View darstellen' geklickt wird
    # die gewählte Adresse (oder alle Adressen einer Strasse) zeichnen
    def accept(self):


        # im treeview auf die Nummer geklickt
        if self.FlagTreeWahl == 'Nummer':
            self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.treeAdressen.selectedIndexes()[0].parent().parent().data() + "' and strasse = '"+ self.treeAdressen.selectedIndexes()[0].parent().data() + "' and hausnr = '" + self.treeAdressen.selectedIndexes()[0].data() + "'")
            self.abfrageNummer.first()
        # im treeview auf die strasse geklickt
        elif self.FlagTreeWahl == 'Strasse':
            #QtGui.QMessageBox.about(None, "Achtung", 'Strasse')
            self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.treeAdressen.selectedIndexes()[0].parent().data() + "' and strasse = '"+ self.treeAdressen.selectedIndexes()[0].data() + "'")
            self.abfrageNummer.first()
        else:   # mache nichts
            return

        #Variablen neu initialisieren
        self.Adresscode = []
        self.Rechtswert = []
        self.Hochwert = []
        self.Strasselist = []
        self.Hausnummer = []
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        durchlaufflag = 0

        #Listenvariablen (für Mehrfachauswahl) mit den Werten aus der SQL Abfrage
        #füllen und zugelich den Zoomextent bestimmen
        while self.abfrageNummer.isValid():
            if ((not self.abfrageNummer.value(0) == None) and (not self.abfrageNummer.value(1) == None) and (not self.abfrageNummer.value(2) == None) and
                (not self.abfrageNummer.value(3) == None) and (not self.abfrageNummer.value(4) == None)):

                self.Adresscode.append(self.abfrageNummer.value(0))
                self.Rechtswert.append(self.abfrageNummer.value(1))   #die Variants sind Listen mit 2 Items bei toDouble!!
                self.Hochwert.append(self.abfrageNummer.value(2))   #die Variants sind Listen mit 2 Items bei toDouble!!
                self.Strasselist.append(self.abfrageNummer.value(3))
                self.Hausnummer.append(self.abfrageNummer.value(4))

            #Extent der Adressauswahl ermitteln
            if durchlaufflag == 0:
                self.maxX = self.abfrageNummer.value(1)
                self.minX = self.abfrageNummer.value(1)
                self.maxY = self.abfrageNummer.value(2)
                self.minY = self.abfrageNummer.value(2)
            else:

                if self.abfrageNummer.value(1) > self.maxX:
                    self.maxX = self.abfrageNummer.value(1)
                elif self.abfrageNummer.value(1) < self.minX:
                    self.minX = self.abfrageNummer.value(1)

                if self.abfrageNummer.value(2) > self.maxY:
                    self.maxY = self.abfrageNummer.value(2)
                elif self.abfrageNummer.value(2) < self.minY:
                    self.minY = self.abfrageNummer.value(2)

            self.abfrageNummer.next()
            durchlaufflag = 1

        #Methode zeichnet die Adressen in das View Fenster von QGIS
        self.AdrZoomtextAnnoXY()




    #eingezeichnete Adressen löschen. Über Pointer
    #werden deren Speicheradressen aufgezeichnet und im Hauptobjekt des VogisMenü gespeichert
    #und immer mitübergeben. Dadurch gehen sie solange das Vogis Menü
    #aktiv ist nicht verloren und können immer wieder gelsöcht werden
    def adrClear(self):
        mc=self.iface.mapCanvas()
        #die Grafiken sind in einer QGraphicsItemScene
        # die man leider undokumentiert über mc.scene() bekommt!!

        if len(self.speicheradressen_adressuche) > 0:
            for items in self.speicheradressen_adressuche:
                try:
                    mc.scene().removeItem(items)
                except:
                    pass
        mc.refresh()



    # klickt man in den Tree View auf eine Gemeinde
    # werden die dazugehörigen Strassen aus der DB geholt
    # und als child drangehängt. Das slebe passiert,
    # wenn man auf die strasse klickt. Dann werden die
    # Nummern aus der DB geholt und als Child
    # drangehängt
    def TreeClicked(self,Index):


        # es sind noch keine daten aus der db geholt und in den tree eingetragen worden
        # jeweils sowohl für den Klick auf die Gemeinde ODER Strasse
        # UND es wird auch nicht über das text Edit Feld für die Strassensuche gesucht - d.h. es wird ins Tree View gklickt!!
        # der Tree ist nicht nicht befüllt
        if len(self.leStrasse.text()) == 0 and not Index.model().hasChildren(Index):


            self.FlagTreeWahl = ''

            if Index.parent().data() != None and Index.parent().parent().data() == None:   # Es wird auf den Strassennamen geklickt, der hat einen Parent (die Gemeinde)
                self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + Index.parent().data() + "' and strasse = '" + Index.data() + "' order by gemeinde,strasse,hausnr")
                self.FlagTreeWahl = 'Strasse'
            elif Index.parent().data() == None: # Es wird auf den Gemeindenamen geklickt , er hat keinen Parent
                self.abfrage.exec_("select distinct gemeinde,strasse  from  " + self.tablename + "  where gemeinde = '" + Index.data() + "' order by gemeinde,strasse")
                self.FlagTreeWahl = 'Gemeinde'
            else:   # Hausnummer wird angeklickt
                self.FlagTreeWahl = 'Nummer'


            gemeindestrasse = ''
            gemeindestrassenummer = ''

            #if self.ModelTree.itemFromIndex(Index).parent() == None: # Gemeinde!
            if self.FlagTreeWahl == 'Gemeinde':
                eins = self.ModelTree.itemFromIndex(Index)
                eins.setEditable(False)
                #QtGui.QMessageBox.about(None, "0", Index.data())
                while self.abfrage.next():
                            zwei = QtGui.QStandardItem(self.abfrage.value(1))
                            zwei.setEditable(False)
                            eins.appendRow(zwei)
                            gemeindestrasse = self.abfrage.value(0) + self.abfrage.value(1)

            if self.FlagTreeWahl == 'Strasse':
                zwei = self.ModelTree.itemFromIndex(Index)


                while self.abfrage.next():
                    drei = QtGui.QStandardItem(self.abfrage.value(2))
                    drei.setEditable(False)
                    zwei.appendRow(drei)



            self.treeAdressen.setModel(self.ModelTree)

        else:   # es wird in das Tree View geklickt, der Tree ist aber schon befüllt!!
            self.FlagTreeWahl = ''
            if Index.parent().data() != None and Index.parent().parent().data() == None:   # Es wird auf den Strassennamen geklickt, der hat einen Parent (die Gemeinde)
                self.FlagTreeWahl = 'Strasse'

            elif Index.parent().data() == None: # Es wird auf den Gemeindenamen geklickt , er hat keinen Parent
                self.FlagTreeWahl = 'Gemeinde'
            else:   # Hausnummer wird angeklickt
                self.FlagTreeWahl = 'Nummer'



    # Methode führt das eigentliche einzeichnen der Adessen
    # ins Mapfenster aus. Diese sind dan QgsTExtAnnotationItems wie
    # die "Sprechblasen" die man einzeichnen kann
    def AdrZoomtextAnnoXY(self):

        mc=self.iface.mapCanvas()

        #ist nur eine Adresse ausgewählt worden
        #(wenn der User ins Listenfeld Hausnummer klickt)
        #QtGui.QMessageBox.about(None, "Achtung", str(self.Adresscode))
        if len(self.Adresscode) == 1:
            height2 = 50 #50m Toleranz
            width2 = 50 #50m Toleranz
            rect = QgsRectangle(self.Rechtswert[0] -width2, self.Hochwert[0] -height2, self.Rechtswert[0] +width2, self.Hochwert[0] +height2)
        #oder werden alle Adressen einer Strasse abgefragt
        #bzw. mehrer Nummern durch den User ausgwählt
        elif len(self.Adresscode) > 1:
            rect = QgsRectangle(self.minX - 50, self.minY - 50, self.maxX + 50, self.maxY + 50)
            #Maßsstab berechnen
##            scaleA = mc.scale()
##            hA = mc.extent().height()
##            wA = mc.extent().width()
##
##            m = 0
##
##            if hA / rect.height() > wA / rect.width() :
##                m = hA / rect.height()
##            else:
##                m = wA / rect.width()
##
##            #QtGui.QMessageBox.about(None, "Achtung", str(hA) + ' ' + str(wA) + ' ' +str(m) + ' ' + str(rect.asWktCoordinates()))
##            scale = scaleA / m

        else:
            return


        # Extent setzen
        mc.setExtent(rect)

        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,0,0', 'color_border' : '255,0,0' , 'name' : 'cross', 'size' : '4' }

        i = 0
        #schleife geht alle ausgewählten adressen
        #durch (ein oder alle der Strasse) und zeichnet sie ins Mapfernster
        while i < len(self.Adresscode):


            #Der Adresstext als Textdokument
            text = QtGui.QTextDocument(self)
            text.setObjectName("adressen" +  self.Strasselist[i] + self.Hausnummer[i])


            # Das Fontobjekt fürs Textobjekt
            font = QtGui.QFont()
            font.setPointSize(12)
            text.setDefaultFont(font)
            text.setHtml("<font color = \"#FF0000\">" + self.Strasselist[i] + " " + self.Hausnummer[i] + "</font>")
            # text.setHtml("<font color = \"#FF0000\">" + self.Strasselist[i]  + "</font>")

            # Hilfspunkt zur Text/Kreuzchen Positionierung
            punkti = QgsPoint(self.Rechtswert[i],self.Hochwert[i])

            # Offset der Textposition
            Offset = QtCore.QPointF()
            Offset.setX(0)
            Offset.setY(0)

            # Benötigte Framgröße
            frame_groesse = text.size()


            # DAS objekt um Kreuzchen und Text zu zeichnen
            textAnno = QgsTextAnnotationItem(self.iface.mapCanvas())
            textAnno.setFrameSize(frame_groesse)   # ohne Framgröße keine Darstellung im Drucklayout
            textAnno.setMapPosition(punkti)
            textAnno.setFrameBorderWidth(0.0)
            textAnno.setOffsetFromReferencePoint(Offset)

            textAnno.setDocument(text)      #Text zuweisen
            farbe = textAnno.frameColor()   #die Framefarbe auf unsichtbar schalten
            farbe.setAlpha(0)               #sonst gibts ein kleines Darstellungsartefakt
            textAnno.setFrameColor(farbe)

            # textAnno.setMarkerSymbol geht nicht!!
            # deshalb so: wir wollen nicht den Standardknödel
            # sondern ein rotes Kreuzchen
            s = textAnno.markerSymbol() #1. das eingestellte Marker Symbol holen
            # Die neuen Properties...
            sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)   #in der Schleife sonst Probleme im Qgis

            s.changeSymbolLayer(0,sl)   #2. das neue Symbol zuweisen

            i = i + 1

            # die Adresse jedes Annotationobjekt wird in einen Listenvariable-Pointer
            # geschrieben. Dadurch gehen sie beim Schließen des Adresswidget nicht verloren sondern
            # bleiben dem Vogis Menü Plugin erhalten (zum späteren löschen notwendig)!!
            self.speicheradressen_adressuche.append(textAnno)

        mc.refresh()



    # Nimmt das Linedit für die Strassensuche ein Edit
    # Ereignis auf, dann wird diese Methode aufgerufen
    # Ist das feld leer, wird die Suche zurückgesetzt, ansonsten
    # wird der Text (der für die Strassensuche vom User eingegeben wurde)
    # in der Adressdatenbank gesucht
    def strassensuche(self, text = None):

        self.nummer = []
        QtGui.QMessageBox.about(None, "Achtung", 'strassensuche')
        if text == None or text == '' or len(text) < 3:
            text = '_alles_'    # nur die Gemeinden aus der DB holen

        self.nummer = re.findall(r'\d+',text)   # enthält der text eine zahl - wenn ja wird sie extrahiert

        if  len(self.nummer) > 0:   # zahl ist vorhanden
            self.nummer = string.strip(self.nummer[0])
            position = text.index(self.nummer)
            text = string.strip(text[0:position])
        else:
            self.nummer = '' # Wenn keine Nummer eingegeben

        # Wie auch immer, Leerzeichen vorne und hinten werden entfernt
        text = string.strip(text)


        if text != "" and len(text) > 3: #das edit feld enthät einen Text! Suche wird durchgeführt
            if  len(self.nummer) > 0:   # und auch eine nummer gibts - gemeinde strasse und nummer aus der db
                self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) LIKE '%" + string.lower(self.nummer) + "%') order by gemeinde,strasse,hausnr")

            else:   # keine nummer
                #Sortierung wichtig!
                if text == '_alles_':   # nur die gemeinden abfragen aus der db
                    self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + " order by gemeinde")
                else:   # gemeindenund strasse abfrage aus er db
                    self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where LOWER(strasse) Like '%" + string.lower(text) + "%' order by gemeinde,strasse")



            # tree view und model jedesmal
            # initialisieren
            self.treeAdressen.reset()
            self.ModelTree.clear()

            gemeindestrasse = ''
            gemeindestrassenummer = ''


            # DER Kernpunkt: Das Model mit dem Ergebnis
            # der Query (richtig) befüllen:
            # die Ergebnis Rekords der abfrage durchgehen
            # und unser Standard Itme Model damit befüllen
            # das geht wie folgt:
            # ACHTUNG: Das funktioniert nur, wenn das Ergbnis
            # der Abfrage mit DISTINCT (alphabetische)geordnet ist!!!
            while self.abfrage.next():
                if not self.ModelTree.findItems(self.abfrage.value(0),QtCore.Qt.MatchRecursive,0):  # Die Gemeinde ist noch nicht als Item im Model -> Hinzufügen
                    eins = QtGui.QStandardItem(self.abfrage.value(0))
                    self.ModelTree.appendRow(eins)

                if not self.abfrage.value(1) == None:
                    if not gemeindestrasse == self.abfrage.value(0) + self.abfrage.value(1):    # die Kombination Gemeinde und Strasse (Strasse als Child von Gemeinde)
                        zwei = QtGui.QStandardItem(self.abfrage.value(1))                       # ist noch noch nicht im Model -> HINZUFÜGEN
                        eins.appendRow(zwei)
                        gemeindestrasse = self.abfrage.value(0) + self.abfrage.value(1)

                if not self.abfrage.value(2) == None:
                    if not gemeindestrassenummer == self.abfrage.value(0) + self.abfrage.value(1)+ self.abfrage.value(2):    # die Kombination Gemeinde und Strasse und Huasnummer(Hausnummer als Child von Strasse)
                        drei = QtGui.QStandardItem(self.abfrage.value(2))                                                    # ist noch noch nicht im Model -> HINZUFÜGEN
                        zwei.appendRow(drei)
                        gemeindestrassenummer = self.abfrage.value(0) + self.abfrage.value(1)+ self.abfrage.value(2)



            # Unser Tree View bekommt das Model umd
            # das ergebnis dem User anzuzeigen
            self.treeAdressen.setModel(self.ModelTree)

            QtGui.QMessageBox.about(None, "Achtung", str('im if ') + text)

        else:   #das Edit Feld ist leer, die Suche wird zurückgesetzt

            #den neuen Mittelpunkt ermitteln und die Gemeinde
            #im Listenfeld dafür auswählen
            QtGui.QMessageBox.about(None, "Achtung", str('mittelpunkt'))
            mittelpunkt = self.findemittelpunkt()
            self.returnGemeinde(mittelpunkt)




    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):
        mc = self.iface.mapCanvas()
        Punkt = mc.extent().center()
        return Punkt



    #Ermittelt anhand des aktuellen Kartenmittelpunkts (Variable ergebnis)
    #im QGIS den Namen passende Gemeinde und ruft die
    #Routine zum Aktualisieren des Listenfelds auf
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde. Wird auch aufgerufen,
    #wenn die Gemeinde mit dem roten Kreuzchen ausgewählt wird
    def returnGemeinde(self,ergebnis):

        mc=self.iface.mapCanvas()

        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er automatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in mc.layers():
            if vorhanden.name() == "Gemeinden":
                yes = True
                break

        if yes:
            gmdLayer = vorhanden
        else:
            #L = QtCore.QStringList()
            #wert = QtCore.QString("Sonntag")
            self.auswahlaenderung("Sonntag")
            return

        #damit nichts flackert
        mc.setRenderFlag(False)

        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des Features der betreffenden politischen Gemeinde
        #im Gemeindelayer in QGIS
        shift=mc.mapUnitsPerPixel()
        wahlRect = QgsRectangle(ergebnis.x(),ergebnis.y(),ergebnis.x()+ shift,ergebnis.y()+ shift)
        #Entsprechendes Feature (=Gemeinde) im Layer selektieren
        gmdLayer.select(wahlRect,False)

        Liste = gmdLayer.selectedFeatures()

        #Auswahl wieder löschen
        gmdLayer.removeSelection()




        if  (len(Liste) > 0):
            self.auswahlaenderung(Liste[0].attribute('PGEM_NAME'))
        else:   #WICHTIG!! ist der Extent so daß mit der Ermittlung des Mittelpunkts
                #keine Gemeinde gefunden wird, stellen wir auf Sonntag!
            wert = "Sonntag"
            self.auswahlaenderung(wert )

        mc.setRenderFlag(True)


    #Methode Aktualisiert das tree view
    def auswahlaenderung(self,SelItem = None,Nummer = None):

        self.Gemeinde = SelItem
        #self.lstGemeinde.keyboardSearch(SelItem)
        #QtGui.QMessageBox.about(None, "Achtung",self.Gemeinde)
        self.treeAdressen.keyboardSearch(SelItem)


        #index = self.lstGemeinde.selectedIndexes()
        index = self.treeAdressen.selectedIndexes()

        try:
            #QtGui.QMessageBox.about(None, "Achtung D",str(index))
            if not len(index) < 1:

                self.treeAdressen.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            else:
                #QtGui.QMessageBox.about(None, "Achtung else",str(index))
                index = self.treeAdressen.rootIndex()

        except:
            #QtGui.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
            pass


    #Klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def themenLaden(self):

        self.iface.mapCanvas().setRenderFlag(False)


        #adressen = ProjektImport(self.iface )   #das Projekt Import Objekt instanzieren
        uri = QgsDataSourceURI()
        #uri.setDatabase(self.pfad + "adressen.sqlite")
        uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(),'','')  # Keine Kennwort nötig, Single Sign On
        #schema = "vorarlberg"
        #table = "adressen"


        # Geometriespalte bestimmen -- geht nur mit OGR
        outputdb = ogr.Open('pg: host =' + self.db.hostName() + ' dbname =' + self.db.databaseName() + ' schemas=' + self.schema)
        geom_column = outputdb.GetLayerByName(string.lower(self.table)).GetGeometryColumn()


        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():


            if button.isChecked():  #wenn gechecked wird geladen

                if   (("Landesfläche").decode('utf-8') in button.text()):

                    #adressen laden
                    #uri.setDataSource(schema, table, geom_column)
                    uri.setDataSource(self.schema, self.table, geom_column)

                    adressen = QgsVectorLayer(uri.uri(), "adressen","postgres")
                    #adressen.setProviderEncoding("utf-8")


                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")
                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( adressen )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(adressen)

                elif   ("Gemeinde" in button.text()):

                    #den mittelpunkt des extent rausfinden
                    #und die passende Gemeinde im ListWidget einstellen
                    mittelpunkt = self.findemittelpunkt()
                    self.returnGemeinde(mittelpunkt)

                    uri.setDataSource(self.schema, self.table, geom_column, "gemeinde = '" + self.Gemeinde + "'")


                    #adressen laden
                    adressen = QgsVectorLayer(uri.uri(),"Adressen-" + self.Gemeinde,"postgres")
                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")
                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( adressen )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(adressen)


        self.iface.mapCanvas().setRenderFlag(True)

    #Reimplementierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):
        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)
        self.db= None
        self.close()
