# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore

from qgis.core import *
from gui_wasser import *
from qgis.gui import *
from qgis.analysis import *
from ProjektImport import *
import os



#Die Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen Wasser
class WasserDialog(QtWidgets.QDialog, Ui_frmWasser):
    def __init__(self,parent,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog
        Ui_frmWasser.__init__(self)


        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.ckButtons.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.wasser = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren



    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def datenladen(self):

        self.iface.mapCanvas().setRenderFlag(False)

        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            bodenseeliste = []
            if button.isChecked(): #wenn gecket wird geladen
                if   ("Brunnen" in button.objectName()):
                    self.fullpath = self.pfad + "Brunnen/Vlbg/Brunnen/brunnen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("SchutzSchongebiete" in button.objectName()):
                    self.fullpath = self.pfad + "Schutz_Schongebiete/Vlbg/SchutzSchongebiete/schutzundschongebiete.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("GWWaermepumpen" in button.objectName()):
                    self.fullpath = self.pfad + "Grundwasser/Vlbg/ThermischeNutzungen/grundwasser_waermepumpen.qgs"
                    self.wasser.importieren(self.fullpath,None,"wpog",False, False, None, None, False)

                elif   ("Erdwaermeanlagen" in button.objectName()):
                    self.fullpath = self.pfad + "Grundwasser/Vlbg/ThermischeNutzungen/erdwaermeanlage.qgs"
                    self.wasser.importieren(self.fullpath,None,"erdwaerme",False, False, None, None, False)

                elif   ("KuehlwasseranlagenGW" in button.objectName()):
                    self.fullpath  = self.pfad +  "Grundwasser/Vlbg/ThermischeNutzungen/kuehlwasseranlage_grundwasser.qgs"
                    self.wasser.importieren(self.fullpath,None, "kuehlwasser" ,False, False, None, None, False)

                elif   ("KuehlwasseranlagenOG" in button.objectName()):
                    self.fullpath  = self.pfad +  "Grundwasser/Vlbg/ThermischeNutzungen/kuehlwasseranlage_oberflaechengewaesser.qgs"
                    self.wasser.importieren(self.fullpath,None,"kwog",False, False, None, None, False) #sonst wirds im Bulk nicht geladen!!

                elif   ("WeitereAnlagen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Grundwasser/Vlbg/Grundwasseranlagen/grundwasser_anlagen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("Kraftwerke" in button.objectName()):
                    self.fullpath  = self.pfad +  "Wassernutzung/Vlbg/Kraftwerke/kraftwerke.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("SonstigeBetriebe" in button.objectName()):
                    self.fullpath  = self.pfad +  "Betriebe/Vlbg/Betriebe/betriebe.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("Geschiebe" in button.objectName()):
                    self.fullpath  = self.pfad +  "Flussbau/Vlbg/Rueckhalteeinrichtungen/geschiebe_rueckhalteeinrichtungen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("SonstigeAnlagen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Wassernutzung/Vlbg/Anlagen/oberflaechengewaesser_anlagen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("KommunaleKlaeranlagen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Abwasser/Vlbg/Klaeranlagen/kommunale_klaeranlagen.qgs"
                    self.wasser.importieren(self.fullpath,None,"kommunale",False, False, None, None, False)

                elif   ("Kleinklaeranlagen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Abwasser/Vlbg/Klaeranlagen/klein_klaeranlagen.qgs"
                    self.wasser.importieren(self.fullpath,None,"klein",False, False, None, None, False)

                elif   ("BetrieblicheKlaeranlagen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Abwasser/Vlbg/Klaeranlagen/betriebliche_klaeranlagen.qgs"
                    self.wasser.importieren(self.fullpath,None,"betrieblich",False, False, None, None, False)

                elif   ("OeffentlicheTankstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Betriebe/Vlbg/OeffentlicheTankstellen/oeffentlichetankstellen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("Niederschlagmessstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Messstellen/Vlbg/Messstellen/niederschlag_messstellen.qgs"
                    self.wasser.importieren(self.fullpath,None,"niederschlag",False, False, None, None, False)

                elif   ("Oberflaechenwassermessstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Messstellen/Vlbg/Messstellen/oberflaechengewaesser_messstellen.qgs"
                    self.wasser.importieren(self.fullpath,None,"oberflaechenwasser",False, False, None, None, False)

                elif   ("Grundwassermessstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Messstellen/Vlbg/Messstellen/grundwasser_messstellen.qgs"
                    self.wasser.importieren(self.fullpath,None,"grundwasser",False, False, None, None, False)

                elif   ("Quellenmessstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Messstellen/Vlbg/Messstellen/quellen_messstellen.qgs"
                    self.wasser.importieren(self.fullpath,None,"quellen",False, False, None, None, False)

                elif   ("ckQuellen" in button.objectName()):
                    self.fullpath = self.pfad + "Quellen/Vlbg/Quellpunkte/quellen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("Grundwasserfelder" in button.objectName()):
                    self.fullpath  = self.pfad +  "Grundwasser/Vlbg/Grundwasserfelder/grundwasserfelder.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("Gewaessernetz2017Vlbg" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg_Umgebung/Gewaessernetz2017/Gewaessernetz2017_nur_Vorarlberg.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg17",False, False, None, None, False)

                elif   ("Gewaessernetz2017Umgebung" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg_Umgebung/Gewaessernetz2017/Gewaessernetz2017.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg_Umgebung17",False, False, None, None, False)

                elif   ("Gewaessernetz2012Vlbg" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg_Umgebung/Fluesse1t/fluesse1t_nur_vorarlberg.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg12",False, False, None, None, False)

                elif   ("Gewaessernetz2012Umgebung" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg_Umgebung/Fluesse1t/Fluesse1t.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg_Umgebung12",False, False, None, None, False)

                elif   ("Gewaessernetz2000Vlbg" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Fluesse50t/Fluesse50t.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg00",False, False, None, None, False)

                elif   ("Gewaessernetz2000Umgebung" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg_Umgebung/Fluesse50t/Fluesse50t.qgs"
                    self.wasser.importieren(self.fullpath,None,"Vlbg_Umgebung00",False, False, None, None, False)

                elif   ("Gewaesserbewirtschaftungsplan2015" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/ngp/NGP2015.qgs"
                    self.wasser.importieren(self.fullpath,None,None,False, False, None, None, False)

                elif   ("Direkteinleitungen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/direkteinleitungen.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   ("Kontinuumsunterbrechungen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/kontinuumsunterbrechungen.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   (("SohleBoeschung") in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/sohle_boeschung.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   ("Strukturzustand" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/strukturzustand.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   ("Ufervegetation" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/ufervegetation.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   ("Abflussregime" in button.objectName()):
                    self.fullpath  = self.pfad +  "Fluesse/Vlbg/Strukturzustand/abflussregime.qgs"
                    self.wasser.importieren(self.fullpath,None,"Strukturzustand",False, False, None, None, False)

                elif   ("ckBodenseeAlles" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/bodensee.qgs"
                    self.wasser.importieren(self.fullpath,None,None,False, False, None, None, False)

                elif   ("ckBodenseeUferlinie" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/Uferlinie/Bodensee_Uferlinie_2012.qgs"
                    self.wasser.importieren(self.fullpath,None,None,False, False, None, None, False)

                elif   ("ckBodenseeWasserflaeche" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/bodensee.qgs"
                    bodenseeliste = ['Bodensee_Wasserflaeche_2012']
                    self.wasser.importieren(self.fullpath,bodenseeliste,None,False, False, None, None, False)
                elif   ("ckBodensee25m" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/bodensee.qgs"
                    bodenseeliste = ['Bodensee_25m-Tiefenlinie_2014', 'Bodensee_25m-Tiefenlinie_2008','Bodensee_25m-Tiefenlinie_1999','Bodensee_25m-Tiefenlinie_1990']
                    self.wasser.importieren(self.fullpath,bodenseeliste,None,False, False, None, None, False)

                elif   ("ckBodensee5m" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/bodensee.qgs"
                    bodenseeliste = ['Bodensee_Tiefenlinien_5m_2014','Bodensee_Tiefenlinien_5m_2008','Bodensee_Tiefenlinien_5m_1999','Bodensee_Tiefenlinien_5m_1990']
                    self.wasser.importieren(self.fullpath,bodenseeliste,None,False, False, None, None, False)

                elif   ("ckBodenseeRelief" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Bodensee/bodensee.qgs"
                    bodenseeliste = ['Bodensee_Schummerung_02m_2008','Bodensee_Schummerung_02m_1999','Bodensee_Schummerung_20m_1990']
                    self.wasser.importieren(self.fullpath,bodenseeliste,None,False, False, None, None, False)

                elif   ("ckSeen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Seen/Vlbg/Seen/Seen.qgs"
                    self.wasser.importieren(self.fullpath,None,None,False, False, None, None, False)

                elif   ("EzQuellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Quellen/Vlbg/Quelleinzugsgebiete/quelleinzugsgebiete.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("EzOberflaechenwasserMesstellen" in button.objectName()):
                    self.fullpath  = self.pfad +  "Einzugsgebiete/Vlbg_Umgebung/Einzugsgebiete_Pegelstellen/EZG_Pegelstellen.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("EzFliessgewaesser" in button.objectName()):
                    self.fullpath  = self.pfad +  "Einzugsgebiete/Vlbg_Umgebung/Einzugsgebiete_FGW/Einzugsgebiete_Vlbg_Umgebung.qgs"
                    self.wasser.importieren(self.fullpath)

                elif   ("EzWasserscheideRheinDonau" in button.objectName()):
                    self.fullpath  = self.pfad +  "Einzugsgebiete/Vlbg/Rhein_Donau/ezg_rhein_donau_vlbg.qgs"
                    self.wasser.importieren(self.fullpath)



        self.iface.mapCanvas().setRenderFlag(True)



    #schließt den Dialog für den Punkt Wasser
    def abbrechen(self):
        self.close()



    #Öffnet das dem Infobutton
    #hinterlegte PDF
    def infobuttton(self):
        os.startfile(self.pfad +  "Seen/Vlbg/Seen/" + "Seen_Kurzbeschreibung.pdf")
