# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtSql
import copy
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_fwp import *
from ladefortschritt import *

#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *





#Klassendefinition für das Laden Des FWP
class FWPDialog (QtGui.QDialog,Ui_frmFWP):


    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    #Initialisierung der GUI
    def __init__(self, parent,iface,dkmstand,pfad = None,vogisPfad = None, PGdb = None, gemeindeliste=None):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmFWP.__init__(self)
        self.iface = iface
        self.mc = self.iface.mapCanvas()
        self.pfad = pfad
        self.vogisPfad = vogisPfad
        self.setupUi(self) #User Interface für Hauptfenster FWP Suche initialisieren
        self.gemeindeliste = gemeindeliste


##
##        #über SQLITE
##        if PGdb == None:
##            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
##            self.db.setDatabaseName(self.vogisPfad + "Grenzen/DKM/_Allgemein/kat_gem.sqlite");
##             #falls es länger dauert, eine kurze Info
##            info = LadefortschrittDialog()
##            info.show()
##            info.repaint()  #sonst bleibt das Fenster leer!
##
##            if  not (self.db.open()):
##                QtGui.QMessageBox.about(None, "Achtung", ("Öffnen Kat_Gem gescheitert").decode('utf8'))
##                return #wenns sich nicht öffnen läßt abbrechen
##            self.abfrage = QtSql.QSqlQuery(self.db)
##            self.abfrage.exec_("SELECT DISTINCT PGEM_NAME  FROM kat_gem_vlbg")
##        else:   # über Postgres
##            self.db = PGdb
##            self.abfrage = QtSql.QSqlQuery(self.db)
##            self.abfrage.exec_("SELECT DISTINCT PGEM_NAME  FROM vorarlberg.kat_gem order by PGEM_NAME")



         #Modell und Widget füllen
        self.modelli = QtGui.QStandardItemModel()

        for item in self.gemeindeliste:
            eins = QtGui.QStandardItem(item)
            eins.setEditable(False)
            self.modelli.appendRow(eins)
        #self.modelli.appendRow(eins)
        self.modelli.sort(0)



##
##        #Modell und Widget füllen
##        self.modelli = QtSql.QSqlQueryModel()
##        self.modelli.setQuery(self.abfrage)
        self.lstGemeinden.setModel(self.modelli)


        #den mittelpunkt des extent rausfinden
        #und die passene Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)


        #Variablen definieren und None setzen.
        #Sind nicht immer mit Werten initialisiert und None kann in
        #If Abfragen unterschieden werden
        #self.zoompunkt = None
        self.tool_vorher = None


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





        #Hauptfenster positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)


         #Ein Maptool erzeugen das den Punkt zurückgibt (wenn man ins Kartnfenster klickt)
        self.PtRueckgabe = QgsMapToolEmitPoint(self.mc)

        #Die Signal Slot Verbindungen funktionieren besser,
        #wenn sie beim Initialisieren egsetzt werden!

        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!
        QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnGemeinde)

        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)

    def MapButtonZuruecksetzen(self,Tool_Gecklickt):
        if not self.PtRueckgabe is None:
            if  not (Tool_Gecklickt == self.PtRueckgabe):   #wenn ident, gleiche Speicheradresse!!
                #QtGui.QMessageBox.about(None, "Achtung", str(Tool_Gecklickt) + " gegen" + str(self.PtRueckgabe))
                self.btGmdChoice.setChecked(False)


    #Der Slots für die Signale des Gemeindeauswahlbuttons (rotes Kreuzchen)
    #Wird draufgeklickkt bzw. der Zustand verändert wird diese Methode aufgerufen
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


            #und QGIS auf das neue Maptool einstellen!
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
    #wenn die GEmeinde mit dem roten Kreuzchen ausgewählt wird
    def returnGemeinde(self,ergebnis):

        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er autonmatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in self.mc.layers():
            if vorhanden.name() == "Gemeinden":
                yes = True
                break

        if yes:
            gmdLayer = vorhanden
        else:
            wert = ("Sonntag")
            self.auswahlaenderung(wert )
            return

        #damit nichts flackert
        self.mc.setRenderFlag(False)


        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des features der betreffenden politischen Gemeinde
        #im Gememindelayer in QGIS
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
    def auswahlaenderung(self,SelItem,Nummer = None):

        #Abhängig von wo aus die Methode aufgerufen wird
        #bekommt sie unterschiedliche Typen übergeben



        #if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!
        if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem
            self.lstGemeinden.clearSelection()
            self.lstGemeinden.keyboardSearch(self.Gemeinde)
            index = self.lstGemeinden.selectedIndexes()
            if len(index) > 0:
                self.lstGemeinden.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            else:
                QtGui.QMessageBox.about(None, "Achtung", ("Layer Gemeinden nicht gefunden oder dessen Codierung prüfen!").decode('utf8'))

        elif isinstance(SelItem, str):
            self.Gemeinde = SelItem
            self.lstGemeinden.clearSelection()
            self.lstGemeinden.keyboardSearch(SelItem)
            index = self.lstGemeinden.selectedIndexes()
            if len(index) > 0:
                self.lstGemeinden.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
            else:
                QtGui.QMessageBox.about(None, "Achtung", ("Layer Gemeinden nicht gefunden oder dessen Codierung prüfen!").decode('utf8'))
        else:
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem.data(0)
            self.lstGemeinden.scrollTo(SelItem,3) #3 bedeutet in die Mitte des Listenfelds scrollen


    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):
        mc = self.iface.mapCanvas()
        Punkt = mc.extent().center()
        return Punkt

    #Den FWP der ausgewählten Gemeinde laden
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
        #(Das zoomen auf den GEmeindeextent ist zwar eingebaut aber auskommentiert!)
        #if not (self.zoompunkt is None): #Existenz eines Objectes Prüfen: OHNE Klammer!!
        #    self.mc.setExtent(self.zoompunkt)

        #Den Pfad für die betreffende Gemeinde setzen
        Pfad = self.pfad + gemeinde_wie_filesystem + "/Flaechenwidmungsplan/FWP.qgs"

        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport
        fwp = ProjektImport(self.iface)


        self.mc.setRenderFlag(False)

        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        #QtGui.QMessageBox.about(None, "About Application",Pfad)
        fwp.importieren(Pfad,None,self.Gemeinde,True)

        self.mc.setRenderFlag(True)

         #zoompunkt wieder zurücksetzen
        #self.zoompunkt = None

    #Das Projekt Beschränkungslayer laden
    #Das geschieht nicht gemeindeweise, sondern für die Landesfläche
    def ladeBZ(self):
        Pfad = self.pfad + "Vorarlberg/FWP_Beschraenkung.qgs"
        bz = ProjektImport(self.iface)

        self.mc.setRenderFlag(False)
        bz.importieren(Pfad)
        self.mc.setRenderFlag(True)

    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)

        if not (self.tool_vorher is None):
            self.mc.setMapTool(self.tool_vorher)
        #disconnect: weil sonst trotz close und del das signal slot verhältnis nicht sauber gelöscht wird
        #wieso??
        QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
        self.close()




