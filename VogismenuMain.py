# -*- coding: utf-8 -*-



# Die Kernbibliotheken für
# Qgis und PyQT importieren
# (Gegebenenfalls läßt sich diese Auswahl
# noch verfeinern)
from PyQt4 import QtCore, QtGui, QtXml
from qgis import core
#from ladefortschritt import *
#from qgis.core import *
#from LayerDialog import *


import sys, os.path,string
import threading, locale


# Unbedingt den Pfad setzen damit die anderen Module gefunden werden
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/standardlayout'))

from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich


from doBlattschnitte import *
from doAdresssuche_pg import *
from doAdresssuche_sqlite import *
from doGstsuche_pg import *
from doGstsuche_sqlite import *
from ProjektImport import *
from doGeonamsuche import *
from doAbfall import *
from doBoden import *
from doLuftbilder import *
from doFWP import *
from doGFZ import *
from doHoehenmodell import *
from doNaturschutz import *
from doVerkehr import *
from doVogisPrint import *
from doEnergie import *
from doWasser import *
from doGrenzen import *
from doJagd import *
from doLandnutzung import *
from doLandwirtschaft import *
from doPointsofInterest import *
from doRaumplanung import *
from doSiedlungen import *
from doGeologie import *
from doTopokarten import *
from doWald import *
from doKlima import *
from doVermessung import *
from doFischerei import *





