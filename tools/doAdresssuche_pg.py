# -*- coding: utf-8 -*-

#!/usr/bin/python



from qgis.PyQt import QtGui, QtCore, QtSql


from qgis.core import *
from qgis.gui import *
from gui_adresssuche_pg import *
from gui_blattschnitte import *
#from ladefortschritt import *
from osgeo import ogr
from direk_laden import *
from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich
from doTextAnno import *

class AdrDialogPG(QtWidgets.QDialog, Ui_frmAdresssuche):



    # Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_adressuche,pfad = None, db = None, schema = '', table = ''):#, adressgrafik = None):

        QtWidgets.QDialog.__init__(self,parent)
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


        self.speicheradressen_adressuche = speicheradressen_adressuche      #enthält die GrafiksItemGroup mit allen Grafiken
                                                                            #vom User eingefügten Geonam Adresse.
                                                                            #Wird beim Schließen des Objektes an VogisMain zurückgegeben bzw.
                                                                            #beim erzeugen des Objektes dem Constructor übergeben (sonst ists halt None)
        self.buttonGroup.setExclusive(True)

        self.db = db
        self.table = table
        self.schema = schema
        self.tablename = schema + '.' + table

        self.db.open()

        self.abfrage = object()
        self.abfrageNummer = object()

        self.FlagTreeWahl = ''
        self.text = ''


        #Abfragen instanzieren
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrageNummer = QtSql.QSqlQuery(self.db)

        # Das Model
        self.ModelTree = QtGui.QStandardItemModel()

        adressen = object()


        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)


        # Die Nötigen Signale einbinden
        self.leStrasse.textEdited.connect(self.strassensuche)
        self.treeAdressen.clicked.connect(self.TreeClicked)
        self.btnEinklappen.clicked.connect(self.einklappen)


        # Focus auf der Eingabefeld für die Strassensuche
        self.leStrasse.setFocus()
        self.strassensuche()


        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)


        #QtWidgets.QMessageBox.about(None, "Fehler", str(self.speicheradressen_adressuche))


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
        if not Index.model().hasChildren(Index):

            self.FlagTreeWahl = ''


            # der user hat nach keiner Strasse gesucht sonern klickt
            # einfach in den hierarchischen Tree
            if str.strip(self.leStrasse.text()) == '':

                if Index.parent().data() != None and Index.parent().parent().data() == None:   # Es wird auf den Strassennamen geklickt, der hat einen Parent (die Gemeinde)
                    self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + Index.parent().data() + "' and strasse = '" + Index.data() + "' order by gemeinde,strasse,hausnr")
                    self.FlagTreeWahl = 'Strasse'

                elif Index.parent().data() == None: # Es wird auf den Gemeindenamen geklickt , er hat keinen Parent
                    self.abfrage.exec_("select distinct gemeinde,strasse  from  " + self.tablename + "  where gemeinde = '" + Index.data() + "' order by gemeinde,strasse")
                    self.FlagTreeWahl = 'Gemeinde'
                    self.Gemeinde = Index.data()

                else:   # Hausnummer wird angeklickt
                    self.FlagTreeWahl = 'Nummer'

            # der user hat in das Strassensuchen Feld was eingegeben,
            # dadurch wird die Auswahl auf diesen String eingeschränkt,
            # und erst danach klickt er in den hierarchischen Tree
            else:
                if Index.parent().data() != None and Index.parent().parent().data() == None:   # Es wird auf den Strassennamen geklickt, der hat einen Parent (die Gemeinde)
                    self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + Index.parent().data() + "'  and (strasse = '" + Index.data() + "' and LOWER(hausnr) LIKE '%" + str.lower(self.nummer) + "%') order by gemeinde,strasse,hausnr")
                    self.FlagTreeWahl = 'Strasse'

                elif Index.parent().data() == None: # Es wird auf den Gemeindenamen geklickt , er hat keinen Parent
                    self.abfrage.exec_("select distinct gemeinde,strasse  from  "  + self.tablename + "  where gemeinde = '" + Index.data() + "'  and (LOWER(strasse) Like '%" + self.text  + "%' and LOWER(hausnr) LIKE '%" + str.lower(self.nummer) + "%') order by gemeinde,strasse")
                    self.FlagTreeWahl = 'Gemeinde'
                    self.Gemeinde = Index.data()

                else:   # Hausnummer wird angeklickt
                    self.FlagTreeWahl = 'Nummer'


            gemeindestrasse = ''
            gemeindestrassenummer = ''


            if self.FlagTreeWahl == 'Gemeinde':
                eins = self.ModelTree.itemFromIndex(Index)
                eins.setEditable(False)

                while (self.abfrage.next()):
                            zwei = QtGui.QStandardItem(self.abfrage.value(1))
                            zwei.setEditable(False)
                            eins.appendRow(zwei)
                            gemeindestrasse = self.abfrage.value(0) + self.abfrage.value(1)

            if self.FlagTreeWahl == 'Strasse':
                zwei = self.ModelTree.itemFromIndex(Index)


                while (self.abfrage.next()):
                    if not self.abfrage.value(2) == None:
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

        else:
            return

        # Extent setzen
        mc.setExtent(rect)


        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,0,0', 'color_border' : '255,0,0' , 'name' : 'cross', 'size' : '4' }

        i = 0
        while i < len(self.Adresscode):
            punkti = QgsPointXY(self.Rechtswert[i],self.Hochwert[i])

            # Offset der Textposition
            Offset = QtCore.QPointF()
            Offset.setX(0)
            Offset.setY(0)

             # Das spezielle QgsMapCanvasAnnotationItem Objekt
            zeichne_mich = draw_text_class(mc, self.Strasselist[i] + ' ' + self.Hausnummer[i],props,punkti,Offset)
            self.textanno = zeichne_mich.gen()
            # die Adresse jedes Annotationobjekt wird in einen Listenvariable-Pointer
            # geschrieben. Dadurch gehen sie beim Schließen des Adresswidget nicht verloren sondern
            # bleiben dem Vogis Menü Plugin erhalten (zum späteren löschen notwendig)!!
            self.speicheradressen_adressuche.append(self.textanno)
            i = i + 1

        mc.refresh()


    # Nimmt das Linedit für die Strassensuche ein Edit
    # Ereignis auf, dann wird diese Methode aufgerufen
    # Ist das feld leer, wird die Suche zurückgesetzt, ansonsten
    # wird der Text (der für die Strassensuche vom User eingegeben wurde)
    # in der Adressdatenbank gesucht

    def strassensuche(self, text = None):

        self.nummer = []
        self.text = text

        if self.text == None or self.text == '' or len(self.text) <= 3:
            self.text = '_alles_'    # nur die Gemeinden aus der DB holen

        self.nummer = re.findall(r'\d+',self.text)   # enthält der text eine zahl - wenn ja wird sie extrahiert

        if  len(self.nummer) > 0:   # zahl ist vorhanden
            self.nummer = str.strip(self.nummer[0])
            position = self.text.index(self.nummer)
            self.text = str.strip(self.text[0:position])

        else:
            self.nummer = '' # Wenn keine Nummer eingegeben

        # Wie auch immer, Leerzeichen vorne und hinten werden entfernt
        self.text = str.strip(self.text)
        self.text = str.lower(self.text)


        # Erst ab drei Zeichen soll gesucht werden,
        # also die Minimaleingabe
        textlen = 3

        if self.text != "" and len(self.text) > textlen: #das edit feld enthät einen Text! Suche wird durchgeführt
            if  len(self.nummer) > 0:   # und auch eine nummer gibts - gemeinde strasse und nummer aus der db
                self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + self.text + "%' and LOWER(hausnr) LIKE '%" + str.lower(self.nummer) + "%') order by gemeinde,strasse,hausnr")

            else:   # keine nummer
                #Sortierung wichtig!
                if self.text == '_alles_':   # nur die gemeinden abfragen aus der db
                    self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + " order by gemeinde")
                else:   # gemeindenund strasse abfrage aus er db
                    self.abfrage.exec_("select distinct gemeinde,strasse,hausnr  from  " + self.tablename + "  where LOWER(strasse) Like '%" + self.text + "%' order by gemeinde,strasse")


        else:
            self.text = '_alles_'
            self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + " order by gemeinde")


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
        while (self.abfrage.next()):


            if not self.ModelTree.findItems(self.abfrage.value(0),QtCore.Qt.MatchRecursive,0):  # Die Gemeinde ist noch nicht als Item im Model -> Hinzufügen
                eins = QtGui.QStandardItem(self.abfrage.value(0))
                self.ModelTree.appendRow(eins)

        # Unser Tree View bekommt das Model um
        # das ergebnis dem User anzuzeigen
        self.treeAdressen.setModel(self.ModelTree)



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
        gmdLayer.selectByRect(wahlRect,False)

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
        self.treeAdressen.keyboardSearch(SelItem)


        index = self.treeAdressen.selectedIndexes()

        try:
            if not len(index) < 1:
                self.treeAdressen.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            else:
                index = self.treeAdressen.rootIndex()

        except:
            QtWidgets.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
            pass


    #Klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def themenLaden(self):

         # Der Username der verwendet werden soll
        if len(auth_user_global) > 0:    # Ist belegt
            auth_user = auth_user_global[0]
        else:
            auth_user = None


        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():


            if button.isChecked():  #wenn gechecked wird geladen

                if   (("Landesfläche") in button.text()):

                    adressen = direk_laden(self.db, "Adressen-Vorarlberg",'adressen',self.pfad + '\Vorarlberg"', self.iface)

                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtWidgets.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")

                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")

                        if not flagge[1]:
                            QtWidgets.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")

                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsProject.instance().addMapLayer(adressen)

                elif   ("Gemeinde" in button.text()):
                    adressen = direk_laden(self.db, "Adressen-" + self.Gemeinde,'adressen',self.pfad + self.Gemeinde, self.iface, 'gemeinde = \''+ self.Gemeinde +'\'')

                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtWidgets.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")

                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")

                        if not flagge[1]:
                            QtWidgets.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")

                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsProject.instance().addMapLayer(adressen)


        self.iface.mapCanvas().setRenderFlag(True)



    # Reimplementierung des closeEvents des Event Handlers!
    # Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    # Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    # das cliccked Signal nichts übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket

    def closeEvent(self,event = None):
        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)
        self.close()

