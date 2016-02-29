# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_wald import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class WaldDialog(QtGui.QDialog, Ui_frmWald):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmWald.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier

        self.wald = ProjektImport(self.iface)   #das Projekt Import Objekt instanzieren


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

                    #schlampig: Legendenshape hier dazuladen
                    waldlegende = QgsVectorLayer(self.pfad + "/Waldflaechen/waldflaeche_luftbild_2001.shp", "waldflaeche_luftbild_2001.shp","ogr")

                    #und prüfen ob erfolgreich geladen
                    if not waldlegende.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Legendenshape konnte nicht geladen werden")
                    else:
                        #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = waldlegende.loadNamedStyle(self.pfad + "/Waldflaechen/wald_legende.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( waldlegende )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Waldlegende QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(waldlegende)
                        self.iface.legendInterface().setLayerVisible(waldlegende,0 )
                        QgsMapLayerRegistry.instance().addMapLayer(waldlegende)

                        #API up to 2.2
                        if QGis.QGIS_VERSION_INT < 20300:
                            self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)
                            dodl = self.legendTree.takeTopLevelItem(0)
                            self.legendTree.addTopLevelItem(dodl)
                            self.legendTree.expandItem(dodl)    #legende aufklappen
                        else:
                            kindi = QgsProject.instance().layerTreeRoot().findLayer(waldlegende.id())
                            zwtsch = kindi.clone()
                            QgsProject.instance().layerTreeRoot().insertChildNode(-1,zwtsch)
                            kindi.parent().removeChildNode(kindi)


                        waldlegende.setLayerName(("1m Wald 2001/02 (Legende)"))


                elif (("WaldflaecheOek").decode('utf8') in button.objectName()):

                   #schlampig: Waldflaech ÖK hier dazuladen
                    waldflaeche = QgsVectorLayer(self.pfad + "/Waldflaechen/waldflaeche_oek.shp", "waldflaeche_oek.shp","ogr")

                    #und prüfen ob erfolgreich geladen
                    if not waldflaeche.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Waldflaeche OEK konnte nicht geladen werden")
                    else:
                        #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = waldflaeche.loadNamedStyle(self.pfad + "/Waldflaechen/waldflaeche_oek.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( waldflaeche )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Waldflaeche QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(waldflaeche)
                        self.iface.legendInterface().setLayerVisible(waldflaeche,0 )
                        QgsMapLayerRegistry.instance().addMapLayer(waldflaeche)
                        waldflaeche.setLayerName(("Waldflaeche ÖK50").decode('utf8'))

                elif ("Waldentwicklungsplan" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"

                    name.append(("WEP Funktionsflächen (a)").decode('utf8'))
                    name.append(("WEP Windschutzstreifen (a)"))
                    name.append(("WEP Zeiger (a)"))
                    name.append(("WEP Kreisflächen (a)").decode('utf8'))


                elif ("Waldregionen" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldaufsicht/waldregion.qgs"
                    name = None
                    #name.append(_fromUtf8("Nicht anrechenbare Jagdfläche"))

                elif ("Waldkarte" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"
                    name.append(("Waldkarte (a)"))

                elif ("Saatgut" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"

                    name.append(("Saatgutbestände (a)").decode('utf8'))
                    name.append(("Saatgutbestände Typ B (a)").decode('utf8'))

                elif ("Auwald" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"

                    name.append(("Auwald").decode('utf8'))

                elif ("Ufergehoelz" in button.objectName()):

                    pfad_ind = self.pfad + "/Waldwirtschaft/waldwirtschaft.qgs"

                    name.append(("Ufergehoelz").decode('utf8'))

                if self.raster:
                    #Rasterdatensatz laden und auf gültigkeit prüfen
                    fileinfo = QtCore.QFileInfo(pfad_ind)
                    basename = fileinfo.baseName()

                    #Raster erzeugen und Darstellung zuweisen
                    raster = QgsRasterLayer(pfad_ind,basename)
                    #raster.setContrastEnhancementAlgorithm(contrast) #Entspricht StretchToMinimumMaximum wenn wert 1
                    #QtGui.QMessageBox.about(None, "Fehler", "nach raster")
                    if not raster.isValid():
                        QtGui.QMessageBox.about(None, "Fehler", "Laden des Datensatzes fehlgeschlagen")
                        return #Ausführung des Sub wird hier einfach abgebrochen


                    QgsMapLayerRegistry.instance().addMapLayer(raster)

                    #API up to 2.2
                    if QGis.QGIS_VERSION_INT < 20300:
                        #Der geladene Rasterlayer wird in der Legende
                        #ganz nach unten gerückt
                        self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)
                        dodl = self.legendTree.takeTopLevelItem(0)
                        self.legendTree.addTopLevelItem(dodl)
                    else:
                        kindi = QgsProject.instance().layerTreeRoot().findLayer(raster.id())
                        zwtsch = kindi.clone()
                        QgsProject.instance().layerTreeRoot().insertChildNode(-1,zwtsch)
                        kindi.parent().removeChildNode(kindi)


                    raster.setLayerName((anzeigename).decode('utf8')) #ACHTUNG: Damit wird auch erzwungen, daß die Layerdarstellung
                                                                #(Reihenfolge) aktualisiert wird!!
                    anzeigename = ""

                else:
                    #das Importobjekt bekommt eine Liste mit den Namen der zu ladenden Layern
                    #mit. (Das eigentliche Projekt enthält ja wesentlich mehr Layer)
                    self.wald.importieren(pfad_ind,name) #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(True)