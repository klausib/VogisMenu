 # -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
#from soverify.tools.dbTools import DbObj
import math, time
from VogisPrint_Utils import *
#import os


class CreateMapBookGrid( QObject ):

    def __init__( self, iface, gridType, printScale, printFormat, layoutIndex, layerName, dkm_stand):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.gridType = gridType
        self.printScale = printScale
        self.printFormat = printFormat
        self.layoutIndex = layoutIndex
        self.layerName = layerName
        self.index = None
        self.dkm_stand = dkm_stand



    def run( self ):

        # Does not work with geographic coordinate systems.
        projectEPSG = self.canvas.mapRenderer().destinationCrs().toProj4()
        if str.find(str(projectEPSG),  "+proj=longlat") >= 0:
            # FIXME Überstzung !
            QMessageBox.warning( None, "", "EasyPrint Mapbook Grid does not work with geographic coordinate systems.")
            return



        #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:35", "self.layerName %s" %(self.layerName))
        mapLayer = getLayerByName(self.layerName)
        if mapLayer == None:
            QMessageBox.warning( None, "Fehler !", "Kein Layer gefunden.")
            return

        mapType = mapLayer.type()

        #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:41", "self.printScale %s  mapType %d  self.gridType %d" %(self.printScale, mapType,  self.gridType))

        # FIXME self.gridType == 3 ?? Ist noch gar nicht auswaehlbar => Baustelle
        if self.gridType == 3:

            # FIXME Wie diese Grid-Memory-Layers uebersetzen ?
            text = QCoreApplication.translate("grid-memoryName-typ3", "Mapbook linear")
            self.memoryName = text

            if mapType <> QgsMapLayer.VectorLayer:
                QMessageBox.warning( None, "", "EasyPrint Mapbook Linear will not work with raster layers.")
                return

            if mapLayer.geometryType() <> 1:
                QMessageBox.warning( None, "", "EasyPrint Mapbook Linear will only work with linestring layers.")
                return

        else:
            # FIXME Wie diese Grid-Memory-Layers uebersetzen ?
            text = QCoreApplication.translate("grid-memoryName", "Mapbook grid")
            self.memoryName = text

            if mapType == QgsMapLayer.VectorLayer:
                if mapLayer.geometryType() == 0:
                    # FIXME Translation
                    QMessageBox.warning( None, "", "Point layers do not work.")
                    return


        # Memory-Layer mit dem Raster vorbereiten (u. a. Attribute anlegen)

        # Vorhandene Grids entfernen
        memlayername = self.memoryName
##        QString.fromUtf8(memlayername)
        memlayer_vorhanden = getVectorLayerByName(memlayername)
        if memlayer_vorhanden == None:
            #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:78", "kein memorylayer vorhanden")
            pass
        else:
            QgsMapLayerRegistry.instance().removeMapLayers( [memlayer_vorhanden.id()] )
            #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:83", "memorylayer geloescht")


        memlayer = QgsVectorLayer("Polygon", self.memoryName, "memory")
        qml = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + '/python/plugins/VogisMenu/standardlayout/styles/regular_grid_andy.qml'))
        memlayer.loadNamedStyle(qml)
        memprovider = memlayer.dataProvider()
        memprovider.addAttributes( [ QgsField("name", QVariant.String), QgsField("rotation", QVariant.Double), QgsField("printformat", QVariant.String), QgsField("printscale", QVariant.Double), QgsField("layoutindex", QVariant.Int)] )
        QgsMapLayerRegistry.instance().addMapLayer(memlayer, True)
