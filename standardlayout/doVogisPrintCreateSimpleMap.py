 # -*- coding: utf8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *
import math, time, os
from VogisPrint_Utils import *

class CreateSimpleMap( QObject ):

    def __init__( self, iface, printScale, printFormat, layoutIndex, titleString, subtitleString, personString, departmentString, crsdesc, grid, legend, copyright, cuttinglines, foldingmarks, stand_dkm, printAsRaster=False, mapExtent=None,  overviewMap=False, adjacentTiles=None, exportPath=None, printToFile=False, tileName=None, printRotation=0, useExtent=False):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        self.printScale = printScale
        self.printFormat = printFormat
        self.layoutIndex = layoutIndex
        self.titleString = titleString
        self.subtitleString = subtitleString
        self.personString = personString
        self.crsdesc = crsdesc
        self.grid = grid
        self.legend = legend
        self.copyright = copyright
        self.cuttinglines = cuttinglines
        self.foldingmarks = foldingmarks
        self.printAsRaster = printAsRaster
        self.mapExtent = mapExtent
        self.overviewMap = overviewMap
        self.adjacentTiles = adjacentTiles
        self.exportPath = exportPath
        self.printToFile= printToFile
        self.tileName = tileName
        self.printRotation = printRotation
        self.useExtent = useExtent
        self.stand_dkm = stand_dkm
        self.departmentString = departmentString

        self.newMapExtent = None
        self.printer = None
        self.painter = None
        self.fileName = None

        self.newMapExtent = " not initialized"
        #QMessageBox.about(None, "CreateSimpleMap:44", "stand_dkm = "  + stand_dkm)


    #******************************************************************************
    # setOutputFileName()
    #******************************************************************************
    def setOutputFileName( self,  fileName ):
        self.fileName = fileName


    #******************************************************************************
    # setPrinterPainter()
    #******************************************************************************
    def setPrinterPainter( self, printer, painter ):
        self.printer = printer
        self.painter = painter


    #******************************************************************************
    # getMapExtent()
    #******************************************************************************
    def getMapExtent( self ):
        #QMessageBox.warning(  None, "CreateSimpleMap:66", "Start getMapExtent")
        if self.newMapExtent == " not initialized":
            QMessageBox.critical( None, "CreateSimpleMap", "getMapExtent not initialized !!" )
            terminate()
        return self.newMapExtent

    #**********************************************************************************
    # run()
    #**********************************************************************************
    def run( self ):




        paperheight,  paperwidth = getPapersize(self.printFormat)

        layouts = getLayouts(self.stand_dkm)
        #QMessageBox.warning( None, "run", str(len(layouts)))
        layout = layouts[self.layoutIndex]
        #QMessageBox.about(None, "dkm", str(self.stand_dkm))
        margins = layout.getMargins()
        margin_top = margins['margin-top']
        margin_right = margins['margin-right']
        margin_bottom = margins['margin-bottom']
        margin_left = margins['margin-left']

        #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:91", "margins: margin-top: %s margin-right = %s margin-bottom = %s margin-left = %s" %(margin_top,margin_right,margin_bottom,margin_left))

        orientation = layout.getOrientation()
        if orientation == "landscape":
            paperwidth_tmp = paperwidth
            paperwidth = paperheight
            paperheight = paperwidth_tmp

        headerHeight = 0
        footerHeight = 0

        #QMessageBox.warning( None, "doVogisPrintCreateSimpleMap.py:79", "def run(self):")

        if self.printToFile == False:
            beforeList = self.iface.activeComposers()
            self.iface.actionPrintComposer().trigger()
            afterList = self.iface.activeComposers()
            #Abbrechen wenn auch cancel geklicht wird!
            if len(afterList) < 1:
                return
            diffList = []
            for item in afterList:
                if not item in beforeList:
                    diffList.append(item)

            composerView = diffList[0]
            composition = composerView.composition()
            composition.setPaperSize(float(paperwidth),  float(paperheight))

        else:
            mapRenderer = self.iface.mapCanvas().mapRenderer()
            composition = QgsComposition(mapRenderer)
            composition.setPlotStyle(QgsComposition.Print)
            composition.setPaperSize(float(paperwidth), float(paperheight))
            composition.setPrintResolution(300)

        #QMessageBox.warning( None, "doVogisPrintCreateSimpleMap.py:124", "Hier")

        #----------------------------------
        # Cutting lines.
        #----------------------------------
        if self.cuttinglines == True:
            if self.printToFile == True:
                self.cuttingLines(composition)
            else:
                self.cuttingLines(composition, composerView)


        #----------------------------------
        # Folding marks.
        #----------------------------------
        if self.foldingmarks == True:
            if self.printToFile == True:
                self.foldingMarks(composition)
            else:
                self.foldingMarks(composition, composerView)


        #---------------------------------------------------------------------------
        #---------------------------------------------------------------------------
        # Loop ueber die Decorations
        #---------------------------------------------------------------------------
        #---------------------------------------------------------------------------
        decorations = layout.getDecorations()
        for decoration in decorations:
            type = decoration.getType()
            offset_x = decoration.getOffsetX()
            offset_y = decoration.getOffsetY()

            if decoration.getAffinityX() == "right":
                offset_x = float(paperwidth) - margin_left - margin_right - offset_x

            if decoration.getAffinityY() == "bottom":
                offset_y = float(paperheight) - margin_top - margin_bottom - decoration.getHeight() - offset_y

            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:160", "type: %s\npaperwidth: %s\noffset_x: %s\noffset_y = %s" %(type,paperwidth,str(offset_x),str(offset_x)))



            # Header und Footer muessen layout.xml vorhanden sein,
            # sonst kann die Groesse der Karte nicht ausgerechnet
            # werden. Dementsprechend muessen sie auch vor
            # der Karte prozessiert werden. => Sie müssen im layout.xml immer vor dem map-Eintrag stehen



            #--------------------------------------------------------------------
            # Picture oder Northarrow
            #--------------------------------------------------------------------
            if type == "picture" or type == "northarrow":
                item = QgsComposerPicture(composition)
                #pic = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/VogisMenu/standardlayout/pictures/" + decoration.getPicture()))
                pic = os.path.dirname(__file__)  + "/pictures/" + decoration.getPicture()

                item.setPictureFile( pic )
                item.setBackgroundEnabled(False)
                item.setSceneRect(QRectF(0,  0, decoration.getWidth(), decoration.getHeight()))
                item.setFrameOutlineWidth(0.2)
                item.setFrameEnabled(True)
                item.setItemPosition(margin_left+offset_x, margin_top+offset_y)
                if type == "northarrow":
                    item.setRotationMap(0)
                    item.setFrameEnabled(False)
