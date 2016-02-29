# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_klima import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import os



class KlimaDialog(QtGui.QDialog, Ui_frmKlima):
    def __init__(self,parent,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmKlima.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad

        #self.ckButtons.setExclusive(True)   #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshlab hier
        self.klima = ProjektImport(self.iface)

        #die Connects
        QtCore.QObject.connect(self.btnKartePDF, QtCore.SIGNAL("clicked()"), self.Kartebutton)
        QtCore.QObject.connect(self.btnBeschreibungPDF, QtCore.SIGNAL("clicked()"), self.Kartebutton)
        #QtCore.QObject.connect(self.btnTempJahresmittelA3, QtCore.SIGNAL(_fromUtf8("clicked()")), self.infobuttton)

    def accept(self):



        #name = [] #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        pfad_ind =""
        for ck in self.ckButtons.buttons():
            anzeigetext = ""
            if ck.isChecked():

                if   ("ckTempJahresmittel" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/Jahresmittel/jahresmittel_lufttemperatur.qgs"
                    anzeigetext = 'Lufttemperatur Jahresmittel'

                elif   ("ckTempMaxJahresmittel" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/MittleresJahresmaximum/mittleresjahresmaximum_lufttemperatur.qgs"
                    anzeigetext = 'Maximumtemperatur Jahresmittel'

                elif   ("ckHeisstage" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/ZahlHeissetage/mittlerezahlheissetage.qgs"
                    anzeigetext = 'Mittlere Anzahl Heisstage'

                elif   ("ckEistage" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/ZahlEistage/mittlerezahleistage.qgs"
                    anzeigetext = 'Mittlere Anzahl Eistage'

                elif   ("ckHeizgrad" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/Heizgradtagszahl/mittlerejaehrlicheheizgradtagszahl.qgs"
                    anzeigetext = 'Mittlere Anzahl Heizgradtage'

                elif   ("ckVegetationsperiode" in ck.objectName()):

                    pfad_ind = self.pfad + "/Temperatur/Vlbg/DauerVegetationsperiode/dauervegetationsperiode.qgs"
                    anzeigetext = 'Dauer Vergetationsperiode'

                elif   ("ckNsJahrGesamt" in ck.objectName()):

                    pfad_ind = self.pfad + "/Niederschlag/Vlbg/NiederschlagssummeJahr/niederschlagssumme_jahr.qgs"
                    anzeigetext = 'Jahresniederschlagssumme'

                elif   ("ckNTage1mm" in ck.objectName()):

                    pfad_ind = self.pfad + "/Niederschlag/Vlbg/ZahlTageMin1mm/tage_mit_1mm_niederschlag.qgs"
                    anzeigetext = 'Tage mit mind. 1 mm Niederschlag'

                elif   ("ckNTage10mm" in ck.objectName()):

                    pfad_ind = self.pfad + "/Niederschlag/Vlbg/ZahlTageMin10mm/tage_mit_10mm_niederschlag.qgs"
                    anzeigetext = 'Tage mit mind. 10 mm Niederschlag'

                self.klima.importieren(pfad_ind,None,None,None,True,anzeigetext)
                #self.klima.importieren(pfad_ind,None,None,None,True,None)
                #elf.klima.importieren(pfad_ind,name) #ACHTUNG. name muß vom Typ Liste sein!!

        self.iface.mapCanvas().setRenderFlag(True)


    #Öffnet das dem Karten/Beschreibungsbuttons
    #hinterlegte PDF
    def Kartebutton(self):
        button = self.sender()
        suffi = ""
        if ("btnKartePDF" in button.objectName()):
            suffi = 'karte'

        elif ("btnBeschreibungPDF" in button.objectName()):
            suffi = 'beschreibung'


        for ck in self.ckButtons.buttons():

                if ck.isChecked():

                    if   ("ckTempJahresmittel" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/Jahresmittel/jahresmittel_lufttemperatur_" + suffi + ".pdf")

                    elif   ("ckTempMaxJahresmittel" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/MittleresJahresmaximum/mittleresjahresmaximum_lufttemperatur_" + suffi + ".pdf")

                    elif   ("ckHeisstage" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/ZahlHeissetage/mittlerezahlheissetage_" + suffi + ".pdf")

                    elif   ("ckEistage" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/ZahlEistage/mittlerezahleistage_" + suffi + ".pdf")

                    elif   ("ckHeizgrad" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/Heizgradtagszahl/mittlerejaehrlicheheizgradtagszahl_" + suffi + ".pdf")

                    elif   ("ckVegetationsperiode" in ck.objectName()):

                        os.startfile(self.pfad + "/Temperatur/Vlbg/DauerVegetationsperiode/dauervegetationsperiode_" + suffi + ".pdf")

                    elif   ("ckNsJahrGesamt" in ck.objectName()):

                        os.startfile(self.pfad + "/Niederschlag/Vlbg/NiederschlagssummeJahr/niederschlagssumme_jahr_" + suffi + ".pdf")

                    elif   ("ckNTage1mm" in ck.objectName()):

                        os.startfile(self.pfad + "/Niederschlag/Vlbg/ZahlTageMin1mm/tage_mit_1mm_niederschlag_" + suffi + ".pdf")

                    elif   ("ckNTage10mm" in ck.objectName()):

                        os.startfile(self.pfad + "/Niederschlag/Vlbg/ZahlTageMin10mm/tage_mit_10mm_niederschlag_" + suffi + ".pdf")

                    #self.klima.importieren(pfad_ind)
                    #elf.klima.importieren(pfad_ind,name) #ACHTUNG. name muß vom Typ Liste sein!!






    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        self.close()
