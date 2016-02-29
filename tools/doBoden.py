# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_boden import *
from qgis.gui import *
from qgis.analysis import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import os


try:
    _fromUtf8 = QtCore.QString.fromUtf8
    _fromLatin1 = QtCore.QString.fromLatin1
except AttributeError:
    _fromUtf8 = lambda s: s




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen Boden
class BodenDialog(QtGui.QDialog, Ui_frmBoden):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog
        Ui_frmBoden.__init__(self)


        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.boden = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren







    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def laden(self):

        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            if button.isChecked(): #wenn gecket wird geladen
                if   ("DigitaleBodenkarte" in button.objectName()):
                    self.fullpath = self.pfad + "Bodentypen/Bodentypen.qgs"
                    self.boden.importieren(self.fullpath)
                elif   ("Bodenprofile" in button.objectName()):
                    self.fullpath = self.pfad + "Profile/Bodenprofile.qgs"
                    self.boden.importieren(self.fullpath)

        self.iface.mapCanvas().setRenderFlag(True)

    #schließt den Dialog für den Punkt Boden
    def abbrechen(self):
        self.close()



    #Öffnet das dem Infobutton
    #hinterlegte PDF
    def infobutton(self):
        os.startfile("http://bfw.ac.at/rz/bfwcms.web?dok=7066")
