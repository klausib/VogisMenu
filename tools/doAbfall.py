# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_abfall import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *

class AbfallDialog(QtGui.QDialog, Ui_frmAbfall):
    def __init__(self,iface,pfad = None):
        QtGui.QDialog.__init__(self)
        Ui_frmAbfall.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.checkButtonsGroup.setExclusive(False)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                        #deshlab hier
    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def accept(self):

        self.iface.mapCanvas().setRenderFlag(False)

        abfall = ProjektImport(self.iface)  #das Projekt Import Objekt instanzieren

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.checkButtonsGroup.buttons():

            if button.isChecked():  #wenn gechecket, wird geladen

                if   ("Deponie" in button.text()):

                    abfall.importieren(self.pfad + "/Deponie/deponie.qgs",)

                elif ("Altstandort" in button.text()):

                    abfall.importieren(self.pfad + "/Altstandort/altstandorte.qgs",)
        self.iface.mapCanvas().setRenderFlag(True)

