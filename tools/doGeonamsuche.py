# -*- coding: utf-8 -*-
#!/usr/bin/python


from PyQt4 import QtGui,QtCore, QtSql

from qgis.core import *
from qgis.gui import *
from gui_geonam import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import sys
import string

class Geonam(QtGui.QDialog, Ui_frmGeonam):
    def __init__(self,iface,pfad = None, name = None, geonamgrafik = None):
        QtGui.QDialog.__init__(self)
        Ui_frmGeonam.__init__(self)

        self.iface = iface
        self.setupUi(self) #User Interface für Hauptfenster GST Suche initialisieren
        self.pfad = pfad
        self.name = name
        self.geonamgrafik = geonamgrafik    #enthält die GrafiksItemGroup mit allen Grafiken
                                            #vom User eingefügten Geonam Adresse.
                                            #Wird beim Schließen des Objektes an VogisMain zurückgegeben bzw.
                                            #beim erzeugen des Objektes dem Constructor übergeben (sonst ists halt None)




        #Referenz auf die Datenquelle
        #Direkt über SQLITE
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
        self.db.setDatabaseName(self.pfad + self.name + ".sqlite");
        self.db.setConnectOptions('QSQLITE_OPEN_READONLY')

        #fehlverbindung abfangen
        if  not (self.db.open()):
            QtGui.QMessageBox.about(None, "Achtung", ("Öffnen ÖK Geonam gescheitert").decode("utf-8"))
            return

        #Abfragen instanzieren
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrage.exec_("SELECT  BEGRIFF  FROM geonam order by BEGRIFF")

        #Modelle instanzieren (Anzeige im Listenfeld)
        self.modelli = QtSql.QSqlQueryModel()
        self.modelli.setQuery(self.abfrage)

        #damit werden alle Datensätze die der Query genügen
        #von der Datenbank geholt!
        while (self.modelli.canFetchMore()):
            self.modelli.fetchMore()
        #Widget füllen
        self.lstGeonam.setModel(self.modelli)


        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)



    #Wird ausgeführt nachdem in der GUI
    #der Button "Im View anzeigen" gedrückt wird
    def accept(self):
        self.geonamZoom()

    #Geonam Grafiken aus dem
    #Anzeigefenster löschen: Sind bereits welche vorhanden
    #werden diese durch das Initialisieren vom VogisMain
    #dem Objekt übergeben
    def geonamClear(self):

        mc=self.iface.mapCanvas()

        #Das GraphicsItemGroup Objekt mit den Geonamgrafiken
        #zerstören und die Objektvariable auf None setzen!
        mc.scene().removeItem(self.geonamgrafik)
        self.geonamgrafik = None


        #Anzeige refreshen
        mc.refresh()


    #Diese Methode ist der Slot, wenn in das ListView mit den Geonamen
    #geklickt wird, wird also jedes mal dann ausgeführt
    def AuswahlAktiviert(self,Index):
        #der Inhalt auf den geklickt wurde
        self.Auswahl = Index.data()#.toString()

        #neue abfrage generieren
        self.abfrage.exec_("SELECT *  FROM geonam where Begriff = '" + self.Auswahl + "'")#.trimmed() + "'")
        self.modell_geonam = QtSql.QSqlQueryModel()
        self.modell_geonam.setQuery(self.abfrage)

        #die gewünschten Informationen aus der Geonam Attributtabelle
        #rausholen: Die Koordinaten des Geonam und den eigentlichen
        #Namend er angezeigt wird
        self.Rechtswert = float(self.modell_geonam.record(0).value("X_coord"))
        self.Hochwert = float(self.modell_geonam.record(0).value("Y_coord"))
        self.Text = self.modell_geonam.record(0).value("Name")

        #Den Anzeigeknopf aktivieren
        self.btnAnzeigen.setDisabled(False)


    #Wird auf den button anzeigen geklickt wird diese Methode als
    #Slot ausgeführt!
    def geonamZoom(self):
        #wieder nur lokale Variable....
        mc=self.iface.mapCanvas()

        #Ist die GraphiksItemGroup auf None gesetzt (durch das aktivieren der
        #löschroutine geonamclear oder durch erstmaliges Verwende vom VogisMenü aus
        #muß sie (wieder) erzeugt werden
        if self.geonamgrafik is None:
            self.geonamgrafik = QtGui.QGraphicsItemGroup(None,mc.scene())


        height2 = 50 #50m Toleranz
        width2 = 50 #50m Toleranz
        #rect = QgsRectangle(self.Rechtswert[0] -width2, self.Hochwert[0] -height2, self.Rechtswert[0] +width2, self.Hochwert[0] +height2)
        rect = QgsRectangle(self.Rechtswert -width2, self.Hochwert -height2, self.Rechtswert +width2, self.Hochwert +height2)


        # dann den extent setzen
        mc.setExtent(rect)
        #und auf den Maßstab 3000 reinzoomen
        #mc.zoomScale(scale)

        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,0,0', 'color_border' : '255,0,0' , 'name' : 'cross', 'size' : '4' }

        #Ein textgrafikobjekt für die Textdarstellung erzeugen
        text = QtGui.QTextDocument(self)

        #Das Fontobjekt fürs Textobjekt
        font = QtGui.QFont()
        font.setPointSize(12)
        text.setDefaultFont(font)
        text.setHtml("<font color = \"#FF0000\">" + self.Text + "</font>")

         # Benötigte Framgröße
        frame_groesse = text.size()


        #Hilfspunkt zur Text/Kreuzchen Positionierung
        #punkti = QgsPoint(self.Rechtswert[0],self.Hochwert[0])
        punkti = QgsPoint(self.Rechtswert,self.Hochwert)

        #Offset der Textposition
        Offset = QtCore.QPointF()
        Offset.setX(0)
        Offset.setY(0)

         #DAS objekt um Kreuzchen und Text zu zeichnen
        textAnno = QgsTextAnnotationItem(self.iface.mapCanvas())
        textAnno.setFrameSize(frame_groesse)   # ohne Framgröße keine Darstellung im Drucklayout
        textAnno.setMapPosition(punkti)
        textAnno.setFrameBorderWidth(0.0)
        textAnno.setOffsetFromReferencePoint(Offset)

        textAnno.setDocument(text)  #Text zuweisen
        farbe = textAnno.frameColor()   #die Framefarbe auf unsichtbar schalten
        farbe.setAlpha(0)               #sonst gibts ein kleines Darstellungsartefakt
        textAnno.setFrameColor(farbe)

        #textAnno.setMarkerSymbol geht nicht!!
        #deshalb so: wir wollen nicht den Standardknödel
        #sondern ein rotes Kreuzchen
        s = textAnno.markerSymbol() #1. das eingestellte Marker Symbol holen
        #Die neuen Properties...
        sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)   #in der Schleife sonst Probleme im Qgis

        s.changeSymbolLayer(0,sl)   #2. das neue Symbol zuweisen
        self.geonamgrafik.addToGroup(textAnno)  #WICHTIG: zur QGraphicsItemGroup
                                                #damit es auch beim löschen in dieser ganz
                                                #klar zugeordnet ist


        #anzeige refreshen
        mc.refresh()


    #Diese Methode ist der Slot der jedesmal aufgerufen wird,
    #wenn im Linedit eigabefeld irgendwas eingegeben wird. Mit dem jeweiligen Text
    #wird jedesmal wenn was getippt wird in der Datenbank nach Treffern gesucht
    def imlistenfeldsuchen(self):

        #Abfrage mit Textinhalt im Lineditfeld machen
        self.abfrage.exec_("SELECT  BEGRIFF  FROM geonam where BEGRIFF LIKE '%" + self.linSuche.text() + "%' order by BEGRIFF")

        #und das dazugehörige Modell erzeugen
        #das dann dem ListView hinterlegt wird
        self.modelli = QtSql.QSqlQueryModel()
        self.modelli.setQuery(self.abfrage)

        #damit werden alle Datensätze die der Query genügen
        #von der Datenbank geholt! Sonst kommen halt nur ein paar
        #und bei jeder Änderung (Scrollen) im Listenfeld weitere nach. Das wollen wir aber nicht so
        while (self.modelli.canFetchMore()):
            self.modelli.fetchMore()

        #Dem Listview zur Darstellung das Modell hinterlegen
        self.lstGeonam.setModel(self.modelli)

        #Den Schaltknopf im View anzeigen deaktivieren
        self.btnAnzeigen.setDisabled(True)


    #Die Geonamsuche Verlassen
    def abbrechen(self):
        self.close()

    #Hier nochmal ganz was wichtigs: Diese Methode ist ein Slot der
    #aufgerufen wird, wenn die GUI der Geonamsuche geschlossen wird (und mit ihm alle Kindobjekte)
    #damit wir aber auch später noch die eventuell eingefügten Geonam Grafikobjekte identifizieren
    #können und dadurch gesondert löschen, werden diese in der QGraphicsItemGroup zusammengefaßt
    #und hier kurz vor dem Ende an VogisMain zurückgegeben!! VogisMain behält das und gibt beim
    #nächsten Aufruf der Geonamsuche diese wieder mit. Dort können dann weitere hinzugefügt werden oder alle gelöscht
    #würde man dies nicht so machen kann man immer nur alle Grafikobjekte löschen, und das könnten
    #den User ärgern...
    def grafikreturn(self):
        return self.geonamgrafik

