# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_energie import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *



#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen

class EnergieDialog(QtGui.QDialog, Ui_frmEnergie):
    def __init__(self,iface,pfad = None):
        QtGui.QDialog.__init__(self)
        Ui_frmEnergie.__init__(self)


        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.checkButtonsGroup.setExclusive(False)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen


    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt

    def accept(self):


        Energie = ProjektImport(self.iface)     #das Projekt Import Objekt instanzieren

        self.iface.mapCanvas().setRenderFlag(False)


        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.checkButtonsGroup.buttons():

            if button.isChecked():

                if   ("Energieversorgung: GAS" in button.text()):

                    Energie.importieren(self.pfad + "/Gasversorgung/gas.qgs",)

                elif ("Energieversorgung: STROM" in button.text()):

                    Energie.importieren(self.pfad + "/Stromversorgung/stromversorgung.qgs",)

        self.iface.mapCanvas().setRenderFlag(True)
