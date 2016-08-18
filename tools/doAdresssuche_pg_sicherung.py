# -*- coding: utf-8 -*-
#!/usr/bin/python


from PyQt4 import QtGui, QtCore, QtSql


from qgis.core import *
from qgis.gui import *
from gui_blattschnitte import *
from gui_adresssuche import *
from doVermessung import *
from ladefortschritt import *
#API up to 2.2
if QGis.QGIS_VERSION_INT < 20300:
    from ProjektImport import *
else:
    from ProjektImport_24 import *
import sys, re


class AdrDialogPG(QtGui.QDialog, Ui_frmAdresssuche):

    #Ein individuelles Signal als Klassenvariable definieren
    Abflug = QtCore.pyqtSignal(object)

    def __init__(self,parent,iface,speicheradressen_adressuche,pfad = None, name = None, db = None, pg_table = ''):
        QtGui.QDialog.__init__(self,parent)
        Ui_frmAdresssuche.__init__(self)

        self.iface = iface
        # Set up the user interface from Designer.
        self.setupUi(self)
        self.pfad = pfad
        self.name = name
        self.Gemeinde = ""
        self.Strasse = ""
        self.Nummer = ""
        self.Adresscode = []
        self.Rechtswert = []
        self.Hochwert = []
        self.Strasse = []
        self.Hausnummer = []
        self.MainWindow = parent
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        self.speicheradressen_adressuche = speicheradressen_adressuche
        self.suchrichtungsFlag = False
        self.buttonGroup.setExclusive(True)
        self.db = db
        self.pg_table = pg_table
        self.tablename = ''
        self.pg_flag = False

        self.abfrage = object()
        self.abfrageStrasse = object()
        self.abfrageNummer = object()




        #Abfragen instanzieren
        self.abfrage = QtSql.QSqlQuery(self.db)
        self.abfrageStrasse = QtSql.QSqlQuery(self.db)
        self.abfrageNummer = QtSql.QSqlQuery(self.db)

        self.tablename = 'vorarlberg.' + pg_table
        self.pg_flag = True
        # Fürs Listenfeld
        self.abfrage.exec_("select distinct pgem_name  from  vorarlberg.gemeinden  order by pgem_name")






        #Modelle instanzieren (Anzeige im Listenfeld)
        self.modell_adresscode = QtSql.QSqlQueryModel()
        self.modell_strasse = QtSql.QSqlQueryModel()
        self.modell_nummer = QtSql.QSqlQueryModel()
        self.modelli = QtSql.QSqlQueryModel()



        #Nach dem Startbereits die
        #Liste mit den Gemeinden füllen

        self.modelli.setQuery(self.abfrage)
        #self.modelli.setQuery("select distinct GEMEINDE  from adressen",self.db)
        self.lstGemeinde.setModel(self.modelli)

        #Nach dem Startbereits die
        #Liste mit den Strassennamen füllen
        #da diese etwas mehr sind wird das gesamte Holen
        #von der Datenbank erzwungen
        self.lstStrasse.setModel(self.modell_strasse)





        #Hauptfenster (GST Suche) positionieren
        #und zwar in die linke Ecke des QGIS Fensters
        linksoben = self.iface.mainWindow().frameGeometry().topLeft()
        self.move(linksoben)


        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        #mittelpunkt = self.findemittelpunkt()
        #self.returnGemeinde(mittelpunkt)

