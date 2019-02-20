# -*- coding: utf-8 -*-
#!/usr/bin/python

from builtins import str
from builtins import range
from builtins import object
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.uic import *

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from ProjektImport import *

from osgeo import gdal, ogr
from osgeo.gdalconst import *
from gui_geologie import *



class GeologieDialog(QtWidgets.QDialog, Ui_frmGeologie):
    def __init__(self,iface,pfad = None,vogisPfad = None):
        QtWidgets.QDialog.__init__(self)
        Ui_frmGeologie.__init__(self)



        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.checkButtonsGroup.setExclusive(True)       #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
        self.checkButtonsGroup2.setExclusive(True)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
        self.checkButtonsGroup5.setExclusive(False)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
        # Legendeninterface instanzieren. Wird gebraucht um die Layer checked oder uncheckd zu schalten (Kreuzchen)
        #self.leginterface = self.iface.legendInterface()
        self.vogisPfad = vogisPfad

    #************************************************************************************************
    # load_raster()
    #************************************************************************************************
    def load_raster(self,path,basename,button_text):

        #Prüfen ob der Layer schon einmal geladen wurde!
        #Das machen wir halt nur über den Namen, aber das reicht!
        #if len(QgsMapLayerRegistry.instance().mapLayersByName(button_text)) < 1:
        if len(QgsProject.instance().mapLayersByName(button_text)) < 1:
            layer = QgsRasterLayer(path,basename)
        else:
            return

        Lyr = rastername() #ind. datentyp!
        if not layer.isValid():
            QtWidgets.QMessageBox.warning(None, "Fehler beim laden des Themas", "Thema:%s /nPfad: %s/nFehler:%s " %(button_text,path,str(layer.lastError())))
        else:
            Lyr.anzeigename = button_text
            Lyr.rasterobjekt = layer
            self.layerliste.append(Lyr)

    #************************************************************************************************
    # accept()
    #************************************************************************************************
    def accept(self):



        rlayer = []
        self.layerliste = []    #leere Liste, wird mit unserem ind. Datentyp gefüllt werden
        projekt = ProjektImport(self.iface)

        mc=self.iface.mapCanvas()
        ext = mc.extent()

        mc.setRenderFlag(False)

        #layercount = QgsMapLayerRegistry.instance().count()
        layercount = len(QgsProject.instance().layerTreeRoot().findLayers())

        #-------------------------------------
        # Lasche: Allgemein
        #-------------------------------------
        if (self.tabWidget.currentIndex() == 0):
            buttoncount = 0

            for button in self.checkButtonsGroup.buttons():
                if button.isChecked():
                    buttoncount =  + 1
                    if   ("Geologische Karte Vorarlberg (GBA, 2007)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Geologischekarte_GBA/geologischekarte.qgs",None,None,None,None,"Geologische Karte Vorarlberg (GBA, 2007)")
                    elif ("Geologische_Tektonische Karte (GBA, 1998)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Geotektonischekarte_GBA/geotektonischekarte.qgs",None,None,None,None,"Geologische_Tektonische Karte (GBA, 1998)")

                    elif ("Bohrprofile" in button.text()):
                        projekt.importieren(self.pfad + "/Bohrungen/Vlbg/Bohrprofil/bohrprofil.qgs",)

                    elif ("Ereigniskataster" in button.text()):
                        projekt.importieren(self.pfad + "/Ereigniskataster/Vlbg/ereigniskataster.qgs",)

                    elif ("Geologische Detailuntersuchungen" in button.text()):
                        projekt.importieren(self.pfad + "/Geologie_Detailuntersuchungen/Vlbg/Geologie_Detailuntersuchungen/Geologie_Detailuntersuchungen.qgs",None,None,None,None,"Geologische Detailuntersuchungen")

                    elif ("Geologische Karte (Richter)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Geologischekarte_Richter/geologischekarte_richter.qgs",None,None,None,None, "Geologische Karte (Richter)")

                    elif ("Geologie Rheintal (Starck, 1970)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Rheintal/Geologie_Starck/Geologie_Starck.qgs",None,None,None,None,None)

                    elif ("Geomorphologische Karten (Uni Amsterdam)" in button.text()):
                        aaa = 23

                    elif ("Gefahrenhinweiskarte (GBA, 2006)" in button.text()):
                        projekt.importieren(self.pfad + "/Georisiko_Karte/Vlbg/Gefahrenhinweiskarte/Gefahrenhinweiskarte.qgs",None,None,None,None,"Gefahrenhinweiskarte (GBA, 2006)")

                    elif ("Georisken Montafon (Bertle, 1995)" in button.text()):
                        projekt.importieren(self.pfad + "/Georisiko_Karte/Montafon/Georisikokarte_Bertle/georisken.qgs",None,None,None,None,None)

                    elif ("Geotop-Inventar" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Geotopinventar/geotopinventar.qgs",None,None,None,None,"Geotop-Inventar")

                    elif ("Grundwasser-Chemismus Rheintal (Starck)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Rheintal/Grundwasser_Starck/gwch_Starck.qgs",None,None,None,None,None)

                    elif ("Grundwasser-Schichten_Linien Rheintal (nur VIIa)" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Rheintal/grundwasser_schichtenlinien.qgs",None,None,None,None,"Grundwasser-Schichten_Linien Rheintal (nur VIIa)")

                    elif (("Historische Übersichtskarte (Schmidt 1839-1841") in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Schmidt_1839/schmidt1839.qgs",None,None,None,None,("Historische Übersichtskarte (Schmidt 1839-1841"))

                    else:
                        QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))

            #Warnung wenn keine Themen ausgewählt wurden
            if buttoncount == 0:
                QtWidgets.QMessageBox.warning(None, "Keine Themen ausgewaehlt", "<P><FONT SIZE='10' COLOR='#B00000'>Keine Themen ausgewaehlt !</FONT></P>")


        #-------------------------------------
        # Lasche: Geologische Gebietskarten
        #-------------------------------------
        if (self.tabWidget.currentIndex() == 1):
            buttoncount = 0
            for button in self.checkButtonsGroup2.buttons():
                if button.isChecked():
                    buttoncount =  + 1
                    if ("Übersichtskarten" in button.text()):
                        projekt.importieren(self.pfad + "/Geologische_Karte/Vlbg/Karten_Uebersicht/geologie_uebersicht.qgs",)

                    elif ("Arlberggebiet (GBA, 1932)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Arlberggebiet.ecw","geo_Arlberggebiet",button.text())

                    elif ("Bezau (GBA, Manuskript)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Bezau.ecw","geo_Bezau",button.text())

                    elif ("Bregenz (GBA, 1982)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Bregenz.ecw","geo_Bregenz",button.text())

                    elif ("Dornbirn Nord (GBA, 1994)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Dornbirn_nord.ecw","geo_Dornbirn_nord",button.text())

                    elif ("Dornbirn Süd (GBA, 1982)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Dornbirn_sued.ecw","geo_Dornbirn_sued",button.text())

                    elif ("Flexenpass (Doert und Helmcke, 1975)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/Geo_Flexenpass.ecw","Geo_Flexenpass",button.text())

                    elif ("Heiterwand (Tirol) (GBA, 1932)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Tirol/geo_Heiterwand.ecw","geo_Heiterwand",button.text())

                    elif ("Klostertal (Helmcke, 1972)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/Geo_Klostertal.ecw","Geo_Klostertal",button.text())

                    elif ("Klostertaler Alpen (GBA, 1932)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Klostertaleralpen.ecw","geo_Klostertaleralpen",button.text())

                    elif ("Liechtenstein (RFL, 1985)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Liechtenstein.ecw","geo_Liechtenstein",button.text())

                    elif ("Mittelberg (GBA, 1990)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Mittelberg.ecw","geo_Mittelberg",button.text())

                    elif ("Parseiergruppe (Tirol)  (GBA, 1932)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Tirol/geo_Parseiergruppe.ecw","geo_Parseiergruppe",button.text())

                    elif ("Partenen Ost (GBA, 1980)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Partenen_ost.ecw","geo_Partenen_ost",button.text())

                    elif ("Partenen West (GBA, 1980)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Partenen_west.ecw","geo_Partenen_west",button.text())

                    elif ("Rätikon (GBA)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Raetikon.ecw","geo_Raetikon",button.text())

                    elif ("Schönenbach" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Schoenenbach.ecw","geo_Schoenenbach",button.text())

                    elif ("Stuben (GBA, 1937)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Stuben.ecw","geo_Stuben",button.text())

                    elif ("Sulzberg (GBA, 1984)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Sulzberg.ecw","geo_Partenen_west",button.text())

                    elif ("Vorderwald (Muheim, 1934)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/Geo_Vorderwald.ecw","Geo_Vorderwald",button.text())

                    elif ("Walgau (GBA, 1967)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/geo_Walgau.ecw","geo_Walgau",button.text())

                    elif ("Walsertal (Otte und Helmcke)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Karte/Vlbg/Geo_Walsertal.ecw","Geo_Walsertal",button.text())

                    else:
                        QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))

            #Warnung wenn keine Themen ausgewählt wurden
            if buttoncount == 0:
                QtWidgets.QMessageBox.warning(None, "Keine Themen ausgewaehlt", "<P><FONT SIZE='10' COLOR='#B00000'>Keine Themen ausgewaehlt !</FONT></P>")



        #-------------------------------------
        # Lasche: Geologische Detailkarten
        #-------------------------------------
        if (self.tabWidget.currentIndex() == 2):
            buttoncount = 0
            for button in self.checkButtonsGroup3.buttons():
                if button.isChecked():
                    buttoncount =  + 1
                    if ("Ausser Montafon (Bertha, 1978)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Ausser_Montafon.ecw","geo_Ausser_Montafon",button.text())

                    elif ("Dalaas (Koehler, 1977)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Dalaas.ecw","geo_Dalaas",button.text())

                    elif ("Davenna (Kasper, 1990)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Davenna.ecw","geo_Davenna",button.text())

                    elif ("Firstkette (Golde, 1993)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Firstkette.ecw","geo_Firstkette",button.text())

                    elif ("Gafadura (Post, 1996)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Gafadura.ecw","geo_Gafadura",button.text())

                    elif ("Gargellen (Bertle, 1972)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Gargellen.ecw","geo_Gargellen",button.text())

                    elif ("Gopfberg (Oberhauser M., 1993)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Gopfberg.ecw","geo_Gopfberg",button.text())

                    elif ("Rätikon östlich (Steinacher, 2004)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Raetikon_st1.ecw","geo_Raetikon_st1",button.text())
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Raetikon_st2.ecw","geo_Raetikon_st2",button.text())

                    elif ("Rätikon östlich (Mayerl, 2005)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Raetikon_ma.ecw","geo_Raetikon_ma",button.text())

                    elif ("Sibratsgfäll (Haak, 1995)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Sibratsgfaell.ecw","geo_Sibratsgfaell",button.text())

                    elif ("Tschagguns - Mauren (Bertle, 1995)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Tschagguns_Mauren.ecw","geo_Tschagguns_Mauren",button.text())

                    elif ("Tschöppa (Bertle, 1992)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Tschoeppa.ecw","geo_Tschoeppa",button.text())

                    elif ("Winterstaude (Oberhauser)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Winterstaude_ka.ecw","geo_Winterstaude_ka",button.text())

                    elif ("Winterstaude (Alexander)" in button.text()):
                        self.load_raster(self.pfad + "/Geologische_Detailkarte/Vlbg/geo_Winterstaude_ka.ecw","geo_Winterstaude_ka",button.text())

                    else:
                        QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))







            #Warnung wenn keine Themen ausgewählt wurden
            if buttoncount == 0:
                QtWidgets.QMessageBox.warning(None, "Keine Themen ausgewaehlt", "<P><FONT SIZE='10' COLOR='#B00000'>Keine Themen ausgewaehlt !</FONT></P>")


        #-------------------------------------
        # Lasche: Georisiko-Kraten (AGK)
        #-------------------------------------
        if (self.tabWidget.currentIndex() == 3):
            buttoncount = 0
            for button in self.checkButtonsGroup4.buttons():
                if button.isChecked():
                    buttoncount =  + 1
                    # Geologie
                    if ("Alberschwende" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geol_Alberschwende.ecw","Geol_Alberschwende",button.text())

                    elif ("Au" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geol_Au.ecw","Geol_Au",button.text())

                    elif ("Faschina" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geol_Faschina.ecw","Geol_Faschina",button.text())

                    elif ("Hochtannberg/Arlberg" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geol_Hochtannberg_Arlberg.ecw","Geol_Hochtannberg_Arlberg",button.text())

                    elif ("Sibratsgfäll" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geol_Sibratsgfaell.ecw","Geol_Sibratsgfaell",button.text())

                    # Rutschung
                    elif ("Alberschwende" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Rutschung_Alberschwende.ecw","Georisk_Rutschung_Alberschwende",button.text())

                    elif ("Faschina" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Rutschung_Faschina.ecw","Georisk_Rutschung_Faschina",button.text())

                    elif ("Hochtannberg" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Rutschung_Hochtannberg.ecw","Georisk_Rutschung_Hochtannberg",button.text())

                    elif ("Schoppernau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Rutschung_Schoppernau.ecw","Georisk_Rutschung_Schoppernau",button.text())

                    elif ("Walgau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Rutschung_Walgau.ecw","Georisk_Rutschung_Walgau",button.text())

                    # Steinschlag
                    elif ("Hochtannberg" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Steinschlag_Hochtannberg.ecw","Georisk_Steinschlag_Hochtannberg",button.text())

                    elif ("Klostertal" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Steinschlag_Klostertal.ecw","Georisk_Steinschlag_Klostertal",button.text())

                    elif ("Mellau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Steinschlag_Mellau.ecw","Georisk_Steinschlag_Mellau",button.text())

                    elif ("Schröcken" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Steinschlag_Schroecken.ecw","Georisk_Steinschlag_Schroecken",button.text())

                    elif ("Walgau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Georisk_Steinschlag_Walgau.ecw","Georisk_Steinschlag_Walgau",button.text())

                    # Geotechnik
                    elif ("Alberschwende Nord" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Alberschwende_N.ecw","Geotech_Alberschwende_N",button.text())

                    elif ("Alberschwende Süd" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Alberschwende_S.ecw","Geotech_Alberschwende_S",button.text())

                    elif ("Au" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Au.ecw","Geotech_Au",button.text())

                    elif ("Flexenpass" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Flexenpass.ecw","Geotech_Flexenpass",button.text())

                    elif ("Ippacherwald" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Ippacherwald.ecw","Geotech_Ippacherwald",button.text())

                    elif ("Lech" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Lech.ecw","Geotech_Lech",button.text())

                    elif ("Mellau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Lech.ecw","Geotech_Lech",button.text())

                    elif ("Schoppernau" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Schoppernau.ecw","Geotech_Schoppernau",button.text())

                    elif ("Schröcken" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Schroecken.ecw","Geotech_Schroecken",button.text())

                    elif ("Schwarzachtobel" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Schwarzachtobel.ecw","Geotech_Schwarzachtobel",button.text())

                    elif ("Sibratsgfäll" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Sibratsgfaell.ecw","Geotech_Sibratsgfaell",button.text())

                    elif ("Warth" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Warth.ecw","Geotech_Warth",button.text())

                    elif ("Warth/Saloberkopf" in button.text()):
                        self.load_raster(self.pfad + "/Georisiko_Karte/Vlbg/Geotech_Warth_Saloberkopf.ecw","Geotech_Warth_Saloberkopf",button.text())

                    else:
                        QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))

            #Warnung wenn keine Themen ausgewählt wurden
            if buttoncount == 0:
                QtWidgets.QMessageBox.warning(None, "Keine Themen ausgewaehlt", "<P><FONT SIZE='10' COLOR='#B00000'>Keine Themen ausgewaehlt !</FONT></P>")

        #-------------------------------------
        # Lasche: Geomorpholigie UNI Amsterdam
        #-------------------------------------
        if (self.tabWidget.currentIndex() == 4):
            buttoncount = 0
            for button in self.checkButtonsGroup5.buttons():
                if button.isChecked():
                    buttoncount =  + 1
                    if ("Geomorph. Legende (Orginal)" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/Geomorphologische_Legende_Original.tif","Geomorphologische_Legende_Original",button.text())

                    elif ("Geomorph. Legende (Deutsch)" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/Geomorphologische_Legende.tif","Geomorphologische_Legende",button.text())

                    elif ("Blatt Au:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_au.tif","geomorph_au",button.text())

                    elif ("Blatt Bartholomäberg:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_bartholomaeberg.tif","geomorph_bartholomaeberg",button.text())

                    elif ("Blatt Bezau:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_bezau.tif","geomorph_bezau",button.text())

                    elif ("Blatt Bizau:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_bizau.tif","geomorph_bizau",button.text())

                    elif ("Blatt Brand-Nord:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_brand-nord.tif","geomorph_brand-nord",button.text())

                    elif ("Blatt Brand-Süd:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_brand-sued.tif","geomorph_brand-sued",button.text())

                    elif ("Blatt Damüls:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_damuels.tif","geomorph_damuels",button.text())

                    elif ("Blatt Damülser Mittagsspitze:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_damuelser-mittagsspitze.tif","geomorph_damuels",button.text())

                    elif ("Blatt Diedamskopf:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_diedamskopf.tif","geomorph_diedamskopf",button.text())

                    elif ("Blatt Dunza-Tschengla:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_dunza-tschengla.tif","geomorph_dunza-tschengla",button.text())

                    elif ("Blatt Fundelkopf:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_fund-kopf.tif","geomorph_fund-kopf",button.text())

                    elif ("Blatt Gampberg:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_gampberg.tif","geomorph_gampberg",button.text())

                    elif ("Blatt Gurtis:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_gurtis.tif","geomorph_gurtis",button.text())

                    elif ("Blatt Klaus-Weiler:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_fund-kopf.tif","geomorph_fund-kopf",button.text())

                    elif ("Blatt Hopfreben:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_hopfreben.tif","geomorph_hopfreben",button.text())

                    elif ("Blatt Ludesch:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_ludesch.tif","geomorph_ludesch",button.text())

                    elif ("Blatt Marul:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_marul.tif","geomorph_marul",button.text())

                    elif ("Blatt Mellau:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_mellau.tif","geomorph_mellau",button.text())

                    elif ("Blatt Mellenspitze:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_mellenspitze.tif","geomorph_mellenspitze",button.text())

                    elif ("Blatt Mittleres Silbertal:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_mittleres-silbertal.tif","geomorph_mittleres-silbertal",button.text())

                    elif ("Blatt Nenzinger Himmel:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_nenzinger-himmel.tif","geomorph_nenzinger-himmel",button.text())

                    elif ("Blatt Rellstal-Golm:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_rellstal-golm.tif","geomorph_rellstal-golm",button.text())

                    elif ("Blatt Rellstal-Zimba:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_rellstal-zimba.tif","geomorph_rellstal-zimba",button.text())

                    elif ("Blatt Satteins:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_satteins.tif","geomorph_satteins",button.text())

                    elif ("Blatt Schnepfau:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_schnepfau.tif","geomorph_schnepfau",button.text())

                    elif ("Blatt Schnifis:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/Geomorph_Schnifis.tif","Geomorph_Schnifis",button.text())

                    elif ("Blatt Schoppernau:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_schoppernau.tif","geomorph_schoppernau",button.text())

                    elif ("Blatt Schönenbach:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_schoenenbach.tif","geomorph_schoenenbach",button.text())

                    elif ("Blatt Silbertal:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_silbertal.tif","geomorph_silbertal",button.text())

                    elif ("Blatt Sonntag:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_sonntag.tif","geomorph_sonntag",button.text())

                    elif ("Blatt St. Gallenkirch:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_st_gallenkirch.tif","geomorph_st_gallenkirch",button.text())

                    elif ("Blatt Zitterklapfen:" in button.text()):
                        self.load_raster(self.pfad + "/Geomorphologische_Karte/Vlbg/geomorph_zitterklapfen.tif","geomorph_zitterklapfen",button.text())

                    else:
                        QtWidgets.QMessageBox.warning(None, "Thema nicht vorhanden", "<P><FONT SIZE='16' COLOR='#800000'>%s</FONT></P>" %(button.text()))

        #--------------------------------------------------------------------------
        # Max-Extent der Layers ermitteln wenn keine Layer zuvor geladen wurden.
        #--------------------------------------------------------------------------
        if layercount == 0:
            xmin =  999999999999.9
            xmax = -999999999999.9
            ymin =  999999999999.9
            ymax = -999999999999.9
            for i in range(len(rlayer)):
                a = rlayer[i].extent()
                if a.xMinimum() < xmin:
                    xmin = a.xMinimum()
                if a.xMaximum() > xmax:
                    xmax = a.xMaximum()
                if a.yMinimum() < ymin:
                    ymin = a.yMinimum()
                if a.yMaximum() > ymax:
                    ymax = a.yMaximum()
            #QtGui.QMessageBox.about(None, "Computed Extent", "<FONT SIZE='12' COLOR='#0000A0'>X: %s  %s   Y: %s  %s</FONT></P>"  %(xmin , xmax, ymin, ymax))

        #-----------------------------------------------------------------
        # Max-Extent stzen wenn keine Layer zuvor geladen wurden.
        #-----------------------------------------------------------------
        if layercount == 0:
            rect = QgsRectangle(xmin, xmax, ymin , ymax )
            mc.setExtent(rect)
        gruppenname = ""
        if (self.tabWidget.currentIndex() == 4): #Geoelogie Allgemein
            gruppenname = "Geomorphologie UNI Amsterdam"
        elif (self.tabWidget.currentIndex() == 3): #Geoelogie Allgemein
            gruppenname = "Georisiko Karten"
        elif (self.tabWidget.currentIndex() == 2): #Geoelogie Allgemein
            gruppenname = "Geologische Detailkarten"
        elif (self.tabWidget.currentIndex() == 1): #Geoelogie Allgemein
            gruppenname = "Geologische Gebietskarten"
        elif (self.tabWidget.currentIndex() == 0): #Geoelogie Allgemein
            gruppenname = "Geologie Allgemein"


        gruppe_vorhanden = False


        legendroot = QgsProject.instance().layerTreeRoot()
        # Raster Layer(s) instanzieren: Dazu die Layerliste durchlaufen
        for i in range(len(self.layerliste)):
            #initialisieren
            self.einzelliste = self.layerliste[i] #gibt  #ind. datentyp zurück!
            QgsProject.instance().addMapLayer(self.einzelliste.rasterobjekt)
            #wenn Gruppenlayer nicht vorhanden ist, anlegen
            index = legendroot.findGroup(gruppenname)
            if index == None:
                #grp = self.leginterface.addGroup(gruppenname,0) #so hat die Gruppe das QGIS spez. Aussehen
                index = legendroot.insertGroup(-1,gruppenname)

            kindi = QgsProject.instance().layerTreeRoot().findLayer(self.einzelliste.rasterobjekt.id())
            zwtsch = kindi.clone()
            index.insertChildNode(-1,zwtsch)
            #QtGui.QMessageBox.about(None, "Gruppe vorhanden", str(kindi))
            kindi.parent().removeChildNode(kindi)
            index.setExpanded(False)
            if type(self.einzelliste.rasterobjekt) is QgsRasterLayer: #nur Raster werden in der Legende nach unten geschoben
                anzeigename = self.einzelliste.anzeigename
                self.einzelliste.rasterobjekt.setName(anzeigename)

        mc.setRenderFlag(True)


    #************************************************************************************************
    # clicked()
    #
    # Funktion fuer die Info-Buttons die verschiedene legenden-PDF's laden
    #************************************************************************************************
    def clicked(self):
        button = self.sender()
        if button is None or not isinstance(button, QPushButton):
            return
        if button.objectName() == "Button_Legend_Geologie_2007":
            os.startfile(self.pfad + "/Geologische_Karte/Vlbg/Geologischekarte_GBA/GeologischeKarte_2007_Legende.pdf")
        elif button.objectName() == "Button_Legend_Tektonisch_1998":
            os.startfile(self.pfad + "/Geologische_Karte/Vlbg/Geotektonischekarte_GBA/GeotektonischeKarte_1998_Legende.pdf")
        elif button.objectName() == "Profilschintt_Vorarlberg":
            os.startfile(self.pfad + "/Geologische_Karte/Vlbg/Geologie_Profilschnitt.pdf")
        elif button.objectName() == "Button_Legend_Geomorpg_Orig":
            os.startfile(self.pfad + "//Geomorphologische_Karte/Vlbg/Geomorphologische_Legende_Original.pdf")
        elif button.objectName() == "Button_Legend_Geomorph_Deutsch":
            os.startfile(self.pfad + "/Geomorphologische_Karte/Vlbg/Geomorphologische_Legende.pdf")

    #************************************************************************************************
    # doGeomorphologie_Amsterdam()
    #
    # Funktion fuer das Subwindow fuer die Geomorphologische Karten (Uni Amsterdam)
    #************************************************************************************************
    def doGeomorphologie_Amsterdam(self):
        Geomorphologie = Geomorphologie_Amsterdam(self.iface,vogisPfad +"Blattschnitte/Vlbg/Blattschnitte.qgs")
        Geomorphologie.exec_()  #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    #sondt müßte der parent dann für die Initialisierung von QDialog verwendet werden
#diese Klasse ist nichts anderes wie eine
#art struct, wir wollen das layerobjekt (Typ QgsMapLayer)
#und den Anzeigename in einem Datentyp zusammenfassen
class rastername(object):
    def __init__(self):
        self.rasterobjekt = QgsRasterLayer()
        self.anzeigename = str