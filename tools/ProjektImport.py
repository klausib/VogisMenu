# -*- coding: utf-8 -*-



# Die Kernbibliotheken für
# Qgis und PyQT importieren
# (Gegebenenfalls läßt sich diese Auswahl
# noch verfeinern)
from PyQt4 import QtCore, QtGui, QtXml
from qgis.core import *
from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich
#from qgis.core import *
#from LayerDialog import *

import os.path
import string,copy, re



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



    def importieren(self, pfad = None, liste = None, ergaenzungsname = None, anzeigename_ergaenzen = False, nach_unten = False, force_gruppenname = None):






        #obwohl ich es mir nicht erklären kann und nicht weiss wieso, aber:
        #wenn bei layern in komplexere gruppen (z.b.) nach dem laden die gruppen
        #vum user verschoben werden, dann kann es passieren, dass nachfolgend beim laden
        #einer anderen gemeinde mit gleicher struktur (gfz) ein layer nicht geladen wird.
        #das tritt nicht immer auf aber bei manchen ladevorgängen und ist unerklärbar!!
        #die erfahrung hat gezeigt, dass wenn ganz oben mind. zwei normale layer in der legende
        #geladen wird, sich der fehler nicht mehr ergibt. wieseo???? deshalb werden jetzt einfach
        #bei jedem laden zuerst zwei memorylayer nach oben geschrieben die dann wieder gelöscht werden

        #memadd(self.iface)


        self.anzeigename_aendern = anzeigename_ergaenzen

        #das ist cool: damit wird die QT Schnittstelle verwendet, die Klasse
        #QTreeWidget um im Qgis die Legendenposition zu verändern. Da Qgis für die
        #Legende ja auf QT Zugreift geht das!!
        self.legendTree = self.iface.mainWindow().findChild(QtGui.QDockWidget,"Legend").findChild(QtGui.QTreeWidget)

        #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
        # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
        # der Legende vor allem Laden als Aktueller Layer gesetztw erden!!!
        self.legendTree.setCurrentItem(self.legendTree.topLevelItem(0))

        if pfad == "":
            return


        # Das Qgis Projektfile ist ein XML und wird
        # hier eingelesen
        try:
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
        #self.maps=self.maps
        #self.legends=self.legends
        #self.gruppen=self.gruppen

        self.lyr = None


        # Legendeninterface instanzieren. Wird gebraucht um die Layer checked oder uncheckd zu schalten (Kreuzchen)
        leginterface = self.iface.legendInterface()
        #mapLayerRegistry = QgsMapLayerRegistry.instance()
        #QtCore.QObject.connect(mapLayerRegistry, QtCore.SIGNAL("layersAdded (QList< QgsMapLayer * >)"), self.layer_added)


        #Zuerst den aktuellen Pfad auf dem
        #Qgis steht auslesen (kann z.B. ein lokaler Pfad sein
        #von dem ein Projekt geladen wird
        CurrentPath = QgsProject.instance().fileName()

        #Dann auf den jeweiligen Pfad setzen, von dem geladen wird. Sonst kann kein Projekt
        #mit absoluten Pfaden abgespeichert werden (für Layer die mit dem
        #VogisMenü geladen werden)
        QgsProject.instance().setFileName(pfad)





        #Schleife geht alle Layer die in der Legende aufscheinen durch. Hier
        #ist nämlich die reihenfolge festgelegt, wie sie in Qgis dargestellt werden
        # Die Layer die zuerst dargestellt werden sind "unten", daher umkehren!
        #Diese Schleife brauch ich nur für die richtige Reihenfolge
        #der importierten Layer in Qgis
        n = 0   #index
        for j in range(self.legends.length(),-1,-1):

            #Schleife geht alle Layer die in der maplayer tags aufscheinen durch
            #dort ist nämlich die wirkliche Information für die Darstellung im
            #Qgis. Also wird zuerst der Layer per ID in der Obigen
            #Schleife ausgewählt und dann in dieser Schlefe im maplayertag
            #identifiziert
            #self.lyr=None
            for i in range(self.maps.length()):


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
                        #QtGui.QMessageBox.about(None, "Achtung", "Layer " + quelli + " bereits geladen!")
                    if (ergaenzungsname != None) and (lyr_tmp.id()  == quelli + ergaenzungsname): #Treffer: der Layer ist schon geladen
                        laden = False
                        #QtGui.QMessageBox.about(None, "Achtung", "Layer " + quelli + ergaenzungsname+ " bereits geladen!")



                #Die Layerid ist in den lagend tags und maplayer tags gleich
                #so kann ein layer genau identifiziert werden. ist laden zudem True
                #gehts also weiter
                if (self.maps.item(i).namedItem("id").firstChild().toText().data() == self.legends.item(j).namedItem("filegroup").namedItem("legendlayerfile").attributes().namedItem("layerid").nodeValue()) and laden:
                    #QtGui.QMessageBox.about(None, "Projekt", "kasperle teil")
                    if liste  <> None:  #wenn nur ein Teil der Layer eines Projekts geladen werden sollen. Die Liste enthält die
                                        #Namen dieser Layer


                        for nd in range(len(liste)):

                            if liste[nd] == self.legends.item(j).attributes().namedItem("name").nodeValue():

                                #ACHTUNG: unbedingt den nodeValue der ID ändern wenn Gemeindeweise
                                #geladen wird (DKM) Da in den Qgis Projekten der Gemeinden die jeweilig ID des Layers
                                #der einfachheit Halber ident ist, würde so qgis den Layer nicht importieren!!!
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
                                #else:
                                    #QtGui.QMessageBox.about(None, "Projekt", str( vogisEncoding_global[0]) + ' ' +  vogisKBS_global[0])



                                # Projekt einlesen!

                                if not QgsProject.instance().read(self.maps.item(i)):                                   #hier wird der Layer geladen und gemäß den Eintragungen
                                    QtGui.QMessageBox.about(None, "Achtung", "Layer " + liste[nd] + " nicht gefunden!") #der DomNode auch gerendert und dargestellt
                                    continue


                                #den Anzeigenamen im Qgis ebenfalls ändern
                                #dazu zuerst den richtigen Layer anhand der Layerid auswählen
                                for lyr_tmp in leginterface.layers():
                                    if lyr_tmp.id() == noddi.firstChild().nodeValue():
                                        self.lyr = lyr_tmp

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

                                #dann in der Apllikation registrieren
                                QgsMapLayerRegistry.instance().addMapLayer(self.lyr)



                                #Und nun noch den Layernamen für die Darstellung
                                #im Qgis ergänzen. Siehe oben, bei gemeindeweisem Laden
                                if (ergaenzungsname != None) and (self.lyr != None) and self.anzeigename_aendern: #noch ein boolean wegen der wasserwirtschaft!!
                                    if not (self.lyr.name().find(ergaenzungsname) > -1):    #ACHTUNG: Sonst wird bei wiederholtem klicken der Name nochmal rangehängt
                                        if self.lyr.name().find("(a)") > -1:
                                            aktname =   self.lyr.name().rstrip("(a)") + "-" + ergaenzungsname + " (a)"
                                            self.lyr.setLayerName(aktname)
                                        else:
                                            aktname =   self.lyr.name() + "-" + ergaenzungsname
                                            self.lyr.setLayerName(aktname)
                                #abschließend schauen ob der aktiviert ist
                                if (self.legends.item(j).attributes().namedItem("checked").nodeValue() == "Qt::Unchecked") and not (self.lyr is None):
                                    leginterface.setLayerVisible(self.lyr,0 )

                                #inti enthält den Index des soeben geladenden Layers
                                #dadurch ist sein Standort identifizierbar in der Legende
                                inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())

                                dummy = self.legendTree.topLevelItem(inti)  #das QTreeWidgetItem des geladene Layer wird identifiziert
                                                                            #brauchen wir anschließend und weiter unten

                                #abschließend schauen ob der aufgeklappt ist
                                #und das flag setzen
                                ex_l = True
                                if (self.legends.item(j).attributes().namedItem("open").nodeValue() == "false") and not (self.lyr is None):
                                    self.legendTree.collapseItem(dummy)
                                    ex_l = False
                                elif (self.legends.item(j).attributes().namedItem("open").nodeValue() == "true") and not (self.lyr is None):
                                    self.legendTree.expandItem(dummy)
                                    ex_l = True

                                #wenn nötig self.gruppenlayer anlegen
                                #diese werden derzeit nur für eine Ebene unterstützt
                                #wenn sie nicht über das Projekt angelegt werden
                                #sondern lediglich ein self.gruppenname vom Ladeprogramme
                                #übergeben wird. Werden sie über das Projekt geladen
                                #werden 4 Hierarchieebenen unterstützt
                                #prüfen ob der layer zu einem self.gruppenlayer gehört

                                #gibts überhaupt eine Gruppe in die der
                                #Layer eingebettet ist bzw. wird die
                                #Erstellung eines self.gruppenlayer erzwungen über force_gruppenname (Flagvariable)

                                if (self.legends.item(j).parentNode().nodeName() == "legendgroup") or not (force_gruppenname is None):

                                    self.gruppenliste = leginterface.groups()
                                    self.gruppe_vorhanden = False

                                    #ACHTUNG: Layername und direkt übergeordneter Gruppenname
                                    #müssen sich unterscheiden, sonst kommts zu einem Fehler. Sollts
                                    #dennoch mal vorkommen, wird es hier abgefangen
                                    if self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue() == self.legends.item(j).attributes().namedItem("name").nodeValue():
                                        aktname =  self.lyr.name()
                                        self.lyr.setLayerName(aktname+"_")

                                    #prüfen ob die Gruppe schon angelegt ist
                                    for einzelgruppe in self.gruppenliste:
                                        if einzelgruppe == self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue(): #Name aus dem QGS Projektfile
                                            self.gruppe_vorhanden = True

                                        elif einzelgruppe == force_gruppenname: #Name ist übergeben worden
                                            self.gruppe_vorhanden = True




                                    #Variablen für die self.gruppenlayerebenen. 4 steht für ganz unten ( dem Layer direkt übergeordnet)
                                    #und 1 für ganz oben. also die erste Gruppe der Hierarchie. die level Variablen enthalten den
                                    #self.gruppennamen und in die Indexvariablen der Index der Gruppe in der jeweilgien Hierarchiebene
                                    #(der Index steuert die Reihenfolge der Darstellung von Oben nach Unten)
                                    #zusätzlich sind variablen für die Zustände Checked und Expanded notwendig
                                    level_4 = ""
                                    level_3 = ""
                                    level_2 = ""
                                    level_1 = ""
                                    index_1 = 0
                                    index_2 = 0
                                    index_3 = 0
                                    index_4 = 0
                                    ex_g1 = ""
                                    ex_g2 = ""
                                    ex_g3 = ""
                                    ex_g4 = ""
                                    ch_g1 = ""
                                    ch_g2 = ""
                                    ch_g3 = ""
                                    ch_g4 = ""


                                    #nun die Namen der Gruppe(n) bestimmen, in die der geladene
                                    #Layer eingebettet ist und auch den Index der Gruppe bestimmen
                                    #Der Index steuert die reihenfolge der Darstellung von oben nach unte
                                    #Die parent Node ist die jeweils übergeordnete Node, wenns eine Gruppe gibt steht unter name was drin

                                    if self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().nodeName() == "legendgroup":

                                        level_4 = self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue()       #der name der dem layer unmittelbar übergeordnete Gruppe: Ebene 4
                                        index_4  = index_zuweisen(self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode())    # Index der Darstellungsreihenfolge der Gruppe in ihrer Hierarchie
                                        ex_g4 = self.legends.item(j).parentNode().attributes().namedItem("open").nodeValue()
                                        ch_g4 = self.legends.item(j).parentNode().attributes().namedItem("checked").nodeValue()

                                        if self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().parentNode().nodeName() == "legendgroup":

                                            level_3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue()  #Gruppe eine Ebene höher: Ebene 3
                                            index_3  = index_zuweisen(self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode())
                                            ex_g3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                            ch_g3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("checked").nodeValue()

                                            if self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().parentNode().parentNode().nodeName() == "legendgroup":

                                                level_2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() #Gruppe zwei Ebenen höher: Ebene 2
                                                index_2  = index_zuweisen(self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode().parentNode())
                                                ex_g2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                                ch_g2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("checked").nodeValue()

                                                if self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() != ""and self.legends.item(j).parentNode().parentNode().parentNode().parentNode().nodeName() == "legendgroup":

                                                    level_1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue()# Gruppe drei Ebenen höher: Ebene 1
                                                    index_1  = index_zuweisen(self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode().parentNode().parentNode())
                                                    ex_g1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                                    ch_g1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("checked").nodeValue()

                                        #inti enthält den Index des soeben geladenden Layers
                                        #dadurch ist sein Standort identifizierbar in der Legende
                                        #inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())


                                        #counter gibt den index an, an dessen Stelle der geladene Layer
                                        #(in der Gruppe in die er eingebettet ist) verschoben werden soll
                                        #counter = index_zuweisen(self.lyr.name(),self.legends.item(j).parentNode())
                                        counter = index_zuweisen(self.maps.item(i).namedItem("layername").firstChild().nodeValue(),self.legends.item(j).parentNode())

                                        #dummy = self.legendTree.takeTopLevelItem(inti)  #der geladene Layer wird ausgeschnitten
                                        #dummy = self.legendTree.topLevelItem(inti)  #der geladene Layer wird identifiziert
                                        dummy.setData(1,0,counter)  #in die data Propertie (andere Möglichkeit nicht gefunden) wird der Zielindex eingetragen (zum später sortieren

                                        #grp enthält das qtreewidgetitem Objekt der Gruppe!, in die der geladene
                                        #Layer verschoben werden soll!
                                        grp = sublayer(self.legendTree,leginterface,level_1,level_2,level_3,level_4,index_1,index_2,index_3,index_4,ex_g1, ex_g2,ex_g3,ex_g4,ch_g1,ch_g2,ch_g3,ch_g4)


                                        # ein spezieller Datentyp. Enthält die information die nötig ist
                                        # um den geladenen Layer in die richtige self.gruppenhierarchi zu befördern
                                        paar_grp = paar()

                                        if isinstance(grp,QtGui.QTreeWidgetItem) and not grp is None:

                                            paar_grp.gruppe = grp   #das qwidgetitem der gruppe (in welche der layer gebettet wird)
                                            paar_grp.layer = dummy  #das qwidgetitem des layers
                                            paar_grp.index= counter #der index des layers in der gruppe
                                            paar_grp.expanded= ex_l #Layer aufgeklappt oder nicht


                                            self.paarliste.append(paar_grp) #dise info wird dann in eine listenvariable geschrieben (sammelt alle layer!)
                                            #rem_item_list.append(lyr_tmp)


                                        else:
                                            QtGui.QMessageBox.about(None, "ACHTUNG","Anlegen der Gruppe gescheitert")
                                            break



                                    letzterplatz = False #Flagvariable ermittelt ob die Gruppe ganz nach unten gehört


                                    #die gruppe in die der layer eingebettet ist kommt nicht aus
                                    #einem projekt, sondern wird erzwungen. hier gibts allerdings
                                    #nur eine ebene (was das ganze einfach macht)
                                    if (not force_gruppenname is None):
                                        inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())
                                        kindi = self.legendTree.takeTopLevelItem(inti)
                                        grp = sublayer(self.legendTree,leginterface,"","","",force_gruppenname)
                                        grp.insertChild(0,kindi)    #layer qtreewidgetitem wird als child in das self.gruppen qtreewidgetitem eingebettet



                                    if nach_unten:   #ganz nach unten mit der Gruppe des Layers wenn das flag gesetzt ist

                                        if not self.gruppe_vorhanden:
                                            dodl = self.legendTree.takeTopLevelItem(0)  #die neue gruppe ist ganz oben
                                            unten = self.legendTree.topLevelItemCount()
                                            self.legendTree.insertTopLevelItem(unten,dodl)    #und dann an den letzten Platz gesetzt


                                else:   #die Layer werden NICHT in einen self.gruppenlayer geladen
                                        #sollen aber nach unten verschoben werden
                                    if nach_unten:
                                        QtGui.QMessageBox.about(None, "Unten",str(unten))
                                        dodl = self.legendTree.takeTopLevelItem(0)

                                        self.legendTree.insertTopLevelItem(self.legendTree.topLevelItemCount() - n,dodl)
                                        n = n+1     #bewirkt praktisch ein "Spiegeln" beim runterschieben: sonst stehen die Layer
                                                    #in der Reihenfolge auf dem Kopf


                                #der nachfolgende Code erzwingt eine Aktualisierung
                                #der Legende und des MapWindow
                                #Ansonsten kanns im Mapwindow darstellungsprobleme geben! Wiso??

                                if not self.lyr is None:
                                    anzeigename = self.lyr.name()
                                    self.lyr.setLayerName(anzeigename+" ")
                                    self.lyr.setLayerName(anzeigename)
                                else:
                                    QtGui.QMessageBox.about(None, "Achtung", "Layer " + liste[nd] + " nicht gefunden!")

                                #Unbedingt zurücksetzen sonst kanns beim wiederholten
                                #laden des gleichen Projektfiles einen Fehler geben:
                                #wenn nämlich die Schleife erneut beginnt, nicht lädt und self.lyr
                                #beim vorherigen laden steht!

                                self.lyr = None


                    # #######################################################################
                    # ACHTUNG: Ab hier eine beginnt ein neuer Programmteil
                    # Keine Auswahl bestimmter Layer. Alle Layer des Projekts werden geladen
                    # Das wird hier eigens behandelt, obwohl sich viele Codeteile von "oben"
                    # (wenn nur bestimmte Layer des Projekts geladene werden) wiederholen
                    # #########################################################################
                    else:



                        #ACHTUNG: unbedingt den nodeValue der ID ändern wenn Gemeindeweise
                        #geladen wird (DKM) Da in den Qgis Projekten der Gemeinden die jeweilig ID des Layers
                        #der einfachheit Halber ident ist, würde so qgis den Layer nicht importieren!!!
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
                        #else:
                            #QtGui.QMessageBox.about(None, "Projekt", str( vogisEncoding_global[0]) + ' ' +  vogisKBS_global[0])



                        # Projekt einlesen!
                        if not QgsProject.instance().read(self.maps.item(i)):                                   #hier wird der Layer geladen und gemäß den Eintragungen
                            QtGui.QMessageBox.about(None, "Achtung", "Layer " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " nicht gefunden!") #der DomNode auch gerendert und dargestellt
                            continue

                       #den Anzeigenamen im Qgis ebenfalls ändern
                       #dazu zuerst den richtigen Layer anhand der Layerid auswählen
                        #leginterface = self.iface.legendInterface()
                        for lyr_tmp in leginterface.layers():
                            if lyr_tmp.id() == noddi.firstChild().nodeValue():
                                self.lyr = lyr_tmp



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

                        #Und nun noch den Layernamen für die Darstellung
                        #im Qgis ergänzen. Siehe oben, bei gemeindeweisem Laden
                        if (ergaenzungsname != None) and (self.lyr != None) and self.anzeigename_aendern: #noch ein boolean wegen der wasserwirtschaft!!
                                if not (self.lyr.name().find(ergaenzungsname) > -1):    #ACHTUNG: Sonst wird bei wiederholtem klicken der Name nochmal rangehängt
                                    if self.lyr.name().find("(a)") > -1:
                                        aktname =   self.lyr.name().rstrip("(a)") + "-" + ergaenzungsname + " (a)"
                                        self.lyr.setLayerName(aktname)
                                    else:
                                        aktname =   self.lyr.name() + "-" + ergaenzungsname
                                        self.lyr.setLayerName(aktname)
                        #abschließend schauen ob der aktiviert ist
                        if (self.legends.item(j).attributes().namedItem("checked").nodeValue() == "Qt::Unchecked") and not (self.lyr is None):
                            leginterface.setLayerVisible(self.lyr,False)

                        #inti enthält den Index des soeben geladenden Layers
                        #dadurch ist sein Standort identifizierbar in der Legende
                        inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())

                        dummy = self.legendTree.topLevelItem(inti)  #das QTreeWidgetItem des geladene Layer wird identifiziert
                                                                    #brauchen wir anschließend und weiter unten

                        #abschließend schauen ob der aufgeklappt ist
                        #und das flag setzen
                        ex_l = True
                        if (self.legends.item(j).attributes().namedItem("open").nodeValue() == "false") and not (self.lyr is None):
                            self.legendTree.collapseItem(dummy)
                            ex_l = False
                        elif (self.legends.item(j).attributes().namedItem("open").nodeValue() == "true") and not (self.lyr is None):
                            self.legendTree.expandItem(dummy)
                            ex_l = True


                       #wenn nötig self.gruppenlayer anlegen
                       #diese werden derzeit nur für eine Ebene unterstützt
                       #wenn sie nicht über das Projekt angelegt werden
                       #sondern lediglich ein self.gruppenname vom Ladeprogramme
                       #übergeben wird. Werden sie über das Projekt geladen
                       #werden bei bedarf automatisch bis 4 Hierarchieebenen unterstützt.

                        #gibts überhaupt eine Gruppe in die der
                        #Layer eingebettet ist bzw. wird die
                        #Erstellung eines self.gruppenlayer erzwungen über force_gruppenname (Flagvariable)

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


                            #Variablen für die self.gruppenlayerebenen. 4 steht für ganz unten ( dem Layer direkt übergeordnet)
                            #und 1 für ganz oben. also die erste Gruppe der Hierarchie. die level Variablen enthalten den
                            #self.gruppennamen und in die Indexvariablen der Index der Gruppe in der jeweilgien Hierarchiebene
                            #(der Index steuert die Reihenfolge der Darstellung von Oben nach Unten)
                            #zusätzlich sind variablen für die Zustände Checked und Expanded notwendig
                            level_4 = ""
                            level_3 = ""
                            level_2 = ""
                            level_1 = ""
                            index_1 = 0
                            index_2 = 0
                            index_3 = 0
                            index_4 = 0
                            ex_g1 = ""
                            ex_g2 = ""
                            ex_g3 = ""
                            ex_g4 = ""
                            ch_g1 = ""
                            ch_g2 = ""
                            ch_g3 = ""
                            ch_g4 = ""


                            #nun die Namen der Gruppe(n) bestimmen, in die der geladene
                            #Layer eingebettet ist und auch den Index der Gruppe bestimmen
                            #Der Index steuert die reihenfolge der Darstellung von oben nach unte
                            #Die parent Node ist die jeweils übergeordnete Node, wenns eine Gruppe gibt steht unter name was drin
                            if self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().nodeName() == "legendgroup":

                                level_4 = self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue()       #der name der dem layer unmittelbar übergeordnete Gruppe: Ebene 4
                                index_4  = index_zuweisen(self.legends.item(j).parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode())    # Index der Darstellungsreihenfolge der Gruppe in ihrer Hierarchie
                                ex_g4 = self.legends.item(j).parentNode().attributes().namedItem("open").nodeValue()
                                ch_g4 = self.legends.item(j).parentNode().attributes().namedItem("checked").nodeValue()
                                #QtGui.QMessageBox.about(None, "Viert Oberste Ebene",level_4)

                                if self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().parentNode().nodeName() == "legendgroup":

                                    level_3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue()  #Gruppe eine Ebene höher: Ebene 3
                                    index_3  = index_zuweisen(self.legends.item(j).parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode())
                                    ex_g3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                    ch_g3 = self.legends.item(j).parentNode().parentNode().attributes().namedItem("checked").nodeValue()
                                    #QtGui.QMessageBox.about(None, "Dritt Oberste Ebene",level_3)

                                    if self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() != "" and self.legends.item(j).parentNode().parentNode().parentNode().nodeName() == "legendgroup":

                                        level_2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() #Gruppe zwei Ebenen höher: Ebene 2
                                        index_2  = index_zuweisen(self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode().parentNode())
                                        ex_g2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                        ch_g2 = self.legends.item(j).parentNode().parentNode().parentNode().attributes().namedItem("checked").nodeValue()
                                        #QtGui.QMessageBox.about(None, "Zweit Oberste Ebene",level_2)

                                        if self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue() != ""and self.legends.item(j).parentNode().parentNode().parentNode().parentNode().nodeName() == "legendgroup":

                                            level_1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue()# Gruppe drei Ebenen höher: Ebene 1
                                            index_1  = index_zuweisen(self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("name").nodeValue(),self.legends.item(j).parentNode().parentNode().parentNode().parentNode().parentNode())
                                            ex_g1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("open").nodeValue()
                                            ch_g1 = self.legends.item(j).parentNode().parentNode().parentNode().parentNode().attributes().namedItem("checked").nodeValue()
                                            #QtGui.QMessageBox.about(None, "Oberste Ebene",level_1)

                                #inti enthält den Index des soeben geladenden Layers
                                #dadurch ist sein Standort identifizierbar in der Legende
                                #inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())


                                #counter gibt den index an, an dessen Stelle der geladene Layer
                                #(in der Gruppe in die er eingebettet ist) verschoben werden soll
                                #counter = index_zuweisen(self.lyr.name(),self.legends.item(j).parentNode())
                                counter = index_zuweisen(self.maps.item(i).namedItem("layername").firstChild().nodeValue(),self.legends.item(j).parentNode())
                                #QtGui.QMessageBox.about(None, "Counter",str(counter))

                                #dummy = self.legendTree.takeTopLevelItem(inti)  #der geladene Layer wird ausgeschnitten
                                #dummy = self.legendTree.topLevelItem(inti)  #der geladene Layer wird identifiziert
                                dummy.setData(1,0,counter)  #in die data Propertie (andere Möglichkeit nicht gefunden) wird der Zielindex eingetragen (zum später sortieren

                                #grp enthält das qtreewidgetitem Objekt der Gruppe!, in die der geladene
                                #Layer verschoben werden soll!
                                grp = sublayer(self.legendTree,leginterface,level_1,level_2,level_3,level_4,index_1,index_2,index_3,index_4,ex_g1, ex_g2,ex_g3,ex_g4,ch_g1,ch_g2,ch_g3,ch_g4)

                                #QtGui.QMessageBox.about(None, "Adressen", "Gruppe = " + grp.text(0) + " " + str(grp) + " Layer = "  + dummy.text(0) + " " +  str(dummy))
                                # ein spezieller Datentyp. Enthält die information die nötig ist
                                # um den geladenen Layer in die richtige self.gruppenhierarchie zu befördern
                                paar_grp = paar()

                                if isinstance(grp,QtGui.QTreeWidgetItem) and not grp is None:

                                    paar_grp.gruppe = grp   #das qwidgetitem der gruppe (in welche der layer gebettet wird)
                                    paar_grp.layer = dummy  #das qwidgetitem des layers
                                    paar_grp.index = counter #der index des layers in der gruppe
                                    paar_grp.expanded= ex_l #Layer aufgeklappt oder nicht

                                    #QtGui.QMessageBox.about(None, "Klappung",grp.text(0) + " = " + ex_g)
                                    self.paarliste.append(paar_grp) #dise info wird dann in eine listenvariable geschrieben (sammelt alle layer!)
                                    #rem_item_list.append(lyr_tmp)

                                else:
                                    QtGui.QMessageBox.about(None, "ACHTUNG","Anlegen der Gruppe gescheitert")
                                    break


                            letzterplatz = False #Flagvariable ermittelt ob die Gruppe ganz nach unten gehört


                            #die gruppe in die der layer eingebettet ist kommt nicht aus
                            #einem projekt, sondern wird erzwungen. hier gibts allerdings
                            #nur eine ebene (was das ganze einfach macht)
                            if (not force_gruppenname is None):
                                inti = self.legendTree.indexOfTopLevelItem(self.legendTree.currentItem())
                                kindi = self.legendTree.takeTopLevelItem(inti)
                                grp = sublayer(self.legendTree,leginterface,"","","",force_gruppenname)
                                grp.insertChild(0,kindi)    #layer qtreewidgetitem wird als child in das self.gruppen qtreewidgetitem eingebettet


                            if nach_unten:   #ganz nach unten mit der Gruppe des Layers wenn das flag gesetzt ist

                                if not self.gruppe_vorhanden:
                                    dodl = self.legendTree.takeTopLevelItem(0)  #die neue gruppe ist ganz oben
                                    unten = self.legendTree.topLevelItemCount()
                                    self.legendTree.insertTopLevelItem(unten,dodl)    #und dann an den letzten Platz gesetzt


                        else:   #die Layer werden NICHT in einen self.gruppenlayer geladen
                                #sollen aber nach unten verschoben werden
                            if nach_unten:
                                dodl = self.legendTree.takeTopLevelItem(0)
                                self.legendTree.insertTopLevelItem(self.legendTree.topLevelItemCount() - n,dodl)
                                n = n+1     #bewirkt praktisch ein "Spiegeln" beim runterschieben: sonst stehen die Layer
                                            #in der Reihenfolge auf dem Kopf


                        #der nachfolgende Code erzwingt eine Aktualisierung
                        #der Legende und des MapWindow
                        #Ansonsten kanns im Mapwindow Darstellungsprobleme geben! Wieso??
                        if not self.lyr is None:

                            anzeigename = self.lyr.name()
                            self.lyr.setLayerName(anzeigename+" ")
                            self.lyr.setLayerName(anzeigename)
                        else:
                            QtGui.QMessageBox.about(None, "Achtung", "Layer " + self.legends.item(j).attributes().namedItem("name").nodeValue() + " nicht gefunden!")

                        #Unbedingt zurücksetzen sonst kanns beim wiederholten
                        #laden des gleichen Projektfiles einen Fehler geben:
                        #wenn nämlich die Schleife erneut beginnt, nicht lädt und self.lyr
                        #beim vorherigen laden steht!
                        self.lyr = None


        #Ganz wichtig: Bei Layern die über das Projektladen
        #ihren self.gruppen zugeteilt werden (bis zu 4 Hierarchien) werden zuerst die self.gruppen
        #angelegt. In eine Listenvariable werden dann die Objekte vom typ paar geschrieben die alles
        #enthalten, um die layer dann in die richtige self.gruppenhierarchie und dort an die richtige stelle
        #einzusetzen. das ist zentral und geschieht in der nachfolgenden schleife
        #QtGui.QMessageBox.about(None, "Top Level Items Count", "schleife")
        #return
        for zuordnung in self.paarliste:

            dummy_2 = object
            inti_2 = self.legendTree.indexOfTopLevelItem(zuordnung.layer)

            if inti_2 > -1:
                dummy_2 = self.legendTree.takeTopLevelItem(inti_2)  #der geladene Layer wird ausgeschnitten

                zuordnung.gruppe.addChild(dummy_2)


                #für die Layer die in eine Gruppe kommen,
                if zuordnung.expanded:  #prüfen ob der Layer aufgeklappt ist oder nicht (geht nur hier, da wie bei checked erst ab version 2.0 möglich!
                    self.legendTree.expandItem(dummy_2)
                else:
                    self.legendTree.collapseItem(dummy_2)
                zuordnung.gruppe.sortChildren(1,QtCore.Qt.AscendingOrder)


                #der nachfolgende Code erzwingt eine Aktualisierung
                #der Legende und des MapWindow
                #Ansonsten kanns im Mapwindow Darstellungsprobleme geben! Wieso??
                texti =  dummy_2.text(0)
                dummy_2.setText(0,texti + " ")
                dummy_2.setText(0,texti)

        #UNBEDINGT QGis wieder auf den usprünglichen
        #Pfad zurücksetzen
