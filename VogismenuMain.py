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
from doGFZ_pg import *
from doHoehenmodell import *
from doHoehenmodell_pg import *
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


        self.gemeindeliste = self.do_gemeindeliste()
        #QtGui.QMessageBox.critical(None, "Fehler", str(self.gemeindeliste))

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
        # Nur einmalig bei der DB Umstellung ANFANG
        #############################################################################
        if vogisDb_global[0] == 'filesystem' or vogisDb_global[0] == '':
            try:
                self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
                vogisDb_global[0] = self.vogisDb
                raus = QtCore.QByteArray()
                d = QtCore.QXmlStreamWriter(raus)   #Das XMAL Handling für diese Zwecke ist damit OK
                d.setAutoFormatting(True)
                d.writeStartDocument()
                d.writeStartElement('vogis')
                d.writeTextElement('mainpath', self.vogisPfad)
                d.writeTextElement('encoding', self.vogisEncoding)
                d.writeTextElement('kbs', self.vogisKBS)
                d.writeTextElement('db', self.vogisDb)
                d.writeEndElement()
                d.writeEndDocument()
                #file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","w+")
                # Codepage bestimmen Sunderzeicehn im Pfad zum Benutzerhome)
                code_page =locale.getpreferredencoding()
                file = open(os.getenv('HOME').decode(code_page) + os.sep + "vogisini.xml","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
                file.write(str(raus))
                file.close()
            except:
                QtGui.QMessageBox.about(None, "Achtung", 'initialisierungsproblem - Vogis Options werden geöffnet'.decode('UTF8'))
                self.doVogisOptions()
                return
        #############################################################################
        # Nur einmalig bei der DB Umstellung ENDE
        #############################################################################






        #############################################################################
        # Das Umschalten der Vektordaten auf die Geodatenbank - unter Bedingungen
        #############################################################################
        if vogisDb_global[0] != 'filesystem geodaten':

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
            self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht die Verbindung individuell - sonst ist eine Default Verbindung
            if host != '':
                self.PGdb.setHostName(host)
            if port != '':
                self.PGdb.setPort(int(port))
            if dbname != '':
                self.PGdb.setDatabaseName(dbname)

            ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist

            if ok:
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


            if not ok:# and host == 'cnvbrwgdi6.net.vlr.gv.at':

                #erneuter Versuch auf anderm Port, vielleicht ist der Load Balancer Offline
                #QtGui.QMessageBox.about(None, "Achtung", 'Keine Verbindung über Load Balancer, versuche Standardport...'.decode('UTF8'))
                self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht die Verbindung individuell - sonst ist eine Default Verbindung
                if host != '':
                    self.PGdb.setHostName(host)
                if port != '':
                    self.PGdb.setPort(int(5432))
                if dbname != '':
                    self.PGdb.setDatabaseName(dbname)

                ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist
            if not ok:# and host == 'cnvbrwgdi6.net.vlr.gv.at':
                #QtGui.QMessageBox.about(None, "Achtung", 'Keine Verbindung auf Primären DB Server, versuche Standby...'.decode('UTF8'))
                self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht die Verbindung individuell - sonst ist eine Default Verbindung
                if host != '':
                    self.PGdb.setHostName('cnvbrwgdi7.net.vlr.gv.at')
                if port != '':
                    self.PGdb.setPort(int(5432))
                if dbname != '':
                    self.PGdb.setDatabaseName(dbname)

                ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist


            if not ok:# and host == 'cnvbrwgdi7.net.vlr.gv.at':
                QtGui.QMessageBox.about(None, "Fehler", 'Keine Verbindung zur Geodatenbank -  bitte in den Vogis Menü Einstellungen auf Filesystem umschalten!'.decode('UTF8'))
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
                    abfrage.exec_("update qgis_user set version = '1.3' where user = '" + username + "'")
                    abfrage.exec_("update qgis_user set qgis_version = '" + QGis.QGIS_VERSION + "' where user = '" + username + "'")
                    self.db.close()
                else: #user nicht gefunden, d.h. noch nicht vorhanden
                    abfrage.exec_("insert into qgis_user ("'user'", "'starts'", "'version'", "'qgis_version'") values ('" + username + "', 1 , '1.3', '" + QGis.QGIS_VERSION + "')")

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

        if vogisDb_global[0] == 'filesystem geodaten':
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
        if vogisDb_global[0] == 'filesystem geodaten':
            self.PGdb = None

        Path = self.vogisPfad + "Points_of_Interest/Adressen/Vlbg/"
        Table = 'adressen'
        Schema = 'vorarlberg'
        #Name = 'adressen_tmp'

        #damit das Fenster nicht zweimal geöffnet wird!
        if self.AdresssucheDialog == None or self.AdresssucheDialog.objectName() == 'Bin_nicht_offen':

            # Unterschiedliche Module für Postgis bzw. SQLITE
            if vogisDb_global[0] != 'filesystem geodaten':
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
            if vogisDb_global[0] != 'filesystem geodaten':
                self.GstsucheGUI = GstDialogPG(self.iface.mainWindow(),self.iface,self.dkmstand,self.vogisPfad,self.PGdb, self.gemeindeliste)
                self.GstsucheGUI.show()
                self.GstsucheGUI.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
            else:
                self.GstsucheGUI = GstDialogSqlite(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad, self.gemeindeliste)
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
            self.FWP = FWPDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,self.PGdb, self.gemeindeliste.keys())
            self.FWP.show()
            self.FWP.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.FWP.raise_()
            self.FWP.activateWindow()



    def doGFZ(self):
        ProjektPath = self.vogisPfad + "Gefahren/Gefahrenzonenplan/"


        if self.GFZ == None or self.GFZ.objectName() == 'Bin_nicht_offen':

            # Unterschiedliche Module für Postgis bzw. SQLITE
            if vogisDb_global[0] != 'filesystem geodaten':
                self.GFZ = GFZDialogPG(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,self.PGdb, self.gemeindeliste.keys())
                self.GFZ.show()     # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht
                                    # hinter dem parent window verschwindet
                self.GFZ.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
            else:
                self.GFZ = GFZDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,None, self.gemeindeliste.keys())
                self.GFZ.show()     # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht
                                    # hinter dem parent window verschwindet
                self.GFZ.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.GFZ.raise_()
            self.GFZ.activateWindow()

    def doNaturschutz(self):
        ProjektPath = self.vogisPfad + "Naturschutz/"

        if self.naturschutz == None or self.naturschutz.objectName() == 'Bin_nicht_offen':
            self.naturschutz = NaturschutzDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad, self.gemeindeliste.keys())
            self.naturschutz.show()

            self.naturschutz.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.naturschutz.raise_()
            self.naturschutz.activateWindow()

    def doVerkehr(self):
        ProjektPath = self.vogisPfad + "Verkehr/"
        self.verkehr = VerkehrDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad,self.PGdb)
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

            if vogisDb_global[0] != 'filesystem geodaten':
                self.hoehenmodell = HoehenmodellDialog_PG(self.iface.mainWindow(),self.iface,self.speicheradressen_hoehenmodell,ProjektPath,self.vogisPfad,self.PGdb)
            else:
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
        self.Topokarten = TopokartenDialog(self.iface,ProjektPath,self.vogisPfad,self.PGdb)
        self.Topokarten.exec_()          #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doWald(self):
        ProjektPath = self.vogisPfad + "Forstwesen/Wald/Vlbg"
        self.wald = WaldDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.PGdb)
        self.wald.exec_()     #ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                        #sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doVermessung(self):
        ProjektPath = self.vogisPfad + "Vermessung"

        #damit das Fenster nicht zweimal geöffnet wird

        if self.vermessung == None or self.vermessung.objectName() == 'Bin_nicht_offen':
            self.vermessung = VermessungDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad,self.PGdb)
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


    def do_gemeindeliste(self):

