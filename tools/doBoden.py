# -*- coding: utf-8 -*-
#!/usr/bin/python

#from qgis.PyQt import QtGui, QtCore, QtWidgets
from PyQt5 import QtGui, QtCore, QtWidgets, QtWebKit, QtWebKitWidgets, QtNetwork
from qgis.core import *
from gui_boden import *
from qgis.gui import *
from qgis.analysis import *

from ProjektImport import *
import os,sys




#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen Boden
class BodenDialog(QtWidgets.QDialog, Ui_frmBoden):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog
        Ui_frmBoden.__init__(self)


        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.boden = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren


        # Fenster für die Anzeige des Webinhalts
        self.web_fenster = QtWidgets.QWidget()
        self.web_fenster.setObjectName("Webview")
        self.web_fenster.setFixedSize(QtCore.QSize(1013,612))
        self.web_fenster.resize(1013, 612)

        # Qgis 3 nimmt defaultmäßig die System Proxy
        # Einstellungen. Die Plugins
        # verwenden die Einstellungen von Qgis, es ist also
        # nichts weiter zu machen.
##        # Proxy für die Verbindung
##        self.web_proxy = QtNetwork.QNetworkProxy()
##        self.web_proxy.setHostName('proxy.intra.vlr.gv.at')
##        self.web_proxy.setPort(8080)
##        self.web_proxy.setType(3)   # http Proxy
##        self.web_proxy.setUser('svc_internet')
##        self.web_proxy.setPassword('internet')



    # klickt man auf OK wird diese Methode ausgeführt
    # Da die Layer recht heterogen geordnet sind ist das
    # setzen der Pfade hardcodiert. Die Importmethode wird
    # in der jeweiligen If clause ausgeführt
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

    # schließt den Dialog für den Punkt Boden
    def abbrechen(self):
        self.close()


    # Öffnet die im Infobutton
    # hinterlegte URL- optional in zwei unterschiedlichen
    # Varianten
    def infobutton(self):
        # Trend Micro kann einen externen Shellaufruf verhindern, wenn er nicht ausgenommen ist....
        try:
            os.startfile("http://bfw.ac.at/rz/bfwcms.web?dok=7066")
        except:
            self.web_fenster.show()
            web_sicht = QtWebKitWidgets.QWebView(self.web_fenster)
            web_sicht.load(QtCore.QUrl("http://bfw.ac.at/rz/bfwcms.web?dok=7066"))
            web_sicht.resize(1013, 612)
            web_sicht.show()