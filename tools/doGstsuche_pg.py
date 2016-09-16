# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtSql
import copy,string
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_blattschnitte import *
from gui_gstsuche import *
from osgeo import ogr


from gui_gstauswahl import *


#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *



#Klassendefinition für die Grundstückssuche, das Laden der DKM sowie der Urmappe
#und der Gebäudeumrisse
#class GstDialog (QtGui.QDialog,Ui_frmGstsuche,QtCore.QObject):
class GstDialogPG (QtGui.QDialog,Ui_frmGstsuche):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)



    #Initialisierung der Grudstückssuche
    #def __init__(self, parent,iface,dkmstand,pfad = None,vogisPfad = None):
    def __init__(self, parent,iface,dkmstand,pfad,PGdb = None, gemeindeliste = None):
        QtGui.QDialog.__init__(self,parent)
        #QtCore.QObject.__init__(self)
        Ui_frmGstsuche.__init__(self)

        self.iface = iface
        self.setupUi(self) #User Interface für Hauptfenster GST Suche initialisieren
        self.mc = self.iface.mapCanvas()
        self.vogisPfad = pfad
        self.db = PGdb
        self.gemeindeliste = gemeindeliste
        self.info = LadefortschrittDialog()
##
##
##        #falls es länger dauert, eine kurze Info
##        self.info = LadefortschrittDialog()
##        self.info.show()
##        self.info.repaint()  #sonst bleibt das Fenster leer!
##
##        if  self.db == None:
##            QtGui.QMessageBox.about(None, "Achtung",("Öffnen Datenbank gescheitert").decode("utf-8"))
##            return #wenns sich nicht öffnen läßt abbrechen
##
##        self.abfrage = QtSql.QSqlQuery(self.db)
##        self.abfrage2 = QtSql.QSqlQuery(self.db)
##        self.abfrage.exec_("SELECT DISTINCT PGEM_NAME  FROM vorarlberg.kat_gem order by PGEM_NAME")
##        #self.abfrage.last()
##        #QtGui.QMessageBox.about(None, "Achtung", str(self.abfrage.size()))
##
####        #Modell und Widget füllen
####        self.modelli = QtSql.QSqlQueryModel()
####        self.modell_kg = QtSql.QSqlQueryModel()
        self.modell_kg = QtGui.QStandardItemModel()
