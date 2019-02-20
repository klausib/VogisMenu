# -*- coding: utf-8 -*-


# Die Kernbibliotheken für
# Qgis und PyQT importieren
# (Gegebenenfalls läßt sich diese Auswahl
# noch verfeinern)

from __future__ import print_function
from builtins import bytes
from builtins import str
from builtins import object
from qgis.PyQt import QtCore, QtGui, QtXml, QtWidgets

from qgis import core
import sys, os.path,string
import locale



# Unbedingt den Pfad setzen damit die anderen Module gefunden werden
currentPath = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/tools'))
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/standardlayout'))


from globale_variablen import *     # Die Adresse der Listen importieren: modulübergreifende globale Variablen sind so möglich


from doAbfall import *
from doGeonamsuche import *
from doAdresssuche_pg import *
from doAdresssuche_sqlite import *
from doBlattschnitte import *
from doGstsuche_pg import *
from doGstsuche_sqlite import *
##from ProjektImport import *
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
        self.speicheradressen_adressuche =[]    # darauf werden die Adressen der Adressuche Grafiken gespeichert
                                                # solange das Vogis Menü geladen ist können sie immer wieder gelöscht werden
                                                # vom Dialogfeld Adressuche aus (da Listen Pointer sind!)

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

        #die vogisini datei oeffnen
        #erstmal nur um zu lesen
        Flagge = False

        try:
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
                QtWidgets.QMessageBox.critical(None, "Fehler", os.getenv('HOME') + os.sep + ( "vogisini.xml scheint beschädigt - bitte kontrollieren sie die Einstellungen!!"))
                self.doVogisOptions()

            #Zur Sicherheit nochmal prüfen ob der Vogis Pfad gefunden werden kann
            if not os.path.exists(self.vogisPfad):
                self.doVogisOptions()


            #die modulübergreifenden globalen Variablen belegen
            #werden dann auch im Modul Projektimport verwendet
            del vogisEncoding_global[:]   #neu initialisieren
            del vogisKBS_global[:]
            del vogisDb_global[:]
            del auth_user_global[:]
            del path_global[:]
            vogisEncoding_global.append(self.vogisEncoding)
            vogisKBS_global.append (self.vogisKBS)
            vogisDb_global.append (self.vogisDb)
            path_global.append (os.path.abspath(os.path.dirname(__file__)+ '/tools'))


            # Postgres DB initialisieren
            # und angemeldeten Benutzer auslesen
            # zuerst mal mit kleinem Benutzernamen
            # Warum das? Siehe PRoblem Usermapping und GRoßKleinschreibung als Konflikt Windows-Linux
            self.username = getpass.getuser().upper() # brauchen wir auch füs Mitloggen
            if vogisDb_global[0] != 'skip':# skip bedeuet das eingestellte Filesystem wird genommen, sonst wird immer zur DB umgeschaltet
                if not self.initPGDB():
                    # hat nicht geklappt
                    # und dann noachmal mit Großem Benutzernamen
                    self.username = getpass.getuser().lower()
                    if not self.initPGDB():
                        # auch nix
                        del auth_user_global[:] # zurücksetzen
                        QtWidgets.QMessageBox.about(None, "Fehler", 'Keine Verbindung zur Geodatenbank! Unter dem Menüpunkt VOGIS->Vogis Menü Einstellungen \"Vektorlayer aus Geodatenbank\" deaktivieren!')
                    else:
                        # Passt!
                        auth_user_global.append (self.username)
                else:
                    # Passt!
                    auth_user_global.append (self.username)
            else:
                vogisDb_global[0] = 'filesystem geodaten'

        else:
            self.unload()



        self.projekti = QgsProject.instance() # Zeiger auf das gerade aktuelle Projekt der QGIS Instanz!
        #self.rewrite = VogisProject(self.projekti) # Das Rewrite Objekt erzeugen
        # Das Signal writeProject geht auf die rewrite Methode des rewrite Objekts
        #self.projekti.projectSaved.connect(self.rewrite.rewrite)
        #self.projekti.projectSaved.connect(self.rewrite.run)
        self.projekti.projectSaved.connect(self.los)






    def initPGDB(self):


        #############################################################################
        # Zwangsumschalten auf die DB wenn Filesystem ANFANG
        #############################################################################
        if vogisDb_global[0] == 'filesystem geodaten':
            try:
                self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
                vogisDb_global[0] = self.vogisDb
                raus = QtCore.QByteArray()
                d = QtCore.QXmlStreamWriter(raus)   #Das XML Handling für diese Zwecke ist damit OK
                d.setAutoFormatting(True)
                d.writeStartDocument()
                d.writeStartElement('vogis')
                d.writeTextElement('mainpath', self.vogisPfad)
                d.writeTextElement('encoding', self.vogisEncoding)
                d.writeTextElement('kbs', self.vogisKBS)
                d.writeTextElement('db', self.vogisDb)
                d.writeEndElement()
                d.writeEndDocument()

                # file = open(os.path.dirname(__file__) + os.sep + "vogisini.xml","w+")
                # Codepage bestimmen Sunderzeicehn im Pfad zum Benutzerhome)
                code_page =locale.getpreferredencoding()
                #file = open(os.getenv('HOME').decode(code_page) + os.sep + "vogisini.xml","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
                file = open(os.getenv('HOME') + os.sep + "vogisini.xml","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
                file.write(str(raus,'utf8')) #Bytearray in String konvertieren
                file.close()
            except:
                QtWidgets.QMessageBox.about(None, "Achtung", 'initialisierungsproblem - Vogis Options werden geöffnet')
                self.doVogisOptions()
                return

        #############################################################################
        # Zwangsumschalten auf die DB wenn Filesystem ENDE
        #############################################################################



        #############################################################################
        # Das Umschalten der Vektordaten auf die Geodatenbank - unter Bedingungen
        #############################################################################
        if vogisDb_global[0] != 'filesystem geodaten':

            ##########################################
            # testen, ob die DB geöffnet werden kann
            # und wenn ja, Datenbankobjekt Instanzieren
            ###########################################

            dbpath = (vogisDb_global[0] + ' sslmode=disable  (the_geom) sql=').lower()
            param_list = (dbpath).split()

            host = ''
            dbname=''
            port=''

            #QtGui.QMessageBox.about(None, "Achtung", str(param_list))

            for param in param_list:

                if str.find(param,'dbname') >= 0:
                    dbname = str.replace(param,'dbname=','')

                elif str.find(param,'host=') >= 0:
                    host = str.replace(param,'host=','')

                elif str.find(param,'port=') >= 0:
                    port = str.replace(param,'port=','')


            # Wir verwenden die Windows Domänen Authentifizierung.
            # Allerdings gibts da Groß-Klein und Mixed Schreibweis
            # was das Usermapping erschwert. Deshalb lesen wir den USer aus und verwenden Ihne
            # direkt. Passwort aufgrund Windowsauthetifizeirung nicht nötig

            self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht die Verbindung individuell - sonst ist eine Default Verbindung

            if host != '':
                self.PGdb.setHostName(host)

            if port != '':
                self.PGdb.setPort(int(port))

            if dbname != '':
                self.PGdb.setDatabaseName(dbname)

            if self.username != '':
                self.PGdb.setUserName(self.username)





            ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist


            if ok:
                try:

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

                if self.username != '':
                    self.PGdb.setUserName(self.username)



                # Unbedingt die globele Variable korrigieren,
                # da diese im Modul Projectimport verwendet wird
                self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=5432'
                del vogisDb_global[:]
                vogisDb_global.append (self.vogisDb)

                ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist
                #QtGui.QMessageBox.about(None, "Achtung 2", str(ok) + ' ' + self.PGdb.hostName() + ' ' + str(self.PGdb.port()) + ' '+ self.PGdb.databaseName() + ' '+ self.username)



            if not ok:# and host == 'cnvbrwgdi6.net.vlr.gv.at':

                #QtGui.QMessageBox.about(None, "Achtung", 'Keine Verbindung auf Primären DB Server, versuche Standby...'.decode('UTF8'))
                self.PGdb = QtSql.QSqlDatabase.addDatabase("QPSQL","vogis");  # Der Name macht die Verbindung individuell - sonst ist eine Default Verbindung

                if host != '':
                    self.PGdb.setHostName('cnvbrwgdi7.net.vlr.gv.at')

                if port != '':
                    self.PGdb.setPort(int(5432))

                if dbname != '':
                    self.PGdb.setDatabaseName(dbname)

                if self.username != '':
                    self.PGdb.setUserName(self.username)



                # Unbedingt die globele Variable korrigieren,
                # da diese im Modul Projectimport verwendet wird
                self.vogisDb = 'dbname=vogis host=cnvbrwgdi7.net.vlr.gv.at port=5432'
                del vogisDb_global[:]
                vogisDb_global.append (self.vogisDb)

                ok = self.PGdb.open()    #Gibt True zurück wenn die Datenbank offen ist
                #QtGui.QMessageBox.about(None, "Achtung 3", str(ok) + ' ' + self.PGdb.hostName() + ' ' + str(self.PGdb.port()) + ' '+ self.PGdb.databaseName() + ' '+ self.username)

            if not ok:# and host == 'cnvbrwgdi7.net.vlr.gv.at':


                # Das Scheitern kann auch durch die erzwungene Grossschreibung
                # des Usernamen entstehen. Da sofort mit der Kleinschreibung ein weiterer
                # Verbindungsaufbau versucht wird, UNBEDINGT alles wieder zurücksetzen!
                self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
                self.PGdb.setHostName('cnvbrwgdi6.net.vlr.gv.at')
                self.PGdb.setPort(int(9000))
                del vogisDb_global[:]
                vogisDb_global.append (self.vogisDb)
                return  False # Zurück


            #hat geklappt
            return True

    def initGui(self):


        #Das Vogis Menü mit seinen Unterpunkten, den Actions, definieren
        self.menuVogis = QtWidgets.QMenu()
        self.menuVogis.setObjectName(("menuVogis"))
        self.menuVogis.setTitle("VOGIS")

        self.actionGeonamsuche = QtWidgets.QAction(self.iface.mainWindow())
        self.actionGeonamsuche.setObjectName(("actionGeonamsuche"))
        #self.actionGeonamsuche.setText(bytes("Suche Ort (ÖK50)").decode("utf-8"))
        self.actionGeonamsuche.setText(("Suche Ort (ÖK50)"))

        self.actionAdresssuche = QtWidgets.QAction(self.iface.mainWindow())
        self.actionAdresssuche.setObjectName(("actionAdresssuche"))
        self.actionAdresssuche.setText("Suche Adresse")

        self.actionGstsuche = QtWidgets.QAction(self.iface.mainWindow())
        self.actionGstsuche.setObjectName(("actionGstsuche"))
        self.actionGstsuche.setText(("Suche Grundstück"))

        self.actionAbfall = QtWidgets.QAction(self.iface.mainWindow())
        self.actionAbfall.setObjectName(("actionAbfall"))
        self.actionAbfall.setText("Abfallwirtschaft")

        self.actionAdressen = QtWidgets.QAction(self.iface.mainWindow())
        self.actionAdressen.setObjectName(("actionAdressen"))
        self.actionAdressen.setText("Adressen")

        self.actionBoden = QtWidgets.QAction(self.iface.mainWindow())
        self.actionBoden.setObjectName(("actionBoden"))
        self.actionBoden.setText("Boden")

        self.actionLuftbilder = QtWidgets.QAction(self.iface.mainWindow())
        self.actionLuftbilder.setObjectName(("actionLuftbilder"))
        self.actionLuftbilder.setText("Bilddaten: Luft- und Satellitenbilder")

        self.actionBlattschnitte = QtWidgets.QAction(self.iface.mainWindow())
        self.actionBlattschnitte.setObjectName(("actionBlattschnitte"))
        self.actionBlattschnitte.setText("Blattschnitte")

        self.actionDKM = QtWidgets.QAction(self.iface.mainWindow())
        self.actionDKM.setObjectName(("actionDKM"))
        self.actionDKM.setText(("Digitaler Kataster (DKM), Urmappe, Gebäudeumrisse"))

        self.actionEnergie = QtWidgets.QAction(self.iface.mainWindow())
        self.actionEnergie.setObjectName(("actionEnergie"))
        self.actionEnergie.setText("Energieversorgung")

        self.actionFischerei = QtWidgets.QAction(self.iface.mainWindow())
        self.actionFischerei.setObjectName(("actionFischerei"))
        self.actionFischerei.setText("Fischerei")

        self.actionFWP = QtWidgets.QAction(self.iface.mainWindow())
        self.actionFWP.setObjectName(("actionFWP"))
        self.actionFWP.setText(("Flächenwidmung"))

        self.actionGFZ = QtWidgets.QAction(self.iface.mainWindow())
        self.actionGFZ.setObjectName(("actionGFZ"))
        self.actionGFZ.setText(("Gefahrenzonen"))

        self.actionGrenzen = QtWidgets.QAction(self.iface.mainWindow())
        self.actionGrenzen.setObjectName(("actionGrenzen"))
        self.actionGrenzen.setText(("Grenzen"))

        self.actionHoehenmodell = QtWidgets.QAction(self.iface.mainWindow())
        self.actionHoehenmodell.setObjectName(("actionHoehenmodell"))
        self.actionHoehenmodell.setText(("Höhenmodelle"))


        self.actionJagd = QtWidgets.QAction(self.iface.mainWindow())
        self.actionJagd.setObjectName(("actionJagd"))
        self.actionJagd.setText(("Jagd"))

        self.actionKlima = QtWidgets.QAction(self.iface.mainWindow())
        self.actionKlima.setObjectName(("actionKlima"))
        self.actionKlima.setText(("Klima"))

        self.actionLandnutzung = QtWidgets.QAction(self.iface.mainWindow())
        self.actionLandnutzung.setObjectName(("actionLandnutzung"))
        self.actionLandnutzung.setText(("Landnutzung"))

        self.actionLandwirtschaft = QtWidgets.QAction(self.iface.mainWindow())
        self.actionLandwirtschaft.setObjectName(("actionLandwirtschaft"))
        self.actionLandwirtschaft.setText(("Landwirtschaft"))

        self.actionNaturschutz = QtWidgets.QAction(self.iface.mainWindow())
        self.actionNaturschutz.setObjectName(("actionNaturschutz"))
        self.actionNaturschutz.setText(("Naturschutz"))

        self.actionPointsofInterest = QtWidgets.QAction(self.iface.mainWindow())
        self.actionPointsofInterest.setObjectName(("actionPointsofInterest"))
        self.actionPointsofInterest.setText(("Points of Interest"))

        self.actionRaumplanung = QtWidgets.QAction(self.iface.mainWindow())
        self.actionRaumplanung.setObjectName(("actionRaumplanung"))
        self.actionRaumplanung.setText(("Raumplanung"))

        self.actionSiedlungen = QtWidgets.QAction(self.iface.mainWindow())
        self.actionSiedlungen.setObjectName(("actionSiedlungen"))
        self.actionSiedlungen.setText(("Siedlungen"))

        self.actionVerkehr = QtWidgets.QAction(self.iface.mainWindow())
        self.actionVerkehr.setObjectName(("actionVerkehr"))
        self.actionVerkehr.setText(("Verkehr, Transport, Infrastruktur"))

        self.actionWasser = QtWidgets.QAction(self.iface.mainWindow())
        self.actionWasser.setObjectName(("actionWasser"))
        self.actionWasser.setText(("Wasser"))

        self.actionWald = QtWidgets.QAction(self.iface.mainWindow())
        self.actionWald.setObjectName(("actionWald"))
        self.actionWald.setText(("Wald"))

        self.actionGeologie = QtWidgets.QAction(self.iface.mainWindow())
        self.actionGeologie.setObjectName(("actionGeologie"))
        self.actionGeologie.setText("Geologie")

        self.actionTopokarten = QtWidgets.QAction(self.iface.mainWindow())
        self.actionTopokarten.setObjectName(("actionTopokarten"))
        self.actionTopokarten.setText("Topographische Karten")

        self.actionVermessung = QtWidgets.QAction(self.iface.mainWindow())
        self.actionVermessung.setObjectName(("actionVermessung"))
        self.actionVermessung.setText("Vermessung")

        self.actionVogisPrint = QtWidgets.QAction(self.iface.mainWindow())
        self.actionVogisPrint.setObjectName(("actionVogisPrint"))
        self.actionVogisPrint.setText(("VOGIS - Standardlayout"))

        self.actionVogisHilfe = QtWidgets.QAction(self.iface.mainWindow())
        self.actionVogisHilfe.setObjectName(("actionVogisHilfe"))
        self.actionVogisHilfe.setText(("VOGIS - Hilfe"))

        self.actionVogisOptions = QtWidgets.QAction(self.iface.mainWindow())
        self.actionVogisOptions.setObjectName(("actionVogisOptions"))
        self.actionVogisOptions.setText(("VOGIS - Menü Einstellungen"))


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
        self.actionGeonamsuche.triggered.connect(self.doGeonamsuche)
        self.actionAdresssuche.triggered.connect(self.doAdresssuche)
        self.actionGstsuche.triggered.connect(self.doGstsuche)  #newstyle
        self.actionAbfall.triggered.connect(self.doAbfall)
        self.actionAdressen.triggered.connect(self.doAdresssuche)
        self.actionBoden.triggered.connect(self.doBoden)
        self.actionLuftbilder.triggered.connect(self.doLuftbilder)
        self.actionBlattschnitte.triggered.connect(self.doBlattschnitte)
        self.actionDKM.triggered.connect(self.doGstsuche)
        self.actionEnergie.triggered.connect(self.doEnergie)
        self.actionFischerei.triggered.connect(self.doFischerei)
        self.actionFWP.triggered.connect(self.doFWP)
        self.actionGeologie.triggered.connect(self.doGeologie)
        self.actionGFZ.triggered.connect(self.doGFZ)
        self.actionGrenzen.triggered.connect(self.doGrenzen)
        self.actionHoehenmodell.triggered.connect(self.doHoehenmodell)
        self.actionJagd.triggered.connect(self.doJagd)
        self.actionKlima.triggered.connect(self.doKlima)
        self.actionLandnutzung.triggered.connect(self.doLandnutzung)
        self.actionLandwirtschaft.triggered.connect(self.doLandwirtschaft)
        self.actionNaturschutz.triggered.connect(self.doNaturschutz)
        self.actionPointsofInterest.triggered.connect(self.doPointsofInterest)
        self.actionRaumplanung.triggered.connect(self.doRaumplanung)
        self.actionSiedlungen.triggered.connect(self.doSiedlungen)
        self.actionTopokarten.triggered.connect(self.doTopokarten)
        self.actionVerkehr.triggered.connect(self.doVerkehr)
        self.actionVermessung.triggered.connect(self.doVermessung)
        self.actionWald.triggered.connect(self.doWald)
        self.actionWasser.triggered.connect(self.doWasser)
        self.actionVogisPrint.triggered.connect(self.doVogisPrint)
        self.actionVogisHilfe.triggered.connect(self.doVogisHilfe)
        self.actionVogisOptions.triggered.connect(self.doVogisOptions)




        #Die Objektvariable für die
        #Grafik(en) initialisieren

        self.Geonamgrafik = None
        self.adressgrafik = None



        #Den DKM Stand auslesen
        try:
            f = open(self.vogisPfad + "Grenzen/DKM/_Allgemein/Stand.txt","r")
            self.dkmstand = f.readline()

        except IOError:
            self.dkmstand = "Kein DKM Stand!"

        #-------------------------------------------------------------------------#
        #Eintrag in die User-Logging-Tabelle

        try:
            #Referenz auf die Datenquelle
            #direkt über SQLITE
            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE");
            dbpfad = self.vogisPfad + "_Allgemein/userreg/vogis_allgemein_db.sqlite"
            self.db.setDatabaseName(dbpfad);

            if os.path.exists(dbpfad) == 1: #sonst erzeugt open eine leer sqllitedb

                #nur wenn Öffnen OK
                if  self.db.open():
                    import getpass
                    abfrage = QtSql.QSqlQuery(self.db)

                    abfrage.exec_("SELECT starts  FROM qgis_user where user = '" + self.username.lower() + "'")


                    if abfrage.first(): #user gefunden
                        abfrage.exec_("update qgis_user set starts = starts + 1 where user = '" + self.username.lower() + "'")
                        abfrage.exec_("update qgis_user set version = '1.3.2' where user = '" + self.username.lower() + "'")
                        abfrage.exec_("update qgis_user set qgis_version = '" + QGis.QGIS_VERSION + "' where user = '" + self.username.lower() + "'")
                        abfrage.exec_("update qgis_user set datasource = '" + self.vogisDb + "' where user = '" + self.username.lower() + "'")
                        self.db.close()

                    else: #user nicht gefunden, d.h. noch nicht vorhanden
                        abfrage.exec_("insert into qgis_user ("'user'", "'starts'", "'version'", "'qgis_version'", "'datasource'") values ('" + self.username.lower() + "', 1 , '1.3.2', '" + QGis.QGIS_VERSION + "', '" + self.vogisDb + "')")

                        self.db.close()

        except:
            pass
        #--------------------------------------------------------------------------#


        #den pfad richten
        self.vogisPfad=self.vogisPfad.replace("\\","/")

    def run(self):
         # fix_print_with_import
         print("TestPlugin: run called!")


    def unload(self):
        #pass
        self.iface.removePluginMenu('Vogismenue', self.vogisaction)

    def doGeonamsuche(self):

        Path = self.vogisPfad + "Points_of_Interest/Ortsbezeichnung/Vlbg/oek_geonam/"
        Name = "geonam"
        if vogisDb_global[0] == 'filesystem geodaten':
            self.GeonamsucheDialog = Geonam(self.iface,Path,Name,self.Geonamgrafik)
        else:
            self.GeonamsucheDialog = Geonam(self.iface,Path,Name,self.Geonamgrafik,self.PGdb, Name)
        self.GeonamsucheDialog.exec_()   #Ergibt einen modalen Dialog: nur er ist für Input aktiv



        # ACHTUNG: Hier krieg ich eine IGraphicsItemGroup
        # zurück die alle Grafik Items enthält, die Geonams darstellen:
        # Dadurch habe ich das Objekt, welches alle Geonam Grafiken enthält
        # und kann so auch nur diese löschen ohne andere Grafik Items mitzulöschen
        # Die Methode Grafikreturn ist ein Slot für das Signal destroyed des
        # frames für die Geonamsuche. So wird das Objekt dem Vogismenü übergeben
        # und das Vogis Menü übergibt es wieder bei Aufruf der Geonamsuche. Dort wird wenn es leer ist ein neues erzeugt
        # oder das bestehende übernommen.!!

        self.Geonamgrafik = self.GeonamsucheDialog.grafikreturn()



    def doAdresssuche(self):

        # Das Postgis DB Objekt an die Einstellungen Anpassen
        if vogisDb_global[0] == 'filesystem geodaten':
            self.PGdb = None
        Path = self.vogisPfad + "Points_of_Interest/Adressen/Vlbg/"
        Table = 'adressen'
        Schema = 'vorarlberg'

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
        self.BlattschnittDialog.exec_() # ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                        # sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden



    def doBoden(self):

        ProjektPath = self.vogisPfad + "Geologie/Bodenkartierung/Vlbg/"
        self.boden = BodenDialog(self.iface.mainWindow(),self.iface,ProjektPath)

        #self.boden.exec_()
        self.boden.show()


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
            self.FWP = FWPDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,self.PGdb, list(self.gemeindeliste.keys()))
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

                self.GFZ = GFZDialogPG(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,self.PGdb, list(self.gemeindeliste.keys()))
                self.GFZ.show()     # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht
                                    # hinter dem parent window verschwindet

                self.GFZ.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug

            else:
                self.GFZ = GFZDialog(self.iface.mainWindow(),self.iface,self.dkmstand,ProjektPath,self.vogisPfad,None, list(self.gemeindeliste.keys()))
                self.GFZ.show()     # ergibt einen Dialog der die Interaction mit Qgis zulässt aber nicht
                                    # hinter dem parent window verschwindet
                self.GFZ.Abflug.connect(self.InstanzMarkieren)   #Ein individuelles Signal mit Namen Abflug
        else:
            self.GFZ.raise_()
            self.GFZ.activateWindow()

    def doNaturschutz(self):

        ProjektPath = self.vogisPfad + "Naturschutz/"

        if self.naturschutz == None or self.naturschutz.objectName() == 'Bin_nicht_offen':
            self.naturschutz = NaturschutzDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.vogisPfad, list(self.gemeindeliste.keys()))
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
        self.klima.exec_()  # ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                            # sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden



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
        self.Geologie.exec_()       # ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    # sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden

    def doTopokarten(self):

        ProjektPath = self.vogisPfad + "Topographische_Karten"
        self.Topokarten = TopokartenDialog(self.iface,ProjektPath,self.vogisPfad,self.PGdb)
        self.Topokarten.exec_()     # ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                                    # sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden



    def doWald(self):

        ProjektPath = self.vogisPfad + "Forstwesen/Wald/Vlbg"
        self.wald = WaldDialog(self.iface.mainWindow(),self.iface,ProjektPath,self.PGdb)
        self.wald.exec_()   # ACHTUNG: wird kein self.iface.mainWindow() als parent übergeben brauchts exec
                            # sonst müßte der parent dann für die Initialisierung von QDialog verwendet werden



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
        del auth_user_global[:]
        vogisEncoding_global.append(self.vogisEncoding)
        vogisKBS_global.append (self.vogisKBS)
        vogisDb_global.append (self.vogisDb)



        # Postgres DB initialisieren
        # und angemeldeten Benutzer auslesen
        # zuerst mal mit kleinem Benutzernamen
        # Warum das? Siehe PRoblem Usermapping und GRoßKleinschreibung als Konflikt Windows-Linux
        self.username = getpass.getuser().upper() # brauchen wir auch füs Mitloggen
        if vogisDb_global[0] != 'filesystem geodaten' and vogisDb_global[0] != '':

            if not self.initPGDB():

                # hat nicht geklappt
                # und dann noachmal mit Großem Benutzernamen

                self.username = getpass.getuser().lower()
                if not self.initPGDB():
                    # auch nix
                    del auth_user_global[:] # zurücksetzen
                    QtWidgets.QMessageBox.about(None, "Fehler", 'Keine Verbindung zur Geodatenbank! Unter dem Menüpunkt VOGIS->Vogis Menü Einstellungen \"Vektorlayer aus Geodatenbank\" deaktivieren!')
                else:
                    # Passt!
                    auth_user_global.append (self.username)
            else:
                # Passt!
                auth_user_global.append (self.username)




    def do_gemeindeliste(self):


        liste = {"Hohenweiler":["91112 - Hohenweiler"],\
        "Möggers":["91118 - Möggers"],\
        "Hörbranz":["91113 - Hörbranz"],\
        "Eichenberg":["91106 - Eichenberg"],\
        "Sulzberg":["91122 - Sulzberg"],\
        "Langen":["91115 - Langen"],\
        "Lochau":["91117 - Lochau"],\
        "Bregenz":["91103 - Bregenz","91107 - Fluh","91119 - Rieden"],\
        "Hard":["91110 - Hard"],\
        "Riefensberg":["91120 - Riefensberg"],\
        "Fußach":["91108 - Fußach"],\
        "Höchst":["91111 - Höchst"],\
        "Doren":["91105 - Doren"],\
        "Gaißau":["91109 - Gaißau"],\
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
        "Sibratsgfäll":["91019 - Sibratsgfäll"],\
        "Schwarzenberg":["91018 - Schwarzenberg"],\
        "Andelsbuch":["91001 - Andelsbuch"],\
        "Bezau":["91003 - Bezau"],\
        "Hohenems":["92004 - Hohenems"],\
        "Mittelberg":["91012 - Mittelberg"],\
        "Reuthe":["91014 - Reuthe"],\
        "Bizau":["91004 - Bizau"],\
        "Mellau":["91011 - Mellau"],\
        "Altach":["92101 - Altach"],\
        "Mäder":["92114 - Mäder"],\
        "Schnepfau":["91015 - Schnepfau"],\
        "Götzis":["92110 - Götzis"],\
        "Koblach":["92112 - Koblach"],\
        "Schoppernau":["91016 - Schoppernau"],\
        "Au":["91002 - Au"],\
        "Fraxern":["92108 - Fraxern"],\
        "Klaus":["92111 - Klaus"],\
        "Viktorsberg":["92127 - Viktorsberg"],\
        "Meiningen":["92115 - Meiningen"],\
        "Weiler":["92128 - Weiler"],\
        "Damüls":["91006 - Damüls"],\
        "Röthis":["92119 - Röthis"],\
        "Rankweil":["92117 - Rankweil"],\
        "Laterns":["92113 - Laterns"],\
        "Zwischenwasser":["92129 - Zwischenwasser"],\
        "Sulz":["92123 - Sulz"],\
        "Feldkirch":["92102 - Altenstadt","92105 - Feldkirch","92116 - Nofels","92124 - Tisis","92125 - Tosters"],\
        "Fontanella":["90008 - Fontanella"],\
        "Warth":["91021 - Warth"],\
        "Schröcken":["91017 - Schröcken"],\
        "Sonntag":["90016 - Sonntag"],\
        "Blons":["90001 - Blons"],\
        "Übersaxen":["92126 - Übersaxen"],\
        "St. Gerold":["90017 - St. Gerold"],\
        "Göfis":["92109 - Göfis"],\
        "Lech":["90011 - Lech"],\
        "Satteins":["92120 - Satteins"],\
        "Dünserberg":["92104 - Dünserberg"],\
        "Thüringerberg":["90019 - Thüringerberg"],\
        "Schnifis":["92122 - Schnifis"],\
        "Düns":["92103 - Düns"],\
        "Röns":["92118 - Röns"],\
        "Raggal":["90015 - Raggal"],\
        "Schlins":["92121 - Schlins"],\
        "Nenzing":["90013 - Nenzing"],\
        "Thüringen":["90018 - Thüringen"],\
        "Ludesch":["90012 - Ludesch"],\
        "Frastanz":["92106 - Frastanz 1","92107 - Frastanz 2 3"],\
        "Bludesch":["90003 - Bludesch"],\
        "Dalaas":["90007 - Dalaas"],\
        "Nüziders":["90014 - Nüziders"],\
        "Bludenz":["90002 - Bludenz"],\
        "Innerbraz":["90009 - Innerbraz"],\
        "Bürs":["90005 - Bürs"],\
        "Bürserberg":["90006 - Bürserberg"],\
        "Klösterle":["90010 - Klösterle"],\
        "Stallehr":["90110 - Stallehr"],\
        "Lorüns":["90103 - Lorüns"],\
        "Bartholomäberg":["90101 - Bartholomäberg"],\
        "St. Anton":["90106 - St. Anton"],\
        "Brand":["90004 - Brand"],\
        "Vandans":["90109 - Vandans"],\
        "Silbertal":["90105 - Silbertal"],\
        "Schruns":["90104 - Schruns"],\
        "Tschagguns":["90108 - Tschagguns"],\
        "St. Gallenkirch":["90107 - St. Gallenkirch"],\
        "Gaschurn":["90102 - Gaschurn"],\
        "Vorarlberg":["91112 - Hohenweiler","91118 - Möggers","91113 - Hörbranz","91106 - Eichenberg","91122 - Sulzberg","91115 - Langen",\
        "91117 - Lochau","91103 - Bregenz","91119 - Rieden","91110 - Hard","91120 - Riefensberg","91108 - Fußach","91107 - Fluh","91111 - Höchst",\
        "91105 - Doren","91109 - Gaißau","91009 - Krumbach","91104 - Buch","91114 - Kennelbach","91101 - Alberschwende","91005 - Bolgenach","91116 - Lauterach",\
        "91123 - Wolfurt","91008 - Hittisau","91020 - Unterlangenegg","91102 - Bildstein","91013 - Oberlangengg","92005 - Lustenau","91010 - Lingenau","91121 - Schwarzach",\
        "91007 - Egg","92001 - Dornbirn","91019 - Sibratsgfäll","91018 - Schwarzenberg","91001 - Andelsbuch","91003 - Bezau","92004 - Hohenems","91012 - Mittelberg",\
        "91014 - Reuthe","91004 - Bizau","91011 - Mellau","92101 - Altach","92002 - Ebnit 1","92114 - Mäder","91015 - Schnepfau","92110 - Götzis",\
        "92112 - Koblach","91016 - Schoppernau","91002 - Au","92108 - Fraxern","92111 - Klaus","92127 - Viktorsberg","92115 - Meiningen","92003 - Ebnit 2","92128 - Weiler",\
        "91006 - Damüls","92119 - Röthis","92117 - Rankweil","92113 - Laterns","92129 - Zwischenwasser","92123 - Sulz","92116 - Nofels",\
        "92102 - Altenstadt","90008 - Fontanella","91021 - Warth","91017 - Schröcken","90016 - Sonntag","90001 - Blons","92126 - Übersaxen",\
        "90017 - St. Gerold","92109 - Göfis","92125 - Tosters","90011 - Lech","92120 - Satteins","92104 - Dünserberg","92105 - Feldkirch",\
        "90019 - Thüringerberg","92122 - Schnifis","92124 - Tisis","92103 - Düns","92106 - Frastanz 1","92118 - Röns",\
        "90015 - Raggal","92121 - Schlins","90013 - Nenzing","90018 - Thüringen","90012 - Ludesch","92107 - Frastanz 2 3","90003 - Bludesch","90007 - Dalaas",\
        "90014 - Nüziders","90002 - Bludenz","90009 - Innerbraz","90005 - Bürs","90006 - Bürserberg","90010 - Klösterle",\
        "90110 - Stallehr","90103 - Lorüns","90101 - Bartholomäberg","90106 - St. Anton","90004 - Brand","90109 - Vandans","90105 - Silbertal",\
        "90104 - Schruns","90108 - Tschagguns","90107 - St. Gallenkirch","90102 - Gaschurn",]
        }

        return liste

    # Die Aufgabe der Methode los ist lediglich
    # Ein Objekt zum Entpacken eines QGZ Files
    # in einem eigenen THREAD zu erzeugen und
    # ihn auch zu kontrollieren
    def los(self):

        infile = self.projekti.fileInfo().absoluteFilePath()

        # Ist das Projektfile ein qgz, müssen wir einen
        # eigenen Dekomprimierungsthread starten
        if str.find(infile,'.qgz') > -1:
            outpath = os.path.dirname(self.projekti.fileInfo().absoluteFilePath())
            outfile = os.path.basename(self.projekti.fileInfo().absoluteFilePath())
            outfile = os.path.splitext(outfile)[0]
            if str.find(outfile,'.qgs') < 0:
                outfile = os.path.splitext(outfile)[0] + '.qgs'