class VogismenuMain(QtCore.QObject):    # Die Vererbung von QtCore.Qobject benötigen
    def __init__(self, iface):          # wir für den Aufruf self.sender() in der Methode
        QtCore.QObject.__init__(self)   # projectimport die als Slot agiert. Dadurch weiß die Slotmethode
                                        # von wo das Signal kommt!



        #Instanzvariablen

        #Referenz auf das Qgis Interface übergeben
        self.iface = iface
        self.vogisPfad = ""
        self.speicheradressen_adressuche =[]    #darauf werden die Adressen der Adressuche Grafiken gespeichert
                                                #solange das Vogis Menü geladen ist können sie immer wieder gelöscht werden
                                                #vom Dialogfeld Adressuche aus (da Listen Pointer sind!)
        self.speicheradressen_hoehenmodell = []

        self.vermessung_offen = []  #damits ein pointer ist

        #die ganzen Subfenster, damits sauberer läuft
        self.AdresssucheDialog = None
        self.GstsucheGUI = None
        self.FWP = None
        self.GFZ = None
        self.naturschutz = None
        self.hoehenmodell = None
        self.vermessung = None
        self.vogisaction = None
        self.PGdb = None

        #nun was skuriles: weil es immer wieder probleme gibt, wenn mehrere instanze
        #auf eine sqlserver datenbank zugreifen (?) darf keine zweite instanz
        #der GUI vermessung aufgemacht werden. damits ein pointer ist, hab ich
        #unsauberweise eine Liste verwendet (weil es kein Boolean Pointer gibt)
        self.vermessung_offen.append(False)

        #Initialtest: Sind nicht bestimmte Grundvoraussetzungen
        #vorhanden, macht das Starten des VoGIS Menü keinen Sinn


        #die vogisini datei oeffnen
        #erstmal nur um zu lesen
        Flagge = False
        try:
            #file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","r")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
            file = open(os.getenv('HOME') + os.sep + "vogisini.xml","r")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
            xml = file.read()
            d = QtXml.QDomDocument()
            d.setContent(xml)   #d enthält das gesamnte XML
            file.close()
            Flagge = True
        except IOError:
            self.doVogisOptions()


        if Flagge:  #vogisin.xml konnte gelesen werden

            #den Tag mainpath abfragen (Nodeliste mit nur einem Element in userem Fall)
            mainpath = d.elementsByTagName("mainpath")
            encoding = d.elementsByTagName("encoding")
            kbs = d.elementsByTagName("kbs")
            db = d.elementsByTagName("db")

            #Den Textinhalt (Pfad) des VoGIS Laufwerks einlesen
            self.vogisPfad = mainpath.item(0).toElement().firstChild().toText().data()
            self.vogisEncoding = encoding.item(0).toElement().firstChild().toText().data()
            self.vogisKBS = kbs.item(0).toElement().firstChild().toText().data()
            self.vogisDb = db.item(0).toElement().firstChild().toText().data()

            #prüfen ob alles belegt ist, ansonsten die vogisini komplett neu schreiben
            #mit Standardwerten!

            if not ((self.vogisEncoding == 'menue' or self.vogisEncoding == 'project') and (self.vogisKBS == 'menue' or self.vogisKBS == 'project')):
                QtGui.QMessageBox.critical(None, "Fehler", os.getenv('HOME') + os.sep + ( "vogisini.xml scheint beschädigt - bitte kontrollieren sie die Einstellungen!!").decode("utf-8"))
                self.doVogisOptions()

            #Zur Sicherheit nochmal prüfen ob der Vogis Pfad gefunden werden kann
            if not os.path.exists(self.vogisPfad):
                self.doVogisOptions()

            #die modulübergreifenden globalen Variablen belegen
            #werden dann auch im Modul Projektimport verwendet
            del vogisEncoding_global[:]   #neu initialisieren
            del vogisKBS_global[:]
            del vogisDb_global[:]
            vogisEncoding_global.append(self.vogisEncoding)
            vogisKBS_global.append (self.vogisKBS)
            vogisDb_global.append (self.vogisDb)

            # Postgres DB initialisieren
            self.initPGDB()

        else:
            self.unload()


    def initPGDB(self):

        #############################################################################
        # Das Umschalten der Vektordaten auf die Geodatenbank - unter Bedingungen
        #############################################################################
        if vogisDb_global[0] != '':


            ##########################################
            # testen, ob die DB geöffnet werden kann
            # und wenn ja, Datenbankobjekt Instanzieren
            ###########################################
            dbpath = string.lower(vogisDb_global[0] + ' sslmode=disable  (the_geom) sql=')
            param_list = string.split(dbpath)

            host = ''
            dbname=''
            port=''
            #QtGui.QMessageBox.about(None, "Achtung", str(param_list))
            for param in param_list:

                if string.find(param,'dbname') >= 0:
                    dbname = string.replace(param,'dbname=','')
                elif string.find(param,'host=') >= 0:
                    host = string.replace(param,'host=','')
                elif string.find(param,'port=') >= 0:
                    port = string.replace(param,'port=','')

            # Username falls benötigt
            #username = getpass.getuser().lower()

            # Wir verwenden die Windows Domänen Authentifizierung. Keine User notwendig
            self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht ie Verbindung individuell - sonst ist eine Default Verbindung
            self.PGdb.setHostName(host)
            self.PGdb.setPort(int(port))
            self.PGdb.setDatabaseName(dbname)

            ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist

            if not ok:
                QtGui.QMessageBox.about(None, "Fehler", 'Keine Verbindung zur Geodatenbank')
                return  #Zurück




    def initGui(self):



        #Das Vogis Menü mit seinen Unterpunkten, den Actions, definieren
        self.menuVogis = QtGui.QMenu()
        self.menuVogis.setObjectName(("menuVogis"))
        self.menuVogis.setTitle("VOGIS")

        self.actionGeonamsuche = QtGui.QAction(self.iface.mainWindow())
        self.actionGeonamsuche.setObjectName(("actionGeonamsuche"))
        self.actionGeonamsuche.setText(bytes("Suche Ort (ÖK50)").decode("utf-8"))

        self.actionAdresssuche = QtGui.QAction(self.iface.mainWindow())
        self.actionAdresssuche.setObjectName(("actionAdresssuche"))
        self.actionAdresssuche.setText("Suche Adresse")

        self.actionGstsuche = QtGui.QAction(self.iface.mainWindow())
        self.actionGstsuche.setObjectName(("actionGstsuche"))
        self.actionGstsuche.setText(("Suche Grundstück").decode('utf-8'))

        self.actionAbfall = QtGui.QAction(self.iface.mainWindow())
        self.actionAbfall.setObjectName(("actionAbfall"))
        self.actionAbfall.setText("Abfallwirtschaft")

        self.actionAdressen = QtGui.QAction(self.iface.mainWindow())
        self.actionAdressen.setObjectName(("actionAdressen"))
        self.actionAdressen.setText("Adressen")

        self.actionBoden = QtGui.QAction(self.iface.mainWindow())
        self.actionBoden.setObjectName(("actionBoden"))
        self.actionBoden.setText("Boden")

        self.actionLuftbilder = QtGui.QAction(self.iface.mainWindow())
        self.actionLuftbilder.setObjectName(("actionLuftbilder"))
        self.actionLuftbilder.setText("Bilddaten: Luft- und Satellitenbilder")

        self.actionBlattschnitte = QtGui.QAction(self.iface.mainWindow())
        self.actionBlattschnitte.setObjectName(("actionBlattschnitte"))
        self.actionBlattschnitte.setText("Blattschnitte")

        self.actionDKM = QtGui.QAction(self.iface.mainWindow())
        self.actionDKM.setObjectName(("actionDKM"))
        self.actionDKM.setText(("Digitaler Kataster (DKM), Urmappe, Gebäudeumrisse").decode("utf-8"))

        self.actionEnergie = QtGui.QAction(self.iface.mainWindow())
        self.actionEnergie.setObjectName(("actionEnergie"))
        self.actionEnergie.setText("Energieversorgung")

        self.actionFischerei = QtGui.QAction(self.iface.mainWindow())
        self.actionFischerei.setObjectName(("actionFischerei"))
        self.actionFischerei.setText("Fischerei")

        self.actionFWP = QtGui.QAction(self.iface.mainWindow())
        self.actionFWP.setObjectName(("actionFWP"))
        self.actionFWP.setText(("Flächenwidmung").decode("utf-8"))

        self.actionGFZ = QtGui.QAction(self.iface.mainWindow())
        self.actionGFZ.setObjectName(("actionGFZ"))
        self.actionGFZ.setText(("Gefahrenzonen"))

        self.actionGrenzen = QtGui.QAction(self.iface.mainWindow())
        self.actionGrenzen.setObjectName(("actionGrenzen"))
        self.actionGrenzen.setText(("Grenzen"))

        self.actionHoehenmodell = QtGui.QAction(self.iface.mainWindow())
        self.actionHoehenmodell.setObjectName(("actionHoehenmodell"))
        self.actionHoehenmodell.setText(("Höhenmodelle").decode("utf-8"))

        self.actionJagd = QtGui.QAction(self.iface.mainWindow())
        self.actionJagd.setObjectName(("actionJagd"))
        self.actionJagd.setText(("Jagd"))

        self.actionKlima = QtGui.QAction(self.iface.mainWindow())
        self.actionKlima.setObjectName(("actionKlima"))
        self.actionKlima.setText(("Klima"))


        self.actionLandnutzung = QtGui.QAction(self.iface.mainWindow())
        self.actionLandnutzung.setObjectName(("actionLandnutzung"))
        self.actionLandnutzung.setText(("Landnutzung"))

        self.actionLandwirtschaft = QtGui.QAction(self.iface.mainWindow())
        self.actionLandwirtschaft.setObjectName(("actionLandwirtschaft"))
        self.actionLandwirtschaft.setText(("Landwirtschaft"))


        self.actionNaturschutz = QtGui.QAction(self.iface.mainWindow())
        self.actionNaturschutz.setObjectName(("actionNaturschutz"))
        self.actionNaturschutz.setText(("Naturschutz"))

        self.actionPointsofInterest = QtGui.QAction(self.iface.mainWindow())
        self.actionPointsofInterest.setObjectName(("actionPointsofInterest"))
        self.actionPointsofInterest.setText(("Points of Interest"))

        self.actionRaumplanung = QtGui.QAction(self.iface.mainWindow())
        self.actionRaumplanung.setObjectName(("actionRaumplanung"))
        self.actionRaumplanung.setText(("Raumplanung"))

        self.actionSiedlungen = QtGui.QAction(self.iface.mainWindow())
        self.actionSiedlungen.setObjectName(("actionSiedlungen"))
        self.actionSiedlungen.setText(("Siedlungen"))

        self.actionVerkehr = QtGui.QAction(self.iface.mainWindow())
        self.actionVerkehr.setObjectName(("actionVerkehr"))
        self.actionVerkehr.setText(("Verkehr, Transport, Infrastruktur"))

        self.actionWasser = QtGui.QAction(self.iface.mainWindow())
        self.actionWasser.setObjectName(("actionWasser"))
        self.actionWasser.setText(("Wasser"))

        self.actionWald = QtGui.QAction(self.iface.mainWindow())
        self.actionWald.setObjectName(("actionWald"))
        self.actionWald.setText(("Wald"))


        self.actionGeologie = QtGui.QAction(self.iface.mainWindow())
        self.actionGeologie.setObjectName(("actionGeologie"))
        self.actionGeologie.setText("Geologie")

        self.actionTopokarten = QtGui.QAction(self.iface.mainWindow())
        self.actionTopokarten.setObjectName(("actionTopokarten"))
        self.actionTopokarten.setText("Topographische Karten")

        self.actionVermessung = QtGui.QAction(self.iface.mainWindow())
        self.actionVermessung.setObjectName(("actionVermessung"))
        self.actionVermessung.setText("Vermessung")

        self.actionVogisPrint = QtGui.QAction(self.iface.mainWindow())
        self.actionVogisPrint.setObjectName(("actionVogisPrint"))
        self.actionVogisPrint.setText(("VOGIS - Standardlayout"))

        self.actionVogisHilfe = QtGui.QAction(self.iface.mainWindow())
        self.actionVogisHilfe.setObjectName(("actionVogisHilfe"))
        self.actionVogisHilfe.setText(("VOGIS - Hilfe"))

        self.actionVogisOptions = QtGui.QAction(self.iface.mainWindow())
        self.actionVogisOptions.setObjectName(("actionVogisOptions"))
        self.actionVogisOptions.setText(("VOGIS - Menü Einstellungen").decode('utf8'))



        # Die Action-Untermenüpunkte dem Vogis Menüpunkt
        # dazuhängen
        self.menuVogis.addAction(self.actionGeonamsuche)
        self.menuVogis.addAction(self.actionAdresssuche)
        self.menuVogis.addAction(self.actionGstsuche)
        self.menuVogis.addSeparator()
        self.menuVogis.addAction(self.actionAbfall)
        self.menuVogis.addAction(self.actionAdressen)
        self.menuVogis.addAction(self.actionBoden)
        self.menuVogis.addAction(self.actionLuftbilder)
        self.menuVogis.addAction(self.actionBlattschnitte)
        self.menuVogis.addAction(self.actionDKM)
        self.menuVogis.addAction(self.actionEnergie)
        self.menuVogis.addAction(self.actionFischerei)
        self.menuVogis.addAction(self.actionFWP)
        self.menuVogis.addAction(self.actionGeologie)
        self.menuVogis.addAction(self.actionGFZ)
        self.menuVogis.addAction(self.actionGrenzen)
        self.menuVogis.addAction(self.actionHoehenmodell)
        self.menuVogis.addAction(self.actionJagd)
        self.menuVogis.addAction(self.actionKlima)
        self.menuVogis.addAction(self.actionLandnutzung)
        self.menuVogis.addAction(self.actionLandwirtschaft)
        self.menuVogis.addAction(self.actionNaturschutz)
        self.menuVogis.addAction(self.actionPointsofInterest)

        self.menuVogis.addAction(self.actionRaumplanung)
        self.menuVogis.addAction(self.actionSiedlungen)
        self.menuVogis.addAction(self.actionTopokarten)

        self.menuVogis.addAction(self.actionVerkehr)
        self.menuVogis.addAction(self.actionVermessung)
        self.menuVogis.addAction(self.actionWald)
        self.menuVogis.addAction(self.actionWasser)

        self.menuVogis.addSeparator()
        self.menuVogis.addAction(self.actionVogisPrint)
        self.menuVogis.addSeparator()
        self.menuVogis.addAction(self.actionVogisOptions)
        self.menuVogis.addAction(self.actionVogisHilfe)



        # Das Vogismenü in die Qgis Menüleiste einhängen. Self.Iface ist eine
        # Referenz auf das Qgis Interface. Zuerst wird die Menubar
        # des Haupfensters auf eine Instanz geholt und dann unser Vogismenü dazugehängt

        self.menu_bar = self.iface.mainWindow().menuBar()
        self.vogisaction = self.menu_bar.addMenu(self.menuVogis)

        # Mit der Connect Methode des QObject wird ein Signal Slot verhältnis erzeugt
        QtCore.QObject.connect(self.actionGeonamsuche,QtCore.SIGNAL("triggered()"),self.doGeonamsuche)
        QtCore.QObject.connect(self.actionAdresssuche,QtCore.SIGNAL("triggered()"),self.doAdresssuche)

        #QtCore.QObject.connect(self.actionGstsuche,QtCore.SIGNAL("triggered()"),self.doGstsuche)

        self.actionGstsuche.triggered.connect(self.doGstsuche)  #newstyle

        QtCore.QObject.connect(self.actionAbfall,QtCore.SIGNAL("triggered()"),self.doAbfall)
        QtCore.QObject.connect(self.actionAdressen,QtCore.SIGNAL("triggered()"),self.doAdresssuche)
        QtCore.QObject.connect(self.actionBoden,QtCore.SIGNAL("triggered()"),self.doBoden)
        QtCore.QObject.connect(self.actionLuftbilder,QtCore.SIGNAL("triggered()"),self.doLuftbilder)
        QtCore.QObject.connect(self.actionBlattschnitte,QtCore.SIGNAL("triggered()"),self.doBlattschnitte)
        QtCore.QObject.connect(self.actionDKM,QtCore.SIGNAL("triggered()"),self.doGstsuche)
        QtCore.QObject.connect(self.actionEnergie,QtCore.SIGNAL("triggered()"),self.doEnergie)
        QtCore.QObject.connect(self.actionFischerei,QtCore.SIGNAL("triggered()"),self.doFischerei)
        QtCore.QObject.connect(self.actionFWP,QtCore.SIGNAL("triggered()"),self.doFWP)
        QtCore.QObject.connect(self.actionGeologie,QtCore.SIGNAL("triggered()"),self.doGeologie)
        QtCore.QObject.connect(self.actionGFZ,QtCore.SIGNAL("triggered()"),self.doGFZ)
        QtCore.QObject.connect(self.actionGrenzen,QtCore.SIGNAL("triggered()"),self.doGrenzen)
        QtCore.QObject.connect(self.actionHoehenmodell,QtCore.SIGNAL("triggered()"),self.doHoehenmodell)
        QtCore.QObject.connect(self.actionJagd,QtCore.SIGNAL("triggered()"),self.doJagd)
        QtCore.QObject.connect(self.actionKlima,QtCore.SIGNAL("triggered()"),self.doKlima)
        QtCore.QObject.connect(self.actionLandnutzung,QtCore.SIGNAL("triggered()"),self.doLandnutzung)
        QtCore.QObject.connect(self.actionLandwirtschaft,QtCore.SIGNAL("triggered()"),self.doLandwirtschaft)
        QtCore.QObject.connect(self.actionNaturschutz,QtCore.SIGNAL("triggered()"),self.doNaturschutz)
        QtCore.QObject.connect(self.actionPointsofInterest,QtCore.SIGNAL("triggered()"),self.doPointsofInterest)

        QtCore.QObject.connect(self.actionRaumplanung,QtCore.SIGNAL("triggered()"),self.doRaumplanung)
        QtCore.QObject.connect(self.actionSiedlungen,QtCore.SIGNAL("triggered()"),self.doSiedlungen)
        QtCore.QObject.connect(self.actionTopokarten,QtCore.SIGNAL("triggered()"),self.doTopokarten)


        QtCore.QObject.connect(self.actionVerkehr,QtCore.SIGNAL("triggered()"),self.doVerkehr)
        QtCore.QObject.connect(self.actionVermessung,QtCore.SIGNAL("triggered()"),self.doVermessung)
        QtCore.QObject.connect(self.actionWald,QtCore.SIGNAL("triggered()"),self.doWald)
        QtCore.QObject.connect(self.actionWasser,QtCore.SIGNAL("triggered()"),self.doWasser)

        QtCore.QObject.connect(self.actionVogisPrint,QtCore.SIGNAL("triggered()"),self.doVogisPrint)
        QtCore.QObject.connect(self.actionVogisHilfe,QtCore.SIGNAL("triggered()"),self.doVogisHilfe)
        QtCore.QObject.connect(self.actionVogisOptions,QtCore.SIGNAL("triggered()"),self.doVogisOptions)



        #Die Objektvariable für die
        #Geonamgrafik initialisieren
        self.Geonamgrafik = None


        #Den DKM Stand auslesen
        try:
            f = open(self.vogisPfad + "Grenzen/DKM/_Allgemein/Stand.txt","r")
            self.dkmstand = f.readline()
        except IOError:
            self.dkmstand = "Kein DKM Stand!"

        #-------------------------------------------------------------------------#
        #Eintrag in die User-Logging-Tabelle

        #Referenz auf die Datenquelle
        #direkt über SQLITE
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
        dbpfad = self.vogisPfad + "_Allgemein/userreg/vogis_allgemein_db.sqlite"
        self.db.setDatabaseName(dbpfad);


        if os.path.exists(dbpfad) == 1: #sonst erzeugt open eine leer sqllitedb

            #nur wenn Öffnen OK
            if  self.db.open():
                import getpass
                username = getpass.getuser().lower()
                abfrage = QtSql.QSqlQuery(self.db)
                abfrage.exec_("SELECT starts  FROM qgis_user where user = '" + username + "'")

                if abfrage.first(): #user gefunden
                    abfrage.exec_("update qgis_user set starts = starts + 1 where user = '" + username + "'")
                    abfrage.exec_("update qgis_user set version = '1.2.7' where user = '" + username + "'")
                    abfrage.exec_("update qgis_user set qgis_version = '" + QGis.QGIS_VERSION + "' where user = '" + username + "'")
                    self.db.close()
                else: #user nicht gefunden, d.h. noch nicht vorhanden
                    abfrage.exec_("insert into qgis_user ("'user'", "'starts'", "'version'", "'qgis_version'") values ('" + username + "', 1 , '1.2.7', '" + QGis.QGIS_VERSION + "')")

                    self.db.close()

        #--------------------------------------------------------------------------#


        #den pfad richten
        self.vogisPfad=self.vogisPfad.replace("\\","/")

    def run(self):
         print "TestPlugin: run called!"

    def unload(self):
        #pass
        self.iface.removePluginMenu('Vogismenue', self.vogisaction)



    def doGeonamsuche(self):

        Path = self.vogisPfad + "Points_of_Interest/Ortsbezeichnung/Vlbg/oek_geonam/"
        #Path = "D:/"
        Name = "geonam"

        if vogisDb_global[0] == '':
            self.GeonamsucheDialog = Geonam(self.iface,Path,Name,self.Geonamgrafik)
        else:
            self.GeonamsucheDialog = Geonam(self.iface,Path,Name,self.Geonamgrafik,self.PGdb, Name)

        self.GeonamsucheDialog.exec_()   #Ergibt einen modalen Dialog: nur er ist für Input aktiv

        #ACHTUNG: Hier krieg ich eine IGraphicsItemGroup
        #zurück die alle Grafik Items enthält, die Geonams darstellen:
        #Dadurch habe ich das Objekt, welches alle Geonam Grafiken enthält
        #und kann so auch nur diese löschen ohne andere Grafik Items mitzulöschen
        #Die Methode Grafikreturn ist ein Slot für das Signal destroyed des
        #frames für die Geonamsuche. So wird das Objekt dem Vogismenü übergeben
        #und das Vogis Menü übergibt es wieder bei Aufruf der Geonamsuche. Dort wird wenn es leer ist ein neues erzeugt
        #oder das bestehende übernommen.!!
        self.Geonamgrafik = self.GeonamsucheDialog.grafikreturn()

    def doAdresssuche(self):


        # Das Postgis DB Objekt an die Einstellungen Anpassen
        if vogisDb_global[0] == '':
            self.PGdb = None


        Path = self.vogisPfad + "Points_of_Interest/Adressen/Vlbg/"
        Table = 'adressen'
        Schema = 'vorarlberg'
        #Name = 'adressen_tmp'

        #damit das Fenster nicht zweimal geöffnet wird!
        if self.AdresssucheDialog == None or self.AdresssucheDialog.objectName() == 'Bin_nicht_offen':

            # Unterschiedliche Module für Postgis bzw. SQLITE
            if vogisDb_global[0] != '':
                self.AdresssucheDialog = AdrDialogPG(self.iface.mainWindow(),self.iface,self.speicheradressen_adressuche,Path, self.PGdb, Schema, Table)
            else:
                self.AdresssucheDialog = AdrDialogSQLITE(self.iface.mainWindow(),self.iface,self.speicheradressen_adressuche,Path,Table)

            self.AdresssucheDialog.show()
            self.AdresssucheDialog.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.AdresssucheDialog.raise_()
            self.AdresssucheDialog.activateWindow()


    def doGstsuche(self):
        ProjektPath = self.vogisPfad + "Grenzen/DKM/Vorarlberg/DKM.qgs"
        #damit das Fenster nicht zweimal geöffnet wird!
        if self.GstsucheGUI == None or self.GstsucheGUI.objectName() == 'Bin_nicht_offen':

            # Unterschiedliche Module für Postgis bzw. SQLITE
            if vogisDb_global[0] != '':
                self.GstsucheGUI = GstDialogPG(self.iface.mainWindow(),self.iface,self.dkmstand,self.vogisPfad,self.PGdb)
                self.GstsucheGUI.show()
                self.GstsucheGUI.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
            else:
                self.GstsucheGUI = GstDialogSqlite(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad)
                self.GstsucheGUI.show()
                self.GstsucheGUI.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.GstsucheGUI.raise_()
            self.GstsucheGUI.activateWindow()

    def doAbfall(self):
        self.Abfall = AbfallDialog(self.iface,self.vogisPfad + "Ver_Entsorgung/Abfall/Vlbg")
        #window.show()
        self.Abfall.exec_()


    def doLuftbilder(self):
        ProjektPath = self.vogisPfad + "Luftbilder/"

        self.Luftbilder = LuftbilderDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath)
        self.Luftbilder.exec_()      # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht


    def doBlattschnitte(self):
        self.BlattschnittDialog = BlsDialog(self.iface,self.vogisPfad + "Blattschnitte/Vlbg/Blattschnitte.qgs")
        self.BlattschnittDialog.exec_()  #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doBoden(self):
        ProjektPath = self.vogisPfad + "Geologie/Bodenkartierung/Vlbg/"

        self.boden = BodenDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.boden.exec_()

    def doEnergie(self):
        self.Energie = EnergieDialog(self.iface,self.vogisPfad + "Ver_Entsorgung/Energie/Vlbg")
        #window.show()
        self.Energie.exec_()

    def doFischerei(self):
        ProjektPath = self.vogisPfad + "Wasser/Fischerei"
        fischerei = FischereiDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        fischerei.exec_()

    def doFWP(self):
        ProjektPath = self.vogisPfad + "Raumplanung/Flaechenwidmung/"

        if self.FWP == None or self.FWP.objectName() == 'Bin_nicht_offen':
            self.FWP = FWPDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad)
            self.FWP.show()
            self.FWP.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.FWP.raise_()
            self.FWP.activateWindow()



    def doGFZ(self):
        ProjektPath = self.vogisPfad + "Gefahren/Gefahrenzonenplan/"


        if self.GFZ == None or self.GFZ.objectName() == 'Bin_nicht_offen':
            self.GFZ = GFZDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad)
            self.GFZ.show()       # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht
                        # hinter dem parent window verschwindet
            self.GFZ.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.GFZ.raise_()
            self.GFZ.activateWindow()

    def doNaturschutz(self):
        ProjektPath = self.vogisPfad + "Naturschutz/"

        if self.naturschutz == None or self.naturschutz.objectName() == 'Bin_nicht_offen':
            self.naturschutz = NaturschutzDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad)
            self.naturschutz.show()

            self.naturschutz.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.naturschutz.raise_()
            self.naturschutz.activateWindow()

    def doVerkehr(self):
        ProjektPath = self.vogisPfad + "Verkehr/"
        self.verkehr = VerkehrDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad)
        self.verkehr.exec_()

    def doWasser(self):
        ProjektPath = self.vogisPfad + "Wasser/"
        self.wasser = WasserDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.wasser.exec_()

    def doGrenzen(self):
        ProjektPath = self.vogisPfad + "Grenzen/Verwaltungsgrenzen"
        self.grenzen = GrenzenDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.grenzen.exec_()

    def doHoehenmodell(self):
        ProjektPath = self.vogisPfad + "Gelaendemodelle"


        if self.hoehenmodell == None or self.hoehenmodell.objectName() == 'Bin_nicht_offen':
            self.hoehenmodell = HoehenmodellDialog(self.iface.mainWindow(),self.iface,self.speicheradressen_hoehenmodell,ProjektPath,self.vogisPfad)
            self.hoehenmodell.show()

            self.hoehenmodell.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.hoehenmodell.raise_()
            self.hoehenmodell.activateWindow()

    def doJagd(self):
        ProjektPath = self.vogisPfad + "Forstwesen/Jagd"
        self.jagd = JagdDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.jagd.exec_()

    def doKlima(self):
        ProjektPath = self.vogisPfad + "Klima"
        #ProjektPath = "V:/_Allg/Uebergabe/UI/Herbert/Klima"
        self.klima = KlimaDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.klima.exec_()    #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                        #sondt müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doLandnutzung(self):
        ProjektPath = self.vogisPfad + "Raumplanung/Landnutzung"
        self.landnutzung = LandnutzungDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.landnutzung.exec_()

    def doLandwirtschaft(self):
        ProjektPath = self.vogisPfad + "Landwirtschaft"
        self.landwirtschaft = LandwirtschaftDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.landwirtschaft.exec_()

    def doPointsofInterest(self):
        ProjektPath = self.vogisPfad + "Points_of_Interest"
        self.pointsofinterest = PointsofInterestDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.pointsofinterest.exec_()

    def doRaumplanung(self):
        ProjektPath = self.vogisPfad + "Raumplanung"
        self.raumplanung = RaumplanungDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.raumplanung.exec_()

    def doSiedlungen(self):
        ProjektPath = self.vogisPfad + "Raumplanung/Siedlung"
        self.siedlungen = SiedlungenDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.siedlungen.exec_()

    def doGeologie(self):
        ProjektPath = self.vogisPfad + "Geologie"
        self.Geologie = GeologieDialog(self.iface,ProjektPath,self.vogisPfad)
        self.Geologie.exec_()            #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden
    def doTopokarten(self):
        ProjektPath = self.vogisPfad + "Topographische_Karten"
        self.Topokarten = TopokartenDialog(self.iface,ProjektPath,self.vogisPfad)
        self.Topokarten.exec_()          #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doWald(self):
        ProjektPath = self.vogisPfad + "Forstwesen/Wald/Vlbg"
        self.wald = WaldDialog(self.iface.mainWindow(),self.iface,ProjektPath)
        self.wald.exec_()     #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                        #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doVermessung(self):
        ProjektPath = self.vogisPfad + "Vermessung"

        #damit das Fenster nicht zweimal geöffnet wird

        if self.vermessung == None or self.vermessung.objectName() == 'Bin_nicht_offen':
            self.vermessung = VermessungDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad)
            if self.vermessung.ok == True:
                self.vermessung.show()
                self.vermessung.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
            else:
                self.vermessung = None
        else:
            self.vermessung.raise_()
            self.vermessung.activateWindow()



    def doVogisPrint(self):
        ProjektPath = self.vogisPfad
        self.VogisPrintGUI = VogisPrintDialog(self.iface,self.iface.mainWindow(),ProjektPath,self.dkmstand)
        # nicht modaler Dialog
        self.VogisPrintGUI.show()

    def doVogisHilfe(self):
        os.startfile(self.vogisPfad +  "_Allgemein/QGIS/QGIS2-VoGIS-Manual.pdf")



    #damit ich weiss wenn Fenster geschlossen ist
    def InstanzMarkieren(self,Instanz):
        Instanz.setObjectName('Bin_nicht_offen')

    def doVogisOptions(self):
        fenster = Options()
        fenster.exec_()

        #Die ini neu einlesen
        #damitdie Einstellungen gleich greifen
        #file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","r")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
        file = open(os.getenv('HOME') + os.sep + "vogisini.xml","r")
        xml = file.read()
        d = QtXml.QDomDocument()
        d.setContent(xml)   #d enthält das gesamnte XML
        file.close()

        #den Tag mainpath abfragen (Nodeliste mit nur einem Element in userem Fall)
        mainpath = d.elementsByTagName("mainpath")
        encoding = d.elementsByTagName("encoding")
        kbs = d.elementsByTagName("kbs")
        db = d.elementsByTagName("db")

        #Den geänderten Textinhalt (Pfad) des VoGIS Laufwerks einlesen
        #damit das Menü die geänderten Einstellung sofort verwendet!
        self.vogisPfad = mainpath.item(0).toElement().firstChild().toText().data()
        self.vogisEncoding = encoding.item(0).toElement().firstChild().toText().data()
        self.vogisKBS = kbs.item(0).toElement().firstChild().toText().data()
        self.vogisDb= db.item(0).toElement().firstChild().toText().data()

        #die modulübergreifenden globalen Variablen belegen
        #werden dann auch im Modul Projektimport verwendet
        del vogisEncoding_global[:]   #neu initialisieren
        del vogisKBS_global[:]
        del vogisDb_global[:]
        vogisEncoding_global.append(self.vogisEncoding)
        vogisKBS_global.append (self.vogisKBS)
        vogisDb_global.append (self.vogisDb)

        # Die Postgres datenbank gegebenenfalls neu instanzieren
        self.initPGDB()