##                item.setFrame(0)
                item.setZValue(30)
                item.setPositionLock(True)

                if self.printToFile == False:
                    composition.addComposerPicture(item)
                    # alter code:   composerView.addComposerPicture(item)
                else:
                    composition.addItem(item)
                    composition.addComposerPicture(item)



            #--------------------------------------------------------------------
            # Header oder Footer
            #--------------------------------------------------------------------
            elif type == "header"  or type == "footer":
                height = decoration.getHeight()
                width = decoration.getWidth()
                if type == "header":
                    headerHeight = height
                    headerWidth = width
                elif type == "footer":
                    footerHeight = height
                    footerWidth = width


                #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:183", "footerWidth: %s\n" %(footerWidth))
                # Keine width im layout.xml angegeben

                # Note: Logik ist nicht von der Orientierung abhängig, da bereits je nach orintierung paperheight und paperwidth korrekt gesetzt sind.

                if footerWidth < 1:
                    if orientation == "portrait":
                        item = QgsComposerShape(margin_left+offset_x,  margin_top+offset_y, float(paperwidth)-(margin_right+margin_left),  height, composition)
                    else:
                        item = QgsComposerShape(margin_left+offset_x,  margin_top+offset_y, float(paperwidth)-(margin_right+margin_left),  height, composition)
                else:
                    # Test in X-Dimension
                    test = float(paperwidth) - width - (margin_right+margin_left) - offset_x
                    if test < 0:
                        QMessageBox.warning(None, "doVogisPrintCreateSimpleMap.py:193", "footerWidth: %s und x-offset: %s passt nicht ins Papier rein\n" %(footerWidth,offset_x))
                    # Test in Y-Dimension
                    test = float(paperheight) - height - (margin_top+margin_bottom) - offset_y
                    if test < -0.1:
                        QMessageBox.warning(None, "doVogisPrintCreateSimpleMap.py:200", "footerHeight: %s und y-offset: %s passt nicht ins Papier rein test = %f\n" %(footerHeight,offset_y,test))
                    # Zeichnen
                    item = QgsComposerShape(margin_left+offset_x,  margin_top+offset_y, width,  height, composition)




                item.setShapeType(1)
##                item.setLineWidth(0.0)
                pen = QPen()
                pen.setWidthF(0.2)
                pen.setJoinStyle(Qt.MiterJoin)
                item.setPen(pen)
                item.setPositionLock(True)


                if self.printToFile == False:
                    composition.addComposerShape(item)
                    #alt composerView.addComposerShape(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerShape(item)

                brush = QBrush()
                brush.setStyle(Qt.SolidPattern)
                brush.setColor(Qt.white)
                item.setBrush(brush)
                item.setBackgroundEnabled(True)
                item.setZValue(20)

            #--------------------------------------------------------------------
            # Title oder Subtitle oder Person
            #--------------------------------------------------------------------
            elif type == "title" or type == "subtitle" or type == "person":
                titleFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsComposerLabel(composition)
                item.setFont(titleFont)
                if type == "title":
                    item.setText(self.titleString)
                elif type == "subtitle":
                    item.setText(self.subtitleString)
                elif type == "person":
                    item.setText(decoration.getText() + self.personString)
                item.adjustSizeToText()