##            #ret = QtWidgets.QMessageBox.information(None, "Vogis Projektsichern", "Soll das Projekt auch von anderen Benutzern verwendet werden?\nDas Projekt  kann dafür zusätzlich auch im qgs Format gesichert werden.",QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
##            #if ret == QtWidgets.QMessageBox.Yes:
##            if os.path.exists(outpath + '/' + outfile):
##                ret = QtWidgets.QMessageBox.information(None, "Vogis Projektsichern", 'Das Projekt ' + outpath + '/' + outfile + ' existiert bereits. Überschreiben?',QtWidgets.QMessageBox.Save | QtWidgets.QMessageBox.Cancel)
##                if ret == QtWidgets.QMessageBox.Save:
##                    entpackObjekt = entpacken(infile,outpath,outfile)
##                    entpackObjekt.start()
##                else:
##                    if os.path.exists(outpath + '/' + outfile):
##                        shutil.copy(outpath + '/' + outfile, outpath + '/' + outfile + '_safeVogisProject')
##                    #QtWidgets.QMessageBox.information(None, "Vogis Projektsichern", 'Nicht sichern')
##                    entpackObjekt = entpacken(infile,outpath,outfile,False)
##                    entpackObjekt.start()
##                    pass
##
##            else:
##                entpackObjekt = entpacken(infile,outpath,outfile)
##                entpackObjekt.start()

            entpackObjekt = entpacken(infile,outpath,outfile)
            entpackObjekt.start()

        else:   # Direkter Aufruf der rewrite Methode, kein qgz File wird gepeichert
            vp = VogisProject (infile)
            vp_ = vp.rewrite()
            if not vp_:
                QtWidgets.QMessageBox.critical(None, "Vogis Projektsichern",'Fehler beim Umschreiben des Projektes!')





