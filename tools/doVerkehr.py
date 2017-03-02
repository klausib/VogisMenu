# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore

from qgis.core import *
from gui_verkehr import *
from gui_wegtafeln import *
from osgeo import ogr
from direk_laden import direk_laden
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *






#Dies Klassendefinition öffnet das Frame für
#die Auswahl der Datenebenen Verkehr und enthält
#auch weitere M
class VerkehrDialog(QtGui.QDialog, Ui_frmVerkehr):
    def __init__(self,parent,iface,pfad = None, vogisPfad = None, PGdb = None):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmVerkehr.__init__(self)


        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.db=PGdb
        self.vogisPfad = vogisPfad
        self.ckButtons.setExclusive(False)  #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                            #deshalb hier

        self.verkehr = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def lade_daten(self):

        self.mc.setRenderFlag(False)
        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.ckButtons.buttons():

            if button.isChecked(): #wenn gecket wird geladen
                if   ("Hauptstrasse" in button.objectName()):
                    self.fullpath = self.pfad + "Strasse/Vlbg/Hoeherrangige_Strasse/Strassen.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Gemeindestrasse" in button.objectName()):
                    self.fullpath = self.pfad + "Strasse/Vlbg/Ortsstrasse/ortsstrasse.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Bahn" in button.objectName()):
                    self.fullpath = self.pfad + "Bahn/Vlbg/OEBB_MBS/bahnlinie.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Oepnv" in button.objectName()):
                    self.fullpath = self.pfad + "Oepnv/Vlbg/oeffentlicher_verkehr/Oeffentlicher_Verkehr.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Seilbahn" in button.objectName()):
                    self.fullpath = self.pfad + "Aufstiegshilfe/Vlbg/Seilbahn/Seilbahn.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Hindernisse" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Gefahren/Luftfahrt/Vlbg/Flughindernis/Flughindernis.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Forstweg" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Forstweg/forstweg.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Gueterweg" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Gueterweg"

                    #schlampig: Legendenshape hier dazuladen
##                    if self.db  != None:
##                        try:
##                            # Geodatenbank
##                            uri = QgsDataSourceURI()
##                            uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(),'','')  # Keine Kennwort nötig, Single Sign On
##
##                            # Geometriespalte bestimmen -- geht nur mit OGR
##                            outputdb = ogr.Open('pg: host =' + self.db.hostName() + ' dbname =' + self.db.databaseName() + ' schemas=vorarlberg')
##                            geom_column = outputdb.GetLayerByName('gueterwege').GetGeometryColumn()
##
##                            uri.setDataSource('vorarlberg', 'gueterwege', geom_column)
##
##                            gueterweg = QgsVectorLayer(uri.uri(), "gueterwege","postgres")
##                        except:
##                            QtGui.QMessageBox.about(None, "Fehler", "Layer ""gueterwege"" in der Datenbank nicht gefunden - es wird aufs Filesystem umgeschaltet")
##                            gueterweg = QgsVectorLayer(self.fullpath + "/gueterwege.shp","Gueterwege","ogr")
##                    else:
##                        gueterweg = QgsVectorLayer(self.fullpath + "/gueterwege.shp","Gueterwege","ogr")
##
                    gueterweg = direk_laden(self.db, "gueterwege", "gueterwege.shp", self.fullpath + "/",self.iface)


                    #und prüfen ob erfolgreich geladen
                    if not gueterweg.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", ("Güterwege konnte nicht geladen werden").decode('utf8'))
                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = gueterweg.loadNamedStyle(self.fullpath + "/gueterwege.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( gueterweg )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", ("Güterweg QML konnte nicht zugewiesen werden!").decode('utf8'))
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(gueterweg)
                        gueterweg.setLayerName(("Güterwege").decode('utf8'))

                elif   ("Wanderwege" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Wanderweg/wandern.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Winterwanderwege" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Winterwanderweg/winterwander.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Radwege" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Radweg/radweg.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Mountainbike" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Mountainbike/mountainbike.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Landesradroute" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Radweg/Landesradrouten.qgs"
                    self.verkehr.importieren(self.fullpath)
                elif   ("Lrr_beschildert" in button.objectName()):
                    self.fullpath = self.vogisPfad + "Verkehr/Weg/Vlbg/Radwegweiser/Landesradrouten_beschildert.qgs"
                    self.verkehr.importieren(self.fullpath)

        self.mc.setRenderFlag(True)

    #wird auf den Button Wegtafeln geklickt
    #startet diese Methode
    def suche_wegtafeln(self):

        yes = False
        #ist der benötigte Layer Wegtafeln im Qgis geladen
        #(ist im Dialogfeld frmVerkehr natürlich vorgesehen: kommte unter
        #dem Punkt wnaderwege mit)
        for vorhanden in self.mc.layers():
            if vorhanden.name() == "Wegweiser (a):":
                yes = True
                break

        #layer ist vorhanden, Dialogfeld
        #Wegtafeln kann geladen werden
        if yes:
            wegtafelnlayer = vorhanden
            wegtafeln = WegtafelnDialog(self,wegtafelnlayer,self.mc)
        else:
            QtGui.QMessageBox.about(None, "Layer fehlt", "Layer Wegweiser ist nicht geladen") #Fehlermedlung falls nicht
            return


        wegtafeln.show()

    #schließt den Dialog für den Punkt Verkehr
    def abbrechen(self):
        self.close()

#diese Klasse bedient den Wegtafeln Dialog frmWegtafeln
class WegtafelnDialog(QtGui.QDialog, Ui_frmWegtafeln):
    def __init__(self,parent,tafeln_layer,mc):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmVerkehr.__init__(self)

        self.setupUi(self)
        self.layer = tafeln_layer
        self.mc = mc


        provider = self.layer.dataProvider()

##
        iter = self.layer.getFeatures()
        Liste = []    #eine Liste instanzieren
        iter.rewind()
        for attr in iter:

            Liste.append(str(attr.attribute("TAFEL_NR")))


        #Listenfeld des Dialogs frmWegtafeln mit den Tafelnummern füllen
        #und sortieren
        self.lstNummern.addItems(Liste)
        self.lstNummern.sortItems()



    #Wird auf OK geklickt wird auf die im Listenfeld ausgewählte
    #Wegtafel gezoomt. Ist keine ausgewählt gibts
    #eine Fehlermeldung
    def zoomtafel(self):

        #Wir erhalten die ListItem Liste der Auswahl (SingleMode Selection!)
        auswahl = self.lstNummern.selectedItems()
        if (len(auswahl) == 0):    #wenn nichts ausgewählt ist
            QtGui.QMessageBox.about(None, ("Nichts ausgewählt").decode('utf8'), ("Bitte eine Wegtafel auswählen").decode('utf8'))
            return #und Methode verlassen

        #da eine Mehrfachauswahl im ListWidget nicht möglich ist, index immer 0
        nummer = auswahl[0].text().strip()


        iter = self.layer.getFeatures()
        Liste = []    #eine Liste instanzieren
        iter.rewind()
        for attr in iter:
            if str(attr.attribute("TAFEL_NR")) == nummer:
                self.zoompunkt = attr.geometry().boundingBox() # zoom Rechteck des richtigen Features
                break   #Schleife verlassen

        #und zum richtigen Ort zoomen
        self.mc.setExtent(self.zoompunkt)
        self.mc.zoomScale(5000)



    #Wegtafeln Dialog schließen
    def abbrechen(self):
        self.close()