##                item.setFrame(0)
                item.setMargin(0)
                brush = QBrush()
                brush.setStyle(Qt.NoBrush)
                brush.setColor(Qt.white)
                item.setBackgroundEnabled(False)
                item.setBrush(brush)
                item.setPositionLock(True)
                item.setZValue(40)
                if type == "title" or type == "subtitle":
                    # Text Zentriert Middle=4
                    # item.setItemPosition(int(paperwidth)/2 -20,  margin_top+offset_y, 4)
                    item.setItemPosition(margin_left+offset_x,  margin_top+offset_y, 4)
                else:
                    item.setItemPosition(margin_left+offset_x,  margin_top+offset_y)
                if self.printToFile == False:
                    composition.addComposerLabel(item)
                    # alter code: composerView.addComposerLabel(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerLabel(item)

            #--------------------------------------------------------------------
            # Dapartment
            #--------------------------------------------------------------------
            elif type == "department":
                departmentFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsComposerLabel(composition)
                item.setBackgroundEnabled(False)
                item.setFont(departmentFont)
                item.setText(decoration.getText() + self.departmentString)
                item.adjustSizeToText()
##                item.setFrame(0)
                item.setMargin(0)
                brush = QBrush()
                brush.setStyle(Qt.NoBrush)
                brush.setColor(Qt.white)
                item.setBrush(brush)
                item.setItemPosition(margin_left+offset_x,  margin_top+offset_y,4)
                item.setPositionLock(True)
                item.setZValue(40)

                if self.printToFile == False:
                    composition.addComposerLabel(item)
                    # alter code:   composerView.addComposerLabel(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerLabel(item)



            #--------------------------------------------------------------------
            # Text oder Author oder Copyright
            #--------------------------------------------------------------------
            elif type == "text" or type == "author" or type == "copyright":
                if self.copyright == True:
                    textFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                    item = QgsComposerLabel(composition)
                    item.setBackgroundEnabled(True)
                    item.setFont(textFont)
                    item.setText(unicode(decoration.getText()))
                    if decoration.getWidth() > 0:
                        item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                    else:
                        item.adjustSizeToText()
##                    item.setFrame(0)
                    item.setMargin(0)
                    brush = QBrush()
                    brush.setStyle(Qt.NoBrush)
                    brush.setColor(Qt.white)
                    item.setBrush(brush)
                    item.setZValue(40)
                    item.setItemPosition(margin_left+offset_x,  margin_top+offset_y)
                    item.setPositionLock(True)

                    # Rotate the item. (does not work...)
                    if decoration.getRotation() != 0:
                        item.setRotation(decoration.getRotation())

                    if type == "copyright" and copyright == False:
                        continue
                    else:
                        if self.printToFile == False:
                            composition.addComposerLabel(item)
                            # alter code:  composerView.addComposerLabel(item)
                        else:
##                            composition.addItem(item)
                            composition.addComposerLabel(item)


            #--------------------------------------------------------------------
            # Date
            #--------------------------------------------------------------------
            elif type == "date":
                dateFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsComposerLabel(composition)
                item.setBackgroundEnabled(False)
                item.setFont(dateFont)
                d = time.localtime()
                item.setText(unicode(decoration.getText()) + "%d.%d.%d" % (d[2],  d[1],  d[0]))
                item.adjustSizeToText()
##                item.setFrame(0)
                item.setMargin(0)
                brush = QBrush()
                brush.setStyle(Qt.NoBrush)
                brush.setColor(Qt.white)
                item.setBrush(brush)
                item.setItemPosition(margin_left+offset_x,  margin_top+offset_y)
                item.setPositionLock(True)
                item.setZValue(40)

                if self.printToFile == False:
                    composition.addComposerLabel(item)
                    # alter code:   composerView.addComposerLabel(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerLabel(item)


            #--------------------------------------------------------------------
            # Crsdescription
            #--------------------------------------------------------------------
            elif type == "crsdescription":
                if self.crsdesc == True:
                    textFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                    item = QgsComposerLabel(composition)
                    item.setFont(textFont)
                    item.setBackgroundEnabled(False)

                    srsDescriptionText = self.iface.mapCanvas().mapRenderer().destinationCrs().description()
                    itemText = unicode(decoration.getText()) + unicode(str(srsDescriptionText))
                    item.setText(itemText)

                    if decoration.getWidth() > 0:
                        item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                    else:
                        item.adjustSizeToText()
##                    item.setFrame(0)
                    item.setMargin(0)
                    brush = QBrush()
                    brush.setStyle(Qt.NoBrush)
                    brush.setColor(Qt.white)
                    item.setBrush(brush)
                    item.setPositionLock(True)
                    item.setZValue(40)
                    item.setItemPosition(margin_right+offset_x,  margin_bottom+offset_y)

                    if self.printToFile == False:
                        composition.addComposerLabel(item)
                        # alter code:   composerView.addComposerLabel(item)

                    else:
