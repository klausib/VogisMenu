# -*- coding: utf-8 -*-
#!/usr/bin/python

from qgis.PyQt import QtGui,QtCore,QtSql, QtPrintSupport

from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_vermessung import *
from gui_topo import *
from direk_laden import direk_laden
from ProjektImport import *

import sys,datetime,string



class VermessungDialog(QtWidgets.QDialog, Ui_frmVermessung):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)


    def __init__(self,parent,iface,pfad = None,vogisPfad = None, PGdb = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmVermessung.__init__(self)

        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.vogisPfad = vogisPfad
        self.pgdb = PGdb
        #self.vermessung_offen = vermessung_offen

        #Ränder des DIN A4 Blattes in mm
        self.links = 25
        self.oben = 20
        self.rechts = 25
        self.unten = 20

        self.vermessung = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

        # Topografie/objekt instanzieren
        # die Topografie wird in einem eigenen Fenster angezeigt
        self.topofenster = TopoAnsicht(self.iface.mainWindow(),self.iface,self.links,self.oben,self.rechts,self.unten)
        #self.topofenster = TopoAnsicht(self.iface.mainWindow(),self.iface) # Unter QT5 funktionieren die Ränder nicht! Bug???

        self.textfenster = QtGui.QTextDocument()
        self.painter = QtGui.QPainter()
        self.painter2 = QtGui.QPainter()


        self.buttonGroup.setExclusive(False)        #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
                                                    #deshalb hier
        for button in self.buttonGroup.buttons():           #wenn im Designer gesetzt, wirds beim Coderzeugen nicht übernommen
            if ("Umrisspolygone" in button.objectName()):   #deshalb hier
                button.setChecked(False)
            else:
                button.setChecked(True)


        #Variablen definieren und None setzen.
        #Sind nicht immer mit Werten initialisiert und None kann in
        #If Abfragen unterschieden werden
        self.zoompunkt = None
        self.tool_vorher = None



        #Die Datenbank öffnen. wenn keine Verbindung möglich
        #ismuss abgebrochen und der Benutzer informiert werden
        #Referenz auf die Datenquelle über ODBC
        #ACHTUNG: Ohne Connection Name HIS würde ich eine Default Connection erzeugen
        #die dann für alle DB Verbindungen gelten würde
        self.db = QtSql.QSqlDatabase.addDatabase("QODBC","HIS");
        #self.db.setDatabaseName("DRIVER={SQL Server};SERVER=vnvfelfs2.net.vlr.gv.at;DATABASE=his;UID=qgis;PWD=qgis" )
        self.db.setDatabaseName("DRIVER={SQL Server};SERVER=CNVSQL2.intra.cnv.at\CNVSQL2;DATABASE=his;UID=qgis;PWD=qgis" )


        self.ok = self.db.open()    #Gibt True zurück wenn die Datenbank offen ist
                                    #Instanzvariable ok, Eigenschaft der Klasse (wird verwendet um

                                    #zu entscheiden ob das Dialogfeld angezeigt wird


        if not self.ok:
            QtWidgets.QMessageBox.about(None, "Fehler", 'Keine Datebankverbindung')
            return

        #Verbindung zur GZ Datenbank herstellen
        #diesmal über die SQL Server Anmeldung: ACHTUNG - Domänenlogin klappt nicht

        self.db2 = QtSql.QSqlDatabase.addDatabase("QODBC","GZ");
       # self.db2.setDatabaseName("DRIVER={SQL Server};SERVER=vnvfelfs2.net.vlr.gv.at;DATABASE=GzDaten;UID=qgis;PWD=qgis" )
        self.db2.setDatabaseName("DRIVER={SQL Server};SERVER=CNVSQL2.intra.cnv.at\CNVSQL2;DATABASE=GzDaten;UID=qgis;PWD=qgis" )


        ok = self.db2.open()    #Gibt True zurück wenn die Datenbank offen ist
        if not ok:
            self.ok = False
            QtWidgets.QMessageBox.warning(None, "Fehler", "GZ Datenbank kann nicht verbunden werden")
            return  #Code wird nicht weiter ausgeführt (sonst else clause)




        #die SQL Abfragenobjekte
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrage_kat = QtSql.QSqlQuery(self.db)
        self.abfrage_kat.exec_("SELECT DISTINCT POL_NAME  FROM gemeinden")


        #Modell und Widget füllen mit Gemeindenamen
        self.modelli_kat = QtSql.QSqlQueryModel()
        self.modelli_kat.setQuery(self.abfrage_kat)
        self.lstPolgem.setModel(self.modelli_kat)


        #den mittelpunkt des aktuellenextent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)



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

        self.topocursor = QtGui.QCursor(QtCore.Qt.PointingHandCursor)



        self.vermessung = ProjektImport(self.iface) #das Objekt führt den Projektimport aus


        #Die Maptoosl erzeugen welche den Punkt zurückgeben (wenn man ins Kartnfenster klickt)
        self.PtRueckgabe = QgsMapToolEmitPoint(self.mc)
        self.PtRueckgabeTopo = QgsMapToolEmitPoint(self.mc)

        #Die Signal Slot Verbindungen funktionieren besser,
        #wenn sie beim Initialisieren egsetzt werden!

        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!
        self.PtRueckgabeTopo.canvasClicked.connect(self.returnTopo)

        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!
        self.PtRueckgabe.canvasClicked.connect(self.returnGemeinde)

        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!
        self.mc.mapToolSet.connect(self.MapButtonZuruecksetzen)

        #das ist cool: damit wird die QT Schnittstelle verwendet, die Klasse
        #QTreeWidget um im Qgis die Legendenposition zu verändern. Da Qgis für die
        #Legende ja auf QT Zugreift geht das!!


    def MapButtonZuruecksetzen(self,Tool_Gecklickt):

        if not self.PtRueckgabe is None:
            if  not (Tool_Gecklickt == self.PtRueckgabe):   #wenn ident, gleiche Speicheradresse!!
                #QtGui.QMessageBox.about(None, "Achtung", str(Tool_Gecklickt) + " gegen" + str(self.PtRueckgabe))
                self.btGmdChoice.setChecked(False)

        if not self.PtRueckgabeTopo is None:
            if not (Tool_Gecklickt == self.PtRueckgabeTopo):
                 self.btTopo.setChecked(False)


    #Wird ausgeführt wenn auf Daten laden
    #geklickt wird
    def accept(self):

        #Am Filesystem gibts keine Sonderzeichen!
        #Also müssen die Pfadstrings korrigiert werden
        gemeinde_wie_filesystem = self.Gemeinde
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ä'),'ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ä'),'Ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ö'),'oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ö'),'Oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ü'),'ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ü'),'Ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ß'),'ss')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace('. ','_')
        gemeinde_wie_filesystem = str.strip(gemeinde_wie_filesystem)

        #rendern ausschalten, sonst flackerts
        self.mc.setRenderFlag(False)

        #die button Group durchlaufen und jede
        #Checkbox prüfen, ob sie checked ist. Wenn ja die Daten
        #übers sub Daten laden holen und qml zuweisen
        for button in self.buttonGroup.buttons():

            if button.isChecked():
                pfad_ind = ""

                if   ("Einschaltpunkte" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    if str.strip(self.Gemeinde) == "Vorarlberg":
                        ep = self.daten("bev_ep","Einschaltpunkte","where kg Like '%'",self.Gemeinde)
                    else:
                        ep = self.daten("bev_ep","Einschaltpunkte",abfrage_where,self.Gemeinde)
                    if not (ep is None):
                        self.qml_zuweisen(ep,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/einschaltpunkte.qml")

                elif ("Triangulierungspunkte" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    if str.strip(self.Gemeinde) == "Vorarlberg":
                        tp = self.daten("bev_tp","Triangulierungspunkte","where kg Like '%'",self.Gemeinde)
                    else:
                        tp = self.daten("bev_tp","Triangulierungspunkte",abfrage_where,self.Gemeinde)
                    if not (tp is None):
                        self.qml_zuweisen(tp,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/triangulierungspunkte.qml")

                elif ("Nivellement" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    if str.strip(self.Gemeinde) == "Vorarlberg":
                        niv = self.daten("bev_niv","Nivellement","where kg Like '%'",self.Gemeinde)
                    else:
                        niv = self.daten("bev_niv","Nivellement",abfrage_where,self.Gemeinde)
                    if not (niv is None):
                        self.qml_zuweisen(niv,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/bev_nivellement.qml")

                elif ("Lva" in button.objectName()):

                    abfrage_where = self.generiere_abfrage()
                    lva = self.daten("lva_pkt","LVA Punkte","","Vorarlberg")
                    if not (lva is None):
                        self.qml_zuweisen(lva,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/lva_punkte.qml")


                elif ("Illwerke" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    illwerke = self.daten("illwerke_steine","Illwerke Flusssteine","","Vorarlberg")
                    if not (illwerke is None):
                        self.qml_zuweisen(illwerke,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/illwerke_flusssteine.qml")

                elif ("Naniv" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    naniv = self.daten("nach_ort_Nivs","Nachgereihtes Nivellement","where ort = 'Naniv'","Vorarlberg")
                    if not (naniv is None):
                        self.qml_zuweisen(naniv,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/naniv.qml")

                elif ("Oniv" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    oniv = self.daten("nach_ort_Nivs","Ortsnivellement","where not (ort = 'Naniv')","Vorarlberg")
                    if not (oniv is None):
                        self.qml_zuweisen(oniv,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/oniv.qml")

                elif ("Polygonpunkte" in button.objectName()):  #ist nun ein Shape, nicht aus der DB!
                    poly = direk_laden(self.pgdb, "polygonpunkte","Polygonpunkte.shp", self.vogisPfad + "Naturbestand/" + gemeinde_wie_filesystem + "/",self.iface)

                    if not (poly is None):
                        #Prüfen ob die Polygonpubnkte geladen sind
                        yes = False
                        for vorhanden in self.mc.layers():
                            if str.strip(vorhanden.name()) == str.strip("VKW-Polygonpunkte-" + self.Gemeinde):  #Aha, den Layer gibts schon
                                yes = True
                        if not yes:
                            self.qml_zuweisen(poly,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/vkw_polygonpunkte.qml")
                            if self.pgdb == None:
                                self.gruppe(str.strip(self.Gemeinde) + "-Vermessung",poly)
                            else:
                                self.gruppe("Vorarlberg-Vermessung",poly)
                elif ("Umrisspolygone" in button.objectName()):  #ist nun ein Projekt, nicht aus der DB!
                    self.vermessung.importieren(self.pfad + "/Vermessungen/vlbg/vermessungen/Vermessungen.qgs")



        #rendern wieder einschalten
        self.mc.setRenderFlag(True)

    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)



        #ACHTUNG!! Die Datenbankverbindung MUSS sauber geschlossen werden
        #das geht nur wenn ALLES Instanzen, welche diese noch irgendwie verwenden
        #geschlossen werden. Der Garbage Collector macht das nicht immer sauber, dann hängt mal wieder eine DB Verbindung...
        self.lstPolgem.setModel(None)
        self.modelli_kat = None
        self.abfrage_kat = None
        self.abfrage2 = None
        self.abfrage = None
        self.abfrage_bilder = None
        self.abfrage_gemeinde = None
        self.abfrage_gz = None
        self.abfrage_logo = None
        self.abfrage_lva_pkt = None
        self.topofenster = None
        self.textfenster = None
        self.painter = None
        self.painter2 = None
        self.modell_kg = None



        if not (self.tool_vorher is None):
            self.mc.setMapTool(self.tool_vorher)

        if not self.db == None:
            self.db.close()

        self.db.close()
        if not self.db2 == None:
            self.db2.close()

        #disconnect: weil sonst trotz close und del das signal slot verhältnis nicht sauber gelöscht wird
        #wieso??
        #QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)



        self.close()


    #Daten aus der Datenbank absaugen, Punktgeometry erzeugen
    #und in einen Memorylayer schreiben
    def daten(self,tabellenname,layername,abfrage_where = None,Gemeindetext = ""):

        self.abfrage.exec_("SELECT DISTINCT *  FROM " +  tabellenname + " " + abfrage_where)
        self.abfrage.first()                #WICHTIG: sonst kann NICHTS abgefragt werden (auch nicht die Feldeigenschaften!) da exec sonst
                                            #auf invalid record steht
        if not self.abfrage.isValid():
            #Abfrage hat keine Daten geliefert, für die betreffende Gemeinde existieren
            #keine Punkte zu diesem Thema.
            return

        #Memory Layer anlegen, wenn nicht vorhanden, die notwendigen
        #attributspalten (typ, name, precision) nach Vorbild der Datenbank anlegen,
        #Punktgeometry erzeugen hineinzeichnen und Attribute dazufüllen
        yes = False
        geomType = 'Point' + '?crs=proj4:' + QgsProject.instance().readEntry("SpatialRefSys","/ProjectCRSProj4String")[0]
        #Die geladenen Layer im QGis durchgehen:

        for vorhanden in self.mc.layers():
            if str.strip(vorhanden.name()) == str.strip(layername + "-" + Gemeindetext):  #Aha, den Layer gibts schon
                #yes = True
                return
        epLayer = QgsVectorLayer(geomType, str.strip(layername) + "-" + str.strip(Gemeindetext), 'memory')
        QgsProject.instance().addMapLayer(epLayer)     #wenn nicht, dann neu anlegen


        #der Memorylayer soll ja nicht nur die Geometrie
        #sondern auch alle Sachattribute aus der datenbanktabelle
        #enthalten
        feld = []   #eine leere Liste initialisieren
        feldnamen = self.db.record(tabellenname)    #Gibt eine Liste mit den Feldnamen zurück


        #Schleife legt die Attributfelder nach Datenbankvorbild
        #in die Listenvariable: Die Namen haben wir ja schon, hier wird der Feldtyp
        #dazu ausgelesen!

        for depp in range(feldnamen.count()):   #Iteration über die einzelnen Felder

            if type(self.abfrage.value(depp)) == long:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.Int, 'qlonglong',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == int:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.Int,'int',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == str:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.String,'str',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == unicode:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.String,'str',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == float:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.Double,'double',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == datetime.date:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.Date,'date',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == datetime.time:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.Time,'time',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            elif  type(self.abfrage.value(depp)) == datetime.datetime:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.DateTime,'datetime',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))
            else:
                feld.append(QgsField(feldnamen.fieldName(depp), QtCore.QVariant.String,'str',self.abfrage.record().field(depp).length(),self.abfrage.record().field(depp).precision(),""))

        epProvider = epLayer.dataProvider()
        epProvider.addAttributes(feld)  #so, die leere Hülse des Memory Layers mit den Attributspalten
                                        #ist fertig




        #Nun zur Geometrie
        #Die Feldindices für die Geomatrie
        #bestimmen. Ist leider nicht einheitlich für unterschiedliche Tabellen

        if (tabellenname == "lva_pkt") or (tabellenname == "illwerke_steine"):
            fieldNoX = self.abfrage.record().indexOf("pkt_rechtswert")
            fieldNoY = self.abfrage.record().indexOf("pkt_hochwert")
        else:
            fieldNoX = self.abfrage.record().indexOf("rechtswert")
            fieldNoY = self.abfrage.record().indexOf("hochwert")


        self.progressBar.setRange(0,self.abfrage.numRowsAffected()-1)   #Fortschrittsbalken initialisieren

        self.abfrage.seek(-1)   #Abfrage wird zurück vor den ersten Rekord positioniert
                                #damit mit .next nicht der erste datensatz verschluckt wird!!

        #benötigte Punkt und Featureobjekte instanzieren
        ep_point = QgsPointXY()
        ep_geom = QgsGeometry()
        ep_feature = QgsFeature()

        featureliste = []
        i=0
        #edit session starten
        epLayer.startEditing()
        ep_feature = QgsFeature()

        #Schleife geht jeden rekord der Datenbanktabelle durch, berechnet die Punktgeometrie
        #fügt die Attribute hinzu und schreibt alles in den Memorylayer
        while self.abfrage.next():
            #Geometry des neuen Features
            ep_point.setX(self.abfrage.value(fieldNoX))
            ep_point.setY(self.abfrage.value(fieldNoY))    #da ein tuple zurückgegeben wird
            ep_feature.setGeometry(ep_geom.fromPointXY(ep_point))         #da ein tuple zurückgegeben wird

            d = []  #attibute map erzeugen: bekommt in der Schleife die Attributwerte
            for depp in range(feldnamen.count()):
                fieldNo = self.abfrage.record().indexOf(feldnamen.fieldName(depp))
                #Typ Documentation unter file:///C:/Python27/Lib/site-packages/PyQt4/doc/html/qvariant.html#Type-enum
                d.append(self.abfrage.value(fieldNo))
            self.progressBar.setValue(i)

            ep_feature.setAttributes(d)   #Nun wird die Attribute Map aufs Feature gesetzt!
            i=i+1
            epLayer.addFeature(ep_feature)  #und nun alles dem Layer hinzugefügt


        #fertig -> edit session beenden
        epLayer.commitChanges()

        if epLayer.isValid():
            #Die Gruppenzugehörigkeit regeln, d.h.
            #den Memorylayer in einen Gruppenlayer legen
            #Das macht die Methode gruppe!
            self.gruppe(str.strip(Gemeindetext) + "-Vermessung",epLayer)

            #referenz auf fertiges Layerobjekt zurückgeben
            return epLayer
        else:
            QtWidgets.QMessageBox.critical(None, "Achtung",'Layer ' + str.strip(layername) + "-" + str.strip(Gemeindetext) + ' nicht erfolgreich geladen!')
            return None

    #Ermittelt anhand des aktuellen Kartenmittelpunkts (Variable ergebnis)
    #im QGIS den Namen passende Gemeinde und ruft die
    #Routine zum Aktualisieren des Listenfelds auf
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde. Wird auch aufgerufen,
    #wenn die GEmeinde mit dem roten Kreuzchen ausgewählt wird
    def returnGemeinde(self,ergebnis):


        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er autonmatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in self.mc.layers():
            if vorhanden.name() == "Gemeinden":
                yes = True
                break

        if yes:
            gmdLayer = vorhanden
        else:
            wert = ("Sonntag")
            self.auswahlaenderung(wert )
            return

        #damit nichts flackert
        self.mc.setRenderFlag(False)


        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des features der betreffenden politischen Gemeinde
        #im Gememindelayer in QGIS
        shift=self.mc.mapUnitsPerPixel()
        wahlRect = QgsRectangle(ergebnis.x(),ergebnis.y(),ergebnis.x()+ shift,ergebnis.y()+ shift)
        #Entsprechendes Feature (=Gemeinde) im Layer selektieren
        gmdLayer.selectByRect(wahlRect,False)

        #Den Index des feldes PGEM_NAME
        #in der Attributtabelle des Layers finden
        #brauch ich um die grafisch ausgewählte Gemeinde
        #im Listenfeld optisch in die mitte zu holen
        Liste = gmdLayer.selectedFeatures()

        #Auswahl wieder löschen
        gmdLayer.removeSelection()



        # API für QGIS 2.0
        if  (len(Liste) > 0):
            self.auswahlaenderung(Liste[0].attribute('PGEM_NAME'))
        else:   #WICHTIG!! ist der Extent so daß mit der Ermittlung des Mittelpunkts
                #keine Gemeinde gefunden wird, stellen wir auf Sonntag!
            self.auswahlaenderung('Sonntag' )
        self.mc.setRenderFlag(True)


    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):
        mc = self.iface.mapCanvas()
        Punkt = mc.extent().center()
        return Punkt

    #Methode Aktualisiert nur das zweite Listenfeld für die KG - Gemeindenummer
    #Wird entweder von der Methode "returnGemeinde" oder
    #über eine Action beim Anklicken des Listenfeldes
    #mit der Gemeindenliste (politische) aufgerufen
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde
    def auswahlaenderung(self,SelItem,Nummer = None):




        #if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!
        if isinstance(SelItem, unicode):    #QGIS 2 hat je keine Qstring mehr!
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem
            self.lstPolgem.keyboardSearch(self.Gemeinde)
            index = self.lstPolgem.selectedIndexes()
            self.lstPolgem.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen

        elif isinstance(SelItem, str):
            self.Gemeinde = SelItem
            self.lstPolgem.keyboardSearch(SelItem)
            index = self.lstPolgem.selectedIndexes()
            self.lstPolgem.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
        else:
            #noch was optisches. Egal ob über Cursor oder Direkt im
            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
            #wird automatisch in die mitte des Listenfeldes gescrollt
            self.Gemeinde = SelItem.data(0)

            self.lstPolgem.scrollTo(SelItem,3) #3 bedeutet in die Mitte des Listenfelds scrollen



        #bei einer Auwhaländerung, d.h. eine neue Gemeinde ist gesucht
        #muß das zweite Listebnfeld auch aktualisiert werden und vorher
        #natürlich eine neue Abfrage der KG gemacht werden
        self.abfrage2 = QtSql.QSqlQuery(self.db)
        self.abfrage2.exec_("SELECT DISTINCT kg FROM gemeinden WHERE POL_NAME = '" + self.Gemeinde + "'")
        self.modell_kg = QtSql.QSqlQueryModel()



        #Der Suchbutton wird deaktiviert, damit der User
        #vor der Suche die KG zur Politischen Gemeinde auswählen muß
        #QtCore.QObject.connect(self.modell_kg, QtCore.SIGNAL("modelReset ()"), self.gstsuche_deaktivieren)

        #Das Listenfeld für KG-Gemeinde mit der Abfrageaktualisieren
        self.modell_kg.setQuery(self.abfrage2)


    #Knopf zur interaktiven
    #Auswahl einer Gemeinde indem man in das QGIS Fenster klicket
    def gmd_choice_toggled(self):

        #Der Kreuzchenknopf ist gechecked
        if self.btGmdChoice.isChecked():


            # erstmal das vorher eingestellte Maptool
            #sicherstellen (um wieder zurücksetzen zu können!)
            if not(self.btTopo.isChecked()):
                self.tool_vorher = self.mc.mapTool()

            self.btTopo.setChecked(False)
            #Das Aussehen des Mauscursor im QGIS Kartenbild

            #wird auf unseren Cursor gesetzt
            self.iface.mapCanvas().setCursor(self.cursor)


            #und QGIS auf das neue Maptool einstellen!
            self.mc.setMapTool(self.PtRueckgabe)
            self.mc.setCursor(self.cursor)


        #Der Kreuzchenknopf ist nicht gechecked
        elif not(self.btGmdChoice.isChecked()):
            self.mc.setMapTool(self.tool_vorher)    #auf ursprüngliches Maptool und zugehörigen Cursor urücksetzen

    #Knopf dum Abfragen der LVA Punkttopographie
    #indem man auf das Punktsymbol klicket. Der LAyer muß
    #dabei nicht ausgewählt, aber geladen sein
    def topo_choice_toggled(self):

        #Der Kreuzchenknopf ist gechecked
        if self.btTopo.isChecked():


            #erstmal das vorher eingestellte Maptool
            #sicherstellen (um wieder zurücksetzen zu können!)
            if not(self.btGmdChoice.isChecked()):
                self.tool_vorher = self.mc.mapTool()

            self.btGmdChoice.setChecked(False)

            #Das Aussehen des Mauscursor im QGIS Kartenbild
            #wird auf unseren Cursor gesetzt
            self.iface.mapCanvas().setCursor(self.topocursor)


            #und QGIS auf das neue Maptool einstellen!
            self.mc.setMapTool(self.PtRueckgabeTopo)
            self.mc.setCursor(self.topocursor)



        #Der Kreuzchenknopf ist nicht gechecked
        elif not(self.btTopo.isChecked()):
            self.mc.setMapTool(self.tool_vorher)    #auf ursprüngliches Maptool und zugehörigen Cursor urücksetzen



    #Die where Clause der Abfrage zusammenstellen
    #die die Daten aus der Datenbank HIS holt
    #Sollte dynamisch sein, deshalb eigenes Sub
    def generiere_abfrage(self):
        counter = 0
        abfrage =""

        iModel = self.modell_kg     #Siehe Doku: Ein  Pointer auf das zugrundeliegende Model
        for i in range(iModel.rowCount()):  #die ausgewählten Records durchlaufen

            iRecord = iModel.record(i)
            #Weil es Gemeinden mit mehreren KGs gibt und ich ja nach
            #KGs auswählen muß!
            if counter < 1:
                abfrage = "where (kg = " + str(iRecord.value("kg")) + ")"
            else:
                abfrage = abfrage + " or (kg = " + str(iRecord.value("kg")) + ")"
            counter = counter + 1

        return abfrage


    # Gruppenlayer falls notwendig erzeugen und
    # Memorylayer reinbewegen
    def gruppe(self,layername,layerobjekt):

        #leginterface = self.iface.legendInterface()

        gruppe_vorhanden = False
        if not (layername is None):

            if QgsProject.instance().layerTreeRoot().findGroup(layername) != None: #Name ist übergeben worden
                gruppe_vorhanden = True


        self.legendTree= QgsProject.instance().layerTreeRoot()

        #Ist die Gruppe nicht vorhanden , anlegen
        if (not gruppe_vorhanden):
            grp = self.legendTree.insertGroup(0,layername)

        zwtsch = QgsProject.instance().layerTreeRoot().findLayer(layerobjekt.id()) #der geladene layer
        index = zwtsch.clone()
        grp = QgsProject.instance().layerTreeRoot().findGroup(layername) #der geladene layer
        grp.insertChildNode(0,index)
        zwtsch.parent().removeChildNode(zwtsch)
        grp.setExpanded(False)



    #Methode weist QML Datei dem
    #Memorylayer zu
    def qml_zuweisen(self,layer,qmlpfad):

        if not layer.isValid(): #nicht erfolgreich geladen
            QtWidgets.QMessageBox.about(None, "Fehler", layer.name())
        else:   #erfolgreich geladen
            #dem Vektorlayer das QML File zuweisen
            #flagge[1] ist false wenn das file nich gefunden wird
            flagge = layer.loadNamedStyle(qmlpfad)
            if flagge[1]:
                #Legendenansicht aktualisieren
                self.iface.layerTreeView().refreshLayerSymbology( layer.id() )
            else:
                QtWidgets.QMessageBox.about(None, "Fehler", ("QML konnte nicht zugewiesen werden! - " + qmlpfad))
            #Zur Map Layer registry hinzufügen damit der Layer
            #dargestellt wird
            QgsProject.instance().addMapLayer(layer)



    #Gibt die Topographie des angeklickten Punktes zurück
    #Nur für LVA Punkte: Daten werden aus den Datenbanken
    #geholt und in einem eigenen Textformular dargestell
    def returnTopo(self,punkt):
        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er autonmatisch dabei
        #Sonst wird abgebrochen

        # Fenster (wieder) leeren
        # sonst addiert sich der Inhalte mit jedem weiteren Klick
        self.topofenster.textView.clear()

        yes = False
        for vorhanden in self.mc.layers():
            if "LVA Punkte" in vorhanden.name():
                yes = True
                break

        if yes:
            topoLayer = vorhanden
        else:
            QtWidgets.QMessageBox.warning(None, "Fehler", "Layer LVA Punkte nicht geladen")
            return


        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des features der betreffenden politischen Gemeinde
        #im Gememindelayer in QGIS. Rechteck deshalb weils erstens eins sein muß
        #und zweitend dadurch ein bißchen Toleranz beim Klicken möglich ist
        shift=self.mc.mapUnitsPerPixel() * 4    # +-vier Pixel Toleranz beim reinklicken ist geplant
        wahlRect = QgsRectangle(punkt.x()- shift,punkt.y() - shift ,punkt.x()+ shift,punkt.y()+ shift)
        #Entsprechendes Feature im Layer selektieren
        topoLayer.removeSelection()
        topoLayer.selectByRect(wahlRect,False)
        #Index des benötigten Attributfeldes "index": Es verknüpft die lva Punkttablle
        #mit der tabelle, die die topographiebilder enthält
        feldindex = topoLayer.fields().lookupField("index")
        if feldindex == -1:
            QtWidgets.QMessageBox.about(None, "Fehler", "Achtung, Feld index nicht gefunden!")
            return
        feat = QgsFeature()

        if not topoLayer.selectedFeatureCount() > 0:
            QtWidgets.QMessageBox.about(None, "Fehler", "Kein Punkt angeklickt!")
            return
        featureliste = topoLayer.selectedFeatures()




        #wir nehemen nur eines der ausgewählten features sollte
        #per Zufahl eine mehrfachauswahl getätigt werden (punkte eng beieinander)
        feat = featureliste[0]
        attribute = feat.attributes()




        #punktinformationen des lva punktes abfragen
        self.abfrage_lva_pkt = QtSql.QSqlQuery(self.db)
        self.abfrage_lva_pkt.exec_("SELECT lva_nummer,pkt_rechtswert,pkt_hochwert,pkt_hoehe,gz,gst_nr,eigentuemer,fp_anschl,bolzen_rechtswert,bolzen_hochwert,bolzen_hoehe,hb_anschl_1,hb_anschl_2,bezeichnung,lva_hoehenbezug,geprueft from lva_pkt where [index] = " + str(attribute[feldindex]))
        self.abfrage_lva_pkt.next()

        #abfrage der GZ Datenbank des ausgewählten punktes
        self.abfrage_gz = QtSql.QSqlQuery(self.db2)
        self.abfrage_gz.exec_("select G_kg1,G_sb,G_dverist, G_dcheck from T_GZ_qt where G_gz = " + self.abfrage_lva_pkt.value(4))    #leider brauchts ein VIEW
        self.abfrage_gz.next()

        #abfrage der Datenbank für die Gemeindebezeichnung
        self.abfrage_gemeinde = QtSql.QSqlQuery(self.db)
        self.abfrage_gemeinde.exec_("select pol_name,kg from gemeinden where kg_name = '" + str.strip(self.abfrage_gz.value(0)) + "'")    #leider brauchts ein VIEW
        self.abfrage_gemeinde.next()


        #die bilddaten werden per binärem stream
        #aus der datenbank (dort blob) geholt und
        #dann in eine imagevariable (objekt) eingelesen
        #topografiebilder in imageobjekt einlesen
        self.abfrage_bilder = QtSql.QSqlQuery(self.db)
        self.abfrage_bilder.exec_("SELECT bild1 from lva_topo where index_lva_pkt = " + str.strip(str(attribute[feldindex])))
        self.abfrage_bilder.next()
        self.bild1 = QtGui.QImage()
        self.bild1.loadFromData(self.abfrage_bilder.value(0))
        if self.bild1.byteCount() < 1:    #keine Topografie vorhanden
            QtWidgets.QMessageBox.information(None, "Hinweis", "Keine Topografie vorhanden")
            return

        self.abfrage_bilder.exec_("SELECT bild2 from lva_topo where index_lva_pkt = " + str.strip(str(attribute[feldindex])))
        self.abfrage_bilder.next()
        self.bild2 = QtGui.QImage()
        self.bild2.loadFromData(self.abfrage_bilder.value(0))
        if self.bild2.byteCount() < 1:        #keine Topografie vorhanden
            QtWidgets.QMessageBox.information(None, "Hinweis", "Keine Topografie vorhanden")
            return

        # das Logo aus der Datenbank holen
        self.abfrage_logo = QtSql.QSqlQuery(self.db)
        self.abfrage_logo.exec_("SELECT logos from logos where lva_log = 'lva'")
        self.abfrage_logo.next()
        self.img = QtGui.QImage()
        self.img.loadFromData(self.abfrage_logo.value(0))


        #nun haben wir alles geholt
        #jetzt gehts zur Darstellung
        #die geht über 2 DIN A4 Seiten mit eingelagerten
        #verschachtelten Tabellen. Als Container für alles
        #dient das QTextDocument und dann für die
        #Darstellung das QTextEdit Objekt
        #Tabelle und Textfenster
        #self.textfenster = QtGui.QTextDocument() #DAS zentrale Texktobjekt, container für alles
        self.textimage = QtGui.QTextCursor(self.textfenster)  #Cursor wird auf das zentrale Texktobjekt referenziert
        self.textimage.movePosition(QtGui.QTextCursor.Start)

        #die Formate der Tabellen definieren: Es gibt
        #Haupt und Subtabellen
        self.tabellenformat = QtGui.QTextTableFormat()
        self.tabellenformat.setBorder(2)
        self.tabellenformat.setCellPadding(1)
        self.tabellenformat.setCellSpacing(1)

        self.tabellenformat_sub = QtGui.QTextTableFormat()
        self.tabellenformat_sub.setBorder(0)
        self.tabellenformat_sub.setCellPadding(1)
        self.tabellenformat_sub.setCellSpacing(1)



        # Imagebreite in Pixel festlegen
        monitoraufloesung = self.topofenster.textView.logicalDpiX()
        breite = 210 - self.links - self.rechts #bezogen auf DIN A4 in mm
        pixelbreite = monitoraufloesung / 2.54 * breite/10

        # Imagehöhe in Pixel festlegen
        hoehe = 125 #bezogen auf DIN A4 in mm
        pixelhoehe = (monitoraufloesung / 2.54 * hoehe/10)

        # spaltenbreite der sub tabellen
        breite=[]
        breite.append (QtGui.QTextLength(QtGui.QTextLength.FixedLength,pixelbreite*0.95/2)) #für die erste spalte!!
        breite.append (QtGui.QTextLength(QtGui.QTextLength.FixedLength,pixelbreite*0.95/2)) #für die zweite spalte!!

        # Schriftformate definieren
        self.standardschrift = QtGui.QFont("Times New Roman", 16)
        self.standardschriftFett = QtGui.QFont("Times New Roman", 16, QtGui.QFont.Bold)
        self.standardschriftFettGroesser = QtGui.QFont("Times New Roman", 18, QtGui.QFont.Bold)
        self.standardformat = QtGui.QTextCharFormat()
        self.standardformat.setFont(self.standardschrift)
        self.standardformatFett = QtGui.QTextCharFormat(self.standardformat)
        self.standardformatFett.setFont(self.standardschriftFett)
        self.standardformatFettGroesser = QtGui.QTextCharFormat(self.standardformat)
        self.standardformatFettGroesser.setFont(self.standardschriftFettGroesser)


        ###################################################################
        # Die erste Tabellenseite #########################################
        ###################################################################

        self.tabelle1 = self.textimage.insertTable(5,1,self.tabellenformat)
        self.tabelle1.setObjectName("tabelle1")  #ein objektname ist wichtig - siehe schreibschutz

        #Logo
        self.cellCursor = self.tabelle1.cellAt(0,0).firstCursorPosition()
        self.cellCursor.insertImage(self.img.scaledToWidth(pixelbreite*0.95,QtCore.Qt.SmoothTransformation))
        #GZ
        self.cellCursor = self.tabelle1.cellAt(1,0).firstCursorPosition()
        self.cellCursor.insertText("GZ: " + str(self.abfrage_lva_pkt.value(4)),self.standardformatFett)
        #HZB und fremde Nr
        self.cellCursor = self.tabelle1.cellAt(2,0).firstCursorPosition()
        self.tabellenformat_sub.setColumnWidthConstraints(breite)
        self.tabelle1_sub = self.cellCursor.insertTable(2,2,self.tabellenformat_sub)
        self.tabelle1_sub.setObjectName("self.tabelle1_sub")  #ein objektname ist wichtig - siehe schreibschutz

        self.cellCursor_sub = self.tabelle1_sub.cellAt(0,1).firstCursorPosition()
        self.cellCursor_sub.setBlockCharFormat(self.standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        self.cellCursor_sub.insertText("HZB: ",self.standardformat)
        self.cellCursor_sub = self.tabelle1_sub.cellAt(1,1).firstCursorPosition()
        self.cellCursor_sub.setBlockCharFormat(self.standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        self.cellCursor_sub.insertText("Fremde Nr.: ",self.standardformat)
        self.cellCursor_sub = self.tabelle1_sub.cellAt(1,0).firstCursorPosition()
        self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + self.abfrage_lva_pkt.value(0),self.standardformatFettGroesser)


        #erster hauptblock
        self.cellCursor = self.tabelle1.cellAt(3,0).firstCursorPosition()
        self.tabellenformat_sub.setColumnWidthConstraints(breite)
        self.tabelle2_sub = self.cellCursor.insertTable(9,2,self.tabellenformat_sub)
        self.tabelle2_sub.setObjectName("self.tabelle2_sub")  #ein objektname ist wichtig - siehe schreibschutz

        self.cellCursor_sub = self.tabelle2_sub.cellAt(0,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Ortsgemeinde:",self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(1,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Katastralgemeinde:",self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(2,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Kg.-Nr.:",self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(3,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Gst.-Nr.:",self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(4,0).firstCursorPosition()
        self.cellCursor_sub.insertText(("Eigentümer:"),self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(5,0).firstCursorPosition()
        self.cellCursor_sub.insertText(("Eigentümer Rohr:"),self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(6,0).firstCursorPosition()
        self.cellCursor_sub.insertText(("Festpunktanschluss:"),self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(7,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Koordinaten Rohr:",self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(8,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Koordinaten Bolzen:",self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(0,1).firstCursorPosition()
        self.cellCursor_sub.insertText(self.abfrage_gemeinde.value(0),self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(1,1).firstCursorPosition()
        self.cellCursor_sub.insertText(self.abfrage_gz.value(0),self.standardformat)
        self.cellCursor_sub = self.tabelle2_sub.cellAt(2,1).firstCursorPosition()
        self.cellCursor_sub.insertText(str(self.abfrage_gemeinde.value(1)),self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(3,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(5) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(5),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(4,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(6) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(6),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(5,1).firstCursorPosition()
        self.cellCursor_sub.setBlockCharFormat(self.standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        self.cellCursor_sub.insertText(("Abt. VIId - Wasserwirtschaft"),self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(6,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(7) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(7),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(7,1).firstCursorPosition()
        self.cellCursor_sub.insertText(str(self.abfrage_lva_pkt.value(1)) + "     " + str(self.abfrage_lva_pkt.value(2)),self.standardformat)

        self.cellCursor_sub = self.tabelle2_sub.cellAt(8,1).firstCursorPosition()
        # Alter Code if not (self.abfrage_lva_pkt.value(8) == None or self.abfrage_lva_pkt.value(9).isNull()):  #falls in der db nicht befüllt wird die spalte leergelassen
        if not (self.abfrage_lva_pkt.value(8) == None or self.abfrage_lva_pkt.value(9) == None):  #falls in der db nicht befüllt wird die spalte leergelassen
            # Alter Code self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(8) + "     " + self.abfrage_lva_pkt.value(9),self.standardformat)
            self.cellCursor_sub.insertText(str(self.abfrage_lva_pkt.value(8)) + "     " + str(self.abfrage_lva_pkt.value(9)),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)
        # erstes Topografie Bild einfügen
        self.cellCursor = self.tabelle1.cellAt(4,0).firstCursorPosition()
        self.zentriert = QtGui.QTextBlockFormat()
        self.zentriert.setAlignment(QtCore.Qt.AlignHCenter)
        self.cellCursor.setBlockFormat(self.zentriert)

        # Damit die Seitenumbrüche und die Seitenränder auch mit unterschiedlichen Bildgrößen korrekt sind
        # wird ein weisses Dummybild erzeugt mit konstanter und passender Größe das denn mit den eigentlichen
        # Topographie Bild überlagert wird. Das Topographiebild wird dabei zur maximal Breite/Höhe (je nach dem
        # was zuerst erreicht wird) vergrößert.
        self.pm1 = QtGui.QPixmap(pixelbreite*0.985,pixelhoehe * 0.92)
        self.pm1.fill(QtGui.QColor(QtCore.Qt.white)) # Weiß
        self.pm2 = QtGui.QPixmap(self.bild1.scaled(pixelbreite*0.985,pixelhoehe * 0.92,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        self.pm = QtGui.QPixmap(pixelbreite * 0.985,pixelhoehe * 0.92)

        self.label = QtWidgets.QLabel()  # um den Qself.painter in QGIS zu initialisieren
                                # sonst gibts einen Crash. Möglicherweise gibt es eine besser Lösung
                                # Achtung: Der self.painter wird bei bild2 auch wieder verwendet
                                # muss aber nicht mehr initialisiert werden, da gleiches Objekt


        self.painter.begin(self.pm)
        self.painter.drawPixmap(0,0, self.pm1)
        self.painter.drawPixmap((pixelbreite * 0.985 - self.pm2.width()) / 2,(pixelhoehe * 0.92 - self.pm2.height()) / 2, self.pm2)
        self.label.setPixmap(self.pm) # Für die self.painter Initialisierung!
        #self.label.show()

        self.cellCursor.insertImage(self.pm.toImage().copy())    # in die Zelle einfügen



        ###################################################################
        # Die zweite Tabellenseite ########################################
        ###################################################################

        # einfügecursor an das Ende der ersten Tabelle bewegen
        self.textimage.movePosition(QtGui.QTextCursor.End)
        self.tabelle2 = self.textimage.insertTable(5,1,self.tabellenformat)
        self.tabelle2.setObjectName("tabelle2")  #ein objektname ist wichtig - siehe schreibschutz

        # Logo
        self.cellCursor = self.tabelle2.cellAt(0,0).firstCursorPosition()
        self.cellCursor.insertImage(self.img.scaledToWidth(pixelbreite*0.95,QtCore.Qt.SmoothTransformation))
        #GZ
        self.cellCursor = self.tabelle2.cellAt(1,0).firstCursorPosition()
        self.cellCursor.insertText("GZ: " + self.abfrage_lva_pkt.value(4),self.standardformatFett)

        self.cellCursor = self.tabelle2.cellAt(2,0).firstCursorPosition()
        self.tabellenformat_sub.setColumnWidthConstraints(breite)
        tabelle3_sub = self.cellCursor.insertTable(2,2,self.tabellenformat_sub)
        tabelle3_sub.setObjectName("tabelle3_sub")  #ein objektname ist wichtig - siehe schreibschutz

        self.cellCursor_sub = tabelle3_sub.cellAt(1,0).firstCursorPosition()
        if self.abfrage_lva_pkt.value(13) == 'GWR':
            bez = 'ROK'
        else:
            bez = self.abfrage_lva_pkt.value(13)
        #self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + str(self.abfrage_lva_pkt.value(3)) + (" müA"),standardformatFettGroesser)
        self.cellCursor_sub.insertText(bez + ": " + str(self.abfrage_lva_pkt.value(3)) + (" müA"),self.standardformatFettGroesser)
        self.cellCursor_sub = tabelle3_sub.cellAt(1,1).firstCursorPosition()

        if not self.abfrage_lva_pkt.value(10) == None :  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText("Bolzen: " + str(self.abfrage_lva_pkt.value(10)) + (" müA"),self.standardformatFettGroesser)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)
        self.cellCursor_sub = tabelle3_sub.cellAt(0,0).firstCursorPosition()
        self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + str(self.abfrage_lva_pkt.value(0)),self.standardformatFettGroesser)


        #erster hauptblock
        self.cellCursor = self.tabelle2.cellAt(3,0).firstCursorPosition()
        self.tabellenformat_sub.setColumnWidthConstraints(breite)
        self.tabelle4_sub = self.cellCursor.insertTable(8,2,self.tabellenformat_sub)
        self.tabelle4_sub.setObjectName("self.tabelle4_sub")  #ein objektname ist wichtig - siehe schreibschutz

        self.cellCursor_sub = self.tabelle4_sub.cellAt(1,0).firstCursorPosition()
        self.cellCursor_sub.insertText("HB Anschluss 1:",self.standardformat)
        self.cellCursor_sub = self.tabelle4_sub.cellAt(1,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(11) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(11),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)
        self.cellCursor_sub = self.tabelle4_sub.cellAt(2,0).firstCursorPosition()
        self.cellCursor_sub.insertText("HB Anschluss 2:",self.standardformat)
        self.cellCursor_sub = self.tabelle4_sub.cellAt(2,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(12) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(self.abfrage_lva_pkt.value(12),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)

        self.cellCursor_sub = self.tabelle4_sub.cellAt(5,0).firstCursorPosition()
        self.cellCursor_sub.insertText("Sachbearbeiter: " + self.abfrage_gz.value(1),self.standardformat)
        self.cellCursor_sub = self.tabelle4_sub.cellAt(6,0).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(15) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            self.cellCursor_sub.insertText(("Geprüft von: ") + self.abfrage_lva_pkt.value(15),self.standardformat)
        else:
            self.cellCursor_sub.insertText("",self.standardformat)


        self.cellCursor_sub = self.tabelle4_sub.cellAt(5,1).firstCursorPosition()
        tag = self.abfrage_gz.value(2).date().day()
        monat = self.abfrage_gz.value(2).date().month()
        jahr = self.abfrage_gz.value(2).date().year()
        self.cellCursor_sub.insertText("Vermessung am: " + str(tag) + "." + str(monat) + "." + str(jahr),self.standardformat)
        self.cellCursor_sub = self.tabelle4_sub.cellAt(6,1).firstCursorPosition()
        tag = self.abfrage_gz.value(3).date().day()
        monat = self.abfrage_gz.value(3).date().month()
        jahr = self.abfrage_gz.value(3).date().year()
        self.cellCursor_sub.insertText(("Geprüft am: ") + str(tag) + "." + str(monat) + "." + str(jahr),self.standardformat)


        #zweites Topografie Bild einfügen
        self.cellCursor2 = self.tabelle2.cellAt(4,0).firstCursorPosition()
        self.cellCursor2.setBlockFormat(self.zentriert)
        # Damit die Seitenumbrüche und die Seitenränder auch mit unterschiedlichen Bildgrößen korrekt sind
        # wird ein weisses Dummybild erzeugt mit konstanter und passender Größe das denn mit den eigentlichen
        # Topographie Bild überlagert wird. Das Topographiebild wird dabei zur maximal Breite/Höhe (je nach dem
        # was zuerst erreicht wird) vergrößert.
        self.pm2 = QtGui.QPixmap(self.bild2.scaled(pixelbreite*0.985,pixelhoehe * 0.92,QtCore.Qt.KeepAspectRatio,QtCore.Qt.SmoothTransformation))
        self.pm = QtGui.QPixmap(pixelbreite * 0.985,pixelhoehe * 0.92)
        #self.painter2 = QtGui.QPainter(self.pm)
        self.painter2.begin(self.pm)
        self.painter2.drawPixmap(0,0, self.pm1)
        self.painter2.drawPixmap((pixelbreite * 0.985 - self.pm2.width()) / 2,(pixelhoehe * 0.92 - self.pm2.height()) / 2, self.pm2)
        self.cellCursor2.insertImage(self.pm.toImage())    # in die Zelle einfügen

        #Alles ins Textview reinschreiben
        self.topofenster.textView.setDocument(self.textfenster)
        self.topofenster.textView.setLineWrapMode(2)
        self.topofenster.textView.setLineWrapColumnOrWidth(pixelbreite)    #die Pixelanzahl die einer realen Breite von "breite" entspricht



        #Signal/Slot für den Schreibschutz der Tabelle
        #mit Schreibrechten in 3 Zellen jedoch!!
        #das Signal wird vomObjekttyp QTextEdit emittiert wann immer der Cursoer
        #neu positioniert wird. Indem man schaut ob das feld editierbar sein soll
        #kann so ein schreibschutz gesetzt werden
        #QtCore.QObject.connect(self.topofenster.textView, QtCore.SIGNAL("cursorPositionChanged ()"), self.schreibschutz)
        self.topofenster.textView.cursorPositionChanged.connect(self.schreibschutz)
        #das Fenster zeigen (und eventschleife draufgeben)
        self.topofenster.show()

        # Wichtig
        self.painter.end()
        self.painter2.end()


    #der slot der berechnet,
    #in welche spalte und zeile der tabelle geklickt wird
    #und so den schreibschutz (des gesamten Dokuments) anpaßt
    def schreibschutz(self):

        editcursor = self.topofenster.textView.textCursor()
        edittable = editcursor.currentTable()
        self.topofenster.textView.setReadOnly(True) #genereller Schreibschutz mit Ausnahmen
        if not edittable == None:
            aktZelle = edittable.cellAt(editcursor)

            #wenn in die Zelle geklickt wird
            #prüfen ob schreiben erlaubt!
            if edittable.objectName() == "self.tabelle1_sub":
                if aktZelle.row() == 0 and aktZelle.column() == 1:
                    self.topofenster.textView.setReadOnly(False)
                elif aktZelle.row() == 1 and aktZelle.column() == 1:
                    self.topofenster.textView.setReadOnly(False)
                else:
                    self.topofenster.textView.setReadOnly(True)

            if edittable.objectName() == "self.tabelle2_sub":
                if aktZelle.row() == 5 and aktZelle.column() == 1:
                    self.topofenster.textView.setReadOnly(False)
                else:
                    self.topofenster.textView.setReadOnly(True)

    def uncheck(self):
        for button in self.buttonGroup.buttons():

            if not ("Umrisspolygone" in button.objectName()):
                button.setChecked(False)



#Klassendefinition für das Topographie Anzeigefenster
#dieses Fenster kann auch den Inhalt drucken!
class TopoAnsicht(QtWidgets.QDialog,Ui_frmTopo):

    def __init__(self,parent,iface,links = 20,oben = 20,rechts = 20,unten = 20):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmTopo.__init__(self)


        # Unter QT5 funktionieren die Ränder nicht! Bug???
        self.links = 6 #links
        self.rechts = 5 #rechts
        self.oben = 5 #oben
        self.unten = 5 #unten


        self.drucker = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)  #ACHTUNG: Druckerobjekt immer als
        self.drucker.setPageSize(QtGui.QPageSize(QtGui.QPageSize.A4))
        self.drucker.setFullPage(True)
        self.drucker.setPageMargins(self.links,self.oben,self.rechts,self.unten,0)



        #depp = QtGui.QTextBlockFormat()
        #depp.setPageBreakPolicy(QtGui.QTextFormat.PageBreak_AlwaysAfter)



        self.setupUi(self)

    #diese paar Zeilen genügen
    #um den Inhalt
    def drucken_text(self):
        dialog_t = QtPrintSupport.QPrintDialog(self.drucker)

        if dialog_t.exec_() == QtWidgets.QDialog.Accepted:

            self.textView.print(self.drucker)  #textView ist das TexteditObjekt im Ui_frmTopo
                                                #es wird ja in diese Klasse veraerbt und hat die Methode Drucken: Der Inhalt wird dann gedruckt

        del dialog_t



    def closeEvent(self,event = None):
        self.drucker = None
        self.close()





