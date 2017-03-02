# -*- coding: utf-8 -*-



# Die Kernbibliotheken für
# Qgis und PyQT importieren
# (Gegebenenfalls läßt sich diese Auswahl
# noch verfeinern)
from PyQt4 import QtCore, QtGui, QtXml, QtSql
from qgis.core import *
from ctypes import *
from fortschrittbalken import *
from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich
#from qgis.core import *
#from LayerDialog import *

import os.path
import string,copy, re, getpass
from osgeo import ogr



# Set up current path, so that we know where to look for mudules
currentPath = os.path.dirname(__file__)
#sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))

#from doBlattschnitte import *



class ProjektImport(QtCore.QObject):    # Die Vererbung von QtCore.Qobject benötigen
    def __init__(self,iface):           # wir für den Aufruf self.sender() in der Methode
        QtCore.QObject.__init__(self)   # projectimport die als Slot agiert. Dadurch weiß die Slotmethode
                                        # von wo das Signal kommt!
        #Referenz auf das Qgis Interface übergeben
        #Wir müssen ja auf die aktuelle
        #Qgis Instanz zugreifen können
        self.iface = iface
        self.gruppe_vorhanden = False
        self.Kindi = None
        self.einf_index = QtCore.QModelIndex()
        self.paarliste = []
        self.joinliste = []



    def importieren(self, pfad = None, liste = None, ergaenzungsname = None, anzeigename_ergaenzen = False, nach_unten = False, force_gruppenname = None, force_scale = None):


        self.iface.layerTreeView().setCurrentLayer(None)    # None entspricht einem Null Pointer -> Auswahl wird entfernt -> nicht ausgewählt

        # Wird in der Regel verwendet wenn
        # Gemeindespezifische Daten geladen werden
        # zwecks Übersichtlichkeit
        self.anzeigename_aendern = anzeigename_ergaenzen
        self.gruppen_erg_name = ergaenzungsname     # oberste Gruppe wird mit diesem Namen ergänzt



        if pfad == "":
            return


        # Das Qgis Projektfile ist ein XML und wird
        # hier eingelesen
        try:
            #pfad = 'd:/delme.qgs'
            xml = file(pfad).read()
            d = QtXml.QDomDocument()
            d.setContent(xml)
        except IOError:
            QtGui.QMessageBox.about(None, "Fehler", "QGIS Projektdatei " + pfad + " nicht gefunden!")
            return



        # Die gewünschten Tagelemente aus dem XML herauslesen
        self.maps = d.elementsByTagName("maplayer")
        self.legends = d.elementsByTagName("legendlayer")
        self.gruppen = d.elementsByTagName("legendgroup")


        self.lyr = None
        self.joinlayerid = None


        # Legendeninterface instanzieren.
        leginterface = self.iface.legendInterface()



        #Zuerst den aktuellen Pfad auf dem
        #Qgis steht auslesen (kann z.B. ein lokaler Pfad sein
        #von dem ein Projekt geladen wird
        CurrentPath = QgsProject.instance().fileName()

        #Dann auf den jeweiligen Pfad setzen, von dem geladen wird. Sonst kann kein Projekt
        #mit absoluten Pfaden abgespeichert werden (für Layer die mit dem
        #VogisMenü geladen werden)
        QgsProject.instance().setFileName(pfad)





        #falls es länger dauert, ein kurzes Infofenster
        #für den Anwender
        self.info = ProgressbarDialog()
        self.info.show()
        self.info.repaint()  #sonst bleibt das Fenster leer!
        self.info.progressBar.setRange(0,self.maps.length())
        #Schleife geht alle Layer die in der Legende aufscheinen durch. Hier
        #ist nämlich die reihenfolge festgelegt, wie sie in Qgis dargestellt werden
        #Diese Schleife brauch ich nur für die richtige Reihenfolge
        #der importierten Layer in Qgis

        zaehler = 0 # der Zähler für die Anzahl der geladenen Layer
        #for j in range(self.legends.length(),-1,-1):
        for j in range(self.legends.length()):

            #Schleife geht alle Layer die in der maplayer tags aufscheinen durch
            #dort ist nämlich die wirkliche Information für die Darstellung im
            #Qgis. Also wird zuerst der Layer per ID in der Obigen
            #Schleife ausgewählt und dann in dieser Schlefe im maplayertag
            #identifiziert
            #self.lyr=None

            for i in range(self.maps.length()):

                self.info.progressBar.setValue(j)
                self.info.raise_()  # nach oben

                #prüfen ob der jeweilige layer nicht schon geladen ist. um das zu tun
                #müssen wir im vogis projektimport die identifikation über
                #die layerid tag machen. berücksichtigt werden muß auch
                #ob die layerid durch den ergaenzungsnamen erweitert wurde!!
                quelli = self.maps.item(i).namedItem("id").firstChild().toText().data()
                laden = True
                lyr_tmp = None
                for lyr_tmp in leginterface.layers(): #alle bereits geladenen Layer durchgehen
                    if (ergaenzungsname == None) and (lyr_tmp.id()  == quelli):  #Treffer: der Layer ist schon geladen
                        laden = False
                    if (ergaenzungsname != None) and (lyr_tmp.id()  == quelli + ergaenzungsname): #Treffer: der Layer ist schon geladen
                        laden = False




                #Die Layerid ist in den legend tags und maplayer tags gleich
                #so kann ein layer genau identifiziert werden. ist laden zudem True
                #gehts also weiter
                if (self.maps.item(i).namedItem("id").firstChild().toText().data() == self.legends.item(j).namedItem("filegroup").namedItem("legendlayerfile").attributes().namedItem("layerid").nodeValue()) and laden:


            #ACHTUNG: Wieder aktivieren!!!!!!!!!!

                    # wenn nur ein Teil der Layer eines Projekts geladen werden sollen. Die Liste enthält die
                    # Namen dieser Layer
                    if liste  <> None:

                        brake_val = True
                        for nd in range(len(liste)):

                            if liste[nd] == self.legends.item(j).attributes().namedItem("name").nodeValue():
                                brake_val = False
                                break

                        if brake_val:
                            continue    # Nächster Layer, ist nicht auf der Liste



                    # prüfen, ob der jeweilige Layer eine oder mehrere Jointabelle(n) verwendet
                    self.joinlayerid = ''
                    for sj in range(self.maps.item(i).namedItem("vectorjoins").childNodes().length()):
                        # leider muss ich dann nochmals alles durchgehen....
                        for lj in range(self.maps.length()):
                            if (self.maps.item(lj).namedItem("id").firstChild().toText().data() == self.maps.item(i).namedItem("vectorjoins").childNodes().item(sj).attributes().namedItem('joinLayerId').nodeValue()):
                                self.joinlayerid = self.maps.item(i).namedItem("vectorjoins").childNodes().item(sj).attributes().namedItem('joinLayerId').nodeValue()



                    #ACHTUNG: unbedingt den nodeValue der ID ändern wenn Gemeindeweise
                    #geladen wird (DKM) Da in den Qgis Projekten der Gemeinden die jeweilig ID des Layers
                    #der Einfachheit halber ident ist, würde so qgis den Layer nicht importieren!!!
                    #So wie der Layername in der Darstellung geändert wird wird auch die ID des Nodes VOR
                    #dem Laden geändert, damit Qgis das dann so übernimmt!!
                    noddi = self.maps.item(i).namedItem("id")
                    if ergaenzungsname != None:
                            noddi.firstChild().setNodeValue(noddi.firstChild().nodeValue() + ergaenzungsname)



                    #Abhängig von der vogisini wird das Encoding
                    #aus der Projektdatei genommen oder CPG datei oder
                    #wird auf System gesetzt
                    #ist self.vogisEncoding == project dann werden die Einstellungen des Projekt verwendet

                    base_name = os.path.dirname(pfad) + '/' + os.path.basename(self.maps.item(i).namedItem("datasource").firstChild().nodeValue())

                    # Achtung, zwischen absolutem und relativem Pfad unterscheiden
                    if len(os.path.dirname(self.maps.item(i).namedItem("datasource").firstChild().nodeValue())) < 2: # relativer Pfad im QGIS Projekt!
                        base_name = os.path.dirname(pfad) + '/' + os.path.basename(self.maps.item(i).namedItem("datasource").firstChild().nodeValue())
                    else:    # absoluter Pfad im QGIS Projekt!
                        base_name = self.maps.item(i).namedItem("datasource").firstChild().nodeValue()

                    if vogisEncoding_global[0] == 'menue':  # entweder CPG datei oder System setzen

                        try:   # gibts ein cpg datei
                            datei = open(os.path.splitext(base_name)[0] + '.cpg','r')
                            codierung_string = datei.read()
                            datei.close()
                            self.maps.item(i).namedItem("provider").attributes().namedItem('encoding').setNodeValue(codierung_string)
                            #QtGui.QMessageBox.about(None, "ERFOLG", os.path.splitext(base_name)[0] + '.cpg')
                        except IOError: # Es wird der Wert System zugewiesen
                            self.maps.item(i).namedItem("provider").attributes().namedItem('encoding').setNodeValue('System')
                            #QtGui.QMessageBox.about(None, "IOERROR", os.path.splitext(base_name)[0] + '.cpg')





                    # unbedingt ALLES DESELEKTIEREN, sonst Probleme mit der Reihenfolge
                    self.iface.layerTreeView().setCurrentLayer(None)    # None entspricht einem Null Pointer -> Auswahl wird entfernt -> nicht ausgewählt

                    nv_ds = ''
                    nv_provider = ''
                    nv_encoding = ''


                    #############################################################################
                    # Das Umschalten der Vektordaten auf die Geodatenbank - unter Bedingungen
                    # es darf kein Layer aus einer Geodatenbank hier verwurschtelt werden
                    #############################################################################
                    if self.maps.item(i).attributes().namedItem('type').nodeValue() == 'vector' and vogisDb_global[0] != 'filesystem geodaten' and self.maps.item(i).namedItem("datasource").firstChild().nodeValue().find('host') < 0:

                        tablename = self.maps.item(i).namedItem("datasource").firstChild().nodeValue()


                        sql = ''
                        depp = ''
                        rc=[]
                        db_ogr = ''

                        # prüfen ob der layer eine shape datenquelle ist
                        # und ob ein subset definiert ist
                        if tablename.find('.shp') > 0 and (tablename.lower().find('subset') > 0 or tablename.lower().find('SUBSET') > 0 or tablename.lower().find('Subset') > 0):


                            rc = textfilter_subset(self.maps.item(i).namedItem("datasource").firstChild().nodeValue())
                            tablename = rc[0]
                            sql = rc[1]
                            db_ogr = rc[0]
                        else:
                            tablename = os.path.basename(self.maps.item(i).namedItem("datasource").firstChild().nodeValue()).split('.shp')[0]
                            db_ogr = tablename

                        if ergaenzungsname != None:
                            tablename = string.lower('\"' + ergaenzungsname + '\".\"' + tablename + '\"')
                        else:
                            tablename = string.lower('\"vorarlberg".\"' + tablename + '\"')

                        # Sonderzeichen berücksichtigen!
                        tablename = tablename.replace(('ä').decode('utf8'),'ae')
                        tablename = tablename.replace(('Ä').decode('utf8'),'Ae')
                        tablename = tablename.replace(('ö').decode('utf8'),'oe')
                        tablename = tablename.replace(('Ö').decode('utf8'),'Oe')
                        tablename = tablename.replace(('ü').decode('utf8'),'ue')
                        tablename = tablename.replace(('Ü').decode('utf8'),'Ue')
                        tablename = tablename.replace(('ß').decode('utf8'),'ss')
                        tablename = tablename.replace('. ','_')

                        ################################################
                        # Geometriespalte bestimmen -- geht nur mit OGR
                        param_list = string.split(vogisDb_global[0])

                        host = ''
                        dbname=''
                        port=''
                        for param in param_list:

                            if string.find(param,'dbname') >= 0:
                                dbname = string.replace(param,'dbname=','')
                            elif string.find(param,'host=') >= 0:
                                host = string.replace(param,'host=','')
                            elif string.find(param,'port=') >= 0:
                                port = string.replace(param,'port=','')
                        #QtGui.QMessageBox.about(None, "Layername", str(db_ogr))
                        try:
                            outputdb = ogr.Open('pg: host=' + host  + ' dbname=' + dbname + ' schemas=vorarlberg' + ' port=' + port)
                            geom_column = outputdb.GetLayerByName(str(db_ogr)).GetGeometryColumn()
                        except:
                            geom_column = 'the_geom'

                        ##################################################



                        if self.maps.item(i).namedItem("datasource").firstChild().nodeValue().find('ogc_fid') > 0:
                            #dbpath = string.lower(vogisDb_global[0] + ' sslmode=disable table=' +  tablename +  ' (the_geom) sql') + sql
                            dbpath = string.lower(vogisDb_global[0] + ' sslmode=disable table=' +  tablename +  ' (' + geom_column + ') sql') + sql
                            #QtGui.QMessageBox.about(None, "Achtung", str('gefunden'))
                        else:
                            #dbpath = string.lower(vogisDb_global[0] + ' sslmode=disable key=ogc_fid table=' +  tablename +  ' (the_geom) sql') + sql
                            dbpath = string.lower(vogisDb_global[0] + ' sslmode=disable key=ogc_fid table=' +  tablename +  ' (' + geom_column + ') sql') + sql
                            #QtGui.QMessageBox.about(None, "Achtung", str('nicht gefunden'))

                        nv_ds = self.maps.item(i).namedItem("datasource").firstChild().nodeValue()
                        nv_provider = self.maps.item(i).namedItem("provider").firstChild().nodeValue()
                        nv_encoding = self.maps.item(i).namedItem("provider").attributes().namedItem('encoding').nodeValue()

                        self.maps.item(i).namedItem("datasource").firstChild().setNodeValue(dbpath)
                        self.maps.item(i).namedItem("provider").firstChild().setNodeValue('postgres')
                        self.maps.item(i).namedItem("provider").attributes().namedItem('encoding').setNodeValue('UTF-8')