##        memlayer.updateFieldMap()
        memlayer.updateFields()
        memlayer.setCrs( self.canvas.mapRenderer().destinationCrs() )

        # Hier sicherheitshabler nochmal prüfen
        mapLayer = getLayerByName(self.layerName)
        if mapLayer == None:
            QMessageBox.critical( None, "Fehler !", "Kein Layer %s gefunden." %(self.layerName))
            return



        # FIXME self.gridType == 3 ?? Ist noch gar nicht auswaehlbar => Baustelle
        if self.gridType == 3:



            # Nur mal so zum testen: erste(s) Feature/Geometry
            provider = mapLayer.dataProvider()
            feat = QgsFeature()
            allAttrs = provider.attributeIndexes()
            provider.select(allAttrs)
            while provider.nextFeature(feat):
                geom = feat.geometry()
                if geom.wkbType() == 5:
                    line = geom.asMultiPolyline()[0]
                else:
                    line = geom.asPolyline()
                break

            lineGeom = QgsGeometry.fromPolyline(line)
            lastPoint = line[len(line)-1]
            startPoint = line[0]

            mapWidth,  mapHeight = self.getMapExtent()
            rect = QgsRectangle (0, 0, mapWidth, mapHeight)
            QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:108", "mapWidth %d  mapHeight %d  self.gridType %d" %(self.printScale, mapType,  self.gridType))

            # while schleife solange SELF.startPoint vorhanden ist. sonst ist ja der Rest innerhalb des Frames.
            # vielleicht noch zur sicherheit ein maximum...

#            for i in range(4):


#"""""""""""""""""""""""""""""""""
            # MMMMMMh, wie finde ich heraus ob ich am Ende angelangt bin? -> nur einen Schnittpunkt. -> muss bei jeder Rotation noch geprüft wreden.
            # aha, ein Schnittpunkt UND lastPoint muss innerhalb polyon sein.
#""""""""""""""""""""""""""""""""""


            dummy = []
            intersectionLength = 0

            for i in range(360):

                #print "Rotation: " + str(i)

                f = QgsFeature()
                g = QgsGeometry.fromRect(rect)
                g.translate(startPoint.x(), startPoint.y()-mapHeight/2)
                g.insertVertex(startPoint.x(), startPoint.y(), 4)
                g = rotate(g, startPoint, i*math.pi/180)

                optimalPoint = rotate(QgsGeometry.fromPoint(QgsPoint(startPoint.x()+mapWidth, startPoint.y())), startPoint, i*math.pi/180).asPoint()
                toleranceSqrDist = (((optimalPoint.sqrDist(g.vertexAt(1)))**0.5)*0.5)**2   # Multiplikator (halbe Strecke) frei waehlbar.

                f.setAttributeMap( { 0 : QVariant(str(i)), 1 : QVariant(float(0.0)), 2 : QVariant(str(self.printFormat)), 3 : QVariant(float(self.printScale[3:])), 4 : QVariant(int(self.layoutIndex)) } )

                #print "*************************"
                #print f.attributeMap()[0].type()


