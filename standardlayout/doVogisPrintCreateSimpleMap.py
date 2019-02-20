 # -*- coding: utf8 -*-
from qgis.PyQt import *
from qgis.PyQt import *
from qgis.core import *
from qgis.gui import *
import math, time, os
from VogisPrint_Utils import *

class CreateSimpleMap( QtCore.QObject ):


    def __init__( self, iface, printScale, printFormat, layoutIndex, titleString, subtitleString, personString, departmentString, crsdesc, grid, legend, copyright, cuttinglines, foldingmarks, stand_dkm):
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
        #QtWidgets.QMessageBox.warning( None, "run", str((layouts)))
        layout = layouts[self.layoutIndex]
        #QMessageBox.about(None, "dkm", str(self.stand_dkm))
        margins = layout.getMargins()
        margin_top = margins['margin-top']
        margin_right = margins['margin-right']
        margin_bottom = margins['margin-bottom']
        margin_left = margins['margin-left']



        orientation = layout.getOrientation()
        #QtWidgets.QMessageBox.about(None, "Papier", str(self.printFormat) + ' ' + str(orientation))
        if orientation == "landscape":
            paperwidth_tmp = paperwidth
            paperwidth = paperheight
            paperheight = paperwidth_tmp

        headerHeight = 0
        footerHeight = 0


        beforeList = QgsProject.instance().layoutManager().layouts()
        self.iface.actionCreatePrintLayout().trigger()
        afterList = QgsProject.instance().layoutManager().layouts()


        # Referenz auf den Print Manager erhalten
        if len(afterList) < 1:
            return
        diffList = []
        for item in afterList:
            if not item in beforeList:
                diffList.append(item)

        composerView = diffList[0]

        # Print Layout erzeugen und die
        # Seiteneinstellungen übernehmen
        composition = QgsLayoutItemPage(composerView)
        composition.setPageSize(QgsLayoutSize(float(paperwidth), float(paperheight)))
        pk = composerView.pageCollection()
        pk.page(0).setPageSize(QgsLayoutSize(float(paperwidth), float(paperheight)))    # wir haben immer nur eine Seite in unserem Printlayout



        #----------------------------------
        # Cutting lines.
        #----------------------------------
        if self.cuttinglines == True:
            self.calcCuttingLines(composition, composerView)


        #----------------------------------
        # Folding marks.
        #----------------------------------
        if self.foldingmarks == True:
            self.foldingMarks(composition, composerView)


        #---------------------------------------------------------------------------
        #---------------------------------------------------------------------------
        # Loop ueber die Decorations
        #---------------------------------------------------------------------------
        #---------------------------------------------------------------------------
        decorations = layout.getDecorations()   # Wird vom Layout XML bestimmt
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

                item = QgsLayoutItemPicture(composerView)
                pic = os.path.dirname(__file__)  + "/pictures/" + decoration.getPicture()

                item.setPicturePath( pic )
                item.setBackgroundEnabled(False)
                item.attemptSetSceneRect(QtCore.QRectF(0,  0, decoration.getWidth(), decoration.getHeight()))
                item.setFrameStrokeWidth(QgsLayoutMeasurement(0.2))

                item.setFrameEnabled(True)
                item.attemptMoveBy(margin_left+offset_x, margin_top+offset_y)
                if type == "northarrow":
                    #item.setRotationMap(0)
                    item.setItemRotation(0)
                    item.setFrameEnabled(False)
                item.setZValue(30)
                item.setLocked(True)

                composerView.addLayoutItem(item)


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
                        item = QgsLayoutItemShape(composerView)
                        item.attemptSetSceneRect(QtCore.QRectF(margin_left+offset_x,  margin_top+offset_y, float(paperwidth)-(margin_right+margin_left),  height))
                    else:
                        item = QgsLayoutItemShape(composerView)
                        item.attemptSetSceneRect(QtCore.QRectF(margin_left+offset_x,  margin_top+offset_y, float(paperwidth)-(margin_right+margin_left),  height))
                else:
                    # Test in X-Dimension
                    test = float(paperwidth) - width - (margin_right+margin_left) - offset_x
                    if test < 0:
                        QtWidgets.QMessageBox.warning(None, "doVogisPrintCreateSimpleMap.py:193", "footerWidth: %s und x-offset: %s passt nicht ins Papier rein\n" %(footerWidth,offset_x))
                    # Test in Y-Dimension
                    test = float(paperheight) - height - (margin_top+margin_bottom) - offset_y
                    if test < -0.1:
                        QtWidgets.QMessageBox.warning(None, "doVogisPrintCreateSimpleMap.py:200", "footerHeight: %s und y-offset: %s passt nicht ins Papier rein test = %f\n" %(footerHeight,offset_y,test))
                    # Zeichnen
                    item = QgsLayoutItemShape(composerView)
                    item.attemptSetSceneRect(QtCore.QRectF(margin_left+offset_x,  margin_top+offset_y, width,  height))




                item.setShapeType(1)
                pen = QtGui.QPen()
                pen.setWidthF(0.2)
                pen.setJoinStyle(0)
                item.setPen(pen)
                item.setLocked(True)

                composerView.addLayoutItem(item)

                brush = QtGui.QBrush()
                brush.setStyle(1)
                brush.setColor(3)
                item.setBrush(brush)
                item.setBackgroundEnabled(True)
                item.setZValue(20)

            #--------------------------------------------------------------------
            # Title oder Subtitle oder Person
            #--------------------------------------------------------------------
            elif type == "title" or type == "subtitle" or type == "person":
                titleFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsLayoutItemLabel(composerView)
                #QtWidgets.QMessageBox.about(None, "title", str(titleFont.pointSize()))
                item.setFont(titleFont)
                if type == "title":
                    item.setText(self.titleString)
                elif type == "subtitle":
                    item.setText(self.subtitleString)
                elif type == "person":
                    item.setText(decoration.getText() + self.personString)
                item.adjustSizeToText()
                item.setMargin(0)
                brush = QtGui.QBrush()
                brush.setStyle(0)
                brush.setColor(3)
                item.setBackgroundEnabled(False)
                item.setBrush(brush)
                item.setLocked(True)
                item.setZValue(40)
                if type == "title" or type == "subtitle":
                    # Text Zentriert Middle=4
                    item.setReferencePoint(4)
                    item.attemptMove(QgsLayoutPoint(margin_left+offset_x,  margin_top+offset_y-1),True)
                else:
                    item.attemptMove(QgsLayoutPoint(margin_left+offset_x,  margin_top+offset_y),True)

                composerView.addLayoutItem(item)

            #--------------------------------------------------------------------
            # Dapartment
            #--------------------------------------------------------------------
            elif type == "department":
                departmentFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsLayoutItemLabel(composerView)
                item.setBackgroundEnabled(False)
                item.setFont(departmentFont)
                item.setText(decoration.getText() + self.departmentString)
                item.adjustSizeToText()
                item.setMargin(0)
                brush = QtGui.QBrush()
                brush.setStyle(0)
                brush.setColor(3)
                item.setBrush(brush)
                item.setReferencePoint(4)
                item.attemptMove(QgsLayoutPoint(margin_left+offset_x,  margin_top+offset_y-1),True)
                item.setLocked(True)
                item.setZValue(40)

                composerView.addLayoutItem(item)



            #--------------------------------------------------------------------
            # Text oder Author oder Copyright
            #--------------------------------------------------------------------
            elif type == "text" or type == "author" or type == "copyright":
                if self.copyright == True:
                    textFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                    item = QgsLayoutItemLabel(composerView)
                    item.setBackgroundEnabled(True)
                    item.setFont(textFont)
                    item.setText(unicode(decoration.getText()))

                    if decoration.getWidth() > 0:
                        item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                    else:
                        item.adjustSizeToText()

                    item.setMargin(0)
                    brush = QtGui.QBrush()
                    brush.setStyle(0)
                    brush.setColor(3)
                    item.setBrush(brush)
                    item.setZValue(40)
                    item.attemptMove(QgsLayoutPoint(margin_left+offset_x,  margin_top+offset_y))
                    item.setLocked(True)

                    # Rotate the item. (does not work...)
                    if decoration.getRotation() != 0:
                        item.setRotation(decoration.getRotation())

                    if type == "copyright" and copyright == False:
                        continue
                    else:
                        composerView.addLayoutItem(item)


            #--------------------------------------------------------------------
            # Date
            #--------------------------------------------------------------------
            elif type == "date":
                dateFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                #item = QgsComposerLabel(composition)
                item = QgsLayoutItemLabel(composerView)
                item.setBackgroundEnabled(False)
                item.setFont(dateFont)
                d = time.localtime()
                item.setText(unicode(decoration.getText()) + "%d.%d.%d" % (d[2],  d[1],  d[0]))
                item.adjustSizeToText()
                item.setMargin(0)
                brush = QtGui.QBrush()
                brush.setStyle(0)
                brush.setColor(3)
                item.setBrush(brush)
                item.attemptMove(QgsLayoutPoint(margin_left+offset_x,  margin_top+offset_y))
                item.setLocked(True)
                item.setZValue(40)

                composerView.addLayoutItem(item)


            #--------------------------------------------------------------------
            # Crsdescription
            #--------------------------------------------------------------------
            elif type == "crsdescription":
                if self.crsdesc == True:
                    textFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())

                    item = QgsLayoutItemLabel(composerView)
                    item.setFont(textFont)
                    item.setBackgroundEnabled(False)

                    srsDescriptionText = self.iface.mapCanvas().mapSettings().destinationCrs().description()
                    itemText = unicode(decoration.getText()) + unicode(str(srsDescriptionText))
                    item.setText(itemText)

                    if decoration.getWidth() > 0:
                        item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                    else:
                        item.adjustSizeToText()

                    item.setMargin(0)
                    brush = QtGui.QBrush()
                    brush.setStyle(0)
                    brush.setColor(3)
                    item.setBrush(brush)
                    item.setLocked(True)
                    item.setZValue(40)
                    item.attemptMove(QgsLayoutPoint(margin_right+offset_x,  margin_bottom+offset_y))

                    composerView.addLayoutItem(item)


            #-----------------------------------------------


            #--------------------------------------------------------------------
            # Legend
            #--------------------------------------------------------------------
            elif type == "legend":
                if self.legend == True:
                    legendFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                    groupFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize()-1)
                    layerFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize()-2)
                    itemFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize()-2)
                    item = QgsLayoutItemLegend(composerView)
                    item.setBackgroundEnabled(True)
                    item.setTitle(decoration.getText())
                    item.adjustBoxSize()
                    item.setLocked(True)
                    item.attemptMove(QgsLayoutPoint(margin_left+offset_x, margin_top+offset_y))

                    try:
                        item.setStyleFont(0,groupFont)
                    except:
