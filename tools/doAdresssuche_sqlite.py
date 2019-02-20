# -*- coding: utf-8 -*-

#!/usr/bin/python



from qgis.PyQt import QtGui, QtCore, QtSql
from qgis.core import *
from qgis.gui import *
from gui_blattschnitte import *
from gui_adresssuche_sqlite import *
#from doVermessung import *
from ladefortschritt import *
from ProjektImport import *
from doTextAnno import *

import sys



class AdrDialogSQLITE(QtWidgets.QDialog, Ui_frmAdresssuche):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_adressuche,pfad = None, name = None):
        QtWidgets.QDialog.__init__(self,parent)
        Ui_frmAdresssuche.__init__(self)


        self.iface = iface

        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.name = name
        self.Gemeinde = ""
        self.Strasse = ""
        self.Nummer = ""
        self.Adresscode = []
        self.Rechtswert = []
        self.Hochwert = []
        self.Strasse = []
        self.Hausnummer = []
        self.MainWindow = parent
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        self.speicheradressen_adressuche = speicheradressen_adressuche
        self.suchrichtungsFlag = False
        self.buttonGroup.setExclusive(True)


        #Referenz auf die Datenquelle
        #direkt über SQLITE
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")
        self.db.setDatabaseName(self.pfad + self.name + ".sqlite")
        self.db.setConnectOptions('QSQLITE_OPEN_READONLY')


        #falls es länger dauert, ein kurzes Infofenster
        #für den Anwender
        self.info = LadefortschrittDialog()
        self.info.show()
        self.info.repaint()  #sonst bleibt das Fenster leer!

        #fehlverbindung abfangen
        if  not (self.db.open()):
            QtWidgets.QMessageBox.about(None, "Achtung", ("Öffnen Adressdaten gescheitert"))
            return

        #Abfragen instanzieren
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrageStrasse = QtSql.QSqlQuery(self.db)
        self.abfrageNummer = QtSql.QSqlQuery(self.db)

        #Modelle instanzieren (Anzeige im Listenfeld)
        self.modell_adresscode = QtSql.QSqlQueryModel()
        self.modell_strasse = QtSql.QSqlQueryModel()
        self.modell_nummer = QtSql.QSqlQueryModel()
        self.modelli = QtSql.QSqlQueryModel()

        self.abfrage.exec_("SELECT DISTINCT GEMEINDE  FROM adressen ORDER by GEMEINDE")

        #Nach dem Startbereits die
        #Liste mit den Gemeinden füllen
        self.modelli.setQuery(self.abfrage)
        self.lstGemeinde.setModel(self.modelli)


        #Nach dem Startbereits die
        #Liste mit den Strassennamen füllen
        #da diese etwas mehr sind wird das gesamte Holen
        #von der Datenbank erzwungen

        self.lstStrasse.setModel(self.modell_strasse)


        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)


        #Infofenster für den Benutzer anschließend schließen
        self.info.close()

        #selection Changed Signal der Listenfelder implementieren
        #das geht wie folgt
        self.SelModelG = self.lstGemeinde.selectionModel()
        self.SelModelG.currentChanged.connect(self.currentChangedG)

        self.SelModelS = self.lstStrasse.selectionModel()
        self.SelModelS.currentChanged.connect(self.currentChangedS)


        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)


    #Wenn auf 'im View darstellen' geklickt wird
    def accept(self):

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

        while (self.abfrageNummer.isValid()):
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


            #next(self.abfrageNummer)
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


    #klickt man in das Listenfeld Gemeinde
    #werden die dazugehörigen Strassen aus der DB geholt und
    #in ein Listenfeld eingetragen  und in eine sql abfrage

    def lstGemeindeKlicked(self,Index):


        if self.suchrichtungsFlag:
            self.Gemeinde = Index.data()#.toString()
            self.abfrageStrasse.exec_("SELECT DISTINCT Hausnr  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "' order by Hausnr")
            self.modell_nummer.setQuery(self.abfrageStrasse)
            self.lstNummer.setModel(self.modell_nummer)
            self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "'")
            self.abfrageNummer.first()
        else:
            self.lstStrasse.reset()
            self.Gemeinde = Index.data()

            self.abfrage.exec_("SELECT DISTINCT Strasse  FROM adressen where Gemeinde = '" + self.Gemeinde + "' order by Strasse")
            self.modell_strasse.setQuery(self.abfrage)
            self.lstStrasse.setModel(self.modell_strasse)
            self.abfrageStrasse.clear()
            self.modell_nummer.setQuery(self.abfrageStrasse)
            self.lstNummer.setModel(self.modell_nummer)



    #klickt man in das Listenfeld Strasse
    #werden die dazugehörigen Hausnummern aus der DB geholt und
    #in ein Listenfeld eingetragen und in eine sql abfrage
    def lstStrasseKlicked(self,Index, Index2 = None):

        self.Strasse = Index.data() #.toString()

        if self.suchrichtungsFlag:

            #gemeinden aktualisieren
            self.lstGemeinde.reset()
            self.abfrage.exec_("SELECT DISTINCT Gemeinde  FROM adressen where Strasse = '" + self.Strasse + "' order by Gemeinde")
            self.modelli.setQuery(self.abfrage)

            self.lstGemeinde.setModel(self.modelli)

            if len(self.lstGemeinde.selectedIndexes()) > 0 :
                self.abfrageStrasse.exec_("SELECT DISTINCT Hausnr  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "' order by Hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

            else:
                self.abfrageStrasse.exec_("SELECT DISTINCT Hausnr  FROM adressen where  Strasse = '"+ self.Strasse + "' order by Hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

        else:

            if len(self.lstGemeinde.selectedIndexes()) > 0 :
                self.abfrageStrasse.exec_("SELECT DISTINCT Hausnr  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "' order by Hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()
            else:
                self.abfrageStrasse.exec_("SELECT DISTINCT Hausnr  FROM adressen where  Strasse = '"+ self.Strasse + "' order by Hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()


    #klickt man in das Listenfeld Hausnummer
    #werden die dazugehörigen Hausnummern aus der DB geholt und
    #in eine sql abfrage eingetragen
    def lstNummerKlicked(self,Index):

        #für die Mehrfachauswahl an Adressen wird ein
        #Liste mit Indices benötigt
        NummernListe = self.lstNummer.selectedIndexes()

        sql_part = ""
        for indi in NummernListe:   #die liste durchgehen und den SQL Teil erzeugen
            if sql_part == "":
                sql_part = "Hausnr = '" + indi.data() + "'"
            else:
                sql_part = sql_part + " or Hausnr = '" + indi.data() + "'"

        if len(self.lstGemeinde.selectedIndexes()) > 0 :
            self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where Gemeinde = '" + self.Gemeinde + "' and Strasse = '"+ self.Strasse + "' and ( " + sql_part + ")")
        else:
            self.abfrageNummer.exec_("SELECT ADRSUBCD,RECHTSWERT,HOCHWERT,STRASSE,HAUSNR  FROM adressen where  Strasse = '"+ self.Strasse + "' and ( " + sql_part + ")")
        self.modell_adresscode.setQuery(self.abfrageNummer)
        self.abfrageNummer.first()


    #Methode führt das eigentliche einzeichnen der Adessen
    #ins Mapfenster aus. Diese sind dan QgsTExtAnnotationItems wie
    #die "Sprechblasen" die man einzeichnen kann
    def AdrZoomtextAnnoXY(self):

        mc=self.iface.mapCanvas()

        #ist nur eine Adresse ausgewählt worden
        #(wenn der User ins Listenfeld Hausnummer klickt)
        if len(self.Adresscode) == 1:
            height2 = 50 #50m Toleranz
            width2 = 50 #50m Toleranz
            rect = QgsRectangle(self.Rechtswert[0] -width2, self.Hochwert[0] -height2, self.Rechtswert[0] +width2, self.Hochwert[0] +height2)

        #oder werden alle Adressen einer Strasse abgefragt
        #bzw. mehrer Nummern durch den User ausgwählt
        elif len(self.Adresscode) > 1:

            rect = QgsRectangle(self.minX - 50, self.minY - 50, self.maxX + 50, self.maxY + 50)
            #Maßsstab berechnen
            scaleA = mc.scale()
            hA = mc.extent().height()
            wA = mc.extent().width()

            m = 0
            if hA / rect.height() > wA / rect.width() :
                m = hA / rect.height()
            else:
                m = wA / rect.width()
            scale = scaleA / m
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

            # QtWidgets.QMessageBox.about(None, "Query", self.Hausnummer[i])
            #Der Adresstext als Textdokument
            text = QtGui.QTextDocument(self)
            text.setObjectName("adressen" +  self.Strasselist[i] + self.Hausnummer[i])

            # Das Fontobjekt fürs Textobjekt
            font = QtGui.QFont()
            font.setPointSize(12)
            text.setDefaultFont(font)
            text.setHtml("<font color = \"#FF0000\">" + self.Strasselist[i] + " " + self.Hausnummer[i] + "</font>")

            # Hilfspunkt zur Text/Kreuzchen Positionierung
            punkti = QgsPointXY(self.Rechtswert[i],self.Hochwert[i])

            # Offset der Textposition
            Offset = QtCore.QPointF()
            Offset.setX(0)
            Offset.setY(0)

            # Benötigte Framgröße
            frame_groesse = text.size()

             # Das spezielle QgsMapCanvasAnnotationItem Objekt
            zeichne_mich = draw_text_class(mc, self.Strasselist[i] + ' ' + self.Hausnummer[i],props,punkti,Offset)
            self.textanno = zeichne_mich.gen()

            # die Adresse jedes Annotationobjekt wird in einen Listenvariable-Pointer
            # geschrieben. Dadurch gehen sie beim Schließen des Adresswidget nicht verloren sondern
            # bleiben dem Vogis Menü Plugin erhalten (zum späteren löschen notwendig)!!
            self.speicheradressen_adressuche.append(self.textanno)

            i = i + 1

        mc.refresh()



    #Nimmt das Linedit für die Strassensuche ein Enter
    #Ereignis auf, dann wird diese MEthode aufgerufen
    #Ist das feld leer, wird die Suche zurückgesetzt, ansonsten
    #wird der Text (der für die Strassensuche vom User eingegeben wurde)
    #in der Adressdatenbank gesucht
    def strassensuche(self):

        self.suchrichtungsFlag = True   # brauchts damit ich weiß, ob ich die strassensuche benützt habe!


        self.info.show()
        self.info.repaint()


        if self.leStrasse.text() != "": #das feld enthät einen Text! Suche wird durchgeführt
            self.lstStrasse.reset()
            self.abfrageStrasse.exec_("SELECT DISTINCT STRASSE  FROM adressen where Strasse Like '" + self.leStrasse.text() + "%'")
            next(self.abfrageStrasse)
            self.modell_strasse.setQuery(self.abfrageStrasse)
            self.lstStrasse.setModel(self.modell_strasse)

        else:   #das Feld ist leer, die Suche wird zurückgesetzt
            self.suchrichtungsFlag = False
            self.lstGemeinde.reset()
            self.abfrage.exec_("SELECT DISTINCT GEMEINDE  FROM adressen")
            next(self.abfrage)
            self.modelli.setQuery(self.abfrage)
            self.lstGemeinde.setModel(self.modelli)

            #den neuen Mittelpunkt ermitteln und die Gemeinde
            #im Listenfeld dafür auswählen
            mittelpunkt = self.findemittelpunkt()
            self.returnGemeinde(mittelpunkt)

        self.info.close()



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
        gmdLayer.removeSelection()



        if  (len(Liste) > 0):
            self.auswahlaenderung(Liste[0].attribute('PGEM_NAME'))

        else:   #WICHTIG!! ist der Extent so daß mit der Ermittlung des Mittelpunkts
                #keine Gemeinde gefunden wird, stellen wir auf Sonntag!
            wert = "Sonntag"
            self.auswahlaenderung(wert )

        mc.setRenderFlag(True)



    #Methode Aktualisiert nur das zweite Listenfeld für die Gemeinde

    def auswahlaenderung(self,SelItem = None,Nummer = None):


        self.Gemeinde = SelItem
        self.lstGemeinde.keyboardSearch(SelItem)
        index = self.lstGemeinde.selectedIndexes()

        try:
            if not index == None:
                self.lstGemeinde.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
        except:
            QtWidgets.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder')
            pass


    def currentChangedG(self,a,b):
        self.lstGemeindeKlicked(a)

    def currentChangedS(self,a,b):
        self.lstStrasseKlicked(a)




    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def themenLaden(self):

        self.iface.mapCanvas().setRenderFlag(False)


        #falls es länger dauert, ein kurzes Infofenster
        #für den Anwender
        self.info = LadefortschrittDialog()
        self.info.show()
        self.info.repaint()  #sonst bleibt das Fenster leer!


        uri = QgsDataSourceUri()
        uri.setDatabase(self.pfad + "adressen.sqlite")
        schema = ""
        table = "Adressen"
        geom_column = "the_geom"

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():

            if button.isChecked():  #wenn gechecked wird geladen

                if   (("Landesfläche") in button.text()):

                    #adressen laden
                    uri.setDataSource(schema, table, geom_column)
                    adressen = QgsVectorLayer(uri.uri(), "Adressen","spatialite")

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
                    uri.setDataSource(schema, table, geom_column, "GEMEINDE = '" + self.Gemeinde + "'")


                    #adressen laden
                    adressen = QgsVectorLayer(uri.uri(),"Adressen-" + self.Gemeinde,"spatialite")
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

        self.info.close()


        self.iface.mapCanvas().setRenderFlag(True)


    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)
        self.close()