# Klassendefinition für den Vogis Menüpukt
# Einstellungen
from gui_options import *
class Options (QtWidgets.QDialog, Ui_frmOptions):

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_frmOptions.__init__(self)


        self.setupUi(self)
        self.d = QtXml.QDomDocument()
        self.mainpath = ''
        self.vogisPfad =''
        self.vogisEncoding = ''
        self.vogisKBS = ''
        self.vogisDb = ''

        #Filedialog Objekt
        self.dialog = QtWidgets.QFileDialog()
        self.dialog.setFileMode(QtWidgets.QFileDialog.Directory)

        self.ButtonPath.clicked.connect(self.ButtonPath_clicked)
        self.ButtonSave.clicked.connect(self.ButtonSave_clicked)


        # Codepage bestimmen Sonderzeicehn im Pfad zum Benutzerhome)
        code_page =locale.getpreferredencoding()

        try:

            file = open(os.getenv('HOME') + os.sep + "vogisini.xml","r")
            xml = file.read()

            self.d.setContent(xml)   #d enthält das gesamnte XML
            file.close()
            Flagge = True

        except IOError:
            QtWidgets.QMessageBox.critical(None, "Fehler", os.getenv('HOME').decode(code_page) + os.sep + ( "vogisini.xml kann nicht gelesen werden - bitte kontrollieren sie die Einstellungen!!"))
            self.vogisPfad = 'V:/Geodaten/'
            self.vogisEncoding = 'menue'
            self.vogisKBS = 'menue'
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
            QtWidgets.QMessageBox.critical(None, "Achtung",("VoGIS Laufwerk nicht gefunden! Bitte den richtigen Pfad wählen!"))


    def ButtonPath_clicked(self):
        if (self.dialog.exec_()):
            auswahl = self.dialog.selectedFiles()
            if len(auswahl) == 1:
                self.vogisPfad = auswahl[0] + os.sep
                raus = self.d.toString()
                self.lblPath.setText(self.vogisPfad.replace("\\","/"))
            else:
                QtWidgets.QMessageBox.critical(None, "Achtung",("Bitte richtiges Verzeichnis auswählen!"))
                return


    def ButtonSave_clicked(self):

        self.vogisPfad = self.lblPath.text()
        rect = QtWidgets.QMessageBox.question(None, "Achtung",("Sollen die neuen Einstellungen gespeichert werden?"))

        if self.ckCRS.checkState() == QtCore.Qt.Checked:
            self.vogisKBS = 'project'
        else:
            self.vogisKBS = 'menue'

        if self.ckEncoding.checkState() == QtCore.Qt.Checked:
            self.vogisEncoding = 'project'
        else:
            self.vogisEncoding = 'menue'

        if self.ckDb.checkState() == QtCore.Qt.Checked:
            self.vogisDb = 'dbname=vogis host=cnvbrwgdi6.net.vlr.gv.at port=9000'
        else:
            self.vogisDb = 'filesystem geodaten'

        if rect == QtWidgets.QMessageBox.Yes:
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
        d = QtCore.QXmlStreamWriter(raus)   #Das XML Handling für diese Zwecke ist damit OK
        d.setAutoFormatting(True)
        d.writeStartDocument()
        d.writeStartElement('vogis')
        d.writeTextElement('mainpath', mainpath)
        d.writeTextElement('encoding', encoding)
        d.writeTextElement('kbs', kbs)
        d.writeTextElement('db', db)
        d.writeEndElement()
        d.writeEndDocument()

        # Codepage bestimmen 8Sunderzeicehn im Pfad zum Benutzerhome)
        code_page =locale.getpreferredencoding()
        file = open(os.getenv('HOME') + os.sep + "vogisini.xml","w+")    #os.path.dirname(__file__) gibt pfad des aktuellen moduls
        file.write(str(raus,'utf8')) #Bytearray in String konvertieren

        file.close()