####        self.modelli.setQuery(self.abfrage)
####        self.lstPolgem.setModel(self.modelli)
##
##
##
##        #Modell und Widget füllen
##        self.modelli = QtGui.QStandardItemModel()
##        self.modell_kg = QtSql.QSqlQueryModel()
##
##        while self.abfrage.next():
##            eins = QtGui.QStandardItem(self.abfrage.value(0))
##            eins.setEditable(False)
##            self.modelli.appendRow(eins)
##
##        eins = QtGui.QStandardItem('Vorarlberg')
##        eins.setEditable(False)
##        self.modelli.appendRow(eins)
##        self.modelli.sort(0)


          #Modell und Widget füllen
        self.modelli = QtGui.QStandardItemModel()

        for item in self.gemeindeliste.keys():
            eins = QtGui.QStandardItem(item)
            eins.setEditable(False)
            self.modelli.appendRow(eins)
        #self.modelli.appendRow(eins)
        self.modelli.sort(0)

        self.lstPolgem.setModel(self.modelli)



        #Suchbutton wird deaktiviert, erst durch wahl KG-Gemeinde
        #im Listenfeld wird er aktiviert
        self.btnGstsuche.setDisabled(True)

        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)

        #Variablen definieren und None setzen.
        #Sind nicht immer mit Werten initialisiert und None kann in
        #If Abfragen unterschieden werden
        self.zoompunkt = None
        self.tool_vorher = None
        #self.Gemeinde = QtCore.QString()


        #Wir definieren einen eigenen Cursor: wird auf den
        #Button mit dem roten Kruez geklickt
        #bekommt der Mauscursor dieses Aussehen
        self.cursor = QtGui.QCursor(QtGui.QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #FFFFFF",
                                      "                ",
                                      "       +.+      ",
                                      "      ++.++     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " ++.    .    .++",
                                      " ... ...+... ...",
                                      " ++.    .    .++",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "   ++.     .+   ",
                                      "    ++.....+    ",
                                      "      ++.++     ",
                                      "       +.+      "]))


        self.auswahlBoxen.setExclusive(False)   #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                #deshlab hier: Mehrfachauswahl der Checkboxen möglich


        #Standardauswahl: die entsprechenden Checkboxen werden aktiviert
        self.standard_auswaehlen()

        #wieder ein optisches detail: die Hintergrundfarbe des Linedit
        #Feldes muß gleich der Fensterfarbe sein. Die wird vom System bestimmt.
        #Sonst scheuts komisch aus
        #Hintergrundfarbe des Linedit setzen
        Palette = QtGui.QPalette(self.palette())    #Palette nach Vorbild des Haupfensters (GST Suche) erzeugen
        HF = self.btnGstsuche.palette().window().color()    #Die Farbe des Hauptfensters holen
        Palette.setColor(QtGui.QPalette.Base, HF)   #Die Farbe des Base Bereichs auf die Farbe des Window Bereichs Haupfenster setzen
        self.gefunden.setPalette(Palette)   #Palette nun den Linedit zuweisen


        #dkm stand anzeigen: wird in Variable übergeben
        self.gbDkm.setTitle("Digitale Katastralmappe (DKM)      " + dkmstand)


        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)

        #das info Fenster schließen
        self.info.close()


        #Ein Maptool erzeugen das den Punkt zurückgibt (wenn man ins Kartnfenster klickt)
        self.PtRueckgabe = QgsMapToolEmitPoint(self.mc)


        #Die Signal Slot Verbindungen funktionieren besser,
        #wenn sie beim Initialisieren ersetzt werden!

        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)

        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!
        QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnGemeinde)




    def MapButtonZuruecksetzen(self,Tool_Gecklickt):
        if not self.PtRueckgabe is None:
            if  not (Tool_Gecklickt == self.PtRueckgabe):   #wenn ident, gleiche Speicheradresse!!
                #QtGui.QMessageBox.about(None, "Achtung", str(Tool_Gecklickt) + " gegen" + str(self.PtRueckgabe))
                self.btGmdChoice.setChecked(False)


    #Der Slots für die Signale des Gemeindeauswahlbuttons (rotes Kreuzchen)
    #Wird draufgeklickt wird diese Methode aufgerufen
    #Sie verändert das Aussehen des Cursors
    #und vor allem erzeugt ein Maptool bzw. setzt diese zurück! klickt man nun in die Karte wird
    #ein Signal ausgelöst das ein Punktobjekt mit den geklickten Koordinaten
    #Die Methode wird immer ausgeführ wenn auf den Kreuzchenknopf geklickt wird
    def gmd_choice_toggled(self):


        #Der Kreuzchenknopf ist gechecked
        if self.btGmdChoice.isChecked():

            # erstmal das vorher eingestellte Maptool
            #sicherstellen (um wieder zurücksetzen zu können!)
            self.tool_vorher = self.mc.mapTool()

            #Das Aussehen des Muascursor im QGIS Kartenbild
            #wird auf unseren Cursor gesetzt
            self.iface.mapCanvas().setCursor(self.cursor)


            #QGIS auf das neue Maptool einstellen!
            self.mc.setMapTool(self.PtRueckgabe)
            self.mc.setCursor(self.cursor)

        #Der Kreuzchenknopf ist nicht gechecked
        elif not(self.btGmdChoice.isChecked()):
            self.mc.setMapTool(self.tool_vorher)    #auf ursprüngliches Maptool und zugehörigen Cursor urücksetzen


    #Ermittelt anhand des aktuellen Kartenmittelpunkts (Variable ergebnis)
    #im QGIS den Namen passende Gemeinde und ruft die
    #Routine zum Aktualisieren des Listenfelds auf
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde. Wird auch aufgerufen,
    #wenn die Gemeinde mit dem roten Kreuzchen ausgewählt wird
    def returnGemeinde(self,ergebnis):



        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er automatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in self.mc.layers():
            if vorhanden.name() == "Gemeinden":
                yes = True
                break

        if yes:
            gmdLayer = vorhanden
        else:
            wert = "Sonntag"
            self.auswahlaenderung(wert )
            return

        #damit nichts flackert
        self.mc.setRenderFlag(False)

        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des Features der betreffenden politischen Gemeinde
        #im Gemeindelayer in QGIS
        shift=self.mc.mapUnitsPerPixel()
        wahlRect = QgsRectangle(ergebnis.x(),ergebnis.y(),ergebnis.x()+ shift,ergebnis.y()+ shift)
        #Entsprechendes Feature (=Gemeinde) im Layer selektieren
        gmdLayer.select(wahlRect,False)


        #Den Index des feldes PGEM_NAME
        #in der Attributtabelle des Layers finden
        #brauch ich um die grafisch ausgewählte Gemeinde
        #im Listenfeld optisch in die mitte zu holen
        Liste = gmdLayer.selectedFeatures()

        #Auswahl wieder löschen
        gmdLayer.removeSelection()


        # API für QGIS 2.0
        if  (len(Liste) > 0):
            self.auswahlaenderung(Liste[0].attribute('PGEM_NAME'))
        else:   #WICHTIG!! ist der Extent so daß mit der Ermittlung des Mittelpunkts
                #keine Gemeinde gefunden wird, stellen wir auf Sonntag!
            self.auswahlaenderung('Sonntag' )


        self.mc.setRenderFlag(True)

    # Auswahl der gesamten Landesflaeche
    # über einen Button
    def landesflaeche(self):
        self.auswahlaenderung('Vorarlberg')

    #Methode Aktualisiert nur das zweite Listenfeld für die KG - Gemeindenummer
    #Wird entweder von der Methode "returnGemeinde" oder
    #über eine Action beim Anklicken des Listenfeldes
    #mit der Gemeindenliste (politische) aufgerufen
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde
    def auswahlaenderung(self,SelItem = None,Nummer = None):

        self.gstsuche_deaktivieren()
        #Abhängig von wo aus die Methode aufgerufen wird
        #bekommt sie unterschiedliche Typen übergeben

        #if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!
        if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!

            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem
            self.lstPolgem.keyboardSearch(self.Gemeinde)
            index = self.lstPolgem.selectedIndexes()



            try:
                if not index == None:
                    self.lstPolgem.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            except:
                QtGui.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
                pass

        elif isinstance(SelItem, str):

            self.Gemeinde = SelItem
            self.lstPolgem.keyboardSearch(SelItem)
            index = self.lstPolgem.selectedIndexes()
            try:
                if not index == None:
                    self.lstPolgem.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            except:
                QtGui.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
                pass
        else:

            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem.data(0)

            try:
                if not SelItem == None:
                    self.lstPolgem.scrollTo(SelItem,3) #3 bedeutet in die Mitte des Listenfelds scrollen
            except:
                QtGui.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
                pass




        #bei einer Auswahländerung, d.h. eine neue Gemeinde ist gesucht
        #muß das zweite Listenfeld auch aktualisiert werden und vorher
        #natürlich eine neue Abfrage der KG gemacht werden


        self.sort()


        #Der Suchbutton wird deaktiviert, damit der User
        #vor der Suche die KG zur Politischen Gemeinde auswählen muß
        QtCore.QObject.connect(self.modell_kg, QtCore.SIGNAL("modelReset ()"), self.gstsuche_deaktivieren)
        #Das Suchfeld wird gelöscht
        self.txtGstnr.clear()
        self.gefunden.clear()



        #Das Listenfeld für KG-Gemeinde mit der Abfrageaktualisieren
        #self.modell_kg.setQuery(self.abfrage2)
        self.lstKatgem.setModel(self.modell_kg)

    #sortiert die Liste das zweite Listenfeld für die KG - Gemeindenummer
    #entweder nach KG oder nach Name
    def sort(self):

