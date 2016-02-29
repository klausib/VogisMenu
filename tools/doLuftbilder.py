# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtSql
import copy
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_blattschnitte import *
from gui_luftbilder import *

#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *


#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class LuftbilderDialog (QtGui.QDialog,Ui_frmLuftbilder):


    def __init__(self, parent,iface,dkmstand,pfad = None):
        QtGui.QDialog.__init__(self,parent) #parent brauchts für einen modalen Dialog
        Ui_frmLuftbilder.__init__(self)
        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.buttonGroup.setExclusive(False)     #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier


        self.luftbilder = ProjektImport(self.iface)     #das Projekt Import Objekt instanzieren

    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def laden(self):


        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():

            if button.isChecked():  #wenn gechecked wird geladen

                if   ("Teil" in button.objectName()):
                    self.ladepfad= self.pfad + "Orthofotos/Teilflaechen/" + button.objectName()+ ".qgs"
                    self.luftbilder.importieren(self.ladepfad,None,None,None,True)

                elif   ("luftbilder_punkte" in button.objectName()):
                    self.ladepfad= self.pfad + "Uebersichten/" + button.objectName()+ ".qgs"
                    self.luftbilder.importieren(self.ladepfad,None,None,None,True,button.objectName())

                else:

                        self.ladepfad = self.pfad + "Orthofotos/Vlbg/" + button.objectName()+ ".qgs"
                        self.luftbilder.importieren(self.ladepfad,None,None,None,True,button.objectName())



        self.iface.mapCanvas().setRenderFlag(True)

     #schließt den Dialog
    def abbrechen(self):
        self.close()