##                        ##########################################
##                        # testen, ob die DB geöffnet werden kann
##                        ###########################################
##                        param_list = string.split(dbpath)
##
##                        host = ''
##                        dbname=''
##                        port=''
##                        #QtGui.QMessageBox.about(None, "Achtung", str(param_list))
##                        for param in param_list:
##
##                            if string.find(param,'dbname') >= 0:
##                                dbname = string.replace(param,'dbname=','')
##                            elif string.find(param,'host=') >= 0:
##                                host = string.replace(param,'host=','')
##                            elif string.find(param,'port=') >= 0:
##                                port = string.replace(param,'port=','')
##
##                        # Username falls benötigt
##                        #username = getpass.getuser().lower()
##
##                        # Wir verwenden die Windows Domänen Authentifizierung. Keine User notwendig
##                        db = QtSql.QSqlDatabase.addDatabase("QPSQL","DbTest");  # Der Name macht ie Verbindung individuell - sonst ist eine Default Verbindung
##                        db.setHostName(host)
##                        db.setPort(int(port))
##                        db.setDatabaseName(dbname)
##
##                        ok = db.open()    #Gibt True zurück wenn die Datenbank offen ist
##
##                        if not ok:
##                            QtGui.QMessageBox.about(None, "Fehler", 'Keine Verbindung zur Geodatenbank')
##                            return  #Zurück


                        #############################################
                        # Db Verbindungstest Ende
                        ##############################################