# Klasse dient zur Erzeugung eines ThreadObjektes
# das dann in einem eigenen Thread (sie Methode los) prüft,
# ob QGIS das QGZ bereits geschrieben hat. Anschliessen
# wird es entpackt und das QGZ Gelöscht

import threading
import time
import zipfile
import shutil

class entpacken(threading.Thread):
    def __init__(self, infile, outpath,outfile):
        threading.Thread.__init__(self)

        # Die notwendigen Instanzvariablen
        self.infile = infile
        self.outpath = outpath + '/'
        self.outfile = outfile

    try:
        def run(self):
            flag = True
            while flag:
                if os.path.exists(self.infile):

                    # Etwas warten sonst ist die Datei noch nicht freigegeben
                    time.sleep(1)

                    # Zum Entpacken des temporören Zipfiles benötigen wir leider das Modul zipfile
                    with zipfile.ZipFile(self.infile) as myzip:
                        myzip.extract(self.outfile,self.outpath)

                    # QGZ Datei immer löschen
                    os.remove(self.infile)
                    flag = False
                    self.proof()

        def proof(self):
            if os.path.exists(self.outpath + self.outfile):
                self.rewrite = VogisProject(self.outpath + self.outfile)
                rw_ok = self.rewrite.rewrite()  # Den Usertag entfernen...
                if not rw_ok:
                    file_out = open(self.outpath + 'ERROR_' + self.outfile,'w+')
                else:
                    # das temporäre qgs File wieder zippen
