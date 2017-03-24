# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_jagd import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *


#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class JagdDialog(QtGui.QDialog, Ui_frmJagd):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmJagd.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)      #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                #deshalb hier
        self.jagd = ProjektImport(self.iface)   #das Projekt Import Objekt instanzieren


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

                if   ("Jagdreviere" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Jagdwirtschaft/jagdwirtschaft.qgs"
                    name.append("Reviere")

                elif ("Wildfuetterungen" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Jagdwirtschaft/jagdwirtschaft.qgs"
                    name.append(("Wildfütterungen").decode('utf8'))

                elif ("Rotwildwintergatter" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Jagdwirtschaft/jagdwirtschaft.qgs"
                    name.append(("Rotwildwintergatter"))


                elif ("Rotwildgebiete" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Rotwildräume").decode('utf8'))

                elif ("Wildregionen" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Wildregion"))

                elif ("Wildfreihaltungen" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Wildfreihaltungen"))


                elif ("Gamszonierung" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Gamswildzonierung"))

                elif ("Wildruhezonen" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Wildruhezone"))

                elif ("Wildbehandlungszonen" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Raumplanung/raumplanung.qgs"
                    name.append(("Rotwildbehandlungszonen"))


                self.jagd.importieren(pfad_ind,name) #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(True)