##        liste = ["Hohenweiler", "Möggers".decode('utf8'), "Hörbranz".decode('utf8'), "Eichenberg", "Sulzberg", "Langen", "Lochau",  "Bregenz",\
##        "Hard", "Riefensberg", "Fußach".decode('utf8'),  "Höchst".decode('utf8'), "Doren", "Gaißau".decode('utf8'), "Krumbach", "Buch", "Kennelbach", "Alberschwende", "Hittisau",\
##        "Lauterach", "Wolfurt", "Bildstein", "Langenegg", "Lustenau", "Lingenau", "Schwarzach", "Egg", "Dornbirn", "Sibratsgfäll".decode('utf8'),\
##        "Schwarzenberg", "Andelsbuch", "Bezau", "Hohenems", "Mittelberg", "Reuthe", "Bizau", "Mellau", "Altach",  "Mäder".decode('utf8'), "Schnepfau", "Götzis".decode('utf8'), "Koblach",\
##        "Schoppernau", "Au", "Fraxern", "Klaus", "Viktorsberg", "Meiningen",  "Weiler", "Damüls".decode('utf8'), "Röthis".decode('utf8'), "Rankweil", "Laterns", "Zwischenwasser", "Sulz",\
##        "Feldkirch",  "Fontanella", "Warth", "Schröcken".decode('utf8'), "Sonntag", "Blons", "Übersaxen".decode('utf8'), "St. Gerold", "Göfis".decode('utf8'), "Lech", "Satteins", "Dünserberg".decode('utf8'),\
##         "Thüringerberg".decode('utf8'), "Schnifis",  "Düns".decode('utf8'), "Röns".decode('utf8'), "Raggal", "Schlins", "Nenzing", "Thüringen".decode('utf8'), "Ludesch", "Frastanz", "Bludesch",\
##        "Dalaas", "Nüziders".decode('utf8'), "Bludenz", "Innerbraz", "Bürs".decode('utf8'), "Bürserberg".decode('utf8'), "Klösterle".decode('utf8'), "Stallehr", "Lorüns".decode('utf8'), "Bartholomäberg".decode('utf8'), "St. Anton", "Brand", "Vandans", "Silbertal",\
##        "Schruns", "Tschagguns", "St. Gallenkirch", "Gaschurn", "Vorarlberg"]

        liste = {"Hohenweiler":["91112 - Hohenweiler"],\
        "Möggers".decode('utf8'):["91118 - Möggers".decode('utf8')],\
        "Hörbranz".decode('utf8'):["91113 - Hörbranz".decode('utf8')],\
        "Eichenberg":["91106 - Eichenberg"],\
        "Sulzberg":["91122 - Sulzberg"],\
        "Langen":["91115 - Langen"],\
        "Lochau":["91117 - Lochau"],\
        "Bregenz":["91103 - Bregenz","91107 - Fluh","91119 - Rieden"],\
        "Hard":["91110 - Hard"],\
        "Riefensberg":["91120 - Riefensberg"],\
        "Fußach".decode('utf8'):["91108 - Fußach".decode('utf8')],\
        "Höchst".decode('utf8'):["91111 - Höchst".decode('utf8')],\
        "Doren":["91105 - Doren"],\
        "Gaißau".decode('utf8'):["91109 - Gaißau".decode('utf8')],\
        "Krumbach":["91009 - Krumbach"],\
        "Buch":["91104 - Buch"],\
        "Kennelbach":["91114 - Kennelbach"],\
        "Alberschwende":["91101 - Alberschwende"],\
        "Hittisau":["91005 - Bolgenach","91008 - Hittisau"],\
        "Lauterach":["91116 - Lauterach"],\
        "Wolfurt":["91123 - Wolfurt"],\
        "Langenegg":["91013 - Oberlangengg","91020 - Unterlangenegg"],\
        "Bildstein":["91102 - Bildstein"],\
        "Lustenau":["92005 - Lustenau"],\
        "Lingenau":["91010 - Lingenau"],\
        "Schwarzach":["91121 - Schwarzach"],\
        "Egg":["91007 - Egg"],\
        "Dornbirn":["92001 - Dornbirn","92002 - Ebnit 1","92003 - Ebnit 2"],\
        "Sibratsgfäll".decode('utf8'):["91019 - Sibratsgfäll".decode('utf8')],\
        "Schwarzenberg":["91018 - Schwarzenberg"],\
        "Andelsbuch":["91001 - Andelsbuch"],\
        "Bezau":["91003 - Bezau"],\
        "Hohenems":["92004 - Hohenems"],\
        "Mittelberg":["91012 - Mittelberg"],\
        "Reuthe":["91014 - Reuthe"],\
        "Bizau":["91004 - Bizau"],\
        "Mellau":["91011 - Mellau"],\
        "Altach":["92101 - Altach"],\
        "Mäder".decode('utf8'):["92114 - Mäder".decode('utf8')],\
        "Schnepfau":["91015 - Schnepfau"],\
        "Götzis".decode('utf8'):["92110 - Götzis".decode('utf8')],\
        "Koblach":["92112 - Koblach"],\
        "Schoppernau":["91016 - Schoppernau"],\
        "Au":["91002 - Au"],\
        "Fraxern":["92108 - Fraxern"],\
        "Klaus":["92111 - Klaus"],\
        "Viktorsberg":["92127 - Viktorsberg"],\
        "Meiningen":["92115 - Meiningen"],\
        "Weiler":["92128 - Weiler"],\
        "Damüls".decode('utf8'):["91006 - Damüls".decode('utf8')],\
        "Röthis".decode('utf8'):["92119 - Röthis".decode('utf8')],\
        "Rankweil":["92117 - Rankweil"],\
        "Laterns":["92113 - Laterns"],\
        "Zwischenwasser":["92129 - Zwischenwasser"],\
        "Sulz":["92123 - Sulz"],\
        "Feldkirch":["92102 - Altenstadt","92105 - Feldkirch","92116 - Nofels","92124 - Tisis","92125 - Tosters"],\
        "Fontanella":["90008 - Fontanella"],\
        "Warth":["91021 - Warth"],\
        "Schröcken".decode('utf8'):["91017 - Schröcken".decode('utf8')],\
        "Sonntag":["90016 - Sonntag"],\
        "Blons":["90001 - Blons"],\
        "Übersaxen".decode('utf8'):["92126 - Übersaxen".decode('utf8')],\
        "St. Gerold":["90017 - St. Gerold"],\
        "Göfis".decode('utf8'):["92109 - Göfis".decode('utf8')],\
        "Lech":["90011 - Lech"],\
        "Satteins":["92120 - Satteins"],\
        "Dünserberg".decode('utf8'):["92104 - Dünserberg".decode('utf8')],\
        "Thüringerberg".decode('utf8'):["90019 - Thüringerberg".decode('utf8')],\
        "Schnifis":["92122 - Schnifis"],\
        "Düns".decode('utf8'):["92103 - Düns".decode('utf8')],\
        "Röns".decode('utf8'):["92118 - Röns".decode('utf8')],\
        "Raggal":["90015 - Raggal"],\
        "Schlins":["92121 - Schlins"],\
        "Nenzing":["90013 - Nenzing"],\
        "Thüringen".decode('utf8'):["90018 - Thüringen".decode('utf8')],\
        "Ludesch":["90012 - Ludesch"],\
        "Frastanz":["92106 - Frastanz 1","92107 - Frastanz 2 3"],\
        "Bludesch":["90003 - Bludesch"],\
        "Dalaas":["90007 - Dalaas"],\
        "Nüziders".decode('utf8'):["90014 - Nüziders".decode('utf8')],\
        "Bludenz":["90002 - Bludenz"],\
        "Innerbraz":["90009 - Innerbraz"],\
        "Bürs".decode('utf8'):["90005 - Bürs".decode('utf8')],\
        "Bürserberg".decode('utf8'):["90006 - Bürserberg".decode('utf8')],\
        "Klösterle".decode('utf8'):["90010 - Klösterle".decode('utf8')],\
        "Stallehr":["90110 - Stallehr"],\
        "Lorüns".decode('utf8'):["90103 - Lorüns".decode('utf8')],\
        "Bartholomäberg".decode('utf8'):["90101 - Bartholomäberg".decode('utf8')],\
        "St. Anton":["90106 - St. Anton"],\
        "Brand":["90004 - Brand"],\
        "Vandans":["90109 - Vandans"],\
        "Silbertal":["90105 - Silbertal"],\
        "Schruns":["90104 - Schruns"],\
        "Tschagguns":["90108 - Tschagguns"],\
        "St. Gallenkirch":["90107 - St. Gallenkirch"],\
        "Gaschurn":["90102 - Gaschurn"],\
        "Vorarlberg":["91112 - Hohenweiler","91118 - Möggers".decode('utf8'),"91113 - Hörbranz".decode('utf8'),"91106 - Eichenberg","91122 - Sulzberg","91115 - Langen",\
        "91117 - Lochau","91103 - Bregenz","91119 - Rieden","91110 - Hard","91120 - Riefensberg","91108 - Fußach".decode('utf8'),"91107 - Fluh","91111 - Höchst".decode('utf8'),\
        "91105 - Doren","91109 - Gaißau".decode('utf8'),"91009 - Krumbach","91104 - Buch","91114 - Kennelbach","91101 - Alberschwende","91005 - Bolgenach","91116 - Lauterach",\
        "91123 - Wolfurt","91008 - Hittisau","91020 - Unterlangenegg","91102 - Bildstein","91013 - Oberlangengg","92005 - Lustenau","91010 - Lingenau","91121 - Schwarzach",\
        "91007 - Egg","92001 - Dornbirn","91019 - Sibratsgfäll".decode('utf8'),"91018 - Schwarzenberg","91001 - Andelsbuch","91003 - Bezau","92004 - Hohenems","91012 - Mittelberg",\
        "91014 - Reuthe","91004 - Bizau","91011 - Mellau","92101 - Altach","92002 - Ebnit 1","92114 - Mäder".decode('utf8'),"91015 - Schnepfau","92110 - Götzis".decode('utf8'),\
        "92112 - Koblach","91016 - Schoppernau","91002 - Au","92108 - Fraxern","92111 - Klaus","92127 - Viktorsberg","92115 - Meiningen","92003 - Ebnit 2","92128 - Weiler",\
        "91006 - Damüls".decode('utf8'),"92119 - Röthis".decode('utf8'),"92117 - Rankweil","92113 - Laterns","92129 - Zwischenwasser","92123 - Sulz","92116 - Nofels",\
        "92102 - Altenstadt","90008 - Fontanella","91021 - Warth","91017 - Schröcken".decode('utf8'),"90016 - Sonntag","90001 - Blons","92126 - Übersaxen".decode('utf8'),\
        "90017 - St. Gerold","92109 - Göfis".decode('utf8'),"92125 - Tosters","90011 - Lech","92120 - Satteins","92104 - Dünserberg".decode('utf8'),"92105 - Feldkirch",\
        "90019 - Thüringerberg".decode('utf8'),"92122 - Schnifis","92124 - Tisis","92103 - Düns".decode('utf8'),"92106 - Frastanz 1","92118 - Röns".decode('utf8'),\
        "90015 - Raggal","92121 - Schlins","90013 - Nenzing","90018 - Thüringen".decode('utf8'),"90012 - Ludesch","92107 - Frastanz 2 3","90003 - Bludesch","90007 - Dalaas",\
        "90014 - Nüziders".decode('utf8'),"90002 - Bludenz","90009 - Innerbraz","90005 - Bürs".decode('utf8'),"90006 - Bürserberg".decode('utf8'),"90010 - Klösterle".decode('utf8'),\
        "90110 - Stallehr","90103 - Lorüns".decode('utf8'),"90101 - Bartholomäberg".decode('utf8'),"90106 - St. Anton","90004 - Brand","90109 - Vandans","90105 - Silbertal",\
        "90104 - Schruns","90108 - Tschagguns","90107 - St. Gallenkirch","90102 - Gaschurn",]
        }