##                        print "EASYPRINT: old qgis version..."
                        QtWidgets.QMessageBox.information(None, 'Warning', "EASYPRINT: old qgis version...")

                    composerView.addLayoutItem(item)

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
                    mapHeight = float(paperheight)-margin_top-margin_bottom
                    composerMap = QgsLayoutItemMap(composerView)
                    composerMap.attemptSetSceneRect(QtCore.QRectF(margin_left+offset_x,  margin_top+offset_y, mapWidth,  mapHeight))
                else:
                    mapWidth = float(paperwidth) - (margin_right+margin_left)
                    mapHeight = float(paperheight) - margin_top-margin_bottom
                    composerMap = QgsLayoutItemMap(composerView)
                    composerMap.attemptSetSceneRect(QtCore.QRectF(margin_left+offset_x,  margin_top+offset_y, mapWidth,  mapHeight))


                # QMessageBox.about( None, "doVogisPrintCreateSimpleMap.py:416", "self.mapExtent == None:")
                # No mapExtent means we are in the standard easyprint mode.
                # This is a workaround for latlon stuff. Why is setNewScale not working?
                projectEPSG = self.canvas.mapSettings().destinationCrs().toProj4()
                if str.find(str(projectEPSG),  "+proj=longlat") >= 0:
                    composerMap.setScale(scale) # Does not center correctly?
                else:
                    rect = self.getMapExtentFromMapCanvas(mapWidth,  mapHeight,  scale)
                    composerMap.setExtent(rect)

                # Ausgabe herrichten

                pen = QtGui.QPen()
                pen.setWidthF(0.2)
                pen.setJoinStyle(0)
                composerMap.setPen(pen)
                composerMap.setLocked(False)
                composerMap.setFrameEnabled(True)
                composerMap.setZValue(1)
                # Grids and grid annotations
                if self.grid == True:
                    #QMessageBox.about(None, "grid", 'grid')
                    interval = self.getGridInterval(composerMap.scale())
                    composerMapGrid = composerMap.grid()
                    composerMapGrid.setEnabled(True)
                    composerMapGrid.setStyle(1)
                    composerMapGrid.setIntervalX(interval)
                    composerMapGrid.setIntervalY(interval)
                    composerMapGrid.setAnnotationEnabled(True)
                    gridFont = QtGui.QFont(decoration.getFontFamily(), 6)
                    gridFont.setItalic(True)
                    composerMapGrid.setAnnotationFont(gridFont)
                    composerMapGrid.setAnnotationPrecision(0)

                    composerMapGrid.setAnnotationPosition(0,0)
                    composerMapGrid.setAnnotationPosition(0,1)
                    composerMapGrid.setAnnotationPosition(0,2)
                    composerMapGrid.setAnnotationPosition(0,3)

                    composerMapGrid.setAnnotationFrameDistance(4)
                    composerMapGrid.setGridLineWidth(0.1)

                composerView.addLayoutItem(composerMap)



            #--------------------------------------------------------------------
            # Scaletext
            #--------------------------------------------------------------------
            elif type == "scaletext":
                textFont = QtGui.QFont(decoration.getFontFamily(), decoration.getFontSize())
                item = QgsLayoutItemLabel(composerView)
                item.setFont(textFont)
                item.setText(unicode(decoration.getText()))
                item.adjustSizeToText()
                item.setBackgroundEnabled(False)
                if decoration.getWidth() > 0:
                    item.setRect(0, 0, decoration.getWidth(),  decoration.getHeight())
                else:
                    item.adjustSizeToText()
                item.setMargin(0)
                brush = QtGui.QBrush()
                brush.setStyle(0)
                brush.setColor(3)
                item.setBrush(brush)
                item.setLocked(True)
                item.setZValue(40)
                item.attemptMove(QgsLayoutPoint(margin_right+offset_x,  margin_bottom+offset_y))

                composerView.addLayoutItem(item)

                composerScaleBar = QgsLayoutItemScaleBar(composerView)

                composerScaleBar.setLinkedMap(composerMap)

                scbFormat = QgsTextFormat()
                scbFormat.setFont(textFont)
                scbFormat.setSizeUnit(4)
                scbFormat.setSize(decoration.getFontSize())
                tbs = QgsTextBackgroundSettings()
                tbs.setEnabled(True)
                scbFormat.setBackground(tbs)

                composerScaleBar.setTextFormat(scbFormat)
                composerScaleBar.setStyle('Numeric')
                composerScaleBar.setLocked(True)
                composerScaleBar.setZValue(40)
                composerScaleBar.setBoxContentSpace(0.0) # heuristic -> sonst passts unter 2.0 nicht!
                composerScaleBar.update()


                width = item.boundingRect().width()
                height = item.boundingRect().height()

                composerScaleBar.attemptMove(QgsLayoutPoint(margin_right + offset_x + width, margin_bottom + offset_y))

                composerView.addLayoutItem(composerScaleBar)


    #******************************************************************************
    # getMapExtentFromFeatureExtent()
    #******************************************************************************
    def getMapExtentFromFeatureExtent(self, mapWidth, mapHeight, featExtent):
        featWidth = featExtent.width()
        featHeight = featExtent.height()

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
    def calcCuttingLines(self, composition, composerView=None):
        offset = 0.1
        lineLength = 10
        paperHeight = composition.pageSize().height()
        paperWidth = composition.pageSize().width()

        pen = QtGui.QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(0) # 0 ist gleich Qt.MiterJoin

        # top,left
        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(0,  0,  lineLength,  0))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)


        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(0,  0,  0,  lineLength))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)

        # top,right
        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(paperWidth-lineLength,  0,  lineLength,  0))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)

        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(paperWidth-offset,  0,  0,  lineLength))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)

        # bottom,right
        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(paperWidth-lineLength,  paperHeight-offset,  lineLength,  0))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)

        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(paperWidth-offset,  paperHeight-lineLength,  0,  lineLength))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)

        # bottom, left
        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(0,  paperHeight-offset,  lineLength,  0))
        item.setLocked(True)
        composerView.addLayoutItem(item)


        item = QgsLayoutItemShape(composerView)
        item.setShapeType(1)
        item.attemptSetSceneRect(QtCore.QRectF(0,  paperHeight-lineLength,  0,  lineLength))
        item.setPen(pen)
        item.setLocked(True)
        composerView.addLayoutItem(item)


    #******************************************************************************
    # foldingMarks()
    #******************************************************************************
    def foldingMarks(self, composition, composerView=None):
        markWidth = 210
        markHeight = 297
        lineLength = 4
        paperHeight = composition.pageSize().height()
        paperWidth = composition.pageSize().width()

        pen = QtGui.QPen()
        pen.setWidthF(0.05)
        pen.setJoinStyle(0) # 0 ist gleich Qt.MiterJoin

        if paperWidth / markWidth > 1:
            count = int(round(paperWidth/markWidth, 0))
            for i in range(1, count):
                item = QgsLayoutItemShape(composerView)
                item.setShapeType(1)
                item.attemptSetSceneRect(QtCore.QRectF(i * markWidth, 0,  0, lineLength))
                item.setPen(pen)
                item.setLocked(True)

                composerView.addLayoutItem(item)

                item = QgsLayoutItemShape(composerView)
                item.setShapeType(1)
                item.attemptSetSceneRect(QtCore.QRectF(i * markWidth,  paperHeight - lineLength,   0, lineLength))
                item.setPen(pen)
                item.setLocked(True)

                composerView.addLayoutItem(item)

        if paperHeight  / markHeight > 1:
            count = int(round(paperHeight/markHeight, 0))
            if count == 1:
                count = count + 1

            for i in range(1, count):
                item = QgsLayoutItemShape(composerView)
                item.setShapeType(1)
                item.attemptSetSceneRect(QtCore.QRectF(0, i * markHeight, lineLength, 0))
                item.setLocked(True)

                composerView.addLayoutItem(item)


                item = QgsLayoutItemShape(composerView)
                item.setShapeType(1)
                item.attemptSetSceneRect(QtCore.QRectF(paperWidth-lineLength, i * markHeight, lineLength, 0))
                item.setPen(pen)
                item.setLocked(True)

                composerView.addLayoutItem(item)
