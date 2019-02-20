# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from gui_landnutzung import *
from ProjektImport import *



#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class LandnutzungDialog(QtWidgets.QDialog, Ui_frmLandnutzung):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmLandnutzung.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(True)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier

        self.landnutzung = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

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

                if   ("LnRheintal" in button.objectName()):

                    pfad_ind = self.pfad + "/Rheintal/Landnutzung/landnutzung.qgs"


                self.landnutzung.importieren(pfad_ind)

        self.iface.mapCanvas().setRenderFlag(True)
