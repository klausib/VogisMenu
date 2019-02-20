# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore,QtSql
import copy
from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_fwp import *
from gui_gfz_pg import *
#from ladefortschritt import *

from ProjektImport import *





#Klassendefinition für das Laden der GFZ
class GFZDialogPG (QtWidgets.QDialog,Ui_frmGFZ):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    #Initialisierung der GUI
    def __init__(self, parent,iface,dkmstand,pfad = None,vogisPfad = None, PGdb = None, gemeindeliste = None):
        QtWidgets.QDialog.__init__(self,parent)
        Ui_frmGFZ.__init__(self)
        self.iface = iface
        self.mc = self.iface.mapCanvas()
        self.pfad = pfad
        self.vogisPfad = vogisPfad
        self.setupUi(self) #User Interface für Hauptfenster GFZ Suche initialisieren
        self.gfz = ProjektImport(self.iface)
        self.gemeindeliste = gemeindeliste
        self.buttonGroup.setExclusive(True)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier


        #Variablen definieren und None setzen.
        #Sind nicht immer mit Werten initialisiert und None kann in
        #If Abfragen unterschieden werden
        #self.zoompunkt = None
        self.tool_vorher = None


        #Wir definieren einen eigenen Cursor: wird auf den
        #Button mit dem roten Kruez geklickt
        #bekommt der Mauscursor dieses Aussehen
        self.cursor = QtGui.QCursor(QtGui.QPixmap(["16 16 3 1",
                                      "      c None",
                                      ".     c #FF0000",
                                      "+     c #FFFFFF",
                                      "                ",
                                      "       +.+      ",
                                      "      ++.++     ",
                                      "     +.....+    ",
                                      "    +.     .+   ",
                                      "   +.   .   .+  ",
                                      "  +.    .    .+ ",
                                      " ++.    .    .++",
                                      " ... ...+... ...",
                                      " ++.    .    .++",
                                      "  +.    .    .+ ",
                                      "   +.   .   .+  ",
                                      "   ++.     .+   ",
                                      "    ++.....+    ",
                                      "      ++.++     ",
                                      "       +.+      "]))





        #Hauptfenster positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()


    #Den GFZ der ausgewählten Gemeinde laden
    #berücksichtigt werden muß auch welche Layer mit Hilfe
    #der Checkboxen ausgewählt wurden
    def ladeGemeinde(self):
        #Am Filesystem gibts keine Sonderzeichen!


        self.Gemeinde = 'Vorarlberg'

        gemeinde_wie_filesystem = self.Gemeinde
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ä'),'ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ä'),'Ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ö'),'oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ö'),'Oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ü'),'ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ü'),'Ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ß'),'ss')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace('. ','_')

        #Prüfen ob ein Zoompunkt gesetzt ist. Das ist nur der Fall wenn ein Grundstück gesucht wird
        #und auf den betreffenden Extent zoomen
        #(Das zoomen auf den Gemeindeextent ist zwar eingebaut aber auskommentiert!)
        #if not (self.zoompunkt is None): #Existenz eines Objectes Prüfen: OHNE Klammer!!
        #    self.mc.setExtent(self.zoompunkt)

        #Den Pfad für die betreffende Gemeinde setzen
        Pfad = self.pfad + gemeinde_wie_filesystem + "/Gefahrenzonenkarte/gfzk.qgs"


        #Pfad = "D:\Bludenz/Gefahrenzonenkarte/gfzk.qgs"
        #Ein Objekt erzeugen mit dem auf
        #den Code Projektimport zurückgegriffen werden kann
        #(Modul und Methode ProjektImport


        self.mc.setRenderFlag(False)

        #nun wenn alles vorbereitet ist: Die IMPORTMETHODE starten für die DKM
        #QtGui.QMessageBox.about(None, "About Application",Pfad)
        self.gfz.importieren(Pfad,None,self.Gemeinde,True, False, None)



        self.mc.setRenderFlag(True)

    #Projekte des Flussbau laden
    #Das geschieht nicht gemeindeweise, sondern für die Landesfläche
    def ladeGFZWB(self):

        self.mc.setRenderFlag(False)

        for button in self.buttonGroup.buttons():
            if button.isChecked(): #wenn gecket wird geladen
                if   ("Ueberflutungsflaechen" in button.objectName()):
                    self.ladepfad  = self.vogisPfad + "Wasser/Flussbau/Vlbg/HW_Ueberflutungsraeume/ueberflutungsflaechen_hora_neu.qgs"
                    self.gfz.importieren(self.ladepfad)#, None,'Abflußuntersuchungen BWV'.decode('utf8'))
                elif   ("GfzBwv" in button.objectName()):
                    self.ladepfad= self.vogisPfad + "Wasser/Flussbau/Vlbg/GZP/gefahrenzonen_bwv.qgs"
                    self.gfz.importieren(self.ladepfad)#, None, "Gefahrenzonen BWV")

        self.mc.setRenderFlag(True)

    #Projekte der kompetenzgrenzen laden
    def ladeKompetenzgrenzen(self):
        self.mc.setRenderFlag(False)
        self.gfz.importieren(self.vogisPfad + "Gefahren/Kompetenzgrenze_WLV_BWV/Vlbg/Kompetenzgrenzen.qgs")
        self.mc.setRenderFlag(True)


    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)

        if not (self.tool_vorher is None):
            self.mc.setMapTool(self.tool_vorher)
        #disconnect: weil sonst trotz close und del das signal slot verhältnis nicht sauber gelöscht wird
        #wieso??

        self.close()




