# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from gui_landwirtschaft import *
from ProjektImport import *


#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class LandwirtschaftDialog(QtWidgets.QDialog, Ui_frmLandwirtschaft):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmLandwirtschaft.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier

        self.landwirtschaft = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def accept(self):




        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            if button.isChecked():
                name = []   #ACHTUNG. name muß vom Typ Liste sein!!
                            #enthält die zu importierenden Layer des Projektes

                pfad_ind = ""

                if   ("ckEigentumsverhaeltnisse" in button.objectName()):

                    pfad_ind = self.pfad + "/Nutzung/Vlbg/Alpgebiet/agrargemeinschaften.qgs"
                    name.append(("agrargem_eigen"))
                elif   ("ckAlpArt" in button.objectName()):

                    pfad_ind = self.pfad + "/Nutzung/Vlbg/Alpgebiet/agrargemeinschaften.qgs"
                    name.append(("Agrargemeinschaften Alpart"))
                elif   ("ckBodenklimazahl" in button.objectName()):

                    pfad_ind = self.pfad + "/Nutzung/Vlbg/Talboden/Bodenklimazahl_Ertragswerte.qgs"
                    name = None
                elif   ("ckAlpenVorMaisaesse" in button.objectName()):

                    pfad_ind = self.pfad + "/Nutzung/Vlbg/Alpgebiet/Alpen_Vorsaess_Maisaess.qgs"
                    name = None
                elif   ("ckBenachteiligteGebiete" in button.objectName()):

                    pfad_ind = self.pfad + "/Foerderung/Vlbg/benachteiligte_Gebiete/benachteiligte_gebiete.qgs"
                    name = None



                self.landwirtschaft.importieren(pfad_ind,name)

        self.iface.mapCanvas().setRenderFlag(True)