##        self.legendTree.update()
        QgsProject.instance().setFileName(CurrentPath)

        #ACHTUNG: Aus irgendeinem Grund gibts Probleme mit den Gruppenlayer: Wenn innerhalb der so angelegten Gruppen
        # ein Layer ausgewählt wird, gibts beim Laden danach einen Fehler. Es MUSS deshalb der oberste Eintrag
        # der Legende vor allem Laden als Aktueller Layer gesetzt werden!!!
        self.legendTree.setCurrentItem(self.legendTree.topLevelItem(0))

        #Objekte besser löschen
        self.legends = None
        self.legendTree = None

        self.maps = None
        self.legends = None
        self.gruppen = None



        #prüfen ob alle Layer der Liste geladen wurden
        #das ist notwendig, da ja beim Projektladen alles passen kann aber
        #ein Layer nicht vorhanden ist
        fehler = 0
        layerzaehler = 0



        if liste  <> None:  #wenn nur ein Teil der Layer eines Projekts geladen werden sollen. Die Liste enthält die
                            #Namen dieser Layer
            for nd in range(len(liste)):
                for lyr_tmp in leginterface.layers(): #alle bereits geladenen Layer durchgehen

                    #Unbedingt die optionale Änderung des
                    #Anzeigenamens (z.B. DKM) mitberücksichtigen!)
                    if (ergaenzungsname != None) and self.anzeigename_aendern:
                        #QtGui.QMessageBox.about(None, "Achtung", lyr_tmp.name() + " = " + )
                        if  liste[nd] + "-" + ergaenzungsname == lyr_tmp.name():

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


