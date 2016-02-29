# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_siedlungsgebiete import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class SiedlungenDialog(QtGui.QDialog, Ui_frmSiedlungsgebiete):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmSiedlungsgebiete.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier


        self.raumplanung = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren


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

                if   ("ckSiedlungsgebiete" in button.objectName()):

                    pfad_ind = self.pfad + "/Vlbg/Siedlungsgebiet/siedlungsgebiet.qgs"


                elif ("ckSiedlungsentwicklung" in button.objectName()):

                    pfad_ind = self.pfad + "/Rheintal/Siedlungsentwicklung/siedlungsentwicklung.qgs"

                elif ("ckEkz" in button.objectName()):

                    pfad_ind = self.pfad + "/Eignungszone/Vlbg/Einkaufszentrum/einkaufszentrum.qgs"

                elif ("ckBauflaechen" in button.objectName()):

                    pfad_ind = self.pfad + "/Bauflaeche/Vlbg/Bauflaechennutzung/bauflaechennutzung.qgs"

                elif ("ckSeveso" in button.objectName()):

                    pfad_ind = self.pfad + "/Beschraenkungszone/Vlbg/Seveso_II/seveso_2.qgs"

                elif ("ckFundzonen" in button.objectName()):

                    pfad_ind = self.pfad + "/Beschraenkungszone/Vlbg/Archaeologische_Fundzonen/Fundzone.qgs"

                elif ("ckRohstoffplan" in button.objectName()):

                    pfad_ind = self.pfad + "/Beschraenkungszone/Vlbg/Rohstoffplan/Lockergesteine.qgs"

                elif ("ckBlauzone" in button.objectName()):

                    pfad_ind = self.pfad + "/Beschraenkungszone/Vlbg/Blauzone/blauzone.qgs"

                elif ("ckWeisszone" in button.objectName()):

                    pfad_ind = self.pfad + "/Beschraenkungszone/Vlbg/WeissZone/Weisszone.qgs"


                self.raumplanung.importieren(pfad_ind)


        self.iface.mapCanvas().setRenderFlag(True)