##                        ##################################################
##                        # DomNode zu Testzwecken als XML
##                        # Datei rausschreiben
##                        strinug = QtCore.QByteArray()
##                        raus = QtCore.QTextStream(strinug)
##                        self.maps.item(i).save(raus,1)
##                        file2 = open("D:/vogisini.xml","w+")
##                        file2.write(str(strinug))
##                        file2.close()
##                        #################################################


                    ######################################################
                    # Umschalten auf Geodatenbank Ende
                    ######################################################


                    # Layer  einlesen!
                    if not QgsProject.instance().read(self.maps.item(i)) and vogisDb_global[0] == 'filesystem geodaten': #hier wird der Layer geladen und gemäß den Eintragungen
                                                                                                                #der DomNode auch gerendert und dargestellt

                        QtGui.QMessageBox.about(None, "Achtung", "Layer " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " nicht gefunden!")
                        continue
                    elif not QgsProject.instance().read(self.maps.item(i)) and vogisDb_global[0] != 'filesystem geodaten':   # Probieren auf Filesystem umzuschalten
                        QtGui.QMessageBox.about(None, "Achtung", "Layer - " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " - in der Datenbank nicht gefunden - es wird aufs Filesystem umgeschaltet")
                        self.maps.item(i).namedItem("datasource").firstChild().setNodeValue(nv_ds)
                        self.maps.item(i).namedItem("provider").firstChild().setNodeValue(nv_provider)
                        self.maps.item(i).namedItem("provider").attributes().namedItem(nv_encoding)

                        if not  QgsProject.instance().read(self.maps.item(i)): #Trotzdem nicht gefunden, wir geben auf
                            QtGui.QMessageBox.about(None, "Achtung", "Layer " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " nicht gefunden!")
                            continue




                   # den Anzeigenamen im Qgis ebenfalls ändern
                   # dazu zuerst den richtigen Layer anhand der Layerid auswählen
                    #leginterface = self.iface.legendInterface()
                    for lyr_tmp in leginterface.layers():
                        if lyr_tmp.id() == noddi.firstChild().nodeValue():
                            self.lyr = lyr_tmp
                            if force_scale != None:
                                self.lyr.setMaximumScale(25000)
                                self.lyr.setScaleBasedVisibility(True)


                    #Abhängig von der vogisini wird das KBS
                    #aus der Projektdatei genommen oder aus dem *.prj File
                    if vogisKBS_global[0] == 'menue':
                        #Koordinatenbezugssystem aus dem prj file holen, wenn vorhanden,
                        #und von dort zuweisen (die Projekteinstellung überschreiben)
                        try:
                            datei = open(os.path.splitext(self.lyr.source())[0] + '.prj','r')
                            bezugssystem_string = datei.read()
                            #falls kein sauberer EPSG String, machen wir eine Zuweisung für unser 31254
                            if (re.search('MGI\D+Austria\D+GK\D+West',bezugssystem_string, re.I)) != None:  #Arcgis macht keinen sauberen EPSG String
                                bezugssystem_crs = QgsCoordinateReferenceSystem()
                                bezugssystem_crs.createFromSrid(31254)
                            else:
                                bezugssystem_crs = QgsCoordinateReferenceSystem(bezugssystem_string)

                            datei.close()

                            self.lyr.setCrs(bezugssystem_crs)
                        except IOError:
                            #QtGui.QMessageBox.about(None, "Fehler", "QGIS KBS Datei nicht gefunden!")
                            pass


                    #dann in der Applikation registrieren
                    QgsMapLayerRegistry.instance().addMapLayer(self.lyr)


                    # gejointe Tabellen brauchen eine Spezialbehandlung: Joininfo wird
                    # ausgelesen, dann der join gelöscht und erst wenn alles geladen wurde
                    # wieder neu erstellt. Sonst kann es Probleme geben! unterstütz
                    # werden beleibig viele layer mit beliebig vielen joins
                    # es handelt sich um einen layer mir midestens einem eingetragenen join
                    single_lyr_join = lyr_join()    # eigenes struktur objekt instanzieren
                    if not self.joinlayerid == '':  # checken ob für den layer mindestens ein join eingetragen ist

                        single_lyr_join.joinlayer = self.lyr
                        single_lyr_join.joininfo = self.lyr.vectorJoins()
                        self.joinliste.append(single_lyr_join)  # eine liste mit joinlayern und deren joininfo führen

                        for rem_join in self.lyr.vectorJoins(): # für den joinlayer die joins entfernen - es können merhere sein
                            kasperle = rem_join.joinLayerId
                            self.lyr.removeJoin(str(rem_join.joinLayerId))


                    #Und nun noch den Layernamen für die Darstellung
                    #im Qgis ergänzen. Siehe oben, bei gemeindeweisem Laden
                    if (ergaenzungsname != None) and (self.lyr != None) and self.anzeigename_aendern: # noch ein boolean wegen der wasserwirtschaft!!
                           if not (self.lyr.name().find(ergaenzungsname) > -1):    # ACHTUNG: Sonst wird bei wiederholtem klicken der Name nochmal rangehängt
                                    if self.lyr.name().find("(a)") > -1:
                                        aktname =  string.strip((self.lyr.name().rstrip("(a)"))) + "-" + ergaenzungsname + " (a)"
                                        self.lyr.setLayerName(aktname)
                                    else:
                                        aktname =   string.strip(self.lyr.name())+ "-" + ergaenzungsname
                                        self.lyr.setLayerName(aktname)



                    # abschließend schauen ob der aktiviert ist
                    if (self.legends.item(j).attributes().namedItem("checked").nodeValue() == "Qt::Unchecked") and not (self.lyr is None):
                        leginterface.setLayerVisible(self.lyr,False)



                    index = QgsProject.instance().layerTreeRoot()
                    zwetsch =QgsProject.instance().layerTreeRoot().findLayer(self.lyr.id())

                    dummy = zwetsch.clone()


                    # Die Layer die später geladen werden müssen
                    # auch weiter unte in der Legende sein Reihenfolge)
                    # das wird mit der Variable zaehler gesteuert
                     # QGIS höher 2.6
                    index_ins = index_zuweisen(self.legends.item(j).attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode())


                    index.insertChildNode(-1,dummy)


                    zaehler = zaehler + 1


                    zwetsch.parent().removeChildNode(zwetsch)

                    # sonst gibts probleme in der Reihenfolge
                    # wenn gruppen und layer im top level vermischt
                    if not (self.legends.item(j).parentNode().nodeName() == "legendgroup") and (force_gruppenname is None):
                        zwetsch =QgsProject.instance().layerTreeRoot().findLayer(self.lyr.id())
                        dummy = zwetsch.clone()
                        index.insertChildNode(index_ins,dummy)
                        zwetsch.parent().removeChildNode(zwetsch)
                        #QgsProject.instance().layerTreeRoot().removeChildNode(zwetsch)




                    #abschließend schauen ob der Layer aufgeklappt ist
                    #und das flag setzen
                    #ex_l = True
                    if (self.legends.item(j).attributes().namedItem("open").nodeValue() == "false") and not (self.lyr is None):
                        dummy.setExpanded(False)
                        #QtGui.QMessageBox.about(None, "Achtung", "false")
                        #ex_l = False
                    elif (self.legends.item(j).attributes().namedItem("open").nodeValue() == "true") and not (self.lyr is None):
                        dummy.setExpanded(True)
                        #QtGui.QMessageBox.about(None, "Achtung", "true")
                        #ex_l = True



                    # hier könnte abgebrochen werden, wenn die layer einfach
                    # nur reingeladen werden OHNE in Gruppenlyer abgelegt zu werden
                    #continue


                    #######################################################
                    # hier beginnt der Programmteil der die Gruppenlayer
                    # behandelt - entweder wenn im Projektfile definiert
                    # oder einfach wenn es im Menü
                    # erwünscht wird
                    #######################################################
                    if (self.legends.item(j).parentNode().nodeName() == "legendgroup") or not (force_gruppenname is None):



                        self.gruppenliste = leginterface.groups()    #eine Liste mit allen self.gruppen die bereits in der QGIS Legende enthalten sind
                        self.gruppe_vorhanden = False

                        #ACHTUNG: Layername und direkt übergeordneter Gruppenname
                        #müssen sich unterscheiden, sonst kommts zu einem Fehler. Sollts
                        #dennoch mal vorkommen, wird es hier abgefangen
                        if self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue() == self.legends.item(j).attributes().namedItem("name").nodeValue():
                            aktname =  self.lyr.name()
                            self.lyr.setLayerName(aktname+"_")

                        #prüfen ob die Gruppe schon angelegt ist
                        for einzelgruppe in self.gruppenliste:
                            if einzelgruppe == self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue(): #Name der Gruppe aus dem QGS Projektfile
                                self.gruppe_vorhanden = True

                            elif einzelgruppe == force_gruppenname: #Name ist übergeben worden
                                self.gruppe_vorhanden = True




                        #########################################################
                        # Gruppenlayer aus Projektdatei
                        #########################################################
                        if self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().nodeName() == "legendgroup":



                            kind = self.legends.item(j).parentNode()
                            gruppen_hierarchie = pos_gruppe()
                            gruppen_liste = []
                            while  (kind.nodeName() == "legendgroup"):
                                gruppen_hierarchie.name = kind.attributes().namedItem("name").nodeValue()       #der name der dem layer unmittelbar übergeordnete Gruppe: Ebene
                                gruppen_hierarchie.index  = index_zuweisen(kind.attributes().namedItem("name").nodeValue(),kind.parentNode())    # Index der Darstellungsreihenfolge der Gruppe in ihrer Hierarchie
                                gruppen_hierarchie.ex = kind.attributes().namedItem("open").nodeValue()
                                gruppen_hierarchie.ch = kind.attributes().namedItem("checked").nodeValue()
                                gruppen_liste.append(copy.deepcopy(gruppen_hierarchie)) # ACHTUNG: Referenz!!
                                kind = kind.parentNode()


                            #grp enthält das qtreewidgetitem Objekt der Gruppe!, in die der geladene
                            #Layer verschoben werden soll!
                            grp  = sublayer(QgsProject.instance().layerTreeRoot(),leginterface,gruppen_liste, self.gruppen_erg_name, nach_unten)[0] #sollten es mehrere sein, immer nur die erste nehmen - sie Erklärung beim Sub selbst

                            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(self.lyr.id())

                            dummy = zwtsch.clone()


                            index_layer  = index_zuweisen(self.legends.item(j).attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode())

                            #QtGui.QMessageBox.about(None, "LayeriD", str(dummy.layerId()))
                            grp.insertChildNode(index_layer,dummy)


                            zwtsch.parent().removeChildNode(zwtsch) # zwilling entfernen!

                            if not (isinstance(grp,QgsLayerTreeGroup)) or grp is None:

                                QtGui.QMessageBox.about(None, "ACHTUNG","Anlegen der Gruppe gescheitert")
                                break


                        ##########################################################
                        # hier Endet der Teil der Gruppenlayer aus Projektdatei!!
                        #########################################################



                        letzterplatz = False #Flagvariable ermittelt ob die Gruppe ganz nach unten gehört






                        #die gruppe in die der layer eingebettet ist kommt nicht aus
                        #einem projekt, sondern wird erzwungen. hier gibts allerdings
                        #nur eine ebene (was das ganze einfacher macht)
                        if (not force_gruppenname is None):

                            # gruppe anlegen
                            gruppen_hierarchie = pos_gruppe()
                            gruppen_hierarchie.name = force_gruppenname
                            grp = sublayer(QgsProject.instance().layerTreeRoot(),leginterface,[gruppen_hierarchie])[0]

                            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(self.lyr.id()) #der geladene layer
                            dummy = zwtsch.clone()

                            # QGIS höher 2.6
                            if QGis.QGIS_VERSION_INT > 20600:

                                # wiviele layer sind in der gruppe bereits vorhanden?
                                baum = QgsLayerTreeModel(grp)
                                anzahl_top_level_eintraege = baum.rowCount()
                                baum = None # Sonst Absturz bei grp.parent().removeChildNode(grp) da baum auf ein Nichts refenrenziert!
                            else:
                                anzahl_top_level_eintraege = -1     #nich ganz so gut

                            # den neuen ganz hinten einsetzen
                            grp.insertChildNode(anzahl_top_level_eintraege,dummy)

                            zwtsch.parent().removeChildNode(zwtsch)
                            grp.setExpanded(False)


                            if nach_unten:   #ganz nach unten mit der gefüllten Gruppe, wenn das Flag gesetzt ist

                                if not self.gruppe_vorhanden:
                                    dummy = grp.clone()
                                    QgsProject.instance().layerTreeRoot().insertChildNode(-1,dummy)
                                    grp.parent().removeChildNode(grp)





                    else:   #die Layer werden NICHT in einen self.gruppenlayer geladen
                            #sollen aber nach unten verschoben werden
                        if nach_unten:

                           # QGIS höher 2.6
                            if QGis.QGIS_VERSION_INT > 20600:

                                # wiviele layer sind in der gruppe bereits vorhanden?
                                baum = QgsLayerTreeModel(QgsProject.instance().layerTreeRoot())
                                anzahl_top_level_eintraege = baum.rowCount()
                                baum = None # Sonst Absturz bei grp.parent().removeChildNode(grp) da baum auf ein Nichts refenrenziert!
                            else:
                                anzahl_top_level_eintraege = -1     #nich ganz so gut

                            zwtsch = QgsProject.instance().layerTreeRoot().findLayer(self.lyr.id()) #der geladene layer
                            dummy = zwtsch.clone()

                            # den neuen ganz hinten einsetzen
                            QgsProject.instance().layerTreeRoot().insertChildNode(anzahl_top_level_eintraege,dummy)
                            zwtsch.parent().removeChildNode(zwtsch)

                    #abschließend schauen ob der Layer aufgeklappt ist
                    #und das flag setzen - beim Verschieben in die Gruppenklayer
                    #verändert sich das nämlich manchmal...
                    if (self.legends.item(j).attributes().namedItem("open").nodeValue() == "false") and not (self.lyr is None):
                        dummy.setExpanded(False)

                    elif (self.legends.item(j).attributes().namedItem("open").nodeValue() == "true") and not (self.lyr is None):
                        dummy.setExpanded(True)


                    #der nachfolgende Code erzwingt eine Aktualisierung
                    #der Legende und des MapWindow
                    #Ansonsten kanns im Mapwindow Darstellungsprobleme geben! Wieso??
                    if not self.lyr is None:
                        anzeigename = self.lyr.name()
                        self.lyr.setLayerName(anzeigename+" ")
                        self.lyr.setLayerName(anzeigename)
                    else:
                        QtGui.QMessageBox.about(None, "Achtung", "Layer " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " nicht gefunden!")





                    # unbedingt ALLES DEselektieren, sonst Probleme mit Reihenfolge
                    self.iface.layerTreeView().setCurrentLayer(None)    # None entspricht einem Null Pointer -> Auswahl wird entfernt -> nicht ausgewählt



                    #Unbedingt zurücksetzen sonst kanns beim wiederholten
                    #laden des gleichen Projektfiles einen Fehler geben:
                    #wenn nämlich die Schleife erneut beginnt, nicht lädt und self.lyr
                    #beim vorherigen laden steht!
                    self.lyr = None

                    # und weiter in der Schleife!

        #UNBEDINGT am Schluss QGis wieder auf den usprünglichen
        #Pfad zurücksetzen

        QgsProject.instance().setFileName(CurrentPath)

        #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
        # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
        # der Legende vor allem Laden als Aktueller Layer gesetzt werden!!!


        #Objekte besser löschen
        self.legends = None
        self.legendTree = None

        self.maps = None
        self.legends = None
        self.gruppen = None

        ######################################################################
        # Abschlussprüfung: sind alle da
        #prüfen ob alle Layer der Liste geladen wurden
        #das ist notwendig, da ja beim Projektladen alles passen kann aber
        #ein Layer nicht vorhanden ist
        ######################################################################
        fehler = 0
        layerzaehler = 0

        # Weg mit dem Fortschrittsbalken
        self.info.close()

        if liste  <> None:  #wenn nur ein Teil der Layer eines Projekts geladen werden sollen. Die Liste enthält die
                            #Namen dieser Layer
            for nd in range(len(liste)):
                for lyr_tmp in leginterface.layers(): #alle bereits geladenen Layer durchgehen

                    #Unbedingt die optionale Änderung des
                    #Anzeigenamens (z.B. DKM) mitberücksichtigen!)
                    if (ergaenzungsname != None) and self.anzeigename_aendern:
                        if  liste[nd] + "-" + ergaenzungsname == lyr_tmp.name():
                            layerzaehler = layerzaehler +1
                        elif  liste[nd].rstrip(" (a)") + "-" + ergaenzungsname + ' (a)' == lyr_tmp.name():
                            layerzaehler = layerzaehler +1
                    else:
                        if liste[nd] == lyr_tmp.name():
                            layerzaehler = layerzaehler +1

        #ACHTUNG: Wurden nicht alle in der Liste (fürs importieren übergebne Layerliste mit Layernamen) angeführten Layer
        #anhand des Layernamensim Projekt gefunden gibts
        #hier noch eine Fehlermeldung
        if not liste is None:
            if len(liste) > layerzaehler: #Ints! Dann wurde was nicht geladen
                QtGui.QMessageBox.about(None, "Achtung", "Nicht alle Layer aus " + pfad + " konnte(n) geladen werden!!")


        # gejointe Relationen wiederherstellen
        # aber erst ganz am Schluss!!
        for singlejoin in self.joinliste:
            for singlejoininfo in singlejoin.joininfo:
                singlejoin.joinlayer.addJoin(singlejoininfo)




