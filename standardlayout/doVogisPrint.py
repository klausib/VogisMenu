# -*- coding: utf-8 -*-
from qgis.PyQt import QtGui,QtCore,QtSql
from qgis.core import *

from Ui_gui_VogisPrint import Ui_VogisPrint
from Ui_gui_VogisPrint_Serien_Grid import Ui_VogisPrintSerieGrid

import os, sys, time, math, locale
import logging

from VogisPrint_Utils import *
## Import some other classes.
from VogisPrint_layout import Layout
#import VogisPrint_resources





class VogisPrintDialog(QtWidgets.QDialog, Ui_VogisPrint,  Ui_VogisPrintSerieGrid):

    #-----------------------------------------------------------------
    # Constructor
    #-----------------------------------------------------------------
    def __init__(self, iface, parent,pfad = None,stand_dkm = None):

        QtWidgets.QDialog.__init__(self,parent)
        Ui_VogisPrint.__init__(self)

        # Save reference to the QGIS interface.
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.scale = "none"

        self.stand_dkm = unicode(stand_dkm)

        locale = QtCore.QSettings().value("locale/userLocale")
        myLocale = locale[0:2]

        pluginPath = os.path.dirname(__file__) +"/i18n/standardlayout_"+myLocale+".qm"



        # Uebersetzung laden
        self.localePath = pluginPath
        if QtCore.QFileInfo(self.localePath).exists():
          self.translator = QtCore.QTranslator()
          self.translator.load(self.localePath)

        QtWidgets.QApplication.installTranslator(self.translator)


        self.tabIndex = 0


        #---------------------------------------------------------------------------------
        # GUI aktivieren
        #---------------------------------------------------------------------------------
        self.setupUi(self)


        # Simplemap-Button mit accept-Funktion verknüpfen
        self.pushButton_2.clicked.connect(self.on_pushButton_2_click)
        self.settings = QtCore.QSettings("CatAIS","doVogisPrint")


        #.......................................................................
        # Sub-Window Seriendruck mit Raster konfigurieren
        #.......................................................................
        self.serie_grid = VogisPrintSerieGrid(self.iface.mainWindow(),self.iface)
        self.serie_grid.btnMbGrid.clicked.connect(self.serie_grid_grid_created)