#Klassendefinition für den Vogis Menüpukt
#Einstellungen
from gui_options import *
class Options (QtGui.QDialog, Ui_frmOptions):


    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_frmOptions.__init__(self)

        self.setupUi(self)
        self.d = QtXml.QDomDocument()
        self.mainpath = ''
        self.vogisPfad =''
        self.vogisEncoding = ''
        self.vogisKBS = ''
        self.vogisDb = ''
        #Filedialog Objekt
        self.dialog = QtGui.QFileDialog()
        self.dialog.setFileMode(QFileDialog.Directory)


        # Codepage bestimmen Sonderzeicehn im Pfad zum Benutzerhome)
        code_page =locale.getpreferredencoding()
        try:
            #file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","r")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
            file = open(os.getenv('HOME').decode(code_page) + os.sep + "vogisini.xml","r")
            xml = file.read()

            self.d.setContent(xml)   #d enthält das gesamnte XML
            file.close()
            Flagge = True
        except IOError:
            QtGui.QMessageBox.critical(None, "Fehler", os.getenv('HOME').decode(code_page) + os.sep + ( "vogisini.xml kann nicht gelesen werden - bitte kontrollieren sie die Einstellungen!!").decode("utf-8"))
            self.vogisPfad = 'V:/Geodaten/'
            self.vogisEncoding = 'menue'
            self.vogisKBS = 'menue'
            self.vogisDb = 'dbname=vogis host=vnvfelfs1.net.vlr.gv.at port=5432'
            Flagge = False

        if Flagge:  #vogisin.xml konnte gelesen werden

            #den Tag mainpath abfragen (Nodeliste mit nur einem Element in userem Fall)
            mainpath = self.d.elementsByTagName("mainpath")
            encoding = self.d.elementsByTagName("encoding")
            kbs = self.d.elementsByTagName("kbs")
            db = self.d.elementsByTagName("db")

            #Den Textinhalt (Pfad) des VoGIS Laufwerks einlesen
            self.vogisPfad = mainpath.item(0).toElement().firstChild().toText().data()
            self.vogisEncoding = encoding.item(0).toElement().firstChild().toText().data()
            self.vogisKBS = kbs.item(0).toElement().firstChild().toText().data()
            self.vogisDb = db.item(0).toElement().firstChild().toText().data()

            #prüfen ob alles belegt ist, ansonsten die vogisini komplett neu schreiben
            #mit Standardwerten!
            if self.vogisPfad == '' or self.vogisEncoding == '' or self.vogisKBS == '' or self.vogisDb == '':
                self.write_vogisini('V:/Geodaten/','menue','menue', '')

            #die Checkboxen befüllen
            if self.vogisEncoding == 'menue':
                self.ckEncoding.setCheckState(0)
            else:
                self.ckEncoding.setCheckState(2)

            if self.vogisKBS == 'menue':
                self.ckCRS.setCheckState(0)
            else:
                self.ckCRS.setCheckState(2)

            if self.vogisDb == '':
                self.ckDb.setCheckState(0)
            else:
                self.ckDb.setCheckState(2)

            #das labelfeld befüllen
            self.lblPath.setText(self.vogisPfad.replace("\\",""))

        else:
            #die Checkboxen befüllen
            if self.vogisEncoding == 'menue':
                self.ckEncoding.setCheckState(0)
            else:
                self.ckEncoding.setCheckState(2)

            if self.vogisKBS == 'menue':
                self.ckCRS.setCheckState(0)
            else:
                self.ckCRS.setCheckState(2)

            if self.vogisDb == '':
                self.ckDb.setCheckState(0)
            else:
                self.ckDb.setCheckState(2)

            #das labelfeld befüllen
            self.lblPath.setText(self.vogisPfad.replace("\\",""))

        #prüfen ob der Pfad gefunden werden kann
        if not os.path.exists(self.vogisPfad):
            QtGui.QMessageBox.critical(None, "Achtung",("VoGIS Laufwerk nicht gefunden! Bitte den richtigen Pfad wählen!").decode("utf-8"))


    @pyqtSignature("")
    def on_ButtonPath_clicked(self):
        if (self.dialog.exec_()):
            auswahl = self.dialog.selectedFiles()
            if len(auswahl) == 1:
                self.vogisPfad = auswahl[0] + os.sep

                raus = self.d.toString()
                self.lblPath.setText(self.vogisPfad.replace("\\","/"))
            else:
                QtGui.QMessageBox.critical(None, "Achtung",("Bitte richtiges Verzeichnis auswählen!").decode("utf-8"))
                return

    @pyqtSignature("")
    def on_ButtonSave_clicked(self):

        self.vogisPfad = self.lblPath.text()
        rect = QtGui.QMessageBox.question(None, "Achtung",("Sollen die neuen Einstellungen gespeichert werden?"))


        if self.ckCRS.checkState() == QtCore.Qt.Checked:
            self.vogisKBS = 'project'
        else:
            self.vogisKBS = 'menue'

        if self.ckEncoding.checkState() == QtCore.Qt.Checked:
            self.vogisEncoding = 'project'
        else:
            self.vogisEncoding = 'menue'

        if self.ckDb.checkState() == QtCore.Qt.Checked:
            self.vogisDb = 'dbname=vogis host=vnvfelfs1.net.vlr.gv.at port=5432'
        else:
            self.vogisDb = ''

        if rect == QMessageBox.Ok:
            self.write_vogisini(self.vogisPfad,self.vogisEncoding,self.vogisKBS, self.vogisDb)

            self.lblPath.setText(self.vogisPfad.replace("\\","/"))



        self.closeEvent()

    #Reimplamentierung des closeEvents des Event Handlers!
    #Wird immer vom Event Handler ausgelöst, wenn auf das schließen Kästchen x geklickt wird
    #Wird hier auch vom Abbrechen Button verwendet, deshalb ist die Variable event = None gesetzt, da
    #das cleccked Signal nicht übergibt (was eine fehlermeldung bewirken würde), wohl aber
    # das x Kästchen wenn geklicket
    def closeEvent(self,event = None):

        self.close()



    #die vogisini anlegen, im lokalen arbeitsverzeichnis des Vogis menüs
    def write_vogisini(self,mainpath,encoding,kbs,db):

        raus = QtCore.QByteArray()
        d = QtCore.QXmlStreamWriter(raus)   #Das XMAL Handling für diese Zwecke ist damit OK
        d.setAutoFormatting(True)
        d.writeStartDocument()
        d.writeStartElement('vogis')
        d.writeTextElement('mainpath', mainpath)
        d.writeTextElement('encoding', encoding)
        d.writeTextElement('kbs', kbs)
        d.writeTextElement('db', db)
        d.writeEndElement()
        d.writeEndDocument()
        #file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","w+")
        # Codepage bestimmen 8Sunderzeicehn im Pfad zum Benutzerhome)
        code_page =locale.getpreferredencoding()
        file = open(os.getenv('HOME').decode(code_page) + os.sep + "vogisini.xml","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
        file.write(str(raus))
        file.close()