#                f.setGeometry(g)
#                memprovider.addFeatures( [ f ] )



                boundary = QgsGeometry.fromPolyline(g.asPolygon()[0])
                boundaryIntersection = boundary.intersection(QgsGeometry.fromPolyline(line))
                wkbType = boundaryIntersection.wkbType()
                result = None

                if wkbType == 1:
                    result = boundaryIntersection.asPoint()
                elif wkbType == 4:
                    result = boundaryIntersection.asMultiPoint()
                else:
                    dummy.append(str(i))
                    print "Should not reach here"
                    QMessageBox.warning( None, "", "Should not reach here. Unknown geometry type.")
                    return

                # Es ist ja auch möglich, dass ein Stück Geometrie, das momentan noch nicht interessiert (weiter vorne liegt) bereits im
                # Kartenausschnitt zu liegen kommt. -> Modulo 2, aber was macht man wenn das letzte Stücke gerade aufhört. -> dann
                # wären das eine ungerade anzahl Schnittpunkte. Einfach überprüfen ob es der letzte Vertexpunkt ist? Reicht das? Was man
                # ja nicht will ist eine ungerade Anzahl und der erste Punkt ist nicht Teil eines Segmentes.
                # AAAAah, Startpunkt ist allein, dann kommt ein Segement und dann endet noch Linie -> 4 Schnittpunkte.... Scheisse. Kann
                # man das einfach so prüfen? Aha, wenns also ne gerade Anzahl ist und der letzte Punkt genau dem letzten Punkt der linie entspricht.


                if wkbType == 1:

                    # noch prüfen ob lastPoint innerhalb, falls ja -> letztes Polygon
                    pass

                    # das optimale ist wahrscheinlich, das Mittel der längsten Folgen von Zahlen (+1)



                if wkbType == 4:

                    # Falls die Linie im Kartenausschnitt endet UND Startpunkt nicht
                    # zu einer Schnittlinie gehört, gibt es trotzdem eine gerade Anzahl
                    # Schnittpunkten. Dies ist aber keine mögliche Lösung.
                    if len(result) % 2 == 0:

                        if g.intersects(QgsGeometry.fromPoint(lastPoint)):
                                continue

                        polygonIntersection = g.intersection(lineGeom)
                        print polygonIntersection.wkbType()
                        if polygonIntersection.wkbType() == 5:
                            mpolyline = polygonIntersection.asMultiPolyline()
                            for k in range(len(mpolyline)):
                                if QgsGeometry.fromPolyline(mpolyline[k]).intersects(QgsGeometry.fromPoint(startPoint)):
                                    polyline = mpolyline[k]
                                else:
                                    pass
                        elif polygonIntersection.wkbType() == 2:
                            polyline = polygonIntersection.asPolyline()
                        else:
                            print "should never reach here #2"


                    if len(result) % 2 == 1 and g.intersects(QgsGeometry.fromPoint(lastPoint)):

                        polygonIntersection = g.intersection(lineGeom)
                        if polygonIntersection.wkbType() == 5:
                            mpolyline = polygonIntersection.asMultiPolyline()
                            for j in range(len(mpolyline)):
                                if QgsGeometry.fromPolyline(mpolyline[j]).intersects(QgsGeometry.fromPoint(lastPoint)):
                                    pass
                                else:
                                    polyline = mpolyline[j]
                        else:
                            print "should never reach here #3"



                    # Jetzt müsste noch geprüft werden, ob  beforeVertex + 1 (also afterVertex) von Schnittpunkt grösser ist als der Drehpunkt (=startPoint)
                    # dann ists i.O. Muss ich den jeweiligen Startpunkt noch einrechne in linie? Ja.



                    polylineGeom = QgsGeometry.fromPolyline(polyline)
#                    print polylineGeom.asPolyline()
                    f.setGeometry(polylineGeom)
                    memprovider.addFeatures( [ f ] )




        # Diese 2 Typen werden tatsächlich unterstützt.
        if self.gridType == 1 or self.gridType == 2:

            # MapWith und MapHeight werden anhand der Papiergröße errechnet.
            mapWidth,  mapHeight = self.getMapExtent()
            #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:336", "mapWidth %s  mapHeight %s  self.gridType %d" %(mapWidth, mapHeight,  self.gridType))

            if mapType == QgsMapLayer.VectorLayer:
                #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:355", "hier kommt das boese self.createSpatialIndex(mapLayer)")
                self.createSpatialIndex(mapLayer)

            # Now create the grid geometry and delete empty ones (if desired).
            extent = mapLayer.extent()

            if mapWidth < 1 or mapHeight < 1:
                QMessageBox.critical(None, "Achtung!", "mapWidth %s  mapHeight %s  " %(mapWidth, mapHeight))
                return


            xCount = math.ceil(extent.width() / mapWidth)
            yCount = math.ceil(extent.height() / mapHeight)

            xStart = extent.xMinimum()
            yStart = extent.yMinimum()

            #QMessageBox.about(None, "doVogisPrintCreateMapBookGrid.py:350", "mapWidth = %s\nmapHeight = %s" %(mapWidth, mapHeight))

            for i in range(int(xCount)):
                xMin = xStart + i * mapWidth
                for j in range(int(yCount)):
                    yMin = yStart + j * mapHeight
                    rect = QgsRectangle (xMin, yMin, xMin + mapWidth, yMin + mapHeight)

                    f = QgsFeature()
                    f.setGeometry(QgsGeometry.fromRect(rect))
                    # Attribute einfügen
