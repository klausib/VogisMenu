# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from gui_wald import *
from osgeo import ogr

from direk_laden import direk_laden

from ProjektImport import *




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class WaldDialog(QtWidgets.QDialog, Ui_frmWald):
    def __init__(self,parent,iface,pfad = None, PGdb = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmWald.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.db = PGdb
        self.ckButtons.setExclusive(False)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier

        self.wald = ProjektImport(self.iface)   #das Projekt Import Objekt instanzieren


    def closeEvent(self,event = None):
        self.close()



    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def accept(self):

        self.iface.mapCanvas().setRenderFlag(False)

        for button in self.ckButtons.buttons():
            self.raster = False
            if button.isChecked():
                name = [] #ACHTUNG. name muß vom Typ Liste sein!!

                pfad_ind = ""

                if   ("Waldklassifizierung" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldflaechen/waldflaeche_luftbild_2001.tif"
                    anzeigename = "1m Wald (aus Orthofotos 2001/02)"
                    self.raster = True

                    # Legendenshape hier dazuladen
                    waldlegende = direk_laden(self.db, "waldflaeche_luftbild_2001", "waldflaeche_luftbild_2001.shp", self.pfad + "/Waldflaechen/",self.iface)


                    #und prüfen ob erfolgreich geladen
                    if not waldlegende.isValid(): #nicht erfolgreich geladen
                        QtWidgets.QMessageBox.about(None, "Fehler", "Legendenshape konnte nicht geladen werden")
                    else:
                        #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = waldlegende.loadNamedStyle(self.pfad + "/Waldflaechen/wald_legende.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.layerTreeView().refreshLayerSymbology( waldlegende.id() )
                        else:
                            QtWidgets.QMessageBox.about(None, "Fehler", "Waldlegende QML konnte nicht zugewiesen werden!")


                        QgsProject.instance().addMapLayer( waldlegende )
                        #self.iface.legendInterface().setLayerVisible(waldflaeche,0 )
                        lyr_tree = QgsProject.instance().layerTreeRoot().findLayer(waldlegende)
                        lyr_tree.setItemVisibilityChecked(False)


                        kindi = QgsProject.instance().layerTreeRoot().findLayer(waldlegende.id())
                        zwtsch = kindi.clone()
                        QgsProject.instance().layerTreeRoot().insertChildNode(-1,zwtsch)
                        kindi.parent().removeChildNode(kindi)


                        waldlegende.setName(("1m Wald 2001/02 (Legende)"))


                elif (("WaldflaecheOek") in button.objectName()):


                    waldflaeche = direk_laden(self.db, "waldflaeche_oek", "waldflaeche_oek.shp", self.pfad + "/Waldflaechen/",self.iface)

                    #und prüfen ob erfolgreich geladen
                    if not waldflaeche.isValid(): #nicht erfolgreich geladen
                        QtWidgets.QMessageBox.about(None, "Fehler", "Waldflaeche OEK konnte nicht geladen werden")
                    else:
                        #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = waldflaeche.loadNamedStyle(self.pfad + "/Waldflaechen/waldflaeche_oek.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            #self.iface.legendInterface().refreshLayerSymbology( waldflaeche )
                            self.iface.layerTreeView().refreshLayerSymbology( waldflaeche.id() )
                        else:
                            QtWidgets.QMessageBox.about(None, "Fehler", "Waldflaeche QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsProject.instance().addMapLayer( waldflaeche )
                        lyr_tree = QgsProject.instance().layerTreeRoot().findLayer(waldflaeche)
                        lyr_tree.setItemVisibilityChecked(False)
                        waldflaeche.setName(("Waldflaeche ÖK50"))

                elif ("Waldentwicklungsplan" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"

                    name.append(("WEP Funktionsflächen (a)"))
                    name.append(("WEP Windschutzstreifen (a)"))
                    name.append(("WEP Zeiger (a)"))
                    name.append(("WEP Kreisflächen (a)"))


                elif ("Waldregionen" in button.objectName()):
                    pfad_ind = self.pfad + "/Waldaufsicht/waldregion.qgs"
                    name = None
                    #name.append(_fromUtf8("Nicht anrechenbare Jagdfläche"))

                elif ("Waldkarte" in button.objectName()):
                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"
                    name.append(("Waldkarte (a)"))

                elif ("Saatgut" in button.objectName()):
                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"
                    name.append(("Saatgutbestände (a)"))
                    name.append(("Saatgutbestände Typ B (a)"))

                elif ("Auwald" in button.objectName()):
                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"
                    name.append(("Auwald"))

                elif ("Ufergehoelz" in button.objectName()):
                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"
                    name.append(("Ufergehoelz"))

                if self.raster:
                    #Rasterdatensatz laden und auf gültigkeit prüfen
                    fileinfo = QtCore.QFileInfo(pfad_ind)
                    basename = fileinfo.baseName()

                    #Raster erzeugen und Darstellung zuweisen
                    raster = QgsRasterLayer(pfad_ind,basename)

                    if not raster.isValid():
                        QtWidgets.QMessageBox.about(None, "Fehler", "Laden des Datensatzes fehlgeschlagen")
                        return #Ausführung des Sub wird hier einfach abgebrochen


                    #QgsMapLayerRegistry.instance().addMapLayer(raster)
                    QgsProject.instance().addMapLayer( raster )
                    kindi = QgsProject.instance().layerTreeRoot().findLayer(raster.id())
                    zwtsch = kindi.clone()
                    QgsProject.instance().layerTreeRoot().insertChildNode(-1,zwtsch)
                    kindi.parent().removeChildNode(kindi)


                    raster.setName((anzeigename)) #ACHTUNG: Damit wird auch erzwungen, daß die Layerdarstellung
                                                                #(Reihenfolge) aktualisiert wird!!
                    anzeigename = ""

                else:
                    #das Importobjekt bekommt eine Liste mit den Namen der zu ladenden Layern
                    #mit. (Das eigentliche Projekt enthält ja wesentlich mehr Layer)
                    self.wald.importieren(pfad_ind,name) #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(True)