#Eine Klasse die eigentlich nur
#die Definition einer Strukt Variable enthält
#trägt die informationen: layer, übergeordnete gruppe und position (index) in diese gruppe)
class paar():
    def init(self):
        gruppe = QtCore.QObject()
        layer = QtGui.QTreeWidgetItem()
        index = 0
        expanded = True


# Gibt ein Dictionary zurück mit den gewünschten Informationen
# aus dem Qgis Projekt(XML)file
def getLegendInfo(mapDom):

    # Inhalt layerid
    layerid = mapDom.namedItem("layerid").firstChild().toText().data()
    # Inhalt checked (also Kreuzchen)
    checked = mapDom.namedItem("checked").firstChild().toText().data()


    return {'layerid':layerid,'checked':checked}


# Returns the absolute legend index of
# a group name.
# (c) Stefan Ziegler
# wird vor allem von anderen Modulen benötigt, hier allerdings nicht
def getGroupIndex(leginterface, groupName):
    relationList = leginterface.groupLayerRelationship()
    i = 0
    for item in relationList:
        if item[0] == groupName:
            i = i # + 1
            return i
        i = i + 1

    return 0



#Die Funktion sublayer ist macht hat folgendes ziel: sie gibt das qtreewidget objekt der gruppe zurück
#das einem layer unmittelbat übergeordnet ist. warum ist das so kompliziert? da die self.gruppen, nicht so wie die layer,
#im qgis projektfile über keinen index verfügen, gleichzeitig aber self.gruppennamen mehrfach vorkommen können, ist die zuordnung sehr schwierig. zumal wir ja nicht immer das
#ganze projekt laden sondern oft nur bestimmte layer die in self.gruppen verschachtelt sind. somit ist eine klare zuordnung, wenn nicht das gesamte projekt
#der reihe nach geladen wird (der raihe nach ist dann die zuordnung) nicht möglich. hier werden 4 self.gruppenhierarchien unterstützt. um eine art zurodnung des
#layer zu einer gruppe zu ermöglichen, wird aus den namen der self.gruppen der hierarchie eine signatur gebildet. diese ist einfach ein textstring mit
#den namen aneinandergehängt. auf dies weise ist eine art zuordnung möglich. wenn 4 hierarchieebenen über dem layer liegen besteht die
#signatur aus den 4 self.gruppennamen, sonst halt weniger. mehr ist leider nicht möglich um die zuordnung zu bestimmen!
def sublayer(legendtree,leginterface,gruppe_1 = "",gruppe_2 = "",gruppe_3 = "",gruppe_4 = "",index_1 = 0, index_2 = 0, index_3 = 0, index_4 = 0, ex_g1 = "", ex_g2 = "", ex_g3 = "", ex_g4 = "",
                                                                                                ch_g1 = "", ch_g2 = "", ch_g3 = "", ch_g4 = ""):

    #der algorithmus in dieser funktion macht es notwendig,
    #dass die variablenzuordnung abgeändert wird wenn nicht
    #alle self.gruppennamen belegt sind. also denk dir nichts dabei
    #ist nur kompliziert programmiert...
    if  gruppe_1 == "" and gruppe_2 == "" and gruppe_3 == "":
        gruppe_1 = gruppe_4
        index_1 = index_4
        ex_g1 = ex_g4
        ch_g1 = ch_g4
        gruppe_2 = ""
        gruppe_3 = ""
        gruppe_4 = ""
        itemliste = legendtree.findItems(gruppe_1,QtCore.Qt.MatchRecursive,0)
    elif gruppe_1 == "" and gruppe_2 == "": #dann ist auch gruppe_1 = 0
        gruppe_1 = gruppe_3
        index_1 = index_3
        ex_g1 = ex_g3
        ch_g1 = ch_g3
        gruppe_2 = gruppe_4
        index_2 = index_4
        ex_g2 = ex_g4
        ch_g2 = ch_g4
        gruppe_3 = ""
        gruppe_4 = ""
        itemliste = legendtree.findItems(gruppe_2,QtCore.Qt.MatchRecursive,0)
    elif gruppe_1 == "":
        gruppe_1 = gruppe_2
        index_1 = index_2
        ex_g1 = ex_g2
        ch_g1 = ch_g2
        gruppe_2 = gruppe_3
        index_2 = index_3
        ex_g2 = ex_g3
        ch_g2 = ch_g3
        gruppe_3 = gruppe_4
        index_3 = index_4
        ex_g3 = ex_g4
        ch_g3 = ch_g4
        gruppe_4 = ""
        itemliste = legendtree.findItems(gruppe_3,QtCore.Qt.MatchRecursive,0)
    else:
        itemliste = legendtree.findItems(gruppe_4,QtCore.Qt.MatchRecursive,0)

    #die signatur, wird aus den namen der self.gruppen (so vorhanden) gebildet
    #diese darf in der Legende nur einmal vorkommen, sonst ist eine
    #Unterscheidung nicht möglich!
    signatur = gruppe_4 +  gruppe_3 +  gruppe_2 +  gruppe_1

    index = None
    allesgefunden = False

    if len(itemliste) > 0:  #dann ist die dem Layer übergeordnete gruppe irgendwo vorhanden!
                            #aber nicht unbedingt die gesamte signatur in die der layer reinmuss
                            #das muss nachfolgend iterativ geprüft werden (wenn itemliste = 0 kann ich mir das halt sparen, mehr nicht)

        #deshalb mu die signatur für die passenden self.gruppen
        #iterativ abgeprüft werden. wieder umständlich programmiert...
        for item in itemliste:
            dummysig = item.text(0)
            if (not item.parent() is None):
                dummysig = dummysig + item.parent().text(0)
                if (not item.parent().parent() is None):
                    dummysig = dummysig + item.parent().parent().text(0)
                    if (not item.parent().parent().parent() is None):
                        dummysig = dummysig + item.parent().parent().parent().text(0)

            if dummysig == signatur:    #die gesamte hierarchie in die der layer reinsoll ist gefunden!
                index = item            #wir können abbrechen, das rückgabeobjekt setzen und die funktion dann verlassen
                allesgefunden = True
                #QtGui.QMessageBox.about(None, "Allesgefundenn", "Gruppe = " +item.text(0) + " " + signatur)
                break

    #die notwendige hierarchie (signatur) wird nicht gefunden, etwas oder
    #alles fehlt. das wird nun hier kompliziert überprüft und
    #auch gleich erledigt (gruppe wird angelegt)
    #wichtig ist auch folgendes: 1 bedeutet die oberste gruppe, 4 die unterste in der hierarchie!
    if not allesgefunden:


        if not gruppe_1 == "" and not (len(legendtree.findItems(gruppe_1,QtCore.Qt.MatchRecursive,0) )> 0): #gruppe gibts nicht
            leginterface.addGroup(gruppe_1,False,None) #wird angelegt

            tmp = legendtree.currentItem()
            index_neu = legendtree.indexOfTopLevelItem(tmp)
            index = legendtree.takeTopLevelItem(index_neu)  #es ist notwendig die oberste gruppe nach oben zu schieben
            legendtree.insertTopLevelItem(0,index)


            #ist die neue Gruppe aufgeklappt?
            if ex_g1 == "true":
                legendtree.expandItem(index)
            elif ex_g1 == "false":
                legendtree.collapseItem(index)
            #ist die neue Gruppe gechecked?
            if ch_g1 == "Qt::Unchecked":
                index.setCheckState(0,0)
            elif ch_g1 == "Qt::PartiallyChecked":
                index.setCheckState(0,1)
            elif ch_g1 == "Qt::PartiallyChecked":
                index.setCheckState(0,2)

            legendtree.setCurrentItem(index) #sonst gibts Probleme mit der Reihenfolge wenn danach Normale LAyer geladen werden
            index.setData(1,0,0)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

        elif not gruppe_1 == "" and (len(legendtree.findItems(gruppe_1,QtCore.Qt.MatchRecursive,0) )> 0):# gruppe gibts
            index = legendtree.findItems(gruppe_1,QtCore.Qt.MatchRecursive,0)[0]

        if not gruppe_2 == ""and not (len(legendtree.findItems(gruppe_2,QtCore.Qt.MatchRecursive,0)) > 0): #gruppe gibts nicht, brauchts aber
            parent_klappe = index.isExpanded()

            #Gruppe einfügen und
            leginterface.addGroup(gruppe_2,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
            tmp = legendtree.currentItem()
            neu_index = index.indexOfChild(tmp)
            #dann rausnehmen
            kindi = index.takeChild(neu_index)
            index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!


            #durch das Einfügen einer Gruppe
            #wird die darüberliegende blödsinnigerweise ausgeklappt
            #also auf vorherigen Zustand zurücksetzen
            if not parent_klappe:
                legendtree.collapseItem(index)
            index = kindi       #nun das "neue" qtreewidget objekt zuweisen

            #ist die nue Gruppe aufgeklappt?
            if ex_g2 == "true":
                legendtree.expandItem(index)
            elif ex_g2 == "false":
                legendtree.collapseItem(index)
            #ist die neue Gruppe gechecked?
            if ch_g2 == "Qt::Unchecked":
                index.setCheckState(0,0)
            elif ch_g2 == "Qt::PartiallyChecked":
                index.setCheckState(0,1)
            elif ch_g2 == "Qt::PartiallyChecked":
                index.setCheckState(0,2)

            index.setData(1,0,index_2)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

        elif not gruppe_2 == "" and (len(legendtree.findItems(gruppe_2,QtCore.Qt.MatchRecursive,0) )> 0):# gruppe gibts

            #stimmt aber die hierarchie auch, d.h. ist die übergeordnete gruppe die gruppe1?
            obe = False
            for subitem in legendtree.findItems(gruppe_2,QtCore.Qt.MatchRecursive,0): # hierarchie paßt, kein neuanlegen nötig
                if not  subitem.parent() is None:
                    if subitem.parent().text(0) == gruppe_1:
                        index = subitem      #nun das "neue" qtreewidget objekt zuweisen
                        obe = True
                        break
            if not obe: #oje, den self.gruppenname gibts bereits, aber in einer anderen hierarchie, die übergeordnete gruppe
                        #entspricht nicht der, den signatur fordert. also neu anlegen, in der benötigten hierarchie!
                parent_klappe = index.isExpanded()

                #Gruppe einfügen und
                leginterface.addGroup(gruppe_2,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
                tmp = legendtree.currentItem()
                neu_index = index.indexOfChild(tmp)
                # dann rausnehmen
                kindi = index.takeChild(neu_index)
                index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!

                #durch das Einfügen einer Gruppe
                #wird die darüberliegende blödsinnigerweise ausgeklappt
                #also auf vorherigen Zustand zurücksetzen
                if not parent_klappe:
                    legendtree.collapseItem(index)
                index = kindi   #nun das "neue" qtreewidget objekt zuweisen

                #ist die neue Gruppe aufgeklappt?
                if ex_g2 == "true":
                    legendtree.expandItem(index)
                elif ex_g2 == "false":
                    legendtree.collapseItem(index)
                #ist die neue Gruppe gechecked?
                if ch_g2 == "Qt::Unchecked":
                    index.setCheckState(0,0)
                elif ch_g2 == "Qt::PartiallyChecked":
                    index.setCheckState(0,1)
                elif ch_g2 == "Qt::PartiallyChecked":
                    index.setCheckState(0,2)
                    index.setData(1,0,index_2)    #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)


        if not gruppe_3 == ""and not (len(legendtree.findItems(gruppe_3,QtCore.Qt.MatchRecursive,0) )> 0): #gruppe gibts nicht, brauchts aber
            parent_klappe = index.isExpanded()

            #Gruppe einfügen und
            leginterface.addGroup(gruppe_3,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
            tmp = legendtree.currentItem()
            neu_index = index.indexOfChild(tmp)
            # dann rausnehmen
            kindi = index.takeChild(neu_index)
            index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!


            #durch das Einfügen einer Gruppe
            #wird die darüberliegende blödsinnigerweise ausgeklappt
            #also auf vorherigen Zustand zurücksetzen
            if not parent_klappe:
                    legendtree.collapseItem(index)
            index = kindi       #nun das "neue" qtreewidget objekt zuweisen

            #ist die neue Gruppe aufgeklappt?
            if ex_g3 == "true":
                legendtree.expandItem(index)
            elif ex_g3 == "false":
                legendtree.collapseItem(index)
            #ist die neue Gruppe gechecked?
            if ch_g3 == "Qt::Unchecked":
                index.setCheckState(0,0)
            elif ch_g3 == "Qt::PartiallyChecked":
                index.setCheckState(0,1)
            elif ch_g3 == "Qt::PartiallyChecked":
                index.setCheckState(0,2)

            index.setData(1,0,index_3)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

        elif not gruppe_3 == "" and (len(legendtree.findItems(gruppe_3,QtCore.Qt.MatchRecursive,0) )> 0):# gruppe gibts

             #stimmt aber die hierarchie auch, d.h. ist die übergeordnete gruppe die gruppe2?
            obe = False
            for subitem in legendtree.findItems(gruppe_3,QtCore.Qt.MatchRecursive,0): # hierarchie paßt, kein neuanlegen nötig
                if not  subitem.parent() is None:
                    if subitem.parent().text(0) == gruppe_2:
                        index = subitem      #nun das "neue" qtreewidget objekt zuweisen
                        obe = True
                        break
            if not obe: #oje, den self.gruppenname gibts bereits, aber in einer anderen hierarchie, die übergeordnete gruppe
                        #entspricht nicht der, den signatur fordert. also neu anlegen, in der benötigten hierarchie!
                parent_klappe = index.isExpanded()

                #Gruppe einfügen und
                leginterface.addGroup(gruppe_3,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
                tmp = legendtree.currentItem()
                neu_index = index.indexOfChild(tmp)
                # dann rausnehmen
                kindi = index.takeChild(neu_index)
                index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!


                #durch das Einfügen einer Gruppe
                #wird die darüberliegende blödsinnigerweise ausgeklappt
                #also auf vorherigen Zustand zurücksetzen
                if not parent_klappe:
                    legendtree.collapseItem(index)
                index = kindi       #nun das "neue" qtreewidget objekt zuweisen

                #ist die neue Gruppe aufgeklappt?
                if ex_g3 == "true":
                    legendtree.expandItem(index)
                elif ex_g3 == "false":
                    legendtree.collapseItem(index)
                #ist die neue Gruppe gechecked?
                if ch_g3 == "Qt::Unchecked":
                    index.setCheckState(0,0)
                elif ch_g3 == "Qt::PartiallyChecked":
                    index.setCheckState(0,1)
                elif ch_g3 == "Qt::PartiallyChecked":
                    index.setCheckState(0,2)

                index.setData(1,0,index_3)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

        if not gruppe_4 == ""and not (len(legendtree.findItems(gruppe_4,QtCore.Qt.MatchRecursive,0) )> 0): #gruppe gibts nicht, brauchts aber
            parent_klappe = index.isExpanded()

            #Gruppe einfügen und
            leginterface.addGroup(gruppe_4,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
            tmp = legendtree.currentItem()
            neu_index = index.indexOfChild(tmp)
            # dann rausnehmen
            kindi = index.takeChild(neu_index)
            index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!


            #durch das Einfügen einer Gruppe
            #wird die darüberliegende blödsinnigerweise ausgeklappt
            #also auf vorherigen Zustand zurücksetzen
            if not parent_klappe:
                    legendtree.collapseItem(index)
            index = kindi       #nun das "neue" qtreewidget objekt zuweisen

            #ist die neue Gruppe aufgeklappt?
            if ex_g4 == "true":
                legendtree.expandItem(index)
            elif ex_g4 == "false":
                legendtree.collapseItem(index)
            #ist die neue Gruppe gechecked?
            if ch_g4 == "Qt::Unchecked":
                index.setCheckState(0,0)
            elif ch_g4 == "Qt::PartiallyChecked":
                index.setCheckState(0,1)
            elif ch_g4 == "Qt::PartiallyChecked":
                index.setCheckState(0,2)

            index.setData(1,0,index_4)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

        elif not gruppe_4 == "" and (len(legendtree.findItems(gruppe_4,QtCore.Qt.MatchRecursive,0) )> 0):# gruppe gibts

             #stimmt aber die hierarchie auch, d.h. ist die übergeordnete gruppe die gruppe3?
            obe = False
            for subitem in legendtree.findItems(gruppe_4,QtCore.Qt.MatchRecursive,0): # hierarchie paßt, kein neuanlegen nötig
                if not  subitem.parent() is None:
                    if subitem.parent().text(0) == gruppe_3:
                        index = subitem     #nun das "neue" qtreewidget objekt zuweisen
                        obe = True
                        break
            if not obe: #oje, den self.gruppenname gibts bereits, aber in einer anderen hierarchie, die übergeordnete gruppe
                        #entspricht nicht der, den signatur fordert. also neu anlegen, in der benötigten hierarchie!
                parent_klappe = index.isExpanded()

                #Gruppe einfügen und
                leginterface.addGroup(gruppe_4,False,index) #wird angelegt und in die übergeordnete gruppe eingebettet (parent)
                tmp = legendtree.currentItem()
                neu_index = index.indexOfChild(tmp)
                # dann rausnehmen
                kindi = index.takeChild(neu_index)
                index.insertChild(0,kindi)  #ganz vorne einfügen, damit sie immer an einem defineirten Platz ist!!


                #durch das Einfügen einer Gruppe
                #wird die darüberliegende blödsinnigerweise ausgeklappt
                #also auf vorherigen Zustand zurücksetzen
                if not parent_klappe:
                    legendtree.collapseItem(index)
                index = kindi       #nun das "neue" qtreewidget objekt zuweisen

                #ist die neue Gruppe aufgeklappt?
                if ex_g4 == "true":
                    legendtree.expandItem(index)
                elif ex_g4 == "false":
                    legendtree.collapseItem(index)
                #ist die neue Gruppe gechecked?
                if ch_g4 == "Qt::Unchecked":
                    index.setCheckState(0,0)
                elif ch_g4 == "Qt::PartiallyChecked":
                    index.setCheckState(0,1)
                elif ch_g4 == "Qt::PartiallyChecked":
                    index.setCheckState(0,2)

                index.setData(1,0,index_4)  #das data attribut des objektes bekommt den positionsindex für die reihenfolge (wird übergeben - hatte keine bessere idee)

    return index


#diese unterprogramm gibt die reihengolge der position (index)
#in der legende zurück. die identifikation geht über das attribut name (haben self.gruppen und layer)
#quelle dafür ist das qgis projektfile
def index_zuweisen(name,aktual_dom_node):
    counter = 0
    positionsliste = aktual_dom_node.childNodes()
    while counter < positionsliste.count():
        if positionsliste.item(counter).attributes().namedItem("name").nodeValue() == name:
            break
        counter = counter + 1

    return counter