##                    file_in = open(self.outpath + self.outfile,'r')
##                    with zipfile.ZipFile(self.infile,'w') as myzip:
##                            myzip.write(file_in)
##                    file_in.close()
                    archi = QgsArchive()
                    archi.addFile(self.outpath + self.outfile)
                    archi.zip(self.infile)

                    # danach temporäres qgs File wieder löschen
                    os.remove(self.outpath + self.outfile)

    except:
        file_out = open(self.outpath + 'ERROR_' + self.outfile,'w+')



# Klasse dient zur Erzeugung eines Objektes
# das den Benutzernamen aus der QGIS Projektdatei
# entfernt. Dadurch ist das Projekt in unserer
# Single Sign On Umgebung unter den Benutzern austauschbar.
import getpass
import shutil
class VogisProject(object):

    def __init__(self,projekt):
        self.projekt_pfad = projekt
        self.d = QtXml.QDomDocument()


    def __read_xml(self):

        # Das Qgis Projektfile ist ein XML und wird
        # hier eingelesen
        try:
            file_in = open(self.projekt_pfad,'r')
            xml = file_in.read()
            self.d.setContent(xml)
            file_in.close()
            return True
        except:
            #QtWidgets.QMessageBox.critical(None, "Klasse VogisProject",'Fehler beim Lesen des zu korrigierenden Projektfiles')
            return False

    def __write_xml(self,xml):

        # Das Qgis Projektfile ist ein XML und wird
        # hier neu geschrieben

        try:
            shutil.copy(self.projekt_pfad,self.projekt_pfad + '_VogisProject')
            file_out = open(self.projekt_pfad,'w')
            #file_out.write(str(bytearray(xml,'utf8')))
            file_out.write(xml)
            file_out.close()
            os.remove(self.projekt_pfad + '_VogisProject')
            return True

        except:
            return False

    def rewrite(self):
        try:
            ergebnis = False
            if self.__read_xml():
                xml = self.d.toString()
                xml = xml.replace('user=\'' + str.lower(str(getpass.getuser())) + '\'', '')
                xml = xml.replace('user=\'' + str.upper(str(getpass.getuser())) + '\'', '')
                ergebnis = self.__write_xml(xml)
            return ergebnis
        except:
            return False

