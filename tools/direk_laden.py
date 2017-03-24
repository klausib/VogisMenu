# -*- coding: utf-8 -*-
from osgeo import ogr
from qgis.core import *
import os, string
from PyQt4 import QtGui,QtCore
from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich


# Um Layer direkt - also nicht über das Modul PRojektimport
# aus einem QGIS Projekt - zu laden
def direk_laden(PGdb, lyr_name, shapename, pfad, iface, subset = None):


    # Der Username der verwendet werden soll
    if len(auth_user_global) > 0:    # Ist belegt
        auth_user = auth_user_global[0]
    else:
        auth_user = None

    iface.layerTreeView().setCurrentLayer(None) # Damit von ganz aussen in der LEgende angefangen wird!
    try:
        db = PGdb
        shapename_ohne_suffix = shapename.replace('.shp','')
        shapename_ohne_suffix = str(string.strip(string.lower(shapename_ohne_suffix)))
        if db != None:
            try:  # Geodatenbank

                ################################################
                # Geometriespalte bestimmen -- geht nur mit OGR
                try:
                    if auth_user == None:
                        outputdb = ogr.Open('pg: host =' + db.hostName() + ' dbname =' + db.databaseName() + ' schemas=' + schema + ' port=' + str(db.port()))
                    else:
                        outputdb = ogr.Open('pg: host =' + db.hostName() + ' dbname =' + db.databaseName() + ' schemas=' + schema + ' port=' + str(db.port()) + ' user=' + auth_user)
                    geom_column = outputdb.GetLayerByName(shapename_ohne_suffix).GetGeometryColumn()
                except:
                    geom_column = 'the_geom'

                ################################################


                #das Laden der Daten
                uri = QgsDataSourceURI()
                uri.setConnection(db.hostName(),str(db.port()),db.databaseName(),'','')

                if not auth_user == None:
                    uri.setUsername(auth_user)
                uri.setDataSource('vorarlberg', shapename_ohne_suffix, geom_column)
                erg_lyr = QgsVectorLayer(uri.uri(), lyr_name,"postgres")

            #und prüfen ob erfolgreich geladen
            except Exception as e: #nicht erfolgreich geladen
                QtGui.QMessageBox.about(None, "Fehler", "Layer " + shapename_ohne_suffix + " in der Datenbank nicht gefunden - es wird aufs Filesystem umgeschaltet")
                erg_lyr = QgsVectorLayer(pfad + '/' + shapename, lyr_name,"ogr")
        elif db == None:
            erg_lyr = QgsVectorLayer(pfad + '/' + shapename, lyr_name,"ogr")

        # Hier die attributive Auswahl
        if subset != None:
            erg_lyr.setSubsetString(subset)

        # prüfen ob was sinnvolles geladen werden konnte
        if erg_lyr.isValid():
            return erg_lyr
        else:
            QtGui.QMessageBox.about(None, "Fehler", "Layer " + shapename + " konnte nicht geladen werden")
            return None

    except Exception as b:
        return None