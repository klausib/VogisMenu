# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtSql

from qgis.core import *
from gui_naturschutz import *
from qgis.gui import *
from qgis.analysis import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import os






#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen Naturschutz
class NaturschutzDialog(QtGui.QDialog, Ui_frmNaturschutz):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,pfad = None,vogispfad = None):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmNaturschutz.__init__(self)


        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.vogisPfad = vogispfad
        self.ckButtons.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.naturschutz = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

        #Instanzierung des einegstellten toolobjektes
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




        #Die Kat_Gem Tabelle öffnen
        #Referenz auf die Datenquelle
        #über SQLITE
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
        self.db.setDatabaseName(self.vogisPfad + "Grenzen/DKM/_Allgemein/kat_gem.sqlite");

        #falls es länger dauert, eine kurze Info
        #info = LadefortschrittDialog()
        #info.show()
        #info.repaint()  #sonst bleibt das Fenster leer!

        if  not (self.db.open()):
            QtGui.QMessageBox.about(None, "Achtung", ("Öffnen Kat_Gem gescheitert").decode('utf8'))
            return #wenns sich nicht öffnen läßt abbrechen

        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrage.exec_("SELECT DISTINCT PGEM_NAME  FROM kat_gem_vlbg")

        Liste = []    #eine QStringList instanzieren
        while self.abfrage.next():
            #QtGui.QMessageBox.about(None, "Achtung", self.abfrage.value(0).toString())
            Liste.append(self.abfrage.value(0))

        #Listenfeld des Dialogs frmWegtafeln mit den Tafelnummern füllen
        #und sortieren
        Liste.sort()
        self.cmbGemeinden.addItems(Liste)



        #den mittelpunkt des extent rausfinden
        #und die passene Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)


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




    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def datenladen(self):

        self.mc.setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            if button.isChecked(): #wenn gecheckt wird geladen
                if   ("Natura2000" in button.objectName()):
                    self.fullpath = self.pfad + "Gebietsschutz/Vlbg/Europaschutzgebiet/Natura_2000.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Naturschutzgebiete" in button.objectName()):
                    self.fullpath = self.pfad + "Gebietsschutz/Vlbg/Naturschutzgebiet/Naturschutzgebiet.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Landschaftsschutzgebiete" in button.objectName()):
                    self.fullpath = self.pfad + "Gebietsschutz/Vlbg/Landschaftsschutzgebiet/Landschaftsschutzgebiet.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Pflanzenschutzgebiete" in button.objectName()):
                    self.fullpath = self.pfad + "Gebietsschutz/Vlbg/Pflanzenschutzgebiet/Pflanzenschutzgebiet.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("GeschLandschaftsteil" in button.objectName()):
                    self.fullpath = self.pfad + "Gebietsschutz/Vlbg/Geschuetzter_Landschaftsteil/Geschuetzter_Landschaftsteil.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Biosphaerenpark" in button.objectName()):
                    self.fullpath  = self.pfad +  "Gebietsschutz/vlbg/Biosphaerenpark/Biosphaerenpark.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Ruhezone" in button.objectName()):
                    self.fullpath  = self.pfad +  "Gebietsschutz/Vlbg/Ruhezone/Ruhezone.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("OertlichesSchutzgebiet" in button.objectName()):
                    self.fullpath  = self.pfad +  "Gebietsschutz/Vlbg/Oertliches_Schutzgebiet/oertliches_schutzgebiet.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Biotopinventar" in button.objectName()):
                    self.fullpath  = self.pfad +  "Inventar/Vlbg/Biotopinventar_2009/Biotope_2009.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Streuwiesen_2000" in button.objectName()):
                    self.fullpath = self.pfad +  "Projekte/Rheintal_Walgau/Streuwiesenevaluierung_2000/Streuwiesenevaluierung_2000.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Streuwiesen_2014" in button.objectName()):
                    self.fullpath = self.pfad +  "Projekte/Rheintal_Walgau/Streuwiesenevaluierung_2014/Streuwiesenevaluierung_2014.qgs"
                    self.naturschutz.importieren(self.fullpath)
                elif   ("Naturdenkmale" in button.objectName()):
                    self.fullpath = self.pfad +  "Projekte/Vlbg/Naturdenkmale/Naturdenkmale.qgs"
                    self.naturschutz.importieren(self.fullpath)


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

    #
    def gemeindebericht(self):
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
        os.startfile(self.pfad +  "Inventar/Vlbg/Biotopinventar_2009/Gemeindeberichte/" + gemeinde_wie_filesystem +".pdf")

    #
    def a3plaene(self):
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
        os.startfile(self.pfad +  "Inventar/Vlbg/Biotopinventar_2009/A3_Plaene/" + gemeinde_wie_filesystem +".pdf")



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
            return

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


    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):

        Punkt = self.mc.extent().center()
        return Punkt


    #Methode Aktualisiert nur das zweite Listenfeld für die KG - Gemeindenummer
    #Wird entweder von der Methode "returnGemeinde" oder
    #über eine Action beim Anklicken des Listenfeldes
    #mit der Gemeindenliste (politische) aufgerufen
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde
    def auswahlaenderung(self,SelItem,Nummer = None):

        #Abhängig von wo aus die Methode aufgerufen wird
        #bekommt sie unterschiedliche String Typen übergeben
        if isinstance(SelItem, unicode):
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem
            index = self.cmbGemeinden.findText(SelItem)
            self.cmbGemeinden.setCurrentIndex(index)
        else:
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem.data(0)
            self.lstGemeinden.scrollTo(SelItem,3) #3 bedeutet in die Mitte des Listenfelds scrollen

