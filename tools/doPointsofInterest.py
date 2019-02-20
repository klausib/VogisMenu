# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from gui_pointsofinterest import *
from ProjektImport import *




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class PointsofInterestDialog(QtWidgets.QDialog, Ui_frmPointsofInterest):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmPointsofInterest.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier

        self.pointsofinterest = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

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

                if   ("ckBergspitzen" in button.objectName()):
                    pfad_ind = self.pfad + "/Ortsbezeichnung/Vlbg/berge/bergspitzen.qgs"
                elif ("ckNamengut" in button.objectName()):
                    pfad_ind = self.pfad + "/Ortsbezeichnung/Vlbg/Namengut/namengut.qgs"


                self.pointsofinterest.importieren(pfad_ind)

        self.iface.mapCanvas().setRenderFlag(True)