##                        composition.addItem(item)
                        composition.addComposerLabel(item)


            #--------------------------------------------------------------------
            # Legend
            #--------------------------------------------------------------------
            elif type == "legend":
                if self.legend == True:
                    legendFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                    groupFont = QFont(decoration.getFontFamily(), decoration.getFontSize()-1)
                    layerFont = QFont(decoration.getFontFamily(), decoration.getFontSize()-2)
                    itemFont = QFont(decoration.getFontFamily(), decoration.getFontSize()-2)
                    item = QgsComposerLegend(composition)
                    item.setBackgroundEnabled(True)
                    item.setTitle(decoration.getText())
                    item.adjustBoxSize()
                    item.setPositionLock(True)
                    item.setItemPosition(margin_left+offset_x, margin_top+offset_y)
##                    item.setItemFont(itemFont)
##                    item.setLayerFont(layerFont)
                    try:
                        item.setStyleFont(0,groupFont)
                    except:
##                        print "EASYPRINT: old qgis version..."
                        QMessageBox.information(None, 'Warning', "EASYPRINT: old qgis version...")


                    if self.printToFile == False:
                        composition.addComposerLegend(item)
                         # alter code:   composerView.addComposerLegend(item)
                    else:
                        item.updateLegend()
                        item.adjustBoxSize()
##                        composition.addItem(item)
                        composition.addComposerLegend(item)

                    item.updateLegend()

            #--------------------------------------------------------------------
            # Map
            #--------------------------------------------------------------------
            elif type == "map":
                #QMessageBox.warning( None, "doVogisPrintCreateSimpleMap:441", "elif type == map:  self.printScale = %s" %(self.printScale))

                scale = float(self.printScale)

                # composermap erstellen
                if orientation == "portrait":
                    mapWidth = float(paperwidth)-(margin_right+margin_left)
                    # mapHeight = float(paperheight)-margin_top-margin_bottom-footerHeight
                    mapHeight = float(paperheight)-margin_top-margin_bottom
                    composerMap = QgsComposerMap(composition, margin_left+offset_x,  margin_top+offset_y, mapWidth,  mapHeight)
                else:
                    mapWidth = float(paperwidth) - (margin_right+margin_left)
                    #mapHeight = float(paperheight) - margin_top-margin_bottom - footerHeight
                    mapHeight = float(paperheight) - margin_top-margin_bottom
                    composerMap = QgsComposerMap(composition, margin_left+offset_x,  margin_top+offset_y, mapWidth,  mapHeight )

                #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:418", "margin_left+offset_x:%s\nmargin_top+offset_y:%s\nmapWidth: %s\nmapHeight: %s\n" %(str(margin_left+offset_x),str(margin_top+offset_y),str(mapWidth),str(mapHeight)))


                # Logik abhaengig vom Mapextent
                if self.mapExtent == None:
                    #QMessageBox.about( None, "doVogisPrintCreateSimpleMap.py:416", "self.mapExtent == None:")
                    # No mapExtent means we are in the standard easyprint mode.
                    # This is a workaround for latlon stuff. Why is setNewScale not working?
                    projectEPSG = self.canvas.mapRenderer().destinationCrs().toProj4()
                    if str.find(str(projectEPSG),  "+proj=longlat") >= 0:
                        composerMap.setNewScale(scale) # Does not center correctly?
                    else:
                        rect = self.getMapExtentFromMapCanvas(mapWidth,  mapHeight,  scale)
                        composerMap.setNewExtent(rect)
                        #QMessageBox.about(None, "doVogisPrintCreateSimpleMap:436",  " rect.height: %s "  %(str(rect.height())) )
                else:
                    # If mapExtent is empty, it is a point.
                    # We do consider the printScale here.
                    if self.mapExtent.isEmpty():
                        #QMessageBox.about( None, "doVogisPrintCreateSimpleMap.py:428", "If mapExtent is empty, it is a point.")
                        projectEPSG = self.canvas.mapRenderer().destinationSrs().toProj4()
                        #QMessageBox.about(None, "CreateMapBookByFeature.getMapExtentFromPoint", "projectEPSG %s" %(str(projectEPSG)))
                        if str.find(str(projectEPSG),  "+proj=longlat") >= 0:
                            composerMap.setNewScale(scale) # Does not center correctly?
                        else:
                            self.newMapExtent = self.getMapExtentFromPoint(mapWidth, mapHeight, scale, self.mapExtent.center())
                            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap:436", "xmin %.0f\nymin %.0f \nxmax %.0f \nymax %.0f " %(self.newMapExtent.xMinimum() , self.newMapExtent.yMinimum() , self.newMapExtent.xMaximum() , self.newMapExtent.yMaximum()))
                            composerMap.setNewExtent(self.newMapExtent)

                    # Extent vorhanden, also Polygone oder Line
                    else:
                        #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:442", "Extent vorhanden, also Polygone oder Line")
                        if self.useExtent == True:
                            # Since the ratio of the feature's extent the one from the map may not be identical (except mapbook by grid)
                            # we have to calculate e new map extent.
                            self.newMapExtent = self.getMapExtentFromFeatureExtent(mapWidth, mapHeight, self.mapExtent)
                            self.newMapExtent.scale(float(1))
                            composerMap.setNewExtent(self.newMapExtent)
                        else:
                            projectEPSG = self.canvas.mapRenderer().destinationCrs().toProj4()
                            if str.find(str(projectEPSG),  "+proj=longlat") >= 0:
                                composerMap.setNewScale(scale) # Does not center correctly?
                            else:
                                self.newMapExtent = self.getMapExtentFromPoint(mapWidth, mapHeight, scale, self.mapExtent.center())
                                composerMap.setNewExtent(self.newMapExtent)

                            self.newMapExtent = self.getMapExtentFromPoint(mapWidth, mapHeight, scale, self.mapExtent.center())
                            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:457", "xmin %.0f\nymin %.0f \nxmax %.0f \nymax %.0f " %(self.newMapExtent.xMinimum() , self.newMapExtent.yMinimum() , self.newMapExtent.xMaximum() , self.newMapExtent.yMaximum()))
                            composerMap.setNewExtent(self.newMapExtent)

                    composerMap.setRotation(float(self.printRotation))

                # Ausgabe herrichten