##        if not self.abfrage2 is None and not self.modell_kg is None and not self.Gemeinde is None:
##
##
##            if self.Gemeinde == "Vorarlberg":
##                if self.rbKG.isChecked():
##                    self.abfrage2.exec_("SELECT DISTINCT kgnrkgname,KGEM_GESNR FROM vorarlberg.kat_gem where not (PGEM_NAME = '" + string.strip(self.Gemeinde) + "') ORDER BY KGEM_GESNR")
##                elif self.rbName.isChecked():
##                    self.abfrage2.exec_("SELECT DISTINCT kgnrkgname,KGEM_NAME FROM vorarlberg.kat_gem where not (PGEM_NAME = '" + string.strip(self.Gemeinde) + "') ORDER BY KGEM_NAME")
##            else:
##                if self.rbKG.isChecked():
##                    self.abfrage2.exec_("SELECT DISTINCT kgnrkgname,KGEM_GESNR FROM vorarlberg.kat_gem WHERE (PGEM_NAME = '" + string.strip(self.Gemeinde) + "') ORDER BY KGEM_GESNR")
##                elif self.rbName.isChecked():
##                    self.abfrage2.exec_("SELECT DISTINCT kgnrkgname,KGEM_NAME FROM vorarlberg.kat_gem WHERE (PGEM_NAME = '" + string.strip(self.Gemeinde) + "') ORDER BY KGEM_NAME")
##
##            self.modell_kg.setQuery(self.abfrage2)

        if  not self.modell_kg is None and not self.Gemeinde is None:
            self.modell_kg.clear()
            for item in self.gemeindeliste[string.strip(self.Gemeinde)]:
                eins = QtGui.QStandardItem(item)
                eins.setEditable(False)
                self.modell_kg.appendRow(eins)

        self.modell_kg.sort(0)






    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):
        #mc = self.iface.mapCanvas()
        Punkt = self.mc.extent().center()
        return Punkt

    #Die DKM der ausgewählten Gemeinde laden
    #berücksichtigt werden muß auch welche Layer mit Hilfe
    #der Checkboxen ausgewählt wurden
    def ladeGemeinde(self):
        #Am Filesystem gibts keine Sonderzeichen!
        gemeinde_wie_filesystem = self.Gemeinde
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ä').decode('utf8'),'ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ä').decode('utf8'),'Ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ö').decode('utf8'),'oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ö').decode('utf8'),'Oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ü').decode('utf8'),'ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ü').decode('utf8'),'Ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ß').decode('utf8'),'ss')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace('. ','_')

        #Prüfen ob ein Zoompunkt gesetzt ist. Das ist nur der Fall wenn ein Grundstück gesucht wird
        #und auf den betreffenden Extent zoomen
        #(Das zoomen auf den Gemeindeextent ist zwar eingebaut aber auskommentiert!)
        if not (self.zoompunkt is None): #Existenz eines Objectes Prüfen: OHNE Klammer!!
            self.mc.setExtent(self.zoompunkt)


        #Den Pfad für die betreffende Gemeinde setzen
        Pfad = self.vogisPfad + "Grenzen/DKM/" + gemeinde_wie_filesystem + "/DKM.qgs"
        #Pfad = "D:/grenzen/dkm/bludenz/DKM.qgs"

        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport
        dkm = ProjektImport(self.iface)

        #Listenobjekt initialisieren
        liste = []

        #Das Sammelobjekt der Checkboxen mit Schleife durchlaufen
        for button in self.auswahlBoxen.buttons():
            #ist der Button gechecked, den Buttontext zur Liste hinzufügen
            if button.isChecked():
                        liste.append(button.text())
                        if button.text() == ("Grundstück Nr").decode("utf-8"):
                            liste.append(button.text() + " Mask.")
                        if button.text() == ("Grundstücke").decode("utf-8"):
                            liste.append(button.text() + " Mask.")
                            liste.append(button.text() + " (a)")

        self.mc.setRenderFlag(False)
        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        dkm.importieren(Pfad,liste,self.Gemeinde,True)
        #dkm.importieren(Pfad,liste,self.Gemeinde,True)

        self.mc.setRenderFlag(True)



        #zoompunkt wieder zurücksetzen
        self.zoompunkt = None

        dkm = None





    #Methode such nach einem bestimmtem Grundstück
    #in einer ausgewählten KG. Gleichzeitig wird auch der
    #Zoompunkt gesetz
    def gstsuche(self):



        self.info.show()    # Infofenster, sollts länger dauern
        self.info.repaint()



        #Textfeldinhalt zurücksetzen
        self.gefunden.setText("")
        self.gefunden.repaint()


       #Am Filesystem gibts keine Sonderzeichen!
        schema = self.Gemeinde
        schema = schema.replace(('ä').decode('utf8'),'ae')
        schema = schema.replace(('Ä').decode('utf8'),'Ae')
        schema = schema.replace(('ö').decode('utf8'),'oe')
        schema = schema.replace(('Ö').decode('utf8'),'Oe')
        schema = schema.replace(('ü').decode('utf8'),'ue')
        schema = schema.replace(('Ü').decode('utf8'),'Ue')
        schema = schema.replace(('ß').decode('utf8'),'ss')
        schema = string.lower(schema.replace('. ','_'))

        #Den Pfad zur betreffenden GEmeinde setzen
        #Pfad = self.vogisPfad + "Grenzen/DKM/" + gemeinde_wie_filesystem + "/Grundstuecke/"

