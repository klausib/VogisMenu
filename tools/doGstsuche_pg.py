# -*- coding: utf-8 -*-

#!/usr/bin/python



from builtins import str
from qgis.PyQt import QtGui, QtCore, QtSql
import copy,string
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_blattschnitte import *
from gui_gstsuche import *
from osgeo import ogr
from globale_variablen import *     # Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich


from gui_gstauswahl import *
from ProjektImport import *




#Klassendefinition für die Grundstückssuche, das Laden der DKM sowie der Urmappe
#und der Gebäudeumrisse
#class GstDialog (QtGui.QDialog,Ui_frmGstsuche,QtCore.QObject):
class GstDialogPG (QtWidgets.QDialog,Ui_frmGstsuche):



    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)


    #Initialisierung der Grudstückssuche
    #def __init__(self, parent,iface,dkmstand,pfad = None,vogisPfad = None):
    def __init__(self, parent,iface,dkmstand,pfad,PGdb = None, gemeindeliste = None):

        QtWidgets.QDialog.__init__(self,parent)
        Ui_frmGstsuche.__init__(self)


        self.iface = iface
        self.setupUi(self) #User Interface für Hauptfenster GST Suche initialisieren
        self.mc = self.iface.mapCanvas()
        self.vogisPfad = pfad
        self.db = PGdb



        # Nochmals Öffnen
        # haproxy scheint sonst die Verbindung wieder zu schliessen?

        ok = self.db.open()
        self.gemeindeliste = gemeindeliste
        self.modell_kg = QtGui.QStandardItemModel()

        #Modell und Widget füllen
        self.modelli = QtGui.QStandardItemModel()

        for item in list(self.gemeindeliste.keys()):
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

        self.gbDkm.setTitle("Digitale Katastralmappe (" + dkmstand + ")")


        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)



        #Ein Maptool erzeugen das den Punkt zurückgibt (wenn man ins Kartnfenster klickt)
        self.PtRueckgabe = QgsMapToolEmitPoint(self.mc)



        #Die Signal Slot Verbindungen funktionieren besser,
        #wenn sie beim Initialisieren ersetzt werden!
        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!

        #QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
        self.mc.mapToolSet.connect(self.MapButtonZuruecksetzen)


        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!

        #QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnGemeinde)
        self.PtRueckgabe.canvasClicked.connect(self.returnGemeinde)









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
            if vorhanden.name() == "Gemeinden" and vorhanden.type() == 0: # o bedeutet Vektorlayer
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

        gmdLayer.selectByRect(wahlRect,False)



        #Den Index des feldes PGEM_NAME
        #in der Attributtabelle des Layers finden
        #brauch ich um die grafisch ausgewählte Gemeinde
        #im Listenfeld optisch in die mitte zu holen

        Liste = gmdLayer.selectedFeatures()



        #Auswahl wieder löschen
        gmdLayer.removeSelection()


        # API für QGIS 2.0
        if  (len(Liste) > 0):
            self.auswahlaenderung(Liste[0].attribute('pgem_name'))
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
        if isinstance(SelItem, str):    #QGIS 2 hat je keine Qstring mehr!

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
                QtWidgets.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder')
                pass

        elif isinstance(SelItem, str):

            self.Gemeinde = SelItem
            self.lstPolgem.keyboardSearch(SelItem)
            index = self.lstPolgem.selectedIndexes()

            try:
                if not index == None:
                    self.lstPolgem.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            except:
                QtWidgets.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder')
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

                QtWidgets.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder')

                pass

        #bei einer Auswahländerung, d.h. eine neue Gemeinde ist gesucht
        #muß das zweite Listenfeld auch aktualisiert werden und vorher
        #natürlich eine neue Abfrage der KG gemacht werden

        self.sort()


        #Der Suchbutton wird deaktiviert, damit der User
        #vor der Suche die KG zur Politischen Gemeinde auswählen muß

        #QtCore.QObject.connect(self.modell_kg, QtCore.SIGNAL("modelReset ()"), self.gstsuche_deaktivieren)
        self.modell_kg.modelReset.connect(self.gstsuche_deaktivieren)

        #Das Suchfeld wird gelöscht
        self.txtGstnr.clear()
        self.gefunden.clear()



        #Das Listenfeld für KG-Gemeinde mit der Abfrageaktualisieren
        #self.modell_kg.setQuery(self.abfrage2)
        self.lstKatgem.setModel(self.modell_kg)



    #sortiert die Liste das zweite Listenfeld für die KG - Gemeindenummer
    #entweder nach KG oder nach Name

    def sort(self):
        if  not self.modell_kg is None and not self.Gemeinde is None:
            self.modell_kg.clear()
            for item in self.gemeindeliste[str.strip(self.Gemeinde)]:
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
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ä'),'ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ä'),'Ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ö'),'oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ö'),'Oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ü'),'ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ü'),'Ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ß'),'ss')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace('. ','_')