##                composerMap.setFrame(1)
                pen = QPen()
                pen.setWidthF(0.2)
                pen.setJoinStyle(Qt.MiterJoin)
                composerMap.setPen(pen)
                composerMap.setPreviewMode(2)   # Does not work!?!?!
                composerMap.setPositionLock(False)
                composerMap.setFrameEnabled(True)
                composerMap.setZValue(1)
                # Grids and grid annotations
                if self.grid == True:
                    #QMessageBox.about(None, "grid", 'grid')
                    interval = self.getGridInterval(composerMap.scale())
                    composerMap.setGridEnabled(True)
                    composerMap.setGridStyle(1)
                    composerMap.setGridIntervalX(interval)
                    composerMap.setGridIntervalY(interval)
                    composerMap.setShowGridAnnotation(True)
                    gridFont = QFont(decoration.getFontFamily(), 6)
                    gridFont.setItalic(True)
                    composerMap.setGridAnnotationFont(gridFont)
                    composerMap.setGridAnnotationPrecision(0)

                    #Position der Grid Annotation für jede Seitenkante einstellen
                    composerMap.setGridAnnotationPosition(0,0)
                    composerMap.setGridAnnotationPosition(0,1)
                    composerMap.setGridAnnotationPosition(0,2)
                    composerMap.setGridAnnotationPosition(0,3)

                    #composerMap.setGridAnnotationDirection(2,3)
                    composerMap.setAnnotationFrameDistance(4)
                    composerMap.setGridPenWidth(0.1)

                if self.printToFile == False:
                    #print "CreateSimpleMap:484 printToFile == False"
                    #QMessageBox.about(None, "printtofile", str(composition))
                    #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:457", 'printtofile false')
                    composition.addComposerMap(composerMap)
                    #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:457", 'printtofile false')
                    # alter code: composerView.addComposerMap(composerMap)
                else:
                    #QMessageBox.about(None, "printtofle", str(composerMap))
                    #print "CreateSimpleMap:484 printToFile == True"
                    #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:457", 'printtofile true')
                    #composition.addItem(composerMap)
                    composition.addComposerMap(composerMap)



            #--------------------------------------------------------------------
            # Scaletext
            #--------------------------------------------------------------------
            elif type == "scaletext":
                textFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsComposerLabel(composition)
                item.setFont(textFont)
                item.setText(unicode(decoration.getText()))
                item.adjustSizeToText()
                item.setBackgroundEnabled(False)
                if decoration.getWidth() > 0:
                    item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                else:
                    item.adjustSizeToText()
##                item.setFrame(0)
                item.setMargin(0)
                brush = QBrush()
                brush.setStyle(Qt.NoBrush)
                brush.setColor(Qt.white)
                item.setBrush(brush)
                item.setPositionLock(True)
                item.setZValue(40)
                item.setItemPosition(margin_right+offset_x,  margin_bottom+offset_y)

                if self.printToFile == False:
                    composition.addComposerLabel(item)
                    # alter code: composerView.addComposerLabel(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerLabel(item)

                composerScaleBar = QgsComposerScaleBar(composition)
##                composerScaleBar.removeSettings()

                composerScaleBar.setComposerMap(composerMap)
                composerScaleBar.setFont(textFont)
                composerScaleBar.setStyle('Numeric')
##                composerScaleBar.setFrame(0)
                composerScaleBar.setBoxContentSpace(0.3) # heuristic
                composerScaleBar.setPositionLock(True)
                composerScaleBar.adjustBoxSize()
                composerScaleBar.setBackgroundEnabled(False)
                composerScaleBar.setZValue(40)
                composerScaleBar.setBoxContentSpace(0.0) # heuristic -> sonst passts unter 2.0 nicht!
                composerScaleBar.update()


                width = item.boundingRect().width()
                height = item.boundingRect().height()


                composerScaleBar.setItemPosition(margin_right + offset_x + width-3, margin_bottom + offset_y)

                if self.printToFile == False:
                    composition.addComposerScaleBar(composerScaleBar)
                    # alter code: composerView.addComposerScaleBar(composerScaleBar)
                else:
##                    composition.addItem(composerScaleBar)
                    composition.addComposerScaleBar(composerScaleBar)


            #--------------------------------------------------------------------
            # Mapbookid
            #--------------------------------------------------------------------
            elif type == "mapbookid" and self.tileName <> None:
                textFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                brush = QBrush()
#                brush.setStyle(Qt.SolidPattern)
                brush.setStyle(Qt.NoBrush)
                brush.setColor(Qt.white)
                pen = QPen()
                pen.setWidthF(0.0)
                pen.setJoinStyle(Qt.MiterJoin)
                item = QgsComposerLabel(composition)
                item.setFont(textFont)
                item.setText("Mapbook Id: " + unicode(self.tileName))
                item.adjustSizeToText()
                item.setBrush(brush)
##                item.setFrame(0)
                item.setMargin(0)
                item.setZValue(20)
                item.setItemPosition(margin_left+offset_x,  margin_top+offset_y)

                if self.printToFile == False:
                    composition.addComposerLabel(item)
                    # alter code: composerView.addComposerLabel(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerLabel(item)


            #--------------------------------------------------------------------
            # tileindicator
            #--------------------------------------------------------------------
            elif type == "tileindicator" and self.adjacentTiles <> None:
                textFont = QFont(decoration.getFontFamily(), decoration.getFontSize())
                brush = QBrush()
                brush.setStyle(Qt.SolidPattern)
                brush.setColor(Qt.white)
                pen = QPen()
                pen.setWidthF(0.1)
                pen.setJoinStyle(Qt.MiterJoin)

                k = 0
                for i in range(3):
                    for j in range(3):
                        item = QgsComposerLabel(composition)
                        item.setFont(textFont)
                        item.setText(unicode(self.adjacentTiles[k]))

                        if decoration.getWidth() > 0 and decoration.getHeight() > 0:
                            item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                            item.setPen(pen)
                            if k == 4:
                                brush.setColor(Qt.lightGray)
                            else:
                                brush.setColor(Qt.white)
                            item.setBrush(brush)
                            item.setZValue(20)

                            if decoration.getAffinityX() == "right":
                                tile_offset_x = offset_x - 3 * decoration.getWidth()

                            if decoration.getAffinityY() == "bottom":
                                tile_offset_y = offset_y - 2 * decoration.getHeight()

                            item.setItemPosition(margin_left+tile_offset_x+j*decoration.getWidth(),  margin_top+tile_offset_y+(2-i)*decoration.getHeight())

                            if self.printToFile == False:
                                composition.addComposerLabel(item)
                                 # alter code: composerView.addComposerLabel(item)
                            else:
##                                composition.addItem(item)
                                composition.addComposerLabel(item)

                        k = k +1

                # No Python binding.... :(
#                item.setHAlign(Qt.AlignHCenter)
#                item.setVAlign(Qt.AlignVCenter)


    #******************************************************************************************#
    #Code wird nicht mehr benötigt?? und stört die Layouterzeugung ab 2.4
    #von hier
    #******************************************************************************************#