##        #Prüfen, ob das GST.shp in dem das Grundstück
##        #gesucht wird bereits geladen ist. Dazu müssen
##        #alle geladenen Layer im Qgis durchgespoolt werden
##        Signal = False
##        for lyr_tmp in self.iface.mapCanvas().layers():
##            if lyr_tmp.name() == self.Gemeinde + ("-Grundstücke").decode("utf-8"):
##                self.dbaseTabelle = lyr_tmp
##                Signal = True   #gst.shp der betreffenden Gemeinde ist schon im QGIS geladen
##
##
##       #ist das gst.shp der betreffenden Gemeinde noch nicht im QGIS
##       #wird es in den Hintergrund geladen
##        if not Signal:



        # Geodatenbank
        uri = QgsDataSourceURI()
        uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(),'','')  # Keine Kennwort nötig, Single Sign On

        # Geometriespalte bestimmen -- geht nur mit OGR
        outputdb = ogr.Open('pg: host =' + self.db.hostName() + ' dbname =' + self.db.databaseName() + ' schemas=' + schema)
        geom_column = outputdb.GetLayerByName('gst').GetGeometryColumn()

        uri.setDataSource(schema, 'gst', geom_column)

        gst_lyr = QgsVectorLayer(uri.uri(), "gst","postgres")


        #-------------------------------------------------------
        #BEGINN der attributiven Suche im QGIS
        #-------------------------------------------------------