##        if not self.pg_flag:
##            #Infofenster für den Benutzer anschließend schließen
##            self.info.close()

        #selection Changed Signal der Listenfelder implementieren
        #das geht wie folgt
        self.SelModelG = self.lstGemeinde.selectionModel()
        QtCore.QObject.connect(self.SelModelG,QtCore.SIGNAL("currentChanged (const QModelIndex&,const QModelIndex&)"),self.currentChangedG)

        self.SelModelS = self.lstStrasse.selectionModel()
        QtCore.QObject.connect(self.SelModelS,QtCore.SIGNAL("currentChanged (const QModelIndex&,const QModelIndex&)"),self.currentChangedS)


        QtCore.QObject.connect(self.leStrasse, QtCore.SIGNAL("textEdited (const QString&)"),self.strassensuche)



        #den mittelpunkt des extent rausfinden
        #und die passende Gemeinde im ListWidget einstellen
        mittelpunkt = self.findemittelpunkt()
        self.returnGemeinde(mittelpunkt)

        self.leStrasse.setFocus()
    #Wenn auf 'im View darstellen' geklickt wird
    def accept(self):

        #Variablen neu initialisieren
        self.Adresscode = []
        self.Rechtswert = []
        self.Hochwert = []
        self.Strasselist = []
        self.Hausnummer = []
        self.maxX = 0
        self.minX = 0
        self.maxY = 0
        self.minY = 0
        durchlaufflag = 0

        #Listenvariablen (für Mehrfachauswahl) mit den Werten aus der SQL Abfrage
        #füllen und zugelich den Zoomextent bestimmen
        while self.abfrageNummer.isValid():
            if ((not self.abfrageNummer.value(0) == None) and (not self.abfrageNummer.value(1) == None) and (not self.abfrageNummer.value(2) == None) and
                (not self.abfrageNummer.value(3) == None) and (not self.abfrageNummer.value(4) == None)):

                self.Adresscode.append(self.abfrageNummer.value(0))
                self.Rechtswert.append(self.abfrageNummer.value(1))   #die Variants sind Listen mit 2 Items bei toDouble!!
                self.Hochwert.append(self.abfrageNummer.value(2))   #die Variants sind Listen mit 2 Items bei toDouble!!
                self.Strasselist.append(self.abfrageNummer.value(3))
                self.Hausnummer.append(self.abfrageNummer.value(4))

            #Extent der Adressauswahl ermitteln
            if durchlaufflag == 0:
                self.maxX = self.abfrageNummer.value(1)
                self.minX = self.abfrageNummer.value(1)
                self.maxY = self.abfrageNummer.value(2)
                self.minY = self.abfrageNummer.value(2)
            else:

                if self.abfrageNummer.value(1) > self.maxX:
                    self.maxX = self.abfrageNummer.value(1)
                elif self.abfrageNummer.value(1) < self.minX:
                    self.minX = self.abfrageNummer.value(1)

                if self.abfrageNummer.value(2) > self.maxY:
                    self.maxY = self.abfrageNummer.value(2)
                elif self.abfrageNummer.value(2) < self.minY:
                    self.minY = self.abfrageNummer.value(2)

            self.abfrageNummer.next()
            durchlaufflag = 1

        #Methode zeichnet die Adressen in das View Fenster von QGIS
        self.AdrZoomtextAnnoXY()

    #eingezeichnete Adressen löschen. Über Pointer
    #werden deren Speicheradressen aufgezeichnet und im Hauptobjekt des VogisMenü gespeichert
    #und immer mitübergeben. Dadurch gehen sie solange das Vogis Menü
    #aktiv ist nicht verloren und können immer wieder gelsöcht werden
    def adrClear(self):
        mc=self.iface.mapCanvas()
        #die Grafiken sind in einer QGraphicsItemScene
        # die man leider undokumentiert über mc.scene() bekommt!!

        if len(self.speicheradressen_adressuche) > 0:
            for items in self.speicheradressen_adressuche:
                try:
                    mc.scene().removeItem(items)
                except:
                    pass
        mc.refresh()

    #klickt man in das Listenfeld Gemeinde
    #werden die dazugehörigen Strassen aus der DB geholt und
    #in ein Listenfeld eingetragen  und in eine sql abfrage
    def lstGemeindeKlicked(self,Index):

