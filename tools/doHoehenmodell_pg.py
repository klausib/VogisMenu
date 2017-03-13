# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtXml

from qgis.core import *
from qgis.gui import *
from gui_hoehenmodell_pg import *
from osgeo import ogr
import logging, os
from direk_laden import direk_laden



class HoehenmodellDialog_PG(QtGui.QDialog, Ui_frmHoehenmodell):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_hoehenmodell,pfad = None,vogisPfad = None, PGdb = None):

         #Ein individuelles Signal als Klassenvariable definieren
        #Abflug = QtCore.pyqtSignal(object)

        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmHoehenmodell.__init__(self)


        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.vogisPfad = vogisPfad
        self.tool_vorher = None
        self.mc = self.iface.mapCanvas()
        self.speicheradressen_hoehenmodell = speicheradressen_hoehenmodell
        self.db = PGdb

        #Das Basishöhenmodell dient zum Abfragen
        #derGeländehöhen mit dem Kreuzchen
        self.basisraster_04 = QgsRasterLayer(pfad+"/Hoehenmodelle/Vlbg/gt2004_01m.img","hidden")
        self.basisraster_11 = QgsRasterLayer(pfad+"/Hoehenmodelle/Vlbg/gt2011_50cm.img","hidden")

        if not self.basisraster_04.isValid():
            QtGui.QMessageBox.about(None, "Fehler", ("Laden des Basishöhenmodells 1m fehlgeschlagen").decode('utf8'))
            self.btHoehenabfrage.setEnabled(False)
            self.leX.setEnabled(False)
            self.leY.setEnabled(False)
            self.leZ.setEnabled(False)
        elif not self.basisraster_11.isValid():
            QtGui.QMessageBox.about(None, "Fehler", ("Laden des Basishöhenmodells 1m fehlgeschlagen").decode('utf8'))
            self.btHoehenabfrage.setEnabled(False)
            self.leX.setEnabled(False)
            self.leY.setEnabled(False)
            self.leZ.setEnabled(False)




        #Wir definieren einen eigenen Cursor: wird auf den
        #Button mit dem roten Kruez geklickt
        #bekommt der Mauscursor dieses Aussehen
        self.tool_vorher = None
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

        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)




    def MapButtonZuruecksetzen(self,Tool_Gecklickt):
        if not self.PtRueckgabe is None:
            if  not (Tool_Gecklickt == self.PtRueckgabe):   #wenn ident, gleiche Speicheradresse!!
                #QtGui.QMessageBox.about(None, "Achtung", str(Tool_Gecklickt) + " gegen" + str(self.PtRueckgabe))
                self.btHoehenabfrage.setChecked(False)
                #self.btnBlattschnitt.setChecked(False)


    #das laden der raster oder vektorlayer
    #hier werden keine projektdateien geladen, sonder die
    #shapes/rasterdaten direkt. den shapes wird ein qml für die richtige
    #darstellung zugewiesen. den rasterdaten bei bedarf auch bzw. wird
    #die darstellungseigenschaft direkt gesetzt
    def laden(self):

        self.raster = True
        pfad_ind = ""
        contrast = 0

        # unbedingt ALLES DEselektieren, sonst Probleme mit reihenfolge
        self.iface.layerTreeView().setCurrentLayer(None)    # None entspricht einem Null Pointer -> Auswahl wird entfernt -> nicht ausgewählt

        self.mc.setRenderFlag(False)
        #schleife geht alle checkbuttons (gruppiert ind der chkeckbuttongroup) durch
        for button in self.ckButtons.buttons():

            if button.isChecked():


                if ("BEVumgebung" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg_Umgebung/htxxxx_05m.tif"
                    anzeigename = "Schummerung 5m Vlbg.+Umg."

                elif ("HSZentraleuropa" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg_Umgebung/htxxxx_50m.tif"
                    anzeigename = "Schummerung 50m Zentraleuropa"

                #Schummerung Oberfläche

                elif ("VLaserVegetation_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg/hs2004_01m.ecw"
                    anzeigename = "Schummerung 2002-04 Oberfläche"

                elif ("VLaserVegetation_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg/hs2011_50cm.ecw"
                    anzeigename = "Schummerung 2011 Oberfläche"

                #Schummerung Gelände

                elif ("VLaserGelaende_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg/ht2004_01m.ecw"
                    anzeigename = "Schummerung 2002-04 Gelände"

                elif ("VLaserGelaende_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Schummerung/Vlbg/ht2011_50cm.ecw"
                    anzeigename = "Schummerung 2011 Gelände"

                #Höhenmodell Oberfläche

                elif ("VDgmVegetation_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenmodelle/Vlbg/gs2004_01m.img"
                    anzeigename = "Höhenmodell 2002-04 Oberfläche"
                    contrast = 1

                elif ("VDgmVegetation_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenmodelle/Vlbg/gs2011_50cm.img"
                    anzeigename = "Höhenmodell 2011 Oberfläche"
                    contrast = 1

                #Höhenmodell Gelände

                elif ("VDgmGelaende_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenmodelle/Vlbg/gt2004_01m.img"
                    anzeigename = "Höhenmodell 2002-04 Gelände"
                    contrast = 1

                elif ("VDgmGelaende_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenmodelle/Vlbg/gt2011_50cm.img"
                    anzeigename = "Höhenmodell 2011 Gelände"
                    contrast = 1

                #Abgeleitete Modelle

                elif ("VNeigungGrad_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Neigung/Vlbg/st2004_05m_gr.img"
                    anzeigename = "Geländeneigung 2002-04 in Grad"

                elif ("VNeigungProzent_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Neigung/Vlbg/st2004_05m_pz.img"
                    anzeigename = "Geländeneigung 2002-04 in Prozent"

                elif ("VExposition_04" in button.objectName()):

                    pfad_ind = self.pfad + "/Exposition/Vlbg/at2004_05m.img"
                    anzeigename = "Geländexposition 2002-04 in Grad"


                elif ("VNeigungGrad_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Neigung/Vlbg/st2011_05m_gr.img"
                    anzeigename = "Geländeneigung 2011 in Grad"

                elif ("VNeigungProzent_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Neigung/Vlbg/st2011_05m_pz.img"
                    anzeigename = "Geländeneigung 2011 in Prozent"

                elif ("VExposition_11" in button.objectName()):

                    pfad_ind = self.pfad + "/Exposition/Vlbg/at2011_05m.img"
                    anzeigename = "Geländexposition 2011 in Grad"


                #Isolinien nach Blattschnitt

                elif ("BLaserIsolinien_04" in button.objectName()):

                    #pfad_ind = self.pfad + "/Hoehenschichten/Kacheln/it2004_01m__" + self.cmbBlattschnitt.currentText().left(4)+ "/it2004_01m_" + self.cmbBlattschnitt.currentText() + ".shp"
                    pfad_ind = self.pfad + "/Hoehenschichten/Kacheln/it2004_01m.shp"
                    basename_vektor = "Isolinien 2002-04 1m"
                    basename_qml = self.vogisPfad + "Gelaendemodelle/_Allgemein/isolinien_1m.qml"
                    self.raster = False #die flagvariable auf 2No Raster" setzen


                elif ("BLaserIsolinien_11" in button.objectName()):

                    #pfad_ind = self.pfad + "/Hoehenschichten/Kacheln/it2004_01m__" + self.cmbBlattschnitt.currentText().left(4)+ "/it2004_01m_" + self.cmbBlattschnitt.currentText() + ".shp"
                    pfad_ind = self.pfad + "/Hoehenschichten/Kacheln/it2011_50cm.shp"
                    basename_vektor = "Isolinien 2011 50cm"
                    basename_qml = self.vogisPfad + "Gelaendemodelle/_Allgemein/isolinien_50cm.qml"
                    self.raster = False #die flagvariable auf 2No Raster" setzen


                #Isolinien Landesfläche

                elif ("B5LaserIsolinien" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenschichten/Vlbg/" + "/it2011_05m.shp"
                    basename_vektor = "Isolinien 5m"
                    basename_qml = self.vogisPfad + "Gelaendemodelle/_Allgemein/isolinien_5m.qml"
                    self.raster = False #die flagvariable auf 2No Raster" setzen

                 #nun die 1m isolinien, die werden anders als die raster behandelt
                elif ("OEKIsolinien" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenschichten/Vlbg/" + "/it_oek.shp"
                    basename_vektor = "Isolinien OEK"
                    basename_qml = self.vogisPfad + "Gelaendemodelle/_Allgemein/isolinien_oek.qml"
                    self.raster = False #die flagvariable auf 2No Raster" setzen

                  #nun die 1m isolinien, die werden anders als die raster behandelt
                elif ("UMGIsolinien" in button.objectName()):

                    pfad_ind = self.pfad + "/Hoehenschichten/Vlbg_Umgebung/" + "/itxxxx_50m.shp"
                    basename_vektor = "Isolinien Vlbg. Umgebung"
                    basename_qml = self.vogisPfad + "Gelaendemodelle/_Allgemein/isolinien_vlbgumg.qml"
                    self.raster = False #die flagvariable auf 2No Raster" setzen

                if self.raster:


                    #Prüfen ob der Layer schon einmal geladen wurde!
                    #Das machen wir halt nur über den Namen, aber das reicht!
                    if len(QgsMapLayerRegistry.instance().mapLayersByName((anzeigename).decode('utf8'))) < 1:



                        #Rasterdatensatz laden und auf gültigkeit prüfen
                        fileinfo = QtCore.QFileInfo(pfad_ind)
                        basename = fileinfo.baseName()

                        #Raster erzeugen und Darstellung zuweisen
                        raster = QgsRasterLayer(pfad_ind,basename)
                        raster.setContrastEnhancement(contrast) #Entspricht StretchToMinimumMaximum wenn wert 1
                        if not raster.isValid():
                            QtGui.QMessageBox.about(None, "Fehler", "Laden des Datensatzes fehlgeschlagen")
                            return #Ausführung des Sub wird hier einfach abgebrochen

                        QgsMapLayerRegistry.instance().addMapLayer(raster)

                        #Der geladene Rasterlayer wird in der Legende
                        #ganz nach unten gerückt
                        #API up to 2.2
                        if QGis.QGIS_VERSION_INT < 20300:
                            #Referenz auf die Legende holen
                            self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)
                            #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
                            # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
                            # der Legende vor allem Laden als Aktueller Layer gesetztw erden!!!
                            self.legendTree.setCurrentItem(self.legendTree.topLevelItem(0))
                            dodl = self.legendTree.takeTopLevelItem(0)
                            self.legendTree.addTopLevelItem(dodl)
                        else:
                            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(raster.id()) #der geladene layer
                            dummy_2 = zwtsch.clone()
                            QgsProject.instance().layerTreeRoot().insertChildNode(-1,dummy_2)
                            zwtsch.parent().removeChildNode(zwtsch)
                            dummy_2.setExpanded(False)




                        #der nachfolgende Code erzwingt eine Aktualisierung
                        #der Legende und des MapWindow
                        #Ansonsten kanns im Mapwindow darstellungsprobleme geben! Wiso??
                        if not raster is None:

                            raster.setLayerName((anzeigename).decode('utf8'))   #ACHTUNG: Damit wird auch erzwungen, daß die Layerdarstellung
                                                                                #(Reihenfolge) aktualisiert wird!!


                        anzeigename = ""
                else:

                    #Prüfen ob der Layer schon einmal geladen wurde!
                    #Das machen wir halt nur über den Namen, aber das reicht!
                    if len(QgsMapLayerRegistry.instance().mapLayersByName(basename_vektor)) < 1:

                        #isolinien laden
                        #isolinien = QgsVectorLayer(pfad_ind, basename_vektor,"ogr")

                        shapename = os.path.basename(pfad_ind)
                        pfad = os.path.dirname(pfad_ind)

                        isolinien = direk_laden(self.db, basename_vektor, shapename, pfad,self.iface)
                        #und prüfen ob erfolgreich geladen
                        if isolinien == None: #nicht erfolgreich geladen
                            QtGui.QMessageBox.about(None, "Fehler", basename_vektor + " konnte nicht geladen werden")
                            return
                        else:   #erfolgreich geladen
                            #dem Vektorlayer das QML File zuweisen
                            #flagge[1] ist false wenn das file nich gefunden wird
                            flagge = isolinien.loadNamedStyle(basename_qml)
                            if flagge[1]:
                                #Legendenansicht aktualisieren
                                self.iface.legendInterface().refreshLayerSymbology( isolinien )
                            else:
                                QtGui.QMessageBox.about(None, "Fehler",  basename_qml + "konnte nicht zugewiesen werden!")
                            #Zur Map Layer registry hinzufügen damit der Layer
                            #dargestellt wird
                            QgsMapLayerRegistry.instance().addMapLayer(isolinien)

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
            self.iface.mapCanvas().setMapTool(self.tool_vorher)
        #disconnect: weil sonst trotz close und del das signal slot verhältnis nicht sauber gelöscht wird
        #wieso??
        QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
        self.basisraster_04 = None
        self.basisraster_11 = None
        self.close()

    #der knopf mit dem roten Kreuzchen
    #wird geklickt: Vorsicht, kann von
    #zwei unterschiedlichen Buttons aus aufgerufen werden
    #hohenabfrage mit klick/auswahl blattschnitt
    def hoehenklick(self):

        #wer hat das Signal ausgelöst, das den Slot trifft? Da gibts zwei
        #Möglichkeiten, der connect wird über einen Wrapper(Lambdafunktion) aufgerufen
        #oder indem das Senderobjekt bestimmt wird. Hier geht nur Variante zwei, weil der QT Designer
        #das connect nicht so flexibel editieren kann und es dann bei händischer Ergänzung
        #wieder mit pyuic4 überschrieben wird
        welcherknopf = self.sender()

        #Variable enthält das vorherigen Maptool (z.B. Lupe...). Das wird
        #hier weggesichter um es wieder zurückstellen zu können
        if self.tool_vorher == None:
            self.tool_vorher = self.iface.mapCanvas().mapTool()


        #die Höhenabfrage ist gedrückt
        if self.btHoehenabfrage.isChecked() and ("Hoehenabfrage" in welcherknopf.objectName()):


            #Das Aussehen des Mauscursors im QGIS Kartenbild
            #wird auf unseren Cursor gesetzt
            self.iface.mapCanvas().setCursor(self.cursor)


            #und QGIS auf das neue Maptool einstellen!
            self.iface.mapCanvas().setMapTool(self.PtRueckgabe)
            self.iface.mapCanvas().setCursor(self.cursor)

            #den anderen Schalter zurücksetzen
            #self.btnBlattschnitt.setChecked(False)

            #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
            #Dabei wird das punktobjekt übertragen!!
            QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnHoehe)
            #den anderen Knopf wieder lösen!
            #QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnBlattschnitt)

##        #die Blattschnittabfrage ist gedrückt
##        elif self.btnBlattschnitt.isChecked() and ("Blattschnitt" in welcherknopf.objectName()):
##
##            #Das Aussehen des Mauscursors im QGIS Kartenbild
##            #wird auf unseren Cursor gesetzt
##            self.iface.mapCanvas().setCursor(self.cursor)
##
##
##            #und QGIS auf das neue Maptool einstellen!
##            self.iface.mapCanvas().setMapTool(self.PtRueckgabe)
##            self.iface.mapCanvas().setCursor(self.cursor)
##
##            #den anderen Schalter zurücksetzen
##            self.btHoehenabfrage.setChecked(False)
##
##            #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
##            #Dabei wird das punktobjekt übertragen!!
##            QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnBlattschnitt)
##            #den anderen Knopf wieder lösen!
##            QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnHoehe)

        #Nichts ist gechecked, deshalb alles zurücksetzen
        else:
            self.iface.mapCanvas().setMapTool(self.tool_vorher)    #auf ursprüngliches Maptool und zugehörigen Cursor zurücksetzen
            self.tool_vorher = None
            #QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnBlattschnitt)
            QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnHoehe)

    #Gibt die Höhe des DGM am angeklickten Ort zurück bzw. füllt damit die lineedit Felder
    #punkt enthält die Koordinaten des angeklickten Punkts
    def returnHoehe(self,punkt):


        #das hab ich nicht ganz verstanden: auf dodl wird eine liste
        #zurückgegeben die als ersten Wert ein Boolean enthält und als zweiten Wert ein Dictionary?
        #dodl_04 = self.basisraster_04.identify(punkt)
        dodl = self.basisraster_11.dataProvider().identify(punkt,QgsRaster.IdentifyFormatValue)

        maeppchen = dodl.results() #das Abfrageergebnis

        #wenn man ins Nirvana klickt gibts sonst nen Fehler
        #Deshalb das Ganze etwas abfangen!
        if not maeppchen[(maeppchen.keys()[0])] == None:
           self.leX.setText(str(int(round(punkt.x(),0))))
           self.leY.setText(str(int(round(punkt.y(),0))))
           self.leZ.setText(str(round(float(maeppchen[(maeppchen.keys()[0])]),1))) #Hohe gerundet auf dezimeter wird ins Linedit geschrieben"
        else:
            QtGui.QMessageBox.critical(None, "Fehler", ("Ungültiger Wertebereich").decode('utf8'))
            self.leX.setText("ungueltig")
            self.leY.setText("ungueltig")
            self.leZ.setText("ungueltig")
            return

        if round(float(maeppchen[(maeppchen.keys()[0])])) < -100:
            QtGui.QMessageBox.information(None, "Hinweis", ("Ungültiger Wertebereich Modell 2011.\nEs wird versucht das Modell 2002-04 zu verwenden").decode('utf8'))
            dodl = self.basisraster_04.dataProvider().identify(punkt,QgsRaster.IdentifyFormatValue)

            maeppchen = dodl.results() #das Dictionäre extrahieren: es enthält ein Wertepaar vom Typ Qstring "Kanal 1:hoehenmeter"
            #wenn man ins Nirvana klickt gibts sonst nen Fehler
            #Deshalb das Ganze etwas abfangen!
            if not maeppchen[(maeppchen.keys()[0])] == None:
               self.leX.setText(str(int(round(punkt.x(),0))))
               self.leY.setText(str(int(round(punkt.y(),0))))
               self.leZ.setText(str(round(float(maeppchen[(maeppchen.keys()[0])]),1))) #Hohe gerundet auf dezimeter wird ins Linedit geschrieben"
            else:
                QtGui.QMessageBox.critical(None, "Fehler", ("Ungültiger Wertebereich").decode('utf8'))
                self.leX.setText("ungueltig")
                self.leY.setText("ungueltig")
                self.leZ.setText("ungueltig")
                return

        #Aufruf der Methode, die an die geklickte Stelle ein kleines Kreuzchen
        #macht und die Höhe dazuschreibt
        self.zeichne_hoehenkote(punkt.x(),punkt.y(),str(round(float(maeppchen[(maeppchen.keys()[0])]),1)))



##    #gibt die Blattschnitt zurück bzw. setzt das Drop Down
##    #auf die Blattschnitnummer die angeklickt wurde
##    def returnBlattschnitt(self,punkt):
##
##        #self.mc.setRenderFlag(False)
##
##        #Auswahlrechteck erzeugen. Es dient der Auswahl
##        #des features der betreffenden politischen Gemeinde
##        #im Gememindelayer in QGIS
##        shift=self.iface.mapCanvas().mapUnitsPerPixel()
##        wahlRect = QgsRectangle(punkt.x(),punkt.y(),punkt.x()+ shift,punkt.y()+ shift)
##
##        #Entsprechendes Feature selektieren
##        self.blattschnitt.select(wahlRect,False)
##
##
##        #mit Hilfe des Index den Namen
##        #der ausgewählte Balttschnittnummer ermitteln
##        Liste = self.blattschnitt.selectedFeatures()
##
##
##
##        if  (len(Liste) > 0):
##            wert = Liste[0].attribute("V10_NR_TXT")
##            #QtGui.QMessageBox.about(None, "Fehler", str(self.index))
##
##            #die Kombobox aktualisieren
##            index = self.cmbBlattschnitt.findText(wert)
##            self.cmbBlattschnitt.setCurrentIndex(index)
##
##
##        #Auswahl wieder löschen
##        self.blattschnitt.removeSelection()
##
##        #self.mc.setRenderFlag(True)

##    #Finde den Mittelpunkt
##    #der aktuellen Kartendarstellung in Map Units
##    #und gibt ihn zurück
##    def findemittelpunkt(self):
##
##        Punkt = self.mc.extent().center()
##        return Punkt


    #die Aufgabe dieser Methode ist: in das View Fenster wird ein Kreuzchen
    #gezeichnet und dann die Höhe dazugeschrieben. Der gesamte Code ist
    #aus dem Modul doAdresssuche kopiert
    def zeichne_hoehenkote(self,xwert,ywert,hoehe):

        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,99,71', 'color_border' : '255,99,71' , 'name' : 'cross', 'size' : '4' }



        #Der Adresstext als Textdokument
        text = QtGui.QTextDocument(self)
        text.setObjectName("hoehe" +  str(hoehe))

        #Das Fontobjekt fürs Textobjekt
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        text.setDefaultFont(font)
        text.setHtml("<font color = \"#FF6347\">" + str(hoehe) + "m" + "</font>")

         # Benötigte Framgröße
        frame_groesse = text.size()

        #Hilfspunkt zur Text/Kreuzchen Positionierung
        punkti = QgsPoint(xwert,ywert)

        #Offset der Textposition
        Offset = QtCore.QPointF()
        Offset.setX(0)
        Offset.setY(0)

        #DAS objekt um Kreuzchen und Text zu zeichnen
        textAnno = QgsTextAnnotationItem(self.iface.mapCanvas())
        textAnno.setFrameSize(frame_groesse)   # ohne Framgröße keine Darstellung im Drucklayout
        textAnno.setMapPosition(punkti)
        textAnno.setFrameBorderWidth(0.0)
        textAnno.setOffsetFromReferencePoint(Offset)

        textAnno.setDocument(text)  #Text zuweisen
        farbe = textAnno.frameColor()   #die Framefarbe auf unsichtbar schalten
        farbe.setAlpha(0)               #sonst gibts ein kleines Darstellungsartefakt
        textAnno.setFrameColor(farbe)


        #textAnno.setMarkerSymbol geht nicht!!
        #deshalb so: wir wollen nicht den Standardknödel
        #sondern ein rotes Kreuzchen
        s = textAnno.markerSymbol() #1. das eingestellte Marker Symbol holen
        #Die neuen Properties...
        sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)   #in der Schleife sonst Probleme im Qgis

        s.changeSymbolLayer(0,sl)   #2. das neue Symbol zuweisen



        #die Adresse jedes Annotationobjekt wird in einen Listenvarible-Pointer
        #geschrieben. Dadurch gehen si beim Schließen des Adresswidget nicht verloren sondern
        #bleiben dem Vogis Menü Plugin erhlaten (zum späteren löschen notwendig)!!
        self.speicheradressen_hoehenmodell.append(textAnno)

        self.mc.refresh()

    #eingezeichnete Hoehenkoten löschen. Über Pointer
    #werden deren Speicheradressen aufgezeichnet und im Hauptobjekt des VogisMenü gespeichert
    #und immer mitübergeben. Dadurch gehen sie solange das Vogis Menü
    #aktiv ist nicht verloren und können immer wieder gelsöcht werden
    def hoeheClear(self):
        mc=self.iface.mapCanvas()
        #die Grafiken sind in einer QGraphicsItemScene
        # die man leider undokumentiert über mc.scene() bekommt!!

        if len(self.speicheradressen_hoehenmodell) > 0:
            for items in self.speicheradressen_hoehenmodell:
                try:
                    mc.scene().removeItem(items)
                except:
                    pass
        mc.refresh()