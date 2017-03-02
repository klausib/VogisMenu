# -*- coding: utf-8 -*-
from osgeo import ogr
from qgis.core import *
import os, string
from PyQt4 import QtGui,QtCore


# Um Layer direkt - also nicht über das Modul PRojektimport
# aus einem QGIS Projekt - zu laden
def direk_laden(PGdb, lyr_name, shapename, pfad, iface):

    iface.layerTreeView().setCurrentLayer(None) # Damit von ganz aussen in der LEgende angefangen wird!
    try:
        db = PGdb
        shapename_ohne_suffix = shapename.replace('.shp','')
        shapename_ohne_suffix = str(string.strip(string.lower(shapename_ohne_suffix)))
        if db != None:
            try:  # Geodatenbank
                uri = QgsDataSourceURI()
                uri.setConnection(db.hostName(),str(db.port()),db.databaseName(),'','')  # Kein Kennwort nötig, Single Sign On


                # Geometriespalte bestimmen -- geht nur mit OGR
                outputdb = ogr.Open('pg: host=' + db.hostName() + ' dbname=' + db.databaseName() + ' schemas=vorarlberg' + ' port=' + str(db.port()))
                #outputdb = ogr.Open('pg: host=' + db.hostName() +  ' dbname=' + db.databaseName() + ' schemas=vorarlberg')
                geom_column = outputdb.GetLayerByName(shapename_ohne_suffix).GetGeometryColumn()
                uri.setDataSource('vorarlberg', shapename_ohne_suffix, geom_column)

                erg_lyr = QgsVectorLayer(uri.uri(), lyr_name,"postgres")
            #und prüfen ob erfolgreich geladen
            except Exception as e: #nicht erfolgreich geladen
                QtGui.QMessageBox.about(None, "Fehler", "Layer " + shapename_ohne_suffix + " in der Datenbank nicht gefunden - es wird aufs Filesystem umgeschaltet")
                #QtGui.QMessageBox.about(None, "Fehler", str(e))
                erg_lyr = QgsVectorLayer(pfad + '/' + shapename, lyr_name,"ogr")
        elif db == None:
            erg_lyr = QgsVectorLayer(pfad + '/' + shapename, lyr_name,"ogr")

        # prüfen ob was sinnvolles geladen werden konnte
        if erg_lyr.isValid():
            return erg_lyr
        else:
            QtGui.QMessageBox.about(None, "Fehler", "Layer " + shapename + " konnte nicht geladen werden")
            return None
    except:
        return None