##        if len(self.leStrasse.text()) > 0: #Eingabe über Listenfeld
##            self.Gemeinde = Index.data()
##
##        else:
        if self.suchrichtungsFlag:

            self.Gemeinde = Index.data()#.toString()

            #QtGui.QMessageBox.about(None, "Achtung", str(self.Gemeinde) + ' ' + str(self.Strasse) + ' ' + str(self.tablename ))

            #QtGui.QMessageBox.about(None, "Achtung", str(self.nummer))
            if len(self.nummer) < 1:
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "' order by hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()
            else:
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "' and hausnr = '"+ self.nummer + "' order by hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

        else:
            self.lstStrasse.reset()
            #self.Gemeinde = Index.data().toString()
            self.Gemeinde = Index.data()

            #self.Gemeinde = Index.indexes()[0].data().toString()

            self.abfrage.exec_("select distinct strasse  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' order by strasse")

            self.modell_strasse.setQuery(self.abfrage)
            self.lstStrasse.setModel(self.modell_strasse)
            self.abfrageStrasse.clear()
            self.modell_nummer.setQuery(self.abfrageStrasse)

            self.lstNummer.setModel(self.modell_nummer)


    #klickt man in das Listenfeld Strasse
    #werden die dazugehörigen Hausnummern aus der DB geholt und
    #in ein Listenfeld eingetragen und in eine sql abfrage
    def lstStrasseKlicked(self,Index, Index2 = None):
