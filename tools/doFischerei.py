# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui, QtCore

from qgis.core import *
from gui_fischerei import *
from ProjektImport import *



#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class FischereiDialog(QtWidgets.QDialog, Ui_frmFischerei):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmFischerei.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                #deshalb hier
        self.fischerei = ProjektImport(self.iface)   #das Projekt Import Objekt instanzieren


    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def accept(self):

        name = [] #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            if button.isChecked():

                if   ("Fischereireviere" in button.objectName()):
                    pfad_ind = self.pfad + "/Vlbg/Fischereireviere/fischereireviere.qgs"


                self.fischerei.importieren(pfad_ind) #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(True)

