  # -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui, QtCore

from qgis.core import *
from gui_blattschnitte import *
from ProjektImport import *



#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class BlsDialog(QtWidgets.QDialog, Ui_frmBlattschnitte):
    def __init__(self,iface,pfad = None):
        QtWidgets.QDialog.__init__(self)
        Ui_frmBlattschnitte.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.checkButtonsGroup.setExclusive(False)          # wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                            # deshlab hier
        self.blattschnitte = ProjektImport(self.iface)      # das Projekt Import Objekt instanzieren

    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt

    def accept(self):
        liste = []

        self.iface.mapCanvas().setRenderFlag(False)

        for button in self.checkButtonsGroup.buttons():

            #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
            #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
            if button.isChecked():

                if   ("Koordinatennetz" in button.text()):
                    liste.append(button.text()+ " 1km")
                    liste.append(button.text()+ " 500m")
                    liste.append(button.text()+ " 100m")

                else:
                    if self.radioButton.isChecked():
                        liste.append(button.text() + " Nr")
                        liste.append(button.text())
                    else:
                        liste.append(button.text())



        self.blattschnitte.importieren(self.pfad,liste)

        self.iface.mapCanvas().setRenderFlag(True)