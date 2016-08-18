# -*- coding: utf-8 -*-
#!/usr/bin/python

from PyQt4 import QtGui,QtCore,QtSql

from qgis.core import *
from qgis.gui import *
from qgis.analysis import *
from gui_vermessung import *
from gui_topo import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import sys,datetime,string



class VermessungDialog(QtGui.QDialog, Ui_frmVermessung):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)


    def __init__(self,parent,iface,pfad = None,vogisPfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmVermessung.__init__(self)

        self.iface = iface
        self.mc = iface.mapCanvas()
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.vogisPfad = vogisPfad
        #self.vermessung_offen = vermessung_offen

        #Ränder des DIN A4 Blattes in mm
        self.links = 25
        self.oben = 20
        self.rechts = 25
        self.unten = 20

        self.vermessung = ProjektImport(self.iface)    #das Projekt Import Objekt instanzieren

        #Topografie/objekt instanzieren
        #die Topografie wird in einem eigenen Fenster angezeigt
        self.topofenster = TopoAnsicht(self.iface.mainWindow(),self.iface,self.links,self.oben,self.rechts,self.unten)


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
            QtGui.QMessageBox.about(None, "Fehler", 'Keine Datebankverbindung')
            return

        #Verbindung zur GZ Datenbank herstellen
        #diesmal über die SQL Server Anmeldung: ACHTUNG - Domänenlogin klappt nicht

        self.db2 = QtSql.QSqlDatabase.addDatabase("QODBC","GZ");
       # self.db2.setDatabaseName("DRIVER={SQL Server};SERVER=vnvfelfs2.net.vlr.gv.at;DATABASE=GzDaten;UID=qgis;PWD=qgis" )
        self.db2.setDatabaseName("DRIVER={SQL Server};SERVER=CNVSQL2.intra.cnv.at\CNVSQL2;DATABASE=GzDaten;UID=qgis;PWD=qgis" )


        ok = self.db2.open()    #Gibt True zurück wenn die Datenbank offen ist
        if not ok:
            self.ok = False
            QtGui.QMessageBox.warning(None, "Fehler", "GZ Datenbank kann nicht verbunden werden")
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
        QtCore.QObject.connect(self.PtRueckgabeTopo, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnTopo)

        #WICHTIG: ein Signal/Slot Verbindung herstellen zwischen dem neuen Maptool
        #und der Methode die die Gemeinde einstellt. Dabei wird das punktobjekt übertragen!!
        QtCore.QObject.connect(self.PtRueckgabe, QtCore.SIGNAL("canvasClicked(const QgsPoint &, Qt::MouseButton)"), self.returnGemeinde)

        #WICHTIG: ein Signal/Slot Verbindung herstellen
        #wenn ein Maptool Change Signal emittiert wird!
        QtCore.QObject.connect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)

        #das ist cool: damit wird die QT Schnittstelle verwendet, die Klasse
        #QTreeWidget um im Qgis die Legendenposition zu verändern. Da Qgis für die
        #Legende ja auf QT Zugreift geht das!!
##        self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)
##        self.legendTree= QgsProject.instance().layerTreeRoot()