#####################################################################################################################################################################
# Die Funktion sublayer hat folgendes ziel: sie gibt das qtreewidget objekt der gruppe zurück
# das einem layer unmittelbat übergeordnet ist und in welche er hineingehört.
# Dabei gibt es zwei Varianten: Die Gesamte Gruppenghierarchi in der der Layer reingehört existiert bereits,
# oder alle Gruppen oder ein Teil davon muss angelegt werden. Zurückgegeben wird aber immer nur die unmittelbar
# dem Layer übergeordnete. Da Gruppen in QGIS keine indiv. ID besitzen sondern sich nur über Namen identifizieren lassen
# ist es theoretischmöglich, dass eine Gruppenhierarchie mehrfach vorkommt. In diesem Sub wird dann einfach nur der erste Treffer
# genommen, die anderen Varianten ignoriert
# Das ganze wird für jeden geladenen Layer von oben nach unten ( in der Hierarchie) durchgeführt.
#####################################################################################################################################################################


def sublayer( legendtree,leginterface, gruppenliste,gruppen_ergname='', nach_unten = False):

    # iterator beginnt hinten - also bei der äußersten Gruppe


    parent_groups = []  # die Gruppen hierarchie, in die eine Gruppe reinkommt (wenn sie erzeugt werden muss)
    parent_groups.append(legendtree)    # wir beginnen mit der Root Node

    # Ergänzungname wenn vorhanden der obersten Gruppe
    # Hinzufügen, meist der Gemeindename
    if not gruppen_ergname == '' and gruppen_ergname != None:
        neuername = gruppenliste[len(gruppenliste) - 1].name + '-' + gruppen_ergname
        gruppenliste[len(gruppenliste) - 1].name = neuername



    # die oberste Gruppe hat den höchsten Index!
    # deshalb Iteration von hinten beginnen

    for j in range(len(gruppenliste) -1 , -1 , -1):

        # gibts die Gruppe?
        gruppen = finde_kinder(gruppenliste[j].name, parent_groups)    # gibt es Gruppe(n) mit dem gesuchten Namen bereits

        if len(gruppen) == 0: # Kind-Gruppe muss angelegt werden, keine Gruppe mit dem Namen in Hierarchielevel vorhanden
            #QtGui.QMessageBox.about(None, "Achtung", "Laenge = " + str(len(gruppenliste)) + " j = " + str(j) + " Name = " + gruppenliste[j].name)
            kindi = QgsLayerTreeGroup(gruppenliste[j].name)

            # ACHTUNG: wenn nach unten geschoben werden soll, dann nur
            # immer die oberste GRuppe beim NEuanlegen!!
            if j == len(gruppenliste) - 1 and nach_unten:
                parent_groups[0].insertChildNode(-1,kindi)   # immer den ersten Treffer nehmen, was soll ich sonst machen da alle gleich - und nach unten
            else:
                parent_groups[0].insertChildNode(gruppenliste[j].index,kindi)   # immer den ersten Treffer nehmen, was soll ich sonst machen da alle gleich - und in die Hierarchie nach der PRojektdatei

            #ist die neue Gruppe aufgeklappt?
            if gruppenliste[j].ex == "true":
                kindi.setExpanded(True)
            elif gruppenliste[j].ex == "false":
                kindi.setExpanded(False)

            #ist die neue Gruppe gechecked?
            if gruppenliste[j].ch == "Qt::Unchecked":
                kindi.setVisible(QtCore.Qt.Unchecked)
            elif gruppenliste[j].ch == "Qt::PartiallyChecked":
                kindi.setVisible(QtCore.Qt.PartiallyChecked)
            elif gruppenliste[j].ch == "Qt::Checked":
                kindi.setVisible(QtCore.Qt.Checked)

            parent_groups = []  # Liste neu initialisieren
            parent_groups.append(kindi)    # die neue Gruppe ist der Parent für den Nächste Hierarchielevel - wenn es noch mehr zum Anlegen darunter gibt

        else:   # Es gibt Gruppe(n) mit dem betreffenden Namen
            parent_groups = gruppen # zurückgeben und event. noch tiefere Hierarchie anlegen/suchen


    return parent_groups    # wie erwähnt (siehe start sub!), können es mehrer idente Hierarchien sein - es wird dann beim Aufruf
                            # ganze einfach nur die erste genommen - anderst gehts nicht