##        gemeinde_wie_filesystem = 'Vorarlberg'

        #Prüfen ob ein Zoompunkt gesetzt ist. Das ist nur der Fall wenn ein Grundstück gesucht wird
        #und auf den betreffenden Extent zoomen
        #(Das zoomen auf den Gemeindeextent ist zwar eingebaut aber auskommentiert!)
        if not (self.zoompunkt is None): #Existenz eines Objectes Prüfen: OHNE Klammer!!
            self.mc.setExtent(self.zoompunkt)


        #Den Pfad für die betreffende Gemeinde setzen
        Pfad = self.vogisPfad + "Grenzen/DKM/" + gemeinde_wie_filesystem + "/DKM.qgs"

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
                        if button.text() == ("Grundstück Nr"):
                            liste.append(button.text() + " Mask.")
                        if button.text() == ("Grundstücke"):
                            liste.append(button.text() + " Mask.")
                            liste.append(button.text() + " (a)")
                        else:
                            liste.append(button.text())




        self.mc.setRenderFlag(False)
        # nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        dkm.importieren(Pfad,liste,self.Gemeinde,True)

        self.mc.setRenderFlag(True)

        # zoompunkt wieder zurücksetzen
        self.zoompunkt = None

        dkm = None

    #Methode such nach einem bestimmtem Grundstück
    #in einer ausgewählten KG. Gleichzeitig wird auch der
    #Zoompunkt gesetz
    def gstsuche(self):



        # Der Username der verwendet werden soll
        if len(auth_user_global) > 0:    # Ist belegt
            auth_user = auth_user_global[0]
        else:
            auth_user = None


        #Textfeldinhalt zurücksetzen
        self.gefunden.setText("")
        self.gefunden.repaint()


        schema = 'vorarlberg'


        ################################################
        # Geometriespalte bestimmen -- geht nur mit OGR
        uri = QgsDataSourceUri()
        uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(),'','')  # Kein Kennwort nötig, Single Sign On

        try:
            if auth_user == None:
                outputdb = ogr.Open('pg: host =' + self.db.hostName() + ' dbname =' + self.db.databaseName() + ' schemas=' + schema + ' port=' + str(self.db.port()))
            else:
                outputdb = ogr.Open('pg: host =' + self.db.hostName() + ' dbname =' + self.db.databaseName() + ' schemas=' + schema + ' port=' + str(self.db.port()) + ' user=' + auth_user)
            geom_column = outputdb.GetLayerByName('gst').GetGeometryColumn()

        except:
            geom_column = 'the_geom'
        ##################################################

        uri.setDataSource(schema, 'gst', geom_column)
        if not auth_user == None:
            uri.setUsername(auth_user)
        gst_lyr = QgsVectorLayer(uri.uri(), "gst","postgres")


        #------------------------------------------------------
        # Subset Suche: Gibts so ein Grundstück überhaupt?
        # erst wenn ja, dann wird geladen
        #------------------------------------------------------
        fid = []

        # Eingabefeld auslesen und gleich splitten
        gstliste = str.split(self.txtGstnr.text(),",")


        abfr_str = ''
        nummer = ''
        for gst in gstliste:
            if abfr_str == '':
                abfr_str = abfr_str + 'gnr = \'' + str.strip(gst) + '\' '
                nummer = nummer + gst + " "
            else:
                abfr_str = abfr_str + 'or gnr = \'' + str.strip(gst) + '\' '
                nummer = nummer + gst + " "


        gst_lyr.setSubsetString('(' + abfr_str +') and kg = (\'' + self.kgnummer + '\')')

        gst_lyr.selectAll()
        fid = gst_lyr.selectedFeatureIds()

        #------------------------------------------------------
        # Ende Subset Suche
        #------------------------------------------------------


        #Wurde was gefunden? ja/nein
        if gst_lyr.selectedFeatureCount() >= 1: #Eins gefunden, Textfeld und Zoompunkt festlegen
            self.gefunden.setText(("Grundstück ") + nummer + " in  KG " + self.Kgemeinde + " gefunden")
            self.zoompunkt = gst_lyr.boundingBoxOfSelected()



            # Erstmal die Gemeinde laden
            self.ladeGemeinde()


            # Ein Problem haben wir, da die FIDs der Layer nicht übereinstimmenm,
            # da diese aus einem VIEW stammen und im Modul Projektimport zugewiesen werden
            # um zu selektieren den geladenen Layer suchen
            #for lyr_tmp in self.iface.legendInterface().layers():
            for lyr_tmp_d in QgsProject.instance().mapLayers(): # vergisst und auch bei einem refresh nicht richtig macht....

                #if lyr_tmp.name() == ("Grundstücke-") + self.Gemeinde + ' (a)':
                lyr_tmp = QgsProject.instance().mapLayers()[lyr_tmp_d]

                if lyr_tmp.name() == ("Grundstücke-") + self.Gemeinde + ' (a)':
                    #lyr_tmp = QgsProject.instance().mapLayers()[lyr_tmp_d]

                #if lyr_tmp.name() == ("Grundstücke-") +  'Vorarlberg (a)':
                    # und nochmal die Subset auswahl durchführen
                    # FIDS abfragen, Subset zurücksetzen und FIDS selektieren

                    if not fid is None:
                        lyr_tmp.setSubsetString('(' + abfr_str +') and kg = (\'' + self.kgnummer + '\')')
                        lyr_tmp.selectAll()
                        fid = lyr_tmp.selectedFeatureIds()
                        lyr_tmp.setSubsetString('')
                        lyr_tmp.selectByIds(fid)    # und selektieren


        else:   #nichts gefunden: Textfeld und Zoompunkt zurücksetzen

            self.gefunden.setText(("Grundstück ") + self.txtGstnr.text() + " in  KG " + self.Kgemeinde + " nicht gefunden")
            self.zoompunkt = None




    #Den Button Grundstückssuche aktivieren
    #und die KG Nummer ermiteln
    #und das Label mit Text füllen

    def gstsuche_aktivieren(self,kg_index):
        self.btnGstsuche.setDisabled(False)
        self.Kgemeinde = kg_index.data()
        self.groupBox_4.setTitle(("Grundstückssuche in ") + self.Gemeinde + " KG " +self.Kgemeinde)



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

        #QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
        #self.mc.mapToolSet.disconnect(self.MapButtonZuruecksetzen)



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



    #naturbestand ins Qgis laden
    def ladeobjekte(self):

        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport

        objekte = ProjektImport(self.iface)



        self.mc.setRenderFlag(False)

        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        objekte.importieren(self.vogisPfad + "Naturbestand/Vorarlberg/Hausobjekte.qgs")

        self.mc.setRenderFlag(True)