##        self.printToFile = False
##        #------------------------------------------------------------------------------
##        # Ausgabe in ein File
##        #------------------------------------------------------------------------------
##        #QMessageBox.warning( None, "doVogisPrintCreateSimpleMap.py:661", "Hier")
##        if self.printToFile == True:
##
##            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:664", "Start File-Print")
##
##
##            if self.printer == None:
##                #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:667", "self.printer == None")
##                self.printer = QPrinter()
##                self.printer.setOutputFormat(QPrinter.PdfFormat)
##                self.printer.setOutputFileName(self.fileName)
##
##            self.printer.newPage()
##            self.printer.setPaperSize(QSizeF(composition.paperWidth(), composition.paperHeight()), QPrinter.Millimeter)
##            self.printer.setFullPage(True)
##            self.printer.setColorMode(QPrinter.Color)
##            self.printer.setResolution(composition.printResolution())
##
##
##
##            # FIXME Warum wird hier nochmals ein Painter angelegt ??????
##            # Es haengt mit dem Seriendruzck zusammen.
##            if self.painter == None:
##                #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:687", "self.painter = QPainter(self.printer)")
##                self.painter = QPainter(self.printer)
##
##
##            paperRectMM = self.printer.pageRect(QPrinter.Millimeter)
##            paperRectPixel = self.printer.pageRect(QPrinter.DevicePixel)
##
##            # Als Bild drucken
##            if self.printAsRaster == True:
##                dpi = composition.printResolution()
##                dpmm = dpi / 25.4
##                width = int(dpmm * composition.paperWidth())
##                height = int(dpmm * composition.paperHeight())
##
##                image = QImage(QSize(width, height), QImage.Format_ARGB32)
##                image.setDotsPerMeterX(dpmm * 1000)
##                image.setDotsPerMeterY(dpmm * 1000)
##                image.fill(0)
##
##                imagePainter = QPainter(image)
##                sourceArea = QRectF(0, 0, composition.paperWidth(), composition.paperHeight())
##                targetArea = QRectF(0, 0, width, height)
##                #print "doVogisPrintCreateSimpleMap.py:665: MIT PrintAsRaster: composition.render(imagePainter, targetArea, sourceArea)"
##                composition.render(imagePainter, targetArea, sourceArea)
##                imagePainter.end()
##
##                # Hier wird gerendert
##                if self.painter.isActive():
##                    #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:685", "vor self.painter.drawImage.")
##                    self.painter.drawImage(paperRectPixel, image, QRectF(0, 0, image.width(), image.height()))
##                else:
##                    message = "<FONT COLOR='#000000' SIZE=4>Datei <FONT COLOR='#000080' SIZE=4>%s<FONT COLOR='#000000' SIZE=4> kann nicht erstellt werden!\nMöglicherweise im PDF-Viewer geöffnet?<br>Bitte PDF-Viewer schließen und Druck danach neu starten." %(str(self.fileName))
##                    message = (message).decode('utf8')
##                    QMessageBox.critical(None, "PDF-Druck-Problem !", message)
##                    # Junk Fehler-Handling. Funktioniert aber.
##                    self.printer = 9999
##            else:
##                #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:713", "composition.render(self.painter, paperRectPixel, paperRectMM)")
##                #print "doVogisPrintCreateSimpleMap.py:713 vor composition.render"
##                if self.painter.isActive():
##                    composition.render(self.painter, paperRectPixel, paperRectMM)
##                else:
##                    message = "<FONT COLOR='#000000' SIZE=4>Datei <FONT COLOR='#000080' SIZE=4>%s<FONT COLOR='#000000' SIZE=4> kann nicht erstellt werden!\nMöglicherweise im PDF-Viewer geöffnet?<br>Bitte PDF-Viewer schließen und Druck danach neu starten." %(str(self.fileName))
##                    message = (message).decode('utf8')
##                    QMessageBox.critical(None, "PDF-Druck-Problem !", message)
##                    # Junk Fehler-Handling. Funktioniert aber.
##                    self.printer = 9999
##
##            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:685", "return self.printer, self.painter.")
##
##
##            return self.printer, self.painter
##
##
##        #------------------------------------------------------------------------------
##        # Ausgabe auf den Schirm
##        #------------------------------------------------------------------------------
##        else:
##            #QMessageBox.about(None, "doVogisPrintCreateSimpleMap.py:674", " Ausgabe auf den Schirm composerView.setComposition(composition)")
##
##            composerView.setComposition(composition)
##            composer = composerView.composerWindow()
##            composer.show()
##
##        #print "doVogisPrintCreateSimpleMap.py:686 Ende von run()"

    #******************************************************************************************#
    #Code wird nicht mehr benötigt?? und stört die Layouterzeugung ab 2.4
    #bis hier
    #******************************************************************************************#


    #******************************************************************************
    # getMapExtentFromFeatureExtent()
    #******************************************************************************
    def getMapExtentFromFeatureExtent(self, mapWidth, mapHeight, featExtent):
        featWidth = featExtent.width()
        featHeight = featExtent.height()

        #print mapWidth/mapHeight
        #print featExtent.width()/featExtent.height()

        if (mapWidth/mapHeight) > (featWidth/featHeight):
            center = featExtent.center()
            xcenter = center.x()
            ycenter = center.y()

            minx = xcenter - (featHeight/(mapHeight/mapWidth)) / 2
            maxx = xcenter + (featHeight/(mapHeight/mapWidth)) / 2

            return QgsRectangle(minx,  featExtent.yMinimum(),  maxx,  featExtent.yMaximum())

        elif (mapWidth/mapHeight) < (featWidth/featHeight):
            center = featExtent.center()
            xcenter = center.x()
            ycenter = center.y()

            miny = ycenter - (featWidth/(mapWidth/mapHeight)) / 2
            maxy = ycenter + (featWidth/(mapWidth/mapHeight)) / 2

            return QgsRectangle(featExtent.xMinimum(),  miny,  featExtent.xMaximum(),  maxy)

        else:
            return featExtent


    #******************************************************************************
    # getMapExtentFromPoint()
    #******************************************************************************
    def getMapExtentFromPoint(self, mapWidth, mapHeight, scale, point):
        #QMessageBox.about(None,"getMapExtentFromPoint" ,  "Start getMapExtentFromPoint")
        center = point
        xcenter = center.x()
        ycenter = center.y()

        mapWidth = mapWidth * scale / 1000
        mapHeight = mapHeight * scale / 1000

        minx = xcenter - mapWidth / 2
        miny = ycenter - mapHeight / 2
        maxx = xcenter + mapWidth / 2
        maxy = ycenter + mapHeight / 2
        #QMessageBox.about(None,"getMapExtentFromPoint" , "Ende getMapExtentFromPoint")

        return QgsRectangle(minx,  miny,  maxx,  maxy)


    #******************************************************************************
    # getMapExtentFromMapCanvas()
    #******************************************************************************
    def getMapExtentFromMapCanvas(self,  mapWidth,  mapHeight,  scale):
        xmin = self.canvas.extent().xMinimum()
        xmax = self.canvas.extent().xMaximum()
        ymin = self.canvas.extent().yMinimum()
        ymax = self.canvas.extent().yMaximum()
        xcenter = xmin + (xmax - xmin) / 2
        ycenter = ymin + (ymax - ymin) / 2

        mapWidth = mapWidth * scale / 1000
        mapHeight = mapHeight * scale / 1000
        minx = xcenter - mapWidth / 2
        miny = ycenter - mapHeight / 2
        maxx = xcenter + mapWidth / 2
        maxy = ycenter + mapHeight / 2

        return QgsRectangle(minx,  miny,  maxx,  maxy)


    #******************************************************************************
    # getGridInterval()
    #******************************************************************************
    def getGridInterval(self,  scale):
        #QMessageBox.about(None,"doVogisPrintCreateSimpleMap.py:766" , "scale = %s" %(scale))
        power = math.floor(math.log10(scale))
        interval = int( round((scale/10)/(pow(10, power-1)))*(pow(10, power-1)) )
        return interval


    #******************************************************************************
    # cuttingLines()
    #******************************************************************************
    def cuttingLines(self, composition, composerView=None):
        offset = 0.1
        lineLength = 10
        paperHeight = composition.paperHeight()
        paperWidth = composition. paperWidth()

        ## top,left
        item = QgsComposerShape(0,  0,  lineLength,  0,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        item = QgsComposerShape(0,  0,  0,  lineLength,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        ## top,right
        item = QgsComposerShape(paperWidth-lineLength,  0,  lineLength,  0,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        item = QgsComposerShape(paperWidth-offset,  0,  0,  lineLength,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        ## bottom,right
        item = QgsComposerShape(paperWidth-lineLength,  paperHeight-offset,  lineLength,  0, composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        item = QgsComposerShape(paperWidth-offset,  paperHeight-lineLength,  0,  lineLength,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        ## bottom,left
        item = QgsComposerShape(0,  paperHeight-offset,  lineLength,  0, composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)

        item = QgsComposerShape(0,  paperHeight-lineLength,  0,  lineLength,  composition)
        item.setShapeType(1)
##        item.setLineWidth(0.0)
        pen = QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(Qt.MiterJoin)
        item.setPen(pen)
        item.setPositionLock(True)
        if self.printToFile == False:
            composition.addComposerShape(item)
            # alter code: composerView.addComposerShape(item)
        else:
##            composition.addItem(item)
            composition.addComposerShape(item)


    #******************************************************************************
    # foldingMarks()
    #******************************************************************************
    def foldingMarks(self, composition, composerView=None):
        markWidth = 210
        markHeight = 297
        lineLength = 4
        paperHeight = composition.paperHeight()
        paperWidth = composition. paperWidth()

        if paperWidth / markWidth > 1:
            count = int(round(paperWidth/markWidth, 0))
            for i in range(1, count):
                item = QgsComposerShape(i * markWidth, 0,  0, lineLength, composition)
                item.setShapeType(1)
##                item.setLineWidth(0.0)
                pen = QPen()
                pen.setWidthF(0.05)
                pen.setJoinStyle(Qt.MiterJoin)
                item.setPen(pen)
                item.setPositionLock(True)
                if self.printToFile == False:
                    composition.addComposerShape(item)
                    # alter code: composerView.addComposerShape(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerShape(item)

                item = QgsComposerShape(i * markWidth,  paperHeight - lineLength,   0, lineLength,  composition)
                item.setShapeType(1)
##                item.setLineWidth(0.0)
                pen = QPen()
                pen.setWidthF(0.05)
                pen.setJoinStyle(Qt.MiterJoin)
                item.setPen(pen)
                item.setPositionLock(True)
                if self.printToFile == False:
                    composition.addComposerShape(item)
                    # alter code: composerView.addComposerShape(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerShape(item)

        if paperHeight  / markHeight > 1:
            count = int(round(paperHeight/markHeight, 0))
            if count == 1:
                count = count + 1

            for i in range(1, count):
                item = QgsComposerShape(0, i * markHeight, lineLength, 0,  composition)
                item.setShapeType(1)
##                item.setLineWidth(0.0)
                pen = QPen()
                pen.setWidthF(0.05)
                pen.setJoinStyle(Qt.MiterJoin)
                item.setPen(pen)
                item.setPositionLock(True)
                if self.printToFile == False:
                    composition.addComposerShape(item)
                    # alter code: composerView.addComposerShape(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerShape(item)

                item = QgsComposerShape(paperWidth-lineLength, i * markHeight, lineLength, 0,  composition)
                item.setShapeType(1)
##                item.setLineWidth(0.0)
                pen = QPen()
                pen.setWidthF(0.05)
                pen.setJoinStyle(Qt.MiterJoin)
                item.setPen(pen)
                item.setPositionLock(True)
                if self.printToFile == False:
                    composition.addComposerShape(item)
                    # alter code: composerView.addComposerShape(item)
                else:
##                    composition.addItem(item)
                    composition.addComposerShape(item)
