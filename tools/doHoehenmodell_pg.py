# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui, QtCore ,QtXml

from qgis.core import *
from qgis.gui import *
from gui_hoehenmodell_pg import *
from osgeo import ogr, gdal
import logging, os
from direk_laden import direk_laden
from doTextAnno import *



class HoehenmodellDialog_PG(QtWidgets.QDialog, Ui_frmHoehenmodell):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_hoehenmodell,pfad = None,vogisPfad = None, PGdb = None):

         #Ein individuelles Signal als Klassenvariable definieren
        #Abflug = QtCore.pyqtSignal(object)

        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
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

        # Das Basishöhenmodell dient zum Abfragen
        # derGeländehöhen mit dem Kreuzchen
        # self.basisraster_04 = QgsRasterLayer(pfad+"/Hoehenmodelle/Vlbg/gt2004_01m.img","hidden")
        # self.basisraster_11 = QgsRasterLayer(pfad+"/Hoehenmodelle/Vlbg/gt2011_50cm.img","hidden")

        # Geht unter QGIS 3 nur mehr mit GDAL vernünftig!
        self.basisraster = gdal.Open(pfad+"/Hoehenmodelle/Vlbg/gt2011_50cm.img", gdal.GA_ReadOnly)

        # Gibt eine Liste mit 6 Werten zurück
        self.transform = self.basisraster.GetGeoTransform()



##        if not self.basisraster_04.isValid():
        if self.basisraster == None:
            QtWidgets.QMessageBox.about(None, "Fehler", ("Laden des Basishöhenmodells fehlgeschlagen"))
            self.btHoehenabfrage.setEnabled(False)
            self.leX.setEnabled(False)
            self.leY.setEnabled(False)
            self.leZ.setEnabled(False)
##        if not self.basisraster_11.isValid():
##            QtWidgets.QMessageBox.about(None, "Fehler", ("Laden des Basishöhenmodells 0.5m fehlgeschlagen"))
##            self.btHoehenabfrage.setEnabled(False)
##            self.leX.setEnabled(False)
##            self.leY.setEnabled(False)
##            self.leZ.setEnabled(False)




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
        #QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
        self.mc.mapToolSet.connect(self.MapButtonZuruecksetzen)




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
                    if len(QgsProject.instance().mapLayersByName((anzeigename))) < 1:



                        #Rasterdatensatz laden und auf gültigkeit prüfen
                        fileinfo = QtCore.QFileInfo(pfad_ind)
                        basename = fileinfo.baseName()

                        # Settings veröndern damit der User kein CRS Prompt
                        # bekommt mit dem er nichts anfangen kann - steht in der QGIS3.ini
                        settings_before = QgsSettings()
                        default_behavior = settings_before.value( "/Projections/defaultBehavior" )
                        default_layer_crs = settings_before.value( "/Projections/layerDefaultCrs" )
                        settings_before.setValue( "/Projections/defaultBehavior", "useGlobal" )
                        settings_before.setValue( "/Projections/layerDefaultCrs", "EPSG:31254" )

                        #Raster erzeugen und Darstellung zuweisen
                        raster = QgsRasterLayer(pfad_ind,basename)

                        # Settings wieder zurücksetzen
                        settings_before.setValue( "/Projections/defaultBehavior", default_behavior )
                        settings_before.setValue( "/Projections/layerDefaultCrs", default_layer_crs )

                        raster.setContrastEnhancement(contrast) #Entspricht StretchToMinimumMaximum wenn wert 1
                        if not raster.isValid():
                            QtWidgets.QMessageBox.about(None, "Fehler", "Laden des Datensatzes fehlgeschlagen")
                            return #Ausführung des Sub wird hier einfach abgebrochen

                        QgsProject.instance().addMapLayer(raster)

                        zwtsch = QgsProject.instance().layerTreeRoot().findLayer(raster.id()) #der geladene layer
                        dummy_2 = zwtsch.clone()
                        QgsProject.instance().layerTreeRoot().insertChildNode(-1,dummy_2)
                        zwtsch.parent().removeChildNode(zwtsch)
                        dummy_2.setExpanded(False)




                        #der nachfolgende Code erzwingt eine Aktualisierung
                        #der Legende und des MapWindow
                        #Ansonsten kanns im Mapwindow darstellungsprobleme geben! Wiso??
                        if not raster is None:

                            raster.setName((anzeigename))   #ACHTUNG: Damit wird auch erzwungen, daß die Layerdarstellung
                                                                                #(Reihenfolge) aktualisiert wird!!


                        anzeigename = ""
                else:

                    #Prüfen ob der Layer schon einmal geladen wurde!
                    #Das machen wir halt nur über den Namen, aber das reicht!
                    if len(QgsProject.instance().mapLayersByName(basename_vektor)) < 1:

                        #isolinien laden
                        #isolinien = QgsVectorLayer(pfad_ind, basename_vektor,"ogr")

                        shapename = os.path.basename(pfad_ind)
                        pfad = os.path.dirname(pfad_ind)

                        isolinien = direk_laden(self.db, basename_vektor, shapename, pfad,self.iface)
                        #und prüfen ob erfolgreich geladen
                        if isolinien == None: #nicht erfolgreich geladen
                            QtWidgets.QMessageBox.about(None, "Fehler", basename_vektor + " konnte nicht geladen werden")
                            return
                        else:   #erfolgreich geladen
                            #dem Vektorlayer das QML File zuweisen
                            #flagge[1] ist false wenn das file nich gefunden wird
                            flagge = isolinien.loadNamedStyle(basename_qml)
                            if flagge[1]:
                                #Legendenansicht aktualisieren
                                self.iface.layerTreeView().refreshLayerSymbology( isolinien.id() )
                            else:
                                QtWidgets.QMessageBox.about(None, "Fehler",  basename_qml + "konnte nicht zugewiesen werden!")
                            #Zur Map Layer registry hinzufügen damit der Layer
                            #dargestellt wird
                            QgsProject.instance().addMapLayer(isolinien)

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
        #QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)
##        self.basisraster_04 = None
##        self.basisraster_11 = None
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
            #QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnHoehe)
            self.PtRueckgabe.canvasClicked.connect(self.returnHoehe)
            #den anderen Knopf wieder lösen!
            #QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnBlattschnitt)


        #Nichts ist gechecked, deshalb alles zurücksetzen
        else:
            self.iface.mapCanvas().setMapTool(self.tool_vorher)    #auf ursprüngliches Maptool und zugehörigen Cursor zurücksetzen
            self.tool_vorher = None
            #QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnBlattschnitt)
            #QtCore.QObject.disconnect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnHoehe)

    #Gibt die Höhe des DGM am angeklickten Ort zurück bzw. füllt damit die lineedit Felder
    #punkt enthält die Koordinaten des angeklickten Punkts
    def returnHoehe(self,punkt):


        # In QGIS 3 nun über GDAL
        xOrigin = self.transform[0] # X Koordinate links Oben des gesamten Rasters
        yOrigin = self.transform[3] # Y Koordinate links Oben des gesamten Rasters
        pixelWidth = self.transform[1] # Pixelbreite in Real World Units
        pixelHeight = self.transform[5]  # Pixelhöhe in Real World Units

        xOffset = int((punkt.x() - xOrigin) / pixelWidth)
        yOffset = int((punkt.y() - yOrigin) / pixelHeight)

        band = self.basisraster.GetRasterBand(1)
        data = band.ReadAsArray(xOffset,yOffset,1,1) # gibt ein numpy Array zurück

        #QtWidgets.QMessageBox.about(None, "Provi",str(data))


        #wenn man ins Nirvana klickt gibts sonst nen Fehler
        #Deshalb das Ganze etwas abfangen!
        #if not maeppchen[(maeppchen.keys()[0])] == None:
        if (not data == None) and round(float(data) > 0):
           data = data [0,0]
           self.leX.setText(str(int(round(punkt.x(),0))))
           self.leY.setText(str(int(round(punkt.y(),0))))
           #self.leZ.setText(str(round(float(maeppchen[(maeppchen.keys()[0])]),1))) #Hohe gerundet auf dezimeter wird ins Linedit geschrieben"
           self.leZ.setText(str(round(float(data),1))) #Hohe gerundet auf dezimeter wird ins Linedit geschrieben"
        else:
            QtWidgets.QMessageBox.critical(None, "Fehler", ("Ungültiger Wertebereich"))
            self.leX.setText("ungueltig")
            self.leY.setText("ungueltig")
            self.leZ.setText("ungueltig")
            return


        #Aufruf der Methode, die an die geklickte Stelle ein kleines Kreuzchen
        #macht und die Höhe dazuschreibt
        self.zeichne_hoehenkote(punkt.x(),punkt.y(),str(round(float(data),1)))




    #die Aufgabe dieser Methode ist: in das View Fenster wird ein Kreuzchen
    #gezeichnet und dann die Höhe dazugeschrieben. Der gesamte Code ist
    #aus dem Modul doAdresssuche kopiert
    def zeichne_hoehenkote(self,xwert,ywert,hoehe):

        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,99,71', 'color_border' : '255,99,71' , 'name' : 'cross', 'size' : '4' }


        #Hilfspunkt zur Text/Kreuzchen Positionierung
        punkti = QgsPointXY(xwert,ywert)

        #Offset der Textposition
        Offset = QtCore.QPointF()
        Offset.setX(0)
        Offset.setY(0)



        # Das spezielle QgsMapCanvasAnnotationItem Objekt
        zeichne_mich = draw_text_class(self.mc, str(hoehe),props,punkti,Offset)
        self.textanno = zeichne_mich.gen()


        self.speicheradressen_hoehenmodell.append(self.textanno)

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

########################################
# Eigene Plugin Klasse.
########################################
class ind_raster(QgsRasterLayer):

    def __init__(self,pfad):
        QgsRasterLayer.__init__(self)