##
##        #Nun die Suche nach der Gewünschten Grundstücksnummer
##        #in der Gemeinde bzw. KG
##
##        progress = QtGui.QProgressDialog ()
##        progress.setLabelText("Suche " + ("Läuft").decode("utf-8"))
##        progress.setWindowModality(QtCore.Qt.WindowModal)
##        count = 0
##        fid = []
##        nummer = ""
##
##        # Eingabefeld auslesen und gleich splitten
##        gstliste = string.split(self.txtGstnr.text(),",")
##
##
##        iter = gst_lyr.getFeatures()
##        progress.setRange(0,gst_lyr.featureCount()*len(gstliste))
##        for gst in gstliste:
##
##            iter.rewind()
##            for attr in iter:
##
##                #hier die Werte der betreffenden Spalten mit den gesuchten Werten vergleichen
##                if attr.attribute("GNR") == gst and attr.attribute("KG") == self.kgnummer:
##                    fid.append(attr.id())
##                    nummer = nummer + gst + " "
##                    break
##                count = count + 1
##                progress.setValue(count)
##                if (progress.wasCanceled()):
##                    break
##
##        if not fid is None:
##            gst_lyr.setSelectedFeatures(fid)


        #-------------------------------------------------------
        #ENDE der attributiven Suche im QGIS
        #-------------------------------------------------------


        #------------------------------------------------------
        # so geht die Suche schneller -Subset
        #------------------------------------------------------


        fid = []
        # Eingabefeld auslesen und gleich splitten
        gstliste = string.split(self.txtGstnr.text(),",")

        abfr_str = ''
        nummer = ''
        for gst in gstliste:
            if abfr_str == '':
                abfr_str = abfr_str + 'gnr = \'' + gst + '\' '
                nummer = nummer + gst + " "
            else:
                abfr_str = abfr_str + 'or gnr = \'' + gst + '\' '
                nummer = nummer + gst + " "


        gst_lyr.setSubsetString('(' + abfr_str +') and kg = (\'' + self.kgnummer + '\')')
        self.info.close()   # Weg mit dem Infofenster

        gst_lyr.selectAll()
        fid = gst_lyr.selectedFeaturesIds()

        #------------------------------------------------------
        # Ende Subset Suche
        #------------------------------------------------------


        #Wurde was gefunden? ja/nein
        if gst_lyr.selectedFeatureCount() >= 1: #Eins gefunden, Textfeld und Zoompunkt festlegen
            self.gefunden.setText(("Grundstück ").decode("utf-8") + nummer + " in  KG " + self.Kgemeinde + " gefunden")
            self.zoompunkt = gst_lyr.boundingBoxOfSelected()