##
##        if len(self.leStrasse.text()) > 0: #Eingabe über Listenfeld
##            self.Strasse = Index.data()
##        else:
        self.Strasse = Index.data() #.toString()
        #self.Strasse = Index.indexes()[0].data().toString()
        #QtGui.QMessageBox.about(None, "Query", str(len(Index.indexes())))
        if self.suchrichtungsFlag:
            #gemeinden aktualisieren
            self.lstGemeinde.reset()
            self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + "  where strasse = '" + self.Strasse + "' order by gemeinde")

            self.modelli.setQuery(self.abfrage)

            self.lstGemeinde.setModel(self.modelli)

            if len(self.lstGemeinde.selectedIndexes()) > 0 :
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "' order by hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

            else:
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where  strasse = '"+ self.Strasse + "' order by hausnr")

                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

        else:

            if len(self.lstGemeinde.selectedIndexes()) > 0 :
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "' order by hausnr")
                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()

            else:
                self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where  strasse = '"+ self.Strasse + "' order by hausnr")

                self.modell_nummer.setQuery(self.abfrageStrasse)
                self.lstNummer.setModel(self.modell_nummer)
                self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where strasse = '"+ self.Strasse + "'")
                self.abfrageNummer.first()




    #klickt man in das Listenfeld Hausnummer
    #werden die dazugehörigen Hausnummern aus der DB geholt und
    #in eine sql abfrage eingetragen
    def lstNummerKlicked(self,Index):


        #für die Mehrfachauswahl an Adressen wird ein
        #Liste mit Indices benötigt
        NummernListe = self.lstNummer.selectedIndexes()

        sql_part = ""
        for indi in NummernListe:   #die liste durchgehen und den SQL Teil erzeugen
            if sql_part == "":
                #sql_part = "Hausnr = '" + indi.data().toString() + "'"
                sql_part = "Hausnr = '" + indi.data() + "'"
            else:
                #sql_part = sql_part + " or Hausnr = '" + indi.data().toString() + "'"
                sql_part = sql_part + " or Hausnr = '" + indi.data() + "'"

        if len(self.lstGemeinde.selectedIndexes()) > 0 :
            #QtGui.QMessageBox.about(None, "Achtung", str(self.tablename) + ' ' + str(self.Gemeinde) + ' ' + str(self.Strasse) + ' ' + str(sql_part))
            self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where gemeinde = '" + self.Gemeinde + "' and strasse = '"+ self.Strasse + "' and ( " + sql_part + ")")
        else:
            self.abfrageNummer.exec_("select adrsubcd,rechtswert,hochwert,strasse,hausnr  from  " + self.tablename + "  where  strasse = '"+ self.Strasse + "' and ( " + sql_part + ")")
        self.modell_adresscode.setQuery(self.abfrageNummer)
        self.abfrageNummer.first()
        #self.colAll.setModel(self.modell_adresscode)


    #Methode führt das eigentliche einzeichnen der Adessen
    #ins Mapfenster aus. Diese sind dan QgsTExtAnnotationItems wie
    #die "Sprechblasen" die man einzeichnen kann
    def AdrZoomtextAnnoXY(self):

        mc=self.iface.mapCanvas()

        #ist nur eine Adresse ausgewählt worden
        #(wenn der User ins Listenfeld Hausnummer klickt)
        if len(self.Adresscode) == 1:
            height2 = 50 #50m Toleranz
            width2 = 50 #50m Toleranz
            rect = QgsRectangle(self.Rechtswert[0] -width2, self.Hochwert[0] -height2, self.Rechtswert[0] +width2, self.Hochwert[0] +height2)
        #oder werden alle Adressen einer Strasse abgefragt
        #bzw. mehrer Nummern durch den User ausgwählt
        elif len(self.Adresscode) > 1:
            rect = QgsRectangle(self.minX - 50, self.minY - 50, self.maxX + 50, self.maxY + 50)
            #Maßsstab berechnen
            scaleA = mc.scale()
            hA = mc.extent().height()
            wA = mc.extent().width()

            m = 0
            if hA / rect.height() > wA / rect.width() :
                m = hA / rect.height()
            else:
                m = wA / rect.width()
            scale = scaleA / m

        else:
            return


        # Extent setzen
        mc.setExtent(rect)

        #Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,0,0', 'color_border' : '255,0,0' , 'name' : 'cross', 'size' : '4' }

        i = 0
        #schleife geht alle ausgewählten adressen
        #durch (ein oder alle der Strasse) und zeichnet sie ins Mapfernster
        while i < len(self.Adresscode):

            # QtGui.QMessageBox.about(None, "Query", self.Hausnummer[i])
            #Der Adresstext als Textdokument
            text = QtGui.QTextDocument(self)
            text.setObjectName("adressen" +  self.Strasselist[i] + self.Hausnummer[i])
            #text.setObjectName("adressen" +  self.Strasselist[i])

            # Das Fontobjekt fürs Textobjekt
            font = QtGui.QFont()
            font.setPointSize(12)
            text.setDefaultFont(font)
            text.setHtml("<font color = \"#FF0000\">" + self.Strasselist[i] + " " + self.Hausnummer[i] + "</font>")
            # text.setHtml("<font color = \"#FF0000\">" + self.Strasselist[i]  + "</font>")

            # Hilfspunkt zur Text/Kreuzchen Positionierung
            punkti = QgsPoint(self.Rechtswert[i],self.Hochwert[i])

            # Offset der Textposition
            Offset = QtCore.QPointF()
            Offset.setX(0)
            Offset.setY(0)

            # Benötigte Framgröße
            frame_groesse = text.size()


            # DAS objekt um Kreuzchen und Text zu zeichnen
            textAnno = QgsTextAnnotationItem(self.iface.mapCanvas())
            textAnno.setFrameSize(frame_groesse)   # ohne Framgröße keine Darstellung im Drucklayout
            textAnno.setMapPosition(punkti)
            textAnno.setFrameBorderWidth(0.0)
            textAnno.setOffsetFromReferencePoint(Offset)

            textAnno.setDocument(text)      #Text zuweisen
            farbe = textAnno.frameColor()   #die Framefarbe auf unsichtbar schalten
            farbe.setAlpha(0)               #sonst gibts ein kleines Darstellungsartefakt
            textAnno.setFrameColor(farbe)

            # textAnno.setMarkerSymbol geht nicht!!
            # deshalb so: wir wollen nicht den Standardknödel
            # sondern ein rotes Kreuzchen
            s = textAnno.markerSymbol() #1. das eingestellte Marker Symbol holen
            # Die neuen Properties...
            sl = QgsSymbolLayerV2Registry.instance().symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)   #in der Schleife sonst Probleme im Qgis

            s.changeSymbolLayer(0,sl)   #2. das neue Symbol zuweisen

            i = i + 1

            # die Adresse jedes Annotationobjekt wird in einen Listenvariable-Pointer
            # geschrieben. Dadurch gehen sie beim Schließen des Adresswidget nicht verloren sondern
            # bleiben dem Vogis Menü Plugin erhalten (zum späteren löschen notwendig)!!
            self.speicheradressen_adressuche.append(textAnno)

        mc.refresh()



    #Nimmt das Linedit für die Strassensuche ein Enter
    #Ereignis auf, dann wird diese Methode aufgerufen
    #Ist das feld leer, wird die Suche zurückgesetzt, ansonsten
    #wird der Text (der für die Strassensuche vom User eingegeben wurde)
    #in der Adressdatenbank gesucht
    def strassensuche(self, text = None):

        self.nummer = []
        self.suchrichtungsFlag = True   # brauchts damit ich weiß, ob ich die strassensuche benützt habe!