##                    f.setAttributeMap( { 0 : QVariant(str(i) + "." + str(j)), 1 : QVariant(float(0.0)), 2 : QVariant(str(self.printFormat)), 3 : QVariant(self.printScale), 4 : QVariant(int(self.layoutIndex)), 5 : QVariant(int(self.overlapPercentage)) } )
                    f.setAttributes( [ (str(i) + "." + str(j)), (float(0.0)), (str(self.printFormat)),  (self.printScale), (int(self.layoutIndex)) ] )

                    if self.gridType == 2 and mapType == QgsMapLayer.VectorLayer:
                        intersect = self.index.intersects(rect)
                        if len(intersect) > 0:
                            for k in intersect:
                                feat = QgsFeature()
                                req = QgsFeatureRequest(k)
                                fit = self.layer.getFeatures(req)
                                fit.nextFeature(feat)
                                if feat.geometry().intersects( rect ) == True:
                                    memprovider.addFeatures( [ f ] )
                                    break
                    else:
                        memprovider.addFeatures( [ f ] )

            memlayer.updateExtents()
            self.iface.legendInterface().setLayerVisible(memlayer,  True)
            self.iface.mapCanvas().refresh()


    # --------------------------------------------------------------------------------------
    # createSpatialIndex()
    # --------------------------------------------------------------------------------------
    def createSpatialIndex( self, layer ):
        if layer == None or layer.type() <> 0:
            return
        self.layer = layer
        self.provider = layer.dataProvider()
        #self.provider.select([])
        layer.selectAll()
        feat = QgsFeature()

        if self.index == None:
            self.index = QgsSpatialIndex()
            alleFeatureListe = layer.selectedFeatures()
            for feat in  alleFeatureListe:
                self.index.insertFeature(feat)

        layer.removeSelection()
    # --------------------------------------------------------------------------------------
    # getMapExtent()
    # --------------------------------------------------------------------------------------
    def getMapExtent( self ):

        #print "\ndoVogisPrintCreateMapBookGrid.py:392 %s" %("def getMapExtent( self ):")
        paperheight,  paperwidth = getPapersize(self.printFormat)

##        QMessageBox.warning( None, "getMapExtent", str(self.dkm_stand))
        layouts = getLayouts(self.dkm_stand)
        layout = layouts[self.layoutIndex]

        margins = layout.getMargins()
        margin_top = margins['margin-top']
        margin_right = margins['margin-right']
        margin_bottom = margins['margin-bottom']
        margin_left = margins['margin-left']

        orientation = layout.getOrientation()
        if orientation == "landscape":
            paperwidth_tmp = paperwidth
            paperwidth = paperheight
            paperheight = paperwidth_tmp

        headerHeight = 0
        headerWidth = 0
        footerHeight = 0

        decorations = layout.getDecorations()
        for decoration in decorations:
            type = decoration.getType()
            #print "doVogisPrintCreateMapBookGrid.py:444 type = %s" %(type)
            offset_x = decoration.getOffsetX()
            offset_y = decoration.getOffsetY()

            if decoration.getAffinityX() == "right":
                offset_x = float(paperwidth) - margin_left - margin_right - offset_x

            if decoration.getAffinityY() == "bottom":
                offset_y = float(paperheight) - margin_top - margin_bottom - decoration.getHeight() - offset_y

            if type == "header"  or type == "footer":
                height = decoration.getHeight()
                width = decoration.getWidth()
                if type == "header":
                    headerHeight = height
                    headerWidth = width
                elif type == "footer":
                    footerHeight = height
                    footerWidth = width

            elif type == "map":
                if orientation == "portrait":
                    mapWidth = float(paperwidth)-(margin_right+margin_left)
                    mapHeight = float(paperheight)-margin_top-margin_bottom-headerHeight-footerHeight
                else:
                    mapWidth = float(paperwidth) - (headerWidth+margin_right+margin_left+(offset_x-headerWidth))
                    mapHeight = float(paperheight) - margin_top-margin_bottom


        newScale = self.printScale #/ (1+(float(self.overlapPercentage)/100))


        return (mapWidth  / 1000 * newScale), (mapHeight  / 1000 * newScale)


    def accept(self):
        if self.mbfexportpath.text() == "":
            QMessageBox.warning( None, "", QtCore.QString.fromUtf8("Kein Pfad für den Export gewählt!"))
            return