##        self.serie_grid.buttonClose.clicked.connect(self.closeEvent)



        #.................................
        # Tooltips einfuegen
        #.................................
        self.insertTooltips()


        self.scales = []
        self.paperformats = []
        self.departments = []
        layouts = self.layouts()


        # Akutellen Massstab für Massstab-Drop-Down merken
        scales = self.preferences("scale",  False)
        scales.insert(0, str(int(self.canvas.scale())))
        # FIXME Evtl. brauch ich das noch.
        self.default_scale = float(self.canvas.scale())

        # Fill the combobox with available scales.
        for scale in scales:
            self.printScale.addItem("1 : " + scale)
            self.serie_grid.mprintScale.addItem("1 : " + scale)


        paperformats = self.preferences("format",  True)

        # Layernamen holen
        self.maplayers = getLayerNames("all")
        self.vectorlayers = getLayerNames([0, 1, 2])
        #self.serie_grid.mbmaplayer.addItems(sorted(self.vectorlayers))
        self.serie_grid.mbmaplayer.addItems(sorted(self.maplayers))




        # Fill the combobox with available paperformats.
        self.printFormat.addItems(paperformats)

        # Fill the combobox with available layouts.
        for l in layouts:
            self.layout.addItem(l.getID())

        departments = self.preferences("department",  True)

        # Fill the combobox with available departments.
        self.department.addItems(departments)



        #---------------------------------------------------------------------------
        # Letzten GUI-Zustand wiederherstellen
        #---------------------------------------------------------------------------
        self.person.setText( unicode(self.settings.value("gui/person")) )

        # Handling fuer die erste Verwendung
        try:
            dummy = int(self.settings.value("gui/department"))
        except:
            dummy = 0
        self.department.setCurrentIndex( dummy )


        if self.settings.value("gui/gridsave") == "True":
            #QMessageBox.about(None, "VogisPrint:155     ", "TRUE self.settings.value gui/grids = "  + self.settings.value("gui/gridsave"))
            self.grid.setChecked( True )
        else:
            #QMessageBox.about(None, "VogisPrint:155     ", "FALSE self.settings.value gui/grids = "  + self.settings.value("gui/gridsave"))
            self.grid.setChecked( False )

        if self.settings.value("gui/legendsave") == "True":
            self.legend.setChecked( True )
        else:
            self.legend.setChecked( False )

        if self.settings.value("gui/cuttinglinessave") == "True":
            self.cuttinglines.setChecked( True )
        else:
            self.cuttinglines.setChecked( False )

        if self.settings.value("gui/foldingmarkssave") == "True":
            self.foldingmarks.setChecked( True )
        else:
            self.foldingmarks.setChecked( False )

        if self.settings.value("gui/crsdescsave") == "True":
            self.crsdesc.setChecked( True )
        else:
            self.crsdesc.setChecked( False )




    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # Button "Seriendruck nach Raster" betaetigt
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    def on_pushButton_2_click(self):
        #QtWidgets.QMessageBox.warning( None, "", "Begin")
        # Aktuell eingestellten Massstab aus dem Hauptfenster übernehmen
        self.serie_grid.mprintScale.setItemText(0,self.printScale.currentText())

        test = self.serie_grid.mbgridtype.findText("--------------------")
        if test == -1:
            self.serie_grid.mbgridtype.insertItem( 0,  QtWidgets.QApplication.translate("VogisPrintDialog", "Regular grid" ),   1  )
            self.serie_grid.mbgridtype.insertItem( 1,  QtWidgets.QApplication.translate("VogisPrintDialog", "Regular grid (w/o empty grids)" ),   2  )
            self.serie_grid.mbgridtype.insertItem( 0,  "--------------------", -1 )

        self.serie_grid.mbgridtype.setCurrentIndex(0)

        self.serie_grid.label.setText('Ausgabemaßstab für' + ' ' + self.printFormat.currentText() + ':')
        self.tabIndex = 1
        self.serie_grid.exec_()
    # Handling für das Erzeugen des Rasters
    def serie_grid_grid_created(self):


        if self.serie_grid.mbmaplayer.currentText() == "":
            #FIXME Translation
            text = QtWidgets.QApplication.translate("warning-no-ref-layer", "No reference map layer selected.")
            QtWidgets.QMessageBox.warning( None, "", text)
            return



        self.scale = self.serie_grid.mprintScale.currentText().replace('.','')
        self.scale = self.Check_Scale(self.scale)
        if self.scale < 1.0:
            return


        # Hier wird der Raster erzeugt
        if self.serie_grid.mbgridtype.currentIndex() != 0:
            from doVogisPrintCreateMapBookGrid import CreateMapBookGrid
            d = CreateMapBookGrid(self.iface, self.serie_grid.mbgridtype.itemData(self.serie_grid.mbgridtype.currentIndex()), self.scale, self.printFormat.currentText(), int(self.layout.currentIndex()), self.serie_grid.mbmaplayer.currentText(),self.stand_dkm)

            d.run()
            self.serie_grid.memoryName = d.memoryName

        else:
            text = QtWidgets.QApplication.translate("warning-no-raster-type", "No raster type selected.")
            QtWidgets.QMessageBox.warning( None, "", text)
            return



    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    # accept
    #
    # Das ist die Methode die aufgefufen wird wenn man den <Enter>-Button drueckt
    #
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    #--------------------------------------------------------------------------------
    def accept(self):           # easyprintgui.py:148:

        self.settings.setValue( "gui/person", ( self.person.text() ) )

        self.settings.setValue( "gui/department", ( str(self.department.currentIndex()) ) )

        if self.legend.isChecked() == True:
            self.settings.setValue( "gui/legendsave", ( "True" ) )
        else:
            self.settings.setValue( "gui/legendsave", ( "False" ) )

        if self.grid.isChecked() == True:
            self.settings.setValue( "gui/gridsave", ( "True" ) )
        else:
            self.settings.setValue( "gui/gridsave", ( "False" ) )

        if self.cuttinglines.isChecked() == True:
            self.settings.setValue( "gui/cuttinglinessave", ( "True" ) )
        else:
            self.settings.setValue( "gui/cuttinglinessave", ( "False" ) )

        if self.foldingmarks.isChecked() == True:
            self.settings.setValue( "gui/foldingmarkssave", ( "True" ) )
        else:
            self.settings.setValue( "gui/foldingmarkssave", ( "False" ) )

        if self.crsdesc.isChecked() == True:
            self.settings.setValue( "gui/crsdescsave", ( "True" ) )
        else:
            self.settings.setValue( "gui/crsdescsave", ( "False" ) )

        # Massstab prüfen
        self.scale = self.printScale.currentText().replace('.','')

        self.scale = self.Check_Scale(self.scale)
        if self.scale < 1.0:
            return
        from doVogisPrintCreateSimpleMap import CreateSimpleMap
        copyright = True
        #QtWidgets.QMessageBox.about(None, "VogisPrintDialog:388", "stand_dkm = "  + self.stand_dkm)
        d = CreateSimpleMap(self.iface,  self.scale ,    self.printFormat.currentText(),  int(self.layout.currentIndex()), self.title.text(), self.subtitle.text(), self.person.text(), self.department.currentText(), self.crsdesc.isChecked(), self.grid.isChecked(), self.legend.isChecked(), copyright,  self.cuttinglines.isChecked(), self.foldingmarks.isChecked(), self.stand_dkm )
        d.run()


    #----------------------------------------------------------------------------------------
    # MapLayerChanged (wenn man einen anderen maplayer in der Drop-Down anwaehlt)
    #----------------------------------------------------------------------------------------
    def MapLayerChanged(self):



        self.vlayer = getVectorLayerByName(self.serie_feature.mbfmaplayer.currentText())
        #FIXME muesst hier nicht eine Fehlerhandling her ??
        if self.vlayer == None:
            return

        # Layertyp ermitteln
        if self.vlayer.geometryType() ==   QGis.Line:
            self.serie_feature.mbuseextent.setEnabled(False)
        elif self.vlayer.geometryType() == QGis.Point:
            self.serie_feature.mbuseextent.setEnabled(False)
        elif self.vlayer.geometryType() == QGis.Polygon:
            self.serie_feature.mbuseextent.setEnabled(True)

        numberList = []
        self.stringList = []

        provider = self.vlayer.dataProvider()
        fields = provider.fields()

        for i in fields:
            fieldType = i.type()
            if fieldType == 6 or fieldType == 2:
                numberList.append(i.name())
            elif fieldType == 10:
                self.stringList.append(i.name())

        self.serie_feature.mbffileattribute.clear()
        self.serie_feature.mbffileattribute.addItems(sorted(self.stringList))
        self.serie_feature.mbffileattribute.insertItem( 0,  "--------------------" )
        self.serie_feature.mbffileattribute.setCurrentIndex(0)

        self.serie_feature.mbftitle.clear()
        self.serie_feature.mbftitle.addItems(sorted(self.stringList))
        self.serie_feature.mbftitle.insertItem( 0,  "--------------------" )
        self.serie_feature.mbftitle.setCurrentIndex(0)

        self.serie_feature.mbfsubtitle.clear()
        self.serie_feature.mbfsubtitle.addItems(sorted(self.stringList))
        self.serie_feature.mbfsubtitle.insertItem( 0,  "--------------------" )
        self.serie_feature.mbfsubtitle.setCurrentIndex(0)

        self.serie_feature.mbfscale.clear()
        self.serie_feature.mbfscale.addItems(sorted(numberList))
        self.serie_feature.mbfscale.insertItem( 0,  "--------------------" )
        self.serie_feature.mbfscale.setCurrentIndex(0)

        self.serie_feature.mbfrotation.clear()
        self.serie_feature.mbfrotation.addItems(sorted(numberList))
        self.serie_feature.mbfrotation.insertItem( 0,  "--------------------" )
        self.serie_feature.mbfrotation.setCurrentIndex(0)




    #-----------------------------------------------------------------
    # preferences
    #-----------------------------------------------------------------
    def preferences(self,  pref,  text):
        prefs = []

        preffilename = os.path.dirname(__file__) + "/preferences/preferences.xml"
        os.path.dirname(__file__)
        try:
            preffile = open(preffilename,"r")
            prefxml = preffile.read()

            doc = QtXml.QDomDocument()
            doc.setContent(prefxml,  True)

            root = doc.documentElement()
            if root.tagName() != "preferences":
                return

            n = root.firstChild()
            while not n.isNull():
                e = n.toElement()
                sube = e.firstChild()
                while not sube.isNull():
                    if sube.toElement().tagName() == pref:
                        try:
                            if not text:
                                float(sube.toElement().text())
                            prefs.append(unicode(sube.toElement().text()))
                        except ValueError:
                            pass
                            #print ("float error: reading scales")
                    sube = sube.nextSibling()
                n = n.nextSibling()

        except IOError:
            pass
            #print ("error opening preferences.xml")

        return prefs


    #-----------------------------------------------------------------
    # layouts
    #-----------------------------------------------------------------
    def layouts(self):
        layouts = []

        layoutsfilename = os.path.dirname(__file__) + "/layouts/layouts.xml"
        try:
            layoutsfile = open(layoutsfilename,"r")
            layoutsxml = layoutsfile.read()

            doc = QtXml.QDomDocument()
            doc.setContent(layoutsxml,  True)

            root = doc.documentElement()
            if root.tagName() != "layouts":
                return

            node = root.firstChild()
            while not node.isNull():
                #print "node.nodeName() = %s" %(node.nodeName())
                if node.toElement() and node.nodeName() == "layout":
                    margins = []
                    id = node.toElement().attribute("id","")
                    layout = Layout(id)
                    ori = node.toElement().attribute("orientation",  "")
                    layout.setOrientation(ori)

                    ## Read a single layout.
                    layoutnode = node.toElement().firstChild()
                    while not layoutnode.isNull():
                        #print ("layoutnode.nodeName() = "+  layoutnode.nodeName())
                        if layoutnode.toElement() and layoutnode.nodeName() == "margins":
                            ## Read margins.
                            marginnode = layoutnode.toElement().firstChild()
                            while not marginnode.isNull():
                                try:
                                    margins.append( float(marginnode.toElement().text()) )
                                    #print "marginnode.toElement().text() = %s" %(marginnode.toElement().text())
                                except ValueError:
                                    margins.append( float(0.0) )
                                marginnode = marginnode.nextSibling()
                            #print (str(margins))
                            layout.setMargins(margins)

                        elif layoutnode.toElement() and layoutnode.nodeName() == "decorations":
                            ## Read decorations.
                            deconode = layoutnode.toElement().firstChild()
                            while not deconode.isNull():
                                type = deconode.toElement().attribute("type","")
                                decoration = Decoration(type)

                                affinity = deconode.toElement().attribute("affinity",  "")
                                offset_x = deconode.toElement().attribute("offset_x","")
                                offset_y = deconode.toElement().attribute("offset_y","")
                                height = deconode.toElement().attribute("height", "")
                                width = deconode.toElement().attribute("width",  "")
                                fontsize = deconode.toElement().attribute("font-size",  "")
                                fontfamily = deconode.toElement().attribute("font-family",  "")
                                rotation = deconode.toElement().attribute("rotation",  "")

                                if str.find(str(affinity),  ",") >= 0:
                                    affx = str(str.split(str(affinity),",")[1]).strip()
                                    affy = str(str.split(str(affinity),",")[0]).strip()

                                    if affx == "left" or affx == "right":
                                        decoration.setAffinityX(affx)

                                    if affy == "top" or affy == "bottom":
                                        decoration.setAffinityY(affy)

                                if fontfamily != None:
                                    decoration.setFontFamily(fontfamily)

                                try:
                                    decoration.setOffsetX(float(offset_x))
                                except ValueError:
                                    pass
                                    #print "float offset_x error"

                                try:
                                    decoration.setOffsetY(float(offset_y))
                                except ValueError:
                                    pass
                                    #print "float offset_y error"

                                try:
                                    decoration.setHeight(float(height))
                                except ValueError:
                                    decoration.setHeight(float(0.0))
                                    #print "float height error or not found."

                                try:
                                    decoration.setWidth(float(width))
                                except ValueError:
                                    decoration.setWidth(float(0.0))
                                    #print "float width error or not found."

                                try:
                                    decoration.setFontSize(float(fontsize))
                                except ValueError:
                                    pass
                                    #print "float fontsize error or not found."

                                try:
                                    decoration.setRotation(float(rotation))
                                except ValueError:
                                    pass
                                    #print "float rotation error or not found."

                                if type == "text" or type == "date" or type == "scaletext" or type == "legend" or type == "person" or type == "department":
                                    text = deconode.toElement().text()
                                    decoration.setText(text)

                                if type == "copyright":
                                    text = deconode.toElement().text()
                                    text = text + self.stand_dkm
                                    decoration.setText(text)

                                if type == "picture" or type == "northarrow":
                                    pic = deconode.toElement().text()
                                    decoration.setPicture(pic)

                                layout.addDecoration(decoration)

                                deconode = deconode.nextSibling()

                        layoutnode = layoutnode.nextSibling()


                #print "doVogisPrint.py: 619"
                layout.getMargins()
                layouts.append(layout)

                node = node.nextSibling()

        except IOError:
            pass
            #print ("error opening preferences.xml")

        #print "Ende layouts()."

        return layouts



    #-----------------------------------------------------------------
    # Check_Scale()
    #-----------------------------------------------------------------
    def Check_Scale(self, scale):
        #QMessageBox.about(None, "doVogisPrint:658", "scale = %s"  %(scale))

        message = "<FONT COLOR='#000000' SIZE=4>Masstab <FONT COLOR='#000080' SIZE=4>%s<FONT COLOR='#000000' SIZE=4> ungültig!<br>Masstab bitte in der Form 1:10.000 oder 1:10000 oder 10000 eingeben." %(scale)
        message = message


        try:
            dummy1 = float(scale)
        except :
            #QMessageBox.about(None, "doVogisPrint:664", "Kein Float")
            scale.replace(".","")
            try:
                dummy1, dummy2 = scale.split(":",1)
            except:
                a = 1
                QMessageBox.warning(  None, "doVogisPrint:676", message)
                return -1
            dummy1 = str(dummy1)
            dummy1 = dummy1.rstrip()
            dummy1 = dummy1.lstrip()
            if dummy1 == "1":
                dummy2 = str(dummy2)
                dummy2 = dummy2.rstrip()
                dummy2 = dummy2.lstrip()
                try:
                    dummy1 = float(dummy2)
                except:
                    a = 1
                    QMessageBox.warning(  None, "doVogisPrint:689", message)
                    return -1
            else:
                a = 1
                QMessageBox.warning(  None, "doVogisPrint:693", message)
                return -1


        #QMessageBox.about(None, "doVogisPrint:694", "Start def __init__(..) printScale = %s  Scheint in Ordnung zu sein."  %(scale))
        return dummy1


    #-----------------------------------------------------------------
    # insertTooltips
    #-----------------------------------------------------------------
    def insertTooltips(self):
        # Tooltips einfuegen

        #---------------------------------------------------------------------
        # Tooltips fuer das Haupt-Fenster
        #---------------------------------------------------------------------
        text = QtWidgets.QApplication.translate("tt-Output-Print-Scale", "Print-scale used to render the plots" )
        self.label.setToolTip(text)
        self.printScale.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-mapbook-simple-button", "Creates a single plot." )
        self.pushButton_3.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-mapbook-grid-button", "Creates a user defined grid." )
        self.pushButton_2.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-papersize", "Selection of plot-papersize (e.g. A4)." )
        self.label_2.setToolTip(text)
        self.printFormat.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-layout", "Selection of plot-layout (e.g. portrait)." )
        self.label_5.setToolTip(text)
        self.layout.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-title", "Title of the plot." )
        self.label_3.setToolTip(text)
        self.title.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-subtitle", "Subtitle of the plot." )
        self.label_4.setToolTip(text)
        self.subtitle.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-person", "Author." )
        self.label_6.setToolTip(text)
        self.person.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-cuttinglines", "Prints cuttinglines." )
        self.label_40.setToolTip(text)
        self.cuttinglines.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-foldingmarks", "Prints foldingmarks." )
        self.label_43.setToolTip(text)
        self.foldingmarks.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-crsdesc", "Prints the crs used for this plot." )
        self.label_42.setToolTip(text)
        self.crsdesc.setToolTip(text)

        text = QtWidgets.QApplication.translate("tt-legend", "Prints a legend." )
        self.label_39.setToolTip(text)
        self.legend.setToolTip(text)



class VogisPrintSerieGrid(QtWidgets.QDialog,Ui_VogisPrintSerieGrid):

    def __init__(self,parent,iface): #,iface,pfad = None):
        QtWidgets.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_VogisPrintSerieGrid.__init__(self)

        self.setupUi(self)

    def VogisPrintSerieGrid_schliessen(self):
        self.close()