##            if Signal:
##                self.mc.setExtent(self.zoompunkt)
##            else:
##                # Wenn die DKM der betreffenden Gemeinde noch nicht geladen ist
##                # einfach laden
            self.ladeGemeinde()


            # um zu selektieren den geladenen Layer suchen
            # for lyr_tmp in self.mc.layers():    # geht nicht, da nicht sofort aktualisiert wird
            for lyr_tmp in self.iface.legendInterface().layers():    # vergisst und auch bei einem refresh nicht richtig macht....
                if lyr_tmp.name() == ("Grundstücke-").decode("utf-8") + self.Gemeinde + ' (a)':
                    if not fid is None:
                        lyr_tmp.setSelectedFeatures(fid)    # und selektieren

        else:   #nichts gefunden: Textfeld und Zoompunkt zurücksetzen
            self.gefunden.setText(("Grundstück ").decode("utf-8") + self.txtGstnr.text() + " in  KG " + self.Kgemeinde + " nicht gefunden")
            self.zoompunkt = None





    #Den Button Grundstückssuche aktivieren
    #und die KG Nummer ermiteln
    #und das Label mit Text füllen
    def gstsuche_aktivieren(self,kg_index):
        self.btnGstsuche.setDisabled(False)
        self.Kgemeinde = kg_index.data()
        self.groupBox_4.setTitle(("Grundstückssuche in ").decode("utf-8") + self.Gemeinde + " KG " +self.Kgemeinde)

        #Für die Grundstücksuche brauch ich noch die KG Nummer
        self.kgnummer = self.Kgemeinde[:5]

    #Methode deaktiviert den Button Suche
    def gstsuche_deaktivieren(self):
        self.btnGstsuche.setDisabled(True)
        self.groupBox_4.setTitle("")


    #Alle Checkboxen für die Grundstücksebenen Auswählen
    def alles_auswaehlen(self):
        for button in self.auswahlBoxen.buttons():
           button.setChecked(True)

    #Standard Checkboxen für die Grundstücksebenen Auswählen
    def standard_auswaehlen(self):
        for button in self.auswahlBoxen.buttons():
           button.setChecked(False)

        self.checkBox.setChecked(True)
        self.checkBox_2.setChecked(True)
        self.checkBox_6.setChecked(True)

    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):


        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)
        try:
            if not (self.tool_vorher is None):
                self.mc.setMapTool(self.tool_vorher)
        except:
            pass
        #disconnect: weil sonst trotz close und del das signal slot verhältnis nicht sauber gelöscht wird
        #wieso??
        QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)

        self.close()


    #urmappe ins Qgis laden
    def ladeurmappe(self):
        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport
        urmappe = ProjektImport(self.iface)

        self.mc.setRenderFlag(False)

        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        urmappe.importieren(self.vogisPfad + "Grenzen/Urmappe/Vlbg/urmappe.qgs",None,None,None,True,"Urmappe 1857")

        self.mc.setRenderFlag(True)

    #urmappe ins Qgis laden
    def ladeobjekte(self):
        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport
        objekte = ProjektImport(self.iface)

        self.mc.setRenderFlag(False)
        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        objekte.importieren(self.vogisPfad + "Naturbestand/Vorarlberg/Hausobjekte.qgs")

        self.mc.setRenderFlag(True)


class LadefortschrittDialog(QtGui.QDialog,Ui_frmGstauswahl):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_frmGstauswahl.__init__(self)



        # Set up the user interface from Designer.
        self.setupUi(self)