##        liste ={"Hohenweiler":["91112 - Hohenweiler"],\
##        "Möggers":["91118 - Möggers"]\
##        }
        #QtGui.QMessageBox.critical(None, "Fehler", str(liste.keys()))
        return liste
        #return sorted(liste)


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
            #self.vogisDb = 'dbname=vogis host=vnvfelfs1.net.vlr.gv.at port=5432'
            self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
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
            if self.vogisPfad == '' or self.vogisEncoding == '' or self.vogisKBS == '' or self.vogisDb == 'filesystem geodaten':
                self.write_vogisini('V:/Geodaten/','menue','menue', 'filesystem geodaten')

            #die Checkboxen befüllen
            if self.vogisEncoding == 'menue':
                self.ckEncoding.setCheckState(0)
            else:
                self.ckEncoding.setCheckState(2)

            if self.vogisKBS == 'menue':
                self.ckCRS.setCheckState(0)
            else:
                self.ckCRS.setCheckState(2)

            if self.vogisDb == 'filesystem geodaten':
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

            if self.vogisDb == 'filesystem geodaten':
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
            #self.vogisDb = 'dbname=vogis host=vnvfelfs1.net.vlr.gv.at port=5432'
            self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
        else:
            self.vogisDb = 'filesystem geodaten'

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