####################################################################
# Sub sucht einfach nach allen Gruppen mit gruppenname in einer
# Liste mit Parent Gruppen in der Legende und gibt
# diese zurück
####################################################################
def finde_kinder( gruppenname, liste_nodes):

    backlist = []


    for node in liste_nodes:
        for kind in node.children():    # Kind mit gesuchtem Namen vorhanden und Node eine Gruppe?
            if kind.nodeType() == 0 and kind.name() == gruppenname:
                backlist.append(kind)

    return backlist # Alle Child Gruppenobjekte die dem Namen entsprechen




############################################################################################################
# diese unterprogramm gibt die Reihenfolge der position (index) in der aktuellen Gruppe
# der legende zurück. die identifikation geht über das attribut name (haben self.gruppen und layer)
# quelle dafür ist das qgis projektfile
############################################################################################################
def index_zuweisen(name,aktual_dom_node):
    counter = 0
    positionsliste = aktual_dom_node.childNodes()
    while counter < positionsliste.count():
        if positionsliste.item(counter).attributes().namedItem("name").nodeValue() == name:
            break
        counter = counter + 1

    return counter


#############################################################
# unterprogramm behandelt die subset einträge im projektfile
# bei shape datenquellen und wandelt sie in anweisungen
# für postgres datenwuellen um
#############################################################
def textfilter_subset(text):


    # zuerst alles innerhalb von double quotes in kleinbuchstaben (spaltennamen)
    # umwandeln
    text_neu = ''
    switch = False
    for char in text:

        if char == "\"":
            if switch:
                switch = False
            else:
                switch = True

        if switch:
            char = char.lower()

        text_neu = text_neu + char

    sql = ''
    sql = text_neu.split('subset')[1]
    if sql == '':
        sql = text_neu.split('Subset')[1]
    if sql == '':
        sql = text_neu.split('SUBSET')[1]


    tablename = text_neu.split('.shp')[0]
    tablename = os.path.basename(tablename)
    return [tablename,sql]

########################################
# Klasse dient as struct Variablendef.
########################################
class pos_gruppe():
    def __init__(self):
        self.name = ""
        self.index = 0
        self.ex = ""
        self.ch = ""


########################################
# Klasse dient as struct Variablendef.
########################################
class lyr_join():
    def __init__(self):
        self.joinlayer = None
        self.joininfo = None


