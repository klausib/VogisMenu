# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_grenzen import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *



#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen
class GrenzenDialog(QtGui.QDialog, Ui_frmGrenzen):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog
        Ui_frmGrenzen.__init__(self)


        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.buttonGroup.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.Grenzen = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren


    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def laden(self):


        self.iface.mapCanvas().setRenderFlag(False)
        name = [] #ACHTUNG. name muß vom Typ Liste sein!!

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():

            if button.isChecked():

                if   ("PolitischeGrenzen" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Vlbg/Politische_Gemeinden/politische_grenzen.qgs",)

                elif ("Katastralgrenzen" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Vlbg/Katastralgemeinden/katastralgemeinden.qgs",)

                elif ("Zaehlsprengel" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Vlbg/Zaehlsprengel/zaehlsprengel.qgs",)

                elif ("ONachbarlaender" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Oesterreich_Umgebung/Staatsgrenzen/laender.qgs",[('Laendergrenzen:').decode('utf8'),('Laendergebiete:').decode('utf8')])

                elif ("OBundeslaender" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Oesterreich_Umgebung/Staatsgrenzen/laender.qgs",[('Länder').decode('utf8')])

                elif ("OBezirke" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Oesterreich_Umgebung/Staatsgrenzen/laender.qgs",[('Bezirke (Österreich)').decode('utf8')])

                elif ("OGemeinden" in button.objectName()):

                    self.Grenzen.importieren(self.pfad + "/Oesterreich_Umgebung/Staatsgrenzen/laender.qgs",[('Gemeinden (Österreich)').decode('utf8')])


                elif ("Gemeinden" in button.objectName()):

                    self.Grenzen.importieren(self.pfad[:2] + "/vogis.qgs",)


        self.iface.mapCanvas().setRenderFlag(True)

    #schließt den Dialog
    def abbrechen(self):
        self.close()


