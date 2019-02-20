# -*- coding: utf-8 -*-
#!/usr/bin/python

import os
from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from qgis.utils import *
from qgis.gui import *

from gui_topokarten import *
#from doHistorische_karten import *
from osgeo import gdal, ogr
from osgeo.gdalconst import *
from direk_laden import direk_laden
from ProjektImport import *


class TopokartenDialog(QtWidgets.QDialog, Ui_frmTopokarten):
    def __init__(self,iface,pfad = None,vogisPfad = None, PGdb = None):
        QtWidgets.QDialog.__init__(self)
        Ui_frmTopokarten.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.db = PGdb
        self.vogisPfad = vogisPfad
        self.mc = self.iface.mapCanvas()
        self.checkButtonsGroup.setExclusive(True)   # wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    # deshalb hier
        # self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)
        self.karten = ProjektImport(self.iface)


    def accept(self):
        self.layerliste = []    #leere Liste, wird mit unserem ind. Datentyp gefüllt werden
        ext = self.mc.extent()


        #layercount = QgsMapLayerRegistry.instance().count()

        buttoncount = 0

        for button in self.checkButtonsGroup.buttons():
            if button.isChecked():
                buttoncount =  + 1
                if   ("Topogr. Karte (VoGIS)" in button.text()):
                    #self.load_raster(self.pfad + "/Topokarte_VoGIS/Vlbg/TopoKarte_Isoli_Text_20t.ecw","Topogr. Karte (VoGIS)",button.text())
                    self.karten.importieren(self.pfad + "/Topokarte_VoGIS/Vlbg/TopoKarte_Sommer.qgs",None,None,None,True,None)

                elif ("Topogr. Karte Winter (VoGIS)" in button.text()):
                    #self.load_raster(self.pfad + "/Topokarte_VoGIS/Vlbg/TopoKarte_Winter_Isoli_Text_20t.ecw","Topogr. Karte Winter (VoGIS",button.text())
                    self.karten.importieren(self.pfad + "/Topokarte_VoGIS/Vlbg/TopoKarte_Winter.qgs",None,None,None,True,None)

                elif ("Topogr. Karte PDF-Ebenen (VoGIS)" in button.text()):
                    os.startfile(self.vogisPfad + "Topographische_Karten/Topokarte_VoGIS/Vlbg/TopoKarte_300t.pdf")

                elif ("Topogr. Karte (Verkehrsverbund)" in button.text()):
                    self.load_raster(self.pfad + "/Topokarte_Verkehrsverbund/topo_vvv.ecw","Topogr. Karte (Verkehrsverbund)",button.text())

                elif (("ÖK 1:50.000 Vlbg. (BEV)") in button.text()):
                    self.load_raster(self.pfad + "/Oek/Vlbg/oek50.tif","ÖK 1:50.000 Vlbg. (BEV)",button.text())

                elif (("ÖK 1:50.000 Vlbg. + Umg. (BEV)") in button.text()):
                    self.load_raster(self.pfad + "/Oek/Vlbg_Umgebung/oek50_umgebung.tif","ÖK 1:50.000 Vlbg. + Umg. (BEV)",button.text())

                elif ("Heimatkarte 1:100.000 (FreytagBerndt)" in button.text()):
                    self.load_raster(self.pfad + "/Freytag_Berndt/Vlbg/freytag_berndt_100.tif","Freytag u. Berndt",button.text())

                elif (("ÖK 1:200.000  (BEV)") in button.text()):
                    self.load_raster(self.pfad + "/Oek/Vlbg/oek200.tif","ÖK 1:200.000  (BEV)",button.text())

                elif (("ÖK 1:500.000  (BEV)") in button.text()):
                    self.load_raster(self.pfad + "/Oek/Vlbg/oek500.tif","ÖK 1:500.000  (BEV",button.text())

                elif ("Urmappe" in button.text()):
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Urmappe/Blattschnitt_Urmappe.shp","Urmappe Blattschnitt",self.pfad + "/_Allgemein/blattschnitt_urmappe.qml",button.text(), 'Urmappe')
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Urmappe/Blattschnitt_Urmappe_Nr.shp","Urmappe Blattschnitt Nr.",self.pfad + "/_Allgemein/blattschnitt_urmappe_nr.qml",button.text(), 'Urmappe')
                    self.load_raster(self.vogisPfad + "Grenzen/Urmappe/Vlbg/um_25cm.ecw","um_25cm",button.text(), 'Urmappe')

                elif ("3. Landesaufnahme" in button.text()):
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_dla.shp","Blattschnitt 3. Landesaufnahme",self.pfad + "/_Allgemein/blattschnitt_hist_dla.qml",button.text(),"3. Landesaufnahme")
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_dla_Nr.shp","Blattschnitt 3. Landesaufnahme Nr",self.pfad + "/_Allgemein/blattschnitt_hist_dla_nr.qml",button.text(),"3. Landesaufnahme")
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/3LA_1871-1872.ecw","3. Landesaufnahme 1871-1872",button.text(),"3. Landesaufnahme")

                elif ("Reambulierte 3. LA 1887:" in button.text()):
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/3RA_1887.ecw","Reambulierte 3. LA 1887:",button.text())

                elif ("Spezialkarte" in button.text()):
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_spezialk.shp","Blattschnitt Spezialkarten",self.pfad + "/_Allgemein/spezialkarte_75000.qml",button.text(), "Spezialkarten")
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_spezialk_Nr.shp","Blattschnitt Spezialkarten Nr",self.pfad + "/_Allgemein/spezialkarte_75000_nr.qml",button.text(), "Spezialkarten")
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/SPZ_1908-1915.ecw","Spezialkarte 1908-15:",button.text(), "Spezialkarten")
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/SPZ_1934-1937.ecw","Spezialkarte 1934-37:",button.text(), "Spezialkarten")

                elif ("Provisorische" in button.text()):
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_prov_oek.shp",("Provisorische ÖK"),self.pfad + "/_Allgemein/provisorische_oeks.qml",button.text(),("Provisorische ÖK"))
                    self.load_vector(self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitt_Hist/Blattschnitt_hist_prov_oek_Nr.shp",("Provisorische ÖK Nr."),self.pfad + "/_Allgemein/provisorische_oeks_nr.qml",button.text(),("Provisorische ÖK"))
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/OEK50_Prov_1946-47.ecw","Provisorische ÖK 1946-47",button.text(),("Provisorische ÖK"))

                elif (("ÖK50 1953-67:") in button.text()):
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/OEK50_1953-1967.ecw",("ÖK50 1953-67"),button.text())

                elif (("ÖK50 1961-74:") in button.text()):
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/oek50_1961-1974.ecw",("ÖK50 1961-74"),button.text())

                elif (("ÖK50 1971-80:") in button.text()):
                    self.load_raster(self.pfad + "/Historische_Karten/Vlbg/OEK50_1971-1980.ecw",("ÖK50 1971-80"),button.text())

                elif self.radioButton_11.isChecked():
                    self.load_vector(self.vogisPfad + "Points_of_Interest/Ortsbezeichnung/Vlbg/oek_geonam/geonam_text.shp",("Geonam ÖK 50"),self.pfad + "/_Allgemein/blattschnitt_urmappe.qml",button.text())

                else:
                    QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))


        #Warnung wenn keine Themen ausgewählt wurden
        if buttoncount == 0:
            QtWidgets.QMessageBox.warning(None, "Keine Themen ausgewaehlt", "<P><FONT SIZE='10' COLOR='#B00000'>Keine Themen ausgewaehlt !</FONT></P>")



    #************************************************************************************************
    # load_raster()
    #************************************************************************************************
    def load_raster(self,path,basename,button_text, gruppenname = ''):

        #Prüfen ob der Layer schon einmal geladen wurde!
        #Das machen wir halt nur über den Namen, aber das reicht!
        #if len(QgsMapLayerRegistry.instance().mapLayersByName(basename)) < 1:
        if len(QgsProject.instance().mapLayersByName(basename)) < 1:
            layer = QgsRasterLayer((path),"base" + basename)         #wichtig für die Aktualisierung der legende
                                                                                    #der anzeigename muß sich ändern sonst gehts nicht
            #QgsMapLayerRegistry.instance().addMapLayer(layer)
            QgsProject.instance().addMapLayer(layer)
        else:
            return
        if not gruppenname == '':
            self.gruppe(gruppenname,layer)

        self.nach_unten(layer,basename,gruppenname)



    #laden von Vektordaten und QML
    #hier wird keine Liste verwendet, sondern der Aufruf erfolgt immer einzeln
    def load_vector(self,path,basename,qmlpath,button_text, gruppenname = ''):

            #Prüfen ob der Layer schon einmal geladen wurde!
            #Das machen wir halt nur über den Namen, aber das reicht!
            #if len(QgsMapLayerRegistry.instance().mapLayersByName(basename)) < 1:
            if len(QgsProject.instance().mapLayersByName(basename)) < 1:
                self.mc.setRenderFlag(False)

                shapename = str.strip(str(os.path.basename(path)))
                path = str.strip(str(os.path.dirname(path)))
                layer = direk_laden(self.db, basename, shapename, path,self.iface)


                if not layer.isValid():
                    QtWidgets.QMessageBox.about(None, "Fehler beim laden des Themas", "%s /nFehler:%s " %(button_text(),str(geonam.lastError())))
                else:
                    if type(layer) is QgsVectorLayer: #nur Raster werden in der Legende nach unten geschoben


                        flagge = layer.loadNamedStyle(qmlpath)
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.layerTreeView().refreshLayerSymbology( layer.id() )
                        else:
                            QtWidgets.QMessageBox.about(None, "Fehler", "QML konnte nicht zugewiesen werden!")
                        QgsProject.instance().addMapLayer(layer)


                if not gruppenname == '':
                    self.gruppe(gruppenname, layer)
                self.mc.setRenderFlag(True)


    # Gruppenlayer falls notwendig erzeugen und
    # VEKTOR layer reinbewegen und dann die Gruppe
    # ganz nach unten schieben. RASTER werden
    # hier nicht abgearbeitet!
    def gruppe(self,layername,layerobjekt):

        gruppe_vorhanden = False
        if not (layername == ''):

            if QgsProject.instance().layerTreeRoot().findGroup(layername) != None: #Name ist übergeben worden
                    gruppe_vorhanden = True



        self.legendTree= QgsProject.instance().layerTreeRoot()

        #Ist die Gruppe nicht vorhanden , anlegen
        if (not gruppe_vorhanden):
            grp = self.legendTree.insertGroup(-1,layername)

        if type(layerobjekt) is QgsVectorLayer:
            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(layerobjekt.id()) #der geladene layer
            index = zwtsch.clone()
            grp = QgsProject.instance().layerTreeRoot().findGroup(layername) #der geladene layer
            grp.insertChildNode(0,index)
            zwtsch.parent().removeChildNode(zwtsch)
            grp.setExpanded(False)
        else:
            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(layerobjekt.id()) #der geladene layer
            dummy_2 = zwtsch.clone()
            grp = QgsProject.instance().layerTreeRoot().findGroup(layername) #der geladene layer
            grp.insertChildNode(-1,dummy_2)
            zwtsch.parent().removeChildNode(zwtsch)
            dummy_2.setExpanded(False)
            grp.setExpanded(False)

        self.legendTree= QgsProject.instance().layerTreeRoot()

    # Die Raster werden in der Legende nach unten geschoben
    # egal ob in einer Gruppe oder ausserhalb
    def nach_unten(self, layer, anzeigename, gruppenname = ''):

        QgsProject.instance().addMapLayer(layer)
        if type(layer) is QgsRasterLayer: #nur Raster werden in der Legende nach unten geschoben

            if gruppenname == '':
                zwtsch = QgsProject.instance().layerTreeRoot().findLayer(layer.id()) #der geladene layer
                dummy_2 = zwtsch.clone()
                QgsProject.instance().layerTreeRoot().insertChildNode(-1,dummy_2)
                zwtsch.parent().removeChildNode(zwtsch)
                dummy_2.setExpanded(False)
                anzeigename = (anzeigename)
                layer.setName(anzeigename)
            else:
                zwtsch = QgsProject.instance().layerTreeRoot().findLayer(layer.id()) #der geladene layer
                dummy_2 = zwtsch.clone()
                grp = QgsProject.instance().layerTreeRoot().findGroup(gruppenname) #der geladene layer
                grp.insertChildNode(-1,dummy_2)

                zwtsch.parent().removeChildNode(zwtsch)
                dummy_2.setExpanded(False)
                anzeigename = (anzeigename)
                layer.setName(anzeigename)
                grp.setExpanded(False)



#diese Klasse ist nichts anderes wie eine
#art struct, wir wollen das layerobjekt (Typ QgsMapLayer)
#und den Anzeigename in einem Datentyp zusammenfassen
class rastername:
    def __init__(self):
        self.rasterobjekt = QgsRasterLayer()
        self.anzeigename = str