##        if not self.pg_flag:
##            self.info.show()
##            self.info.repaint()

        if text == None:
            text = self.leStrasse.text()
            #QtGui.QMessageBox.about(None, "Achtung", text)

        #else:
        self.nummer = re.findall(r'\d+',text)


        if  len(self.nummer) > 0:
            self.nummer = string.strip(self.nummer[0])
            position = text.index(self.nummer)
            text = string.strip(text[0:position])
        else:
            self.nummer = '' # Wenn keine Nummer eingegeben
            #QtGui.QMessageBox.about(None, "Achtung", nummer)

        #QtGui.QMessageBox.about(None, "Achtung", str(len(text)))
        # Wie auch immer, Leerzeichen vorne und hinten werden entfernt
        text = string.strip(text)

        #QtGui.QMessageBox.about(None, "Achtung", str(len(text)))



        #if self.leStrasse.text() != "": #das feld enthät einen Text! Suche wird durchgeführt
        if text != "": #das feld enthät einen Text! Suche wird durchgeführt

            ##################################
            # Listenfeld Strasse aktualisieren
            ##################################
            self.lstStrasse.reset()
            #self.abfrageStrasse.exec_("select distinct strasse  from  " + self.tablename + "  where LOWER(strasse) Like '%" + string.lower(self.leStrasse.text()) + "%'")
            self.abfrageStrasse.exec_("select distinct strasse from  " + self.tablename + "  where LOWER(strasse) Like '%" + string.lower(text) + "%'")
            self.abfrageStrasse.next()
            self.modell_strasse.setQuery(self.abfrageStrasse)

            self.lstStrasse.setModel(self.modell_strasse)
            self.lstStrasse.setModelColumn(1)


            # Erstes inder Liste markieren
            #self.lstStrasse.keyboardSearch(self.modell_strasse.record(0).field(0).value())
            self.lstStrasse.scrollToTop()
            self.lstStrasse.setSelection(QtCore.QRect(0,0,10,10),QtGui.QItemSelectionModel.SelectCurrent)

            if len(self.lstStrasse.selectedIndexes()) > 0:
                self.Strasse = self.lstStrasse.selectedIndexes()[0].data()



            #####################################
            # Listenfeld Gemeinde aktualisieren
            #####################################
            self.lstGemeinde.reset()

            if  len(self.nummer) > 0:
                #QtGui.QMessageBox.about(None, "Achtung", "select distinct gemeinde  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) = '" + string.lower(nummer) + "') order by gemeinde")
                self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) = '" + string.lower(self.nummer) + "') order by gemeinde")
            else:
                self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + "  where LOWER(strasse) Like '%" + string.lower(text) + "%' order by gemeinde")

            self.modelli.setQuery(self.abfrage)
            self.lstGemeinde.setModel(self.modelli)

            # Erstes inder Liste markieren
            #self.lstGemeinde.keyboardSearch(self.modelli.record(0).field(0).value())


            #selmodel_gemeinde = QtGui.QItemSelectionModel(self.modelli)
            #indexmodel_gemeinde = self.modelli.index(0,0)
            #selmodel_gemeinde.select(indexmodel_gemeinde,QtGui.QItemSelectionModel.SelectCurrent)
            self.lstGemeinde.scrollToTop()
            self.lstGemeinde.setSelection(QtCore.QRect(0,0,10,10),QtGui.QItemSelectionModel.SelectCurrent)
            #self.lstGemeinde.scrollTo(selmodel_gemeinde.selectedIndexes()[0])

            #selmodel_gemeinde.select(indexmodel_gemeinde,QtGui.QItemSelectionModel.Current)

            #QtGui.QMessageBox.about(None, "Achtung", str(selmodel_gemeinde.selectedIndexes()[0].data()) + ' ' )
            if len(self.lstGemeinde.selectedIndexes()) > 0:
                self.Gemeinde = self.lstGemeinde.selectedIndexes()[0].data()

            ###########################################
            # Listenfeld Strassennummern aktualisieren
            ###########################################
            self.lstNummer.reset()
            #self.abfrageStrasse.exec_("select distinct hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "' order by hausnr")
            if  len(self.nummer) > 0:
                self.abfrageNummer.exec_("select distinct hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) like '%" + string.lower(self.nummer) + "%' and LOWER(gemeinde) like '%" + string.lower(self.Gemeinde) + "%')")
                #QtGui.QMessageBox.about(None, "Achtung", "select distinct hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) like '%" + string.lower(self.nummer) + "%' and LOWER(gemeinde) like '%" + string.lower(self.Gemeinde) + "%')")
            else:
                self.abfrageNummer.exec_("select distinct hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) +  "%' and LOWER(gemeinde) like '%" + string.lower(self.Gemeinde) + "%')")
                #QtGui.QMessageBox.about(None, "Achtung", "select distinct hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) +  "%' and LOWER(gemeinde) like '%" + string.lower(self.Gemeinde) + "%')")
            #QtGui.QMessageBox.about(None, "Achtung", "select hausnr  from  " + self.tablename + "  where (LOWER(strasse) Like '%" + string.lower(text) + "%' and LOWER(hausnr) = '" + string.lower(nummer) + "')")
            self.modell_nummer.setQuery(self.abfrageNummer)
            #QtGui.QMessageBox.about(None, "Achtung", self.modell_nummer.query().executedQuery())
            #QtGui.QMessageBox.about(None, "Achtung", str(self.abfrageNummer.lastQuery()))
            self.lstNummer.setModel(self.modell_nummer)

            self.lstNummer.scrollToTop()
            self.lstNummer.setSelection(QtCore.QRect(0,0,10,10), QtGui.QItemSelectionModel.SelectCurrent)

            if len(self.lstNummer.selectedIndexes()) > 0:
                self.lstNummerKlicked(self.lstNummer.selectedIndexes()[0].data())



        else:   #das Feld ist leer, die Suche wird zurückgesetzt
            self.suchrichtungsFlag = False
            self.lstGemeinde.reset()
            self.abfrage.exec_("select distinct gemeinde  from  " + self.tablename + " ")
            self.abfrage.next()
            self.modelli.setQuery(self.abfrage)

            self.lstGemeinde.setModel(self.modelli)

            #den neuen Mittelpunkt ermitteln und die Gemeinde
            #im Listenfeld dafür auswählen
            mittelpunkt = self.findemittelpunkt()
            self.returnGemeinde(mittelpunkt)

##        if not self.pg_flag:
##            self.info.close()


    #Finde den Mittelpunkt
    #der aktuellen Kartendarstellung in Map Units
    #und gibt ihn zurück
    def findemittelpunkt(self):
        mc = self.iface.mapCanvas()
        Punkt = mc.extent().center()
        return Punkt



    #Ermittelt anhand des aktuellen Kartenmittelpunkts (Variable ergebnis)
    #im QGIS den Namen passende Gemeinde und ruft die
    #Routine zum Aktualisieren des Listenfelds auf
    #Auskommentiert ist die Ermittlung des Zoomextents
    #auf die ausgewählte Gemeinde. Wird auch aufgerufen,
    #wenn die Gemeinde mit dem roten Kreuzchen ausgewählt wird
    def returnGemeinde(self,ergebnis):




        mc=self.iface.mapCanvas()


        #Prüfen ob der Layer Gemeinde im Qgis eingebunden ist
        #Startet man das Vogis Projekt ist er automatisch dabei
        #Sonst wird abgebrochen
        yes = False
        for vorhanden in mc.layers():
            if vorhanden.name() == "Gemeinden":
                yes = True
                break

        if yes:
            gmdLayer = vorhanden
        else:
            #L = QtCore.QStringList()
            #wert = QtCore.QString("Sonntag")
            self.auswahlaenderung("Sonntag")
            return

        #damit nichts flackert
        mc.setRenderFlag(False)

        #Auswahlrechteck erzeugen. Es dient der Auswahl
        #des Features der betreffenden politischen Gemeinde
        #im Gemeindelayer in QGIS
        shift=mc.mapUnitsPerPixel()
        wahlRect = QgsRectangle(ergebnis.x(),ergebnis.y(),ergebnis.x()+ shift,ergebnis.y()+ shift)
        #Entsprechendes Feature (=Gemeinde) im Layer selektieren
        gmdLayer.select(wahlRect,False)

##        #Den Index des Feldes PGEM_NAME
##        #in der Attributtabelle des Layers finden
##        gmdProvider = gmdLayer.dataProvider()
##        gmdFelder = gmdProvider.fields()
##        #gmdFelder ist ein dictionary: index = field index, wert = QgsFeatureAttribute

        # API für QGIS 2.0
##        for (index,feldname) in gmdFelder.iteritems():
##            if ("PGEM_NAME"==str(feldname.name())):
##                self.pgem_name_index = index

##
##        #Den Index des feldes PGEM_NAME
##        #in der Attributtabelle des Layers finden
##        #brauch ich um die grafisch ausgewählte Gemeinde
##        #im Listenfeld optisch in die mitte zu holen
        Liste = gmdLayer.selectedFeatures()

##        #Auswahl wieder löschen
        gmdLayer.removeSelection()




        if  (len(Liste) > 0):

            # API für QGIS 2.0
##            wert = Liste[0].attributeMap()
##            self.auswahlaenderung( wert[self.pgem_name_index].toString())
            #self.auswahlaenderung(Liste[0].attribute('PGEM_NAME').toString())
            self.auswahlaenderung(Liste[0].attribute('PGEM_NAME'))
        else:   #WICHTIG!! ist der Extent so daß mit der Ermittlung des Mittelpunkts
                #keine Gemeinde gefunden wird, stellen wir auf Sonntag!
            #wert = QtCore.QString("Sonntag")
            wert = "Sonntag"
            self.auswahlaenderung(wert )

        mc.setRenderFlag(True)


    #Methode Aktualisiert nur das zweite Listenfeld für die Gemeinde
    def auswahlaenderung(self,SelItem = None,Nummer = None):


##
##        #Abhängig von wo aus die Methode aufgerufen wird
##        #bekommt sie unterschiedliche String Typen übergeben
##        #if isinstance(SelItem,QtCore.QString):
##        if isinstance(SelItem,str):
##            #noch was optisches. Egal ob über Cursor oder Direkt im
##            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
##            #wird automatisch in die mitte des Listenfeldes gescrollt
##            self.Gemeinde = SelItem
##            self.lstGemeinde.keyboardSearch(self.Gemeinde)
##            index = self.lstGemeinde.selectedIndexes()
##
##            self.lstGemeinde.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
##
##        else:
##            #noch was optisches. Egal ob über Cursor oder Direkt im
##            #Listenfeld ausgewählt: Die gewählte politische Gemeinde
##            #wird automatisch in die mitte des Listenfeldes gescrollt
##            #self.Gemeinde = SelItem.data(0).toString()
##            self.Gemeinde = SelItem
##            self.lstGemeinde.keyboardSearch(SelItem)
##            index = self.lstGemeinde.selectedIndexes()
##            self.lstGemeinde.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen

        self.Gemeinde = SelItem
        self.lstGemeinde.keyboardSearch(SelItem)

        index = self.lstGemeinde.selectedIndexes()
        try:
            if not index == None:
                self.lstGemeinde.scrollTo(index[0],3) #3 bedeutet in die Mitte des Listenfelds scrollen
        except:
            QtGui.QMessageBox.about(None, "Achtung", 'Fehler beim befüllen der Listenfelder'.decode('utf8'))
            pass


    def currentChangedG(self,a,b):
        #QtGui.QMessageBox.about(None, "Achtung", "Gemeinde")
        self.lstGemeindeKlicked(a)

    def currentChangedS(self,a,b):
        #QtGui.QMessageBox.about(None, "Achtung", "Strasse")
        self.lstStrasseKlicked(a)



    #klickt man auf OK wird diese Methode ausgeführt
    #Da die Layer recht heterogen geordnet sind ist das
    #setzen der Pfade hardcodiert. Die Importmethode wird
    #in der jeweiligen If clause ausgeführt
    def themenLaden(self):

        self.iface.mapCanvas().setRenderFlag(False)
##
##        if not self.pg_flag:
##            #falls es länger dauert, ein kurzes Infofenster
##            #für den Anwender
##            self.info = LadefortschrittDialog()
##            self.info.show()
##            self.info.repaint()  #sonst bleibt das Fenster leer!

        #adressen = ProjektImport(self.iface )   #das Projekt Import Objekt instanzieren
        uri = QgsDataSourceURI()
        #uri.setDatabase(self.pfad + "adressen.sqlite")
        uri.setConnection(self.db.hostName(),str(self.db.port()),self.db.databaseName(),'','')  # Keine Kennwort nötig, Single Sign On
        schema = "vorarlberg"
        table = "adressen"
        geom_column = "the_geom"


        #sämtliche Radiobuttons des Dialogfeldes sind gruppiert in ckButtons
        #und können so in einer Schleife auf ihren Zustand (gechecket) geprüft werden
        for button in self.buttonGroup.buttons():


            if button.isChecked():  #wenn gechecked wird geladen

                if   (("Landesfläche").decode('utf-8') in button.text()):

                    #adressen laden
                    #uri.setDataSource(schema, table, geom_column)
                    uri.setDataSource(schema, table, geom_column)

                    adressen = QgsVectorLayer(uri.uri(), "adressen","postgres")
                    #adressen.setProviderEncoding("utf-8")


                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")
                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( adressen )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(adressen)

                elif   ("Gemeinde" in button.text()):
                    uri.setDataSource(schema, table, geom_column, "gemeinde = '" + self.Gemeinde + "'")


                    #adressen laden
                    adressen = QgsVectorLayer(uri.uri(),"Adressen-" + self.Gemeinde,"postgres")
                    #und prüfen ob erfolgreich geladen
                    if not adressen.isValid(): #nicht erfolgreich geladen
                        QtGui.QMessageBox.about(None, "Fehler", "Adressen konnte nicht geladen werden")
                    else:   #erfolgreich geladen
                        #dem Vektorlayer das QML File zuweisen
                        #flagge[1] ist false wenn das file nich gefunden wird
                        flagge = adressen.loadNamedStyle(self.pfad + "adressen.qml")
                        if flagge[1]:
                            #Legendenansicht aktualisieren
                            self.iface.legendInterface().refreshLayerSymbology( adressen )
                        else:
                            QtGui.QMessageBox.about(None, "Fehler", "Adressen QML konnte nicht zugewiesen werden!")
                        #Zur Map Layer registry hinzufügen damit der Layer
                        #dargestellt wird
                        QgsMapLayerRegistry.instance().addMapLayer(adressen)

##        if not self.pg_flag:
##            self.info.close()

        self.iface.mapCanvas().setRenderFlag(True)

    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):
        #Nun unser Abflug Signal senden
        self.Abflug.emit(self)
        self.db= None
        self.close()