##        #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
##        # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
##        # der Legende vor allem Laden als Aktueller Layer gesetztw erden!!!
##        self.legendTree.setCurrentItem(self.legendTree.topLevelItem(0))


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
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ä').decode('utf8'),'ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ä').decode('utf8'),'Ae')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ö').decode('utf8'),'oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ö').decode('utf8'),'Oe')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ü').decode('utf8'),'ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('Ü').decode('utf8'),'Ue')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace(('ß').decode('utf8'),'ss')
        gemeinde_wie_filesystem = gemeinde_wie_filesystem.replace('. ','_')
        gemeinde_wie_filesystem = string.strip(gemeinde_wie_filesystem)

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
                    if string.strip(self.Gemeinde) == "Vorarlberg":
                        ep = self.daten("bev_ep","Einschaltpunkte","where kg Like '%'",self.Gemeinde)
                    else:
                        ep = self.daten("bev_ep","Einschaltpunkte",abfrage_where,self.Gemeinde)
                    if not (ep is None):
                        self.qml_zuweisen(ep,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/einschaltpunkte.qml")

                elif ("Triangulierungspunkte" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    if string.strip(self.Gemeinde) == "Vorarlberg":
                        tp = self.daten("bev_tp","Triangulierungspunkte","where kg Like '%'",self.Gemeinde)
                    else:
                        tp = self.daten("bev_tp","Triangulierungspunkte",abfrage_where,self.Gemeinde)
                    if not (tp is None):
                        self.qml_zuweisen(tp,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/triangulierungspunkte.qml")

                elif ("Nivellement" in button.objectName()):
                    abfrage_where = self.generiere_abfrage()
                    if string.strip(self.Gemeinde) == "Vorarlberg":
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
                        lva.setAnnotationForm(self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/ui/gz.ui")


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
                    poly = QgsVectorLayer(self.vogisPfad + "Naturbestand/" + gemeinde_wie_filesystem + "/Polygonpunkte.shp","VKW-Polygonpunkte-" + self.Gemeinde ,"ogr")
                    if not (poly is None):
                        #Prüfen ob die Polygonpubnkte geladen sind
                        yes = False
                        for vorhanden in self.mc.layers():
                            if string.strip(vorhanden.name()) == string.strip("VKW-Polygonpunkte-" + self.Gemeinde):  #Aha, den Layer gibts schon
                                yes = True
                        if not yes:
                            self.qml_zuweisen(poly,self.pfad + "/Vermessungspunkte/Vlbg/hoehengis/vkw_polygonpunkte.qml")
                            self.gruppe(string.strip(self.Gemeinde) + "-Vermessung",poly)
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
        QtCore.QObject.disconnect(self.mc, QtCore.SIGNAL("mapToolSet (QgsMapTool *)"), self.MapButtonZuruecksetzen)


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
            if string.strip(vorhanden.name()) == string.strip(layername + "-" + Gemeindetext):  #Aha, den Layer gibts schon
                #yes = True
                return

##        if yes:
##            epLayer = vorhanden #Wenns ihn schon gibt, wird er verwendet um die Daten reinzuschreiben
##        else:
        epLayer = QgsVectorLayer(geomType, string.strip(layername) + "-" + string.strip(Gemeindetext), 'memory')
        QgsMapLayerRegistry.instance().addMapLayer(epLayer)     #wenn nicht, dann neu anlegen


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
        ep_point = QgsPoint()
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
            ep_feature.setGeometry(ep_geom.fromPoint(ep_point))         #da ein tuple zurückgegeben wird

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
            self.gruppe(string.strip(Gemeindetext) + "-Vermessung",epLayer)

            #referenz auf fertiges Layerobjekt zurückgeben
            return epLayer
        else:
            QtGui.QMessageBox.critical(None, "Achtung",'Layer ' + string.strip(layername) + "-" + string.strip(Gemeindetext) + ' nicht erfolgreich geladen!')
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
        gmdLayer.select(wahlRect,False)

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

        leginterface = self.iface.legendInterface()


        if not (layername is None):
            gruppenliste = leginterface.groups()
            gruppe_vorhanden = False
            #prüfen ob die Gruppe schon angelegt ist
            for einzelgruppe in gruppenliste:
                if einzelgruppe == layername: #Name ist übergeben worden
                    gruppe_vorhanden = True

        if QGis.QGIS_VERSION_INT < 20300:

            self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)


            #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
            # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
            # der Legende vor allem Laden als Aktueller Layer gesetztw erden!!!
            self.legendTree.setCurrentItem(self.legendTree.findItems(layerobjekt.name(),QtCore.Qt.MatchRecursive,0)[0])

            tmp_ly = self.legendTree.currentItem()  #Widget Item des gerade eingefügten Layers
            index_neu = self.legendTree.indexOfTopLevelItem(tmp_ly) #index bestimmen
            index = self.legendTree.takeTopLevelItem(index_neu)  #und rausnehmen!

                #Ist die Gruppe nicht vorhanden , anlegen
            if (not gruppe_vorhanden):
                #QtGui.QMessageBox.about(None, "Fehler", 'Gruppi')
                grp = leginterface.addGroup(layername,False,None)    #Name ist übergeben worden
                #es ist notwendig die gruppe nach oben zu schieben
                tmp = self.legendTree.currentItem()
                grp_unten = self.legendTree.indexOfTopLevelItem(tmp)
                grp_oben = self.legendTree.takeTopLevelItem(grp_unten)
                self.legendTree.insertTopLevelItem(0,grp_oben)


            liste = self.legendTree.findItems(layername,QtCore.Qt.MatchRecursive,0)[0]

                #den Layer in die Legende unterhalb des Gruppenlayers einfügen
            liste.insertChild(0,index)

        else:


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
            QtGui.QMessageBox.about(None, "Fehler", layer.name())
        else:   #erfolgreich geladen
            #dem Vektorlayer das QML File zuweisen
            #flagge[1] ist false wenn das file nich gefunden wird
            flagge = layer.loadNamedStyle(qmlpfad)
            if flagge[1]:
                #Legendenansicht aktualisieren
                self.iface.legendInterface().refreshLayerSymbology( layer )
            else:
                QtGui.QMessageBox.about(None, "Fehler", ("QML konnte nicht zugewiesen werden! - " + qmlpfad))
            #Zur Map Layer registry hinzufügen damit der Layer
            #dargestellt wird
            QgsMapLayerRegistry.instance().addMapLayer(layer)



    #Gibt die Topographie des angeklickten Punktes zurück
    #Nur für LVA Punkte: Daten werden aus den Datenbanken
    #geholt und in einem eigenen Textformular dargestell
    def returnTopo(self,punkt):
        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er autonmatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in self.mc.layers():
            if "LVA Punkte" in vorhanden.name():
                yes = True
                break

        if yes:
            topoLayer = vorhanden
        else:
            QtGui.QMessageBox.warning(None, "Fehler", "Layer LVA Punkte nicht geladen")
            return


        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des features der betreffenden politischen Gemeinde
        #im Gememindelayer in QGIS. Rechteck deshalb weils erstens eins sein muß
        #und zweitend dadurch ein bißchen Toleranz beim Klicken möglich ist
        shift=self.mc.mapUnitsPerPixel() * 4    # +-vier Pixel Toleranz beim reinklicken ist geplant
        wahlRect = QgsRectangle(punkt.x()- shift,punkt.y() - shift ,punkt.x()+ shift,punkt.y()+ shift)
        #Entsprechendes Feature im Layer selektieren
        topoLayer.removeSelection()
        topoLayer.select(wahlRect,False)
        #Index des benötigten Attributfeldes "index": Es verknüpft die lva Punkttablle
        #mit der tabelle, die die topographiebilder enthält
        feldindex = topoLayer.fieldNameIndex("index")
        if feldindex == -1:
            QtGui.QMessageBox.about(None, "Fehler", "Achtung, Feld index nicht gefunden!")
            return
        feat = QgsFeature()

        if not topoLayer.selectedFeatureCount() > 0:
            QtGui.QMessageBox.about(None, "Fehler", "Kein Punkt angeklickt!")
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
        self.abfrage_gemeinde.exec_("select pol_name,kg from gemeinden where kg_name = '" + string.strip(self.abfrage_gz.value(0)) + "'")    #leider brauchts ein VIEW
        self.abfrage_gemeinde.next()


        #die bilddaten werden per binärem stream
        #aus der datenbank (dort blob) geholt und
        #dann in eine imagevariable (objekt) eingelesen
        #topografiebilder in imageobjekt einlesen
        self.abfrage_bilder = QtSql.QSqlQuery(self.db)
        self.abfrage_bilder.exec_("SELECT bild1 from lva_topo where index_lva_pkt = " + string.strip(str(attribute[feldindex])))
        self.abfrage_bilder.next()
        bild1 = QtGui.QImage()
        bild1.loadFromData(self.abfrage_bilder.value(0))
        if bild1.numBytes() < 1:    #keine Topografie vorhanden
            QtGui.QMessageBox.information(None, "Hinweis", "Keine Topografie vorhanden")
            return

        self.abfrage_bilder.exec_("SELECT bild2 from lva_topo where index_lva_pkt = " + string.strip(str(attribute[feldindex])))
        self.abfrage_bilder.next()
        bild2 = QtGui.QImage()
        bild2.loadFromData(self.abfrage_bilder.value(0))
        if bild2.numBytes() < 1:        #keine Topografie vorhanden
            QtGui.QMessageBox.information(None, "Hinweis", "Keine Topografie vorhanden")
            return

        # das Logo aus der Datenbank holen
        self.abfrage_logo = QtSql.QSqlQuery(self.db)
        self.abfrage_logo.exec_("SELECT logos from logos where lva_log = 'lva'")
        self.abfrage_logo.next()
        img = QtGui.QImage()
        img.loadFromData(self.abfrage_logo.value(0))


        #nun haben wir alles geholt
        #jetzt gehts zur Darstellung
        #die geht über 2 DIN A4 Seiten mit eingelagerten
        #verschachtelten Tabellen. Als Container für alles
        #dient das QTextDocument und dann für die
        #Darstellung das QTextEdit Objekt
        #Tabelle und Textfenster
        textfenster = QtGui.QTextDocument() #DAS zentrale Texktobjekt, container für alles
        textimage = QtGui.QTextCursor(textfenster)  #Cursor wird auf das zentrale Texktobjekt referenziert
        textimage.movePosition(QtGui.QTextCursor.Start)

        #die Formate der Tabellen definieren: Es gibt
        #Haupt und Subtabellen
        tabellenformat = QtGui.QTextTableFormat()
        tabellenformat.setBorder(2)
        tabellenformat.setCellPadding(1)
        tabellenformat.setCellSpacing(1)
        tabellenformat_sub = QtGui.QTextTableFormat()
        tabellenformat_sub.setBorder(0)
        tabellenformat_sub.setCellPadding(1)
        tabellenformat_sub.setCellSpacing(1)

        #Imagebreite in Pixel festlegen
        monitoraufloesung = self.topofenster.textView.physicalDpiX()
        breite = 210 - self.links - self.rechts #bezogen auf DIN A4 in mm
        pixelbreite = monitoraufloesung / 2.54 * breite/10

        #Imagehöhe in Pixel festlegen
        hoehe = 120 #bezogen auf DIN A4 in mm
        pixelhoehe = (monitoraufloesung / 2.54 * hoehe/10)

        #spaltenbreite der sub tabellen
        breite=[]
        breite.append (QtGui.QTextLength(QtGui.QTextLength.FixedLength,pixelbreite*0.95/2)) #für die erste spalte!!
        breite.append (QtGui.QTextLength(QtGui.QTextLength.FixedLength,pixelbreite*0.95/2)) #für die zweite spalte!!

        #Schriftformate definieren
        standardschrift = QtGui.QFont("Times New Roman", 16)
        standardschriftFett = QtGui.QFont("Times New Roman", 16, QtGui.QFont.Bold)
        standardschriftFettGroesser = QtGui.QFont("Times New Roman", 18, QtGui.QFont.Bold)
        standardformat = QtGui.QTextCharFormat()
        standardformat.setFont(standardschrift)
        standardformatFett = QtGui.QTextCharFormat(standardformat)
        standardformatFett.setFont(standardschriftFett)
        standardformatFettGroesser = QtGui.QTextCharFormat(standardformat)
        standardformatFettGroesser.setFont(standardschriftFettGroesser)


        ###################################################################
        # Die erste Tabellenseite #########################################
        ###################################################################

        tabelle1 = textimage.insertTable(5,1,tabellenformat)
        tabelle1.setObjectName("tabelle1")  #ein objektname ist wichtig - siehe schreibschutz

        #Logo
        cellCursor = tabelle1.cellAt(0,0).firstCursorPosition()
        cellCursor.insertImage(img.scaledToWidth(pixelbreite*0.95,QtCore.Qt.SmoothTransformation))
        #GZ
        cellCursor = tabelle1.cellAt(1,0).firstCursorPosition()
        cellCursor.insertText("GZ: " + str(self.abfrage_lva_pkt.value(4)),standardformatFett)
        #HZB und fremde Nr
        cellCursor = tabelle1.cellAt(2,0).firstCursorPosition()
        tabellenformat_sub.setColumnWidthConstraints(breite)
        tabelle1_sub = cellCursor.insertTable(2,2,tabellenformat_sub)
        tabelle1_sub.setObjectName("tabelle1_sub")  #ein objektname ist wichtig - siehe schreibschutz

        cellCursor_sub = tabelle1_sub.cellAt(0,1).firstCursorPosition()
        cellCursor_sub.setBlockCharFormat(standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        cellCursor_sub.insertText("HZB: ",standardformat)
        cellCursor_sub = tabelle1_sub.cellAt(1,1).firstCursorPosition()
        cellCursor_sub.setBlockCharFormat(standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        cellCursor_sub.insertText("Fremde Nr.: ",standardformat)
        cellCursor_sub = tabelle1_sub.cellAt(1,0).firstCursorPosition()
        cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + self.abfrage_lva_pkt.value(0),standardformatFettGroesser)


        #erster hauptblock
        cellCursor = tabelle1.cellAt(3,0).firstCursorPosition()
        tabellenformat_sub.setColumnWidthConstraints(breite)
        tabelle2_sub = cellCursor.insertTable(9,2,tabellenformat_sub)
        tabelle2_sub.setObjectName("tabelle2_sub")  #ein objektname ist wichtig - siehe schreibschutz

        cellCursor_sub = tabelle2_sub.cellAt(0,0).firstCursorPosition()
        cellCursor_sub.insertText("Ortsgemeinde:",standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(1,0).firstCursorPosition()
        cellCursor_sub.insertText("Katastralgemeinde:",standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(2,0).firstCursorPosition()
        cellCursor_sub.insertText("Kg.-Nr.:",standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(3,0).firstCursorPosition()
        cellCursor_sub.insertText("Gst.-Nr.:",standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(4,0).firstCursorPosition()
        cellCursor_sub.insertText(("Eigentümer:").decode('utf8'),standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(5,0).firstCursorPosition()
        cellCursor_sub.insertText(("Eigentümer Rohr:").decode('utf8'),standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(6,0).firstCursorPosition()
        cellCursor_sub.insertText(("Festpunktanschluß:").decode('utf8'),standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(7,0).firstCursorPosition()
        cellCursor_sub.insertText("Koordinaten Rohr:",standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(8,0).firstCursorPosition()
        cellCursor_sub.insertText("Koordinaten Bolzen:",standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(0,1).firstCursorPosition()
        cellCursor_sub.insertText(self.abfrage_gemeinde.value(0),standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(1,1).firstCursorPosition()
        cellCursor_sub.insertText(self.abfrage_gz.value(0),standardformat)
        cellCursor_sub = tabelle2_sub.cellAt(2,1).firstCursorPosition()
        cellCursor_sub.insertText(str(self.abfrage_gemeinde.value(1)),standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(3,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(5) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(self.abfrage_lva_pkt.value(5),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(4,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(6) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(self.abfrage_lva_pkt.value(6),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(5,1).firstCursorPosition()
        cellCursor_sub.setBlockCharFormat(standardformat)   #gesamte Zelle auf Format setzen: Sonst kanns beim Editieren verloren gehen wenn text gelöscht wird
        cellCursor_sub.insertText(("Abt. VIId - Wasserwirtschaft"),standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(6,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(7) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(self.abfrage_lva_pkt.value(7),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(7,1).firstCursorPosition()
        cellCursor_sub.insertText(str(self.abfrage_lva_pkt.value(1)) + "     " + str(self.abfrage_lva_pkt.value(2)),standardformat)

        cellCursor_sub = tabelle2_sub.cellAt(8,1).firstCursorPosition()
        # Alter Code if not (self.abfrage_lva_pkt.value(8) == None or self.abfrage_lva_pkt.value(9).isNull()):  #falls in der db nicht befüllt wird die spalte leergelassen
        if not (self.abfrage_lva_pkt.value(8) == None or self.abfrage_lva_pkt.value(9) == None):  #falls in der db nicht befüllt wird die spalte leergelassen
            # Alter Code cellCursor_sub.insertText(self.abfrage_lva_pkt.value(8) + "     " + self.abfrage_lva_pkt.value(9),standardformat)
            cellCursor_sub.insertText(str(self.abfrage_lva_pkt.value(8)) + "     " + str(self.abfrage_lva_pkt.value(9)),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)

        #erstes Topografie Bild einfügen
        cellCursor = tabelle1.cellAt(4,0).firstCursorPosition()
        zentriert = QtGui.QTextBlockFormat()
        zentriert.setAlignment(QtCore.Qt.AlignHCenter)
        cellCursor.setBlockFormat(zentriert)
        cellCursor.insertImage(bild1.scaledToHeight(pixelhoehe*0.94,QtCore.Qt.SmoothTransformation))    #damits auf eine Seite paßt


        ###################################################################
        # Die zweite Tabellenseite ########################################
        ###################################################################

        #einfügecursor an das Ende der ersten Tabelle bewegen
        textimage.movePosition(QtGui.QTextCursor.End)
        tabelle2 = textimage.insertTable(5,1,tabellenformat)
        tabelle2.setObjectName("tabelle2")  #ein objektname ist wichtig - siehe schreibschutz

        #Logo
        cellCursor = tabelle2.cellAt(0,0).firstCursorPosition()
        cellCursor.insertImage(img.scaledToWidth(pixelbreite*0.95,QtCore.Qt.SmoothTransformation))
        #GZ
        cellCursor = tabelle2.cellAt(1,0).firstCursorPosition()
        cellCursor.insertText("GZ: " + self.abfrage_lva_pkt.value(4),standardformatFett)

        cellCursor = tabelle2.cellAt(2,0).firstCursorPosition()
        tabellenformat_sub.setColumnWidthConstraints(breite)
        tabelle3_sub = cellCursor.insertTable(2,2,tabellenformat_sub)
        tabelle3_sub.setObjectName("tabelle3_sub")  #ein objektname ist wichtig - siehe schreibschutz

        cellCursor_sub = tabelle3_sub.cellAt(1,0).firstCursorPosition()
        if self.abfrage_lva_pkt.value(13) == 'GWR':
            bez = 'ROK'
        else:
            bez = self.abfrage_lva_pkt.value(13)
        #cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + str(self.abfrage_lva_pkt.value(3)) + (" müA").decode('utf8'),standardformatFettGroesser)
        cellCursor_sub.insertText(bez + ": " + str(self.abfrage_lva_pkt.value(3)) + (" müA").decode('utf8'),standardformatFettGroesser)
        cellCursor_sub = tabelle3_sub.cellAt(1,1).firstCursorPosition()

        if not self.abfrage_lva_pkt.value(10) == None :  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText("Bolzen: " + str(self.abfrage_lva_pkt.value(10)) + (" müA").decode('utf8'),standardformatFettGroesser)
        else:
            cellCursor_sub.insertText("",standardformat)
        cellCursor_sub = tabelle3_sub.cellAt(0,0).firstCursorPosition()
        cellCursor_sub.insertText(self.abfrage_lva_pkt.value(13) + ": " + str(self.abfrage_lva_pkt.value(0)),standardformatFettGroesser)


        #erster hauptblock
        cellCursor = tabelle2.cellAt(3,0).firstCursorPosition()
        tabellenformat_sub.setColumnWidthConstraints(breite)
        tabelle4_sub = cellCursor.insertTable(8,2,tabellenformat_sub)
        tabelle4_sub.setObjectName("tabelle4_sub")  #ein objektname ist wichtig - siehe schreibschutz

        cellCursor_sub = tabelle4_sub.cellAt(1,0).firstCursorPosition()
        cellCursor_sub.insertText("HB Anschluss 1:",standardformat)
        cellCursor_sub = tabelle4_sub.cellAt(1,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(11) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(self.abfrage_lva_pkt.value(11),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)
        cellCursor_sub = tabelle4_sub.cellAt(2,0).firstCursorPosition()
        cellCursor_sub.insertText("HB Anschluss 2:",standardformat)
        cellCursor_sub = tabelle4_sub.cellAt(2,1).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(12) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(self.abfrage_lva_pkt.value(12),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)

        cellCursor_sub = tabelle4_sub.cellAt(5,0).firstCursorPosition()
        cellCursor_sub.insertText("Sachbearbeiter: " + self.abfrage_gz.value(1),standardformat)
        cellCursor_sub = tabelle4_sub.cellAt(6,0).firstCursorPosition()
        if not self.abfrage_lva_pkt.value(15) == None:  #falls in der db nicht befüllt wird die spalte leergelassen
            cellCursor_sub.insertText(("Geprüft von: ").decode('utf8') + self.abfrage_lva_pkt.value(15),standardformat)
        else:
            cellCursor_sub.insertText("",standardformat)


        cellCursor_sub = tabelle4_sub.cellAt(5,1).firstCursorPosition()
        tag = self.abfrage_gz.value(2).date().day()
        monat = self.abfrage_gz.value(2).date().month()
        jahr = self.abfrage_gz.value(2).date().year()
        cellCursor_sub.insertText("Vermessung am: " + str(tag) + "." + str(monat) + "." + str(jahr),standardformat)
        cellCursor_sub = tabelle4_sub.cellAt(6,1).firstCursorPosition()
        tag = self.abfrage_gz.value(3).date().day()
        monat = self.abfrage_gz.value(3).date().month()
        jahr = self.abfrage_gz.value(3).date().year()
        cellCursor_sub.insertText(("Geprüft am: ").decode('utf8') + str(tag) + "." + str(monat) + "." + str(jahr),standardformat)

        #zweites Topografie Bild einfügen
        cellCursor = tabelle2.cellAt(4,0).firstCursorPosition()
        cellCursor.setBlockFormat(zentriert)
        cellCursor.insertImage(bild2.scaledToHeight(pixelhoehe*0.94,QtCore.Qt.SmoothTransformation))


        #Alles ins Textview reinschreiben

        self.topofenster.textView.setDocument(textfenster)
        self.topofenster.textView.setLineWrapMode(2)
        self.topofenster.textView.setLineWrapColumnOrWidth(pixelbreite)    #die Pixelanzahl die einer realen Breite von "breite" entspricht

        #Signal/Slot für den Schreibschutz der Tabelle
        #mit Schreibrechten in 3 Zellen jedoch!!
        #das Signal wird vomObjekttyp QTextEdit emittiert wann immer der Cursoer
        #neu positioniert wird. Indem man schaut ob das feld editierbar sein soll
        #kann so ein schreibschutz gesetzt werden
        QtCore.QObject.connect(self.topofenster.textView, QtCore.SIGNAL("cursorPositionChanged ()"), self.schreibschutz)

        #das Fenster zeigen (und eventschleife draufgeben)
        self.topofenster.show()


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
            if edittable.objectName() == "tabelle1_sub":
                if aktZelle.row() == 0 and aktZelle.column() == 1:
                    self.topofenster.textView.setReadOnly(False)
                elif aktZelle.row() == 1 and aktZelle.column() == 1:
                    self.topofenster.textView.setReadOnly(False)
                else:
                    self.topofenster.textView.setReadOnly(True)

            if edittable.objectName() == "tabelle2_sub":
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
class TopoAnsicht(QtGui.QDialog,Ui_frmTopo):

    def __init__(self,parent,iface,links = 20,oben = 20,rechts = 20,unten = 20): #,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_frmTopo.__init__(self)


        self.drucker = QtGui.QPrinter(QtGui.QPrinter.PrinterResolution) #ACHTUNG: Druckerobjekt immer als
                                                                        #Instanzvariable sonst klappts nicht!
        self.drucker.setPageSize(QtGui.QPrinter.A4)
        self.drucker.setPageMargins(links,oben,rechts,unten,0)

        self.setupUi(self)

    #diese paar Zeilen genügen
    #um den Inhalt
    def drucken_text(self):
        dialog_t = QtGui.QPrintDialog(self.drucker)

        if dialog_t.exec_() == QtGui.QDialog.Accepted:
            self.textView.print_(self.drucker)  #textView ist das TexteditObjekt im Ui_frmTopo
                                                #es wird ja in diese Klasse veraerbt und hat die Methode Drucken: Der Inhalt wird dann gedruckt
        del dialog_t



    def closeEvent(self,event = None):
        self.close()




