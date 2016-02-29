# -*- coding: utf-8 -*-
from PyQt4 import QtGui,QtCore,QtSql
from qgis.core import *

from Ui_gui_VogisPrint import Ui_VogisPrint
from Ui_gui_VogisPrint_Serien_Grid import Ui_VogisPrintSerieGrid

import os, sys, time, math, locale
import logging

from VogisPrint_Utils import *
## Import some other classes.
from VogisPrint_layout import Layout
#import VogisPrint_resources





class VogisPrintDialog(QtGui.QDialog, Ui_VogisPrint,  Ui_VogisPrintSerieGrid):

    #-----------------------------------------------------------------
    # Constructor
    #-----------------------------------------------------------------
    def __init__(self, iface, parent,pfad = None,stand_dkm = None):

        QDialog.__init__(self, parent)
        Ui_VogisPrint.__init__(self, parent)

        # Save reference to the QGIS interface.
        self.iface = iface
        self.canvas = iface.mapCanvas()

        self.scale = "none"

        self.stand_dkm = unicode(stand_dkm)
        #QMessageBox.about(None, "VogisPrintDialog:54", "stand_dkm = "  + stand_dkm)

        #--------------------------------------------------------
        # Initialize the translation environment.
        # War ursprünglich in EasyPrint __init__()
        #--------------------------------------------------------
        # Eigene Pfade
##        userPluginPath = QFileInfo(QgsApplication.qgisUserDbFilePath()).path()+"/python/plugins/VogisMenu/standardlayout"
##        systemPluginPath = QgsApplication.prefixPath()+"/python/plugins/VogisMenu/standardlayout"
##
##
##
        locale = QSettings().value("locale/userLocale")
        myLocale = locale[0:2]
##
##
##        # Pfad fuer QM-Files setzen
##        if QFileInfo(userPluginPath).exists():
##          pluginPath = userPluginPath+"/i18n/standardlayout_"+myLocale+".qm"
##          # Debug
##          #QMessageBox.about(None, "VogisPrintDialog:54", "pluginPath = "  + pluginPath)
##        elif QFileInfo(systemPluginPath).exists():
##          pluginPath = systemPluginPath+"/i18n/standardlayout_"+myLocale+".qm"


        pluginPath = os.path.dirname(__file__) +"/i18n/standardlayout_"+myLocale+".qm"



        # Ueberstzung laden
        self.localePath = pluginPath
        if QFileInfo(self.localePath).exists():
          self.translator = QTranslator()
          self.translator.load(self.localePath)

          # QT-Uebersetzer aktivieren.
          if qVersion() > '4.3.3':
            QCoreApplication.installTranslator(self.translator)


        self.tabIndex = 0


        #---------------------------------------------------------------------------------
        # GUI aktivieren
        #---------------------------------------------------------------------------------
        self.setupUi(self)


        # Simplemap-Button mit accept-Funktion verknüpfen
        self.connect(self.pushButton_3, SIGNAL("accepted()"), self.accept)
        self.settings = QSettings("CatAIS","doVogisPrint")
        #self.connect(self.printScale.lineEdit(), SIGNAL("editingFinished()"),  self.Check_Scale)


        #.......................................................................
        # Sub-Window Seriendruck mit Raster konfigurieren
        #.......................................................................
        self.serie_grid = VogisPrintSerieGrid(self.iface.mainWindow(),self.iface)
        QtCore.QObject.connect(self.serie_grid.btnMbGrid, QtCore.SIGNAL(("pressed()")), self.serie_grid_grid_created)
        QtCore.QObject.connect(self.serie_grid.buttonClose, QtCore.SIGNAL(("clicked()")), self.closeEvent)



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
#  alt   self.grid.setChecked( bool(self.settings.value("gui/grids")) )

        if self.settings.value("gui/legendsave") == "True":
            self.legend.setChecked( True )
        else:
            self.legend.setChecked( False )
#  alt   self.legend.setChecked( bool(self.settings.value("gui/legend")) )

        if self.settings.value("gui/cuttinglinessave") == "True":
            self.cuttinglines.setChecked( True )
        else:
            self.cuttinglines.setChecked( False )
#  alt   self.legend.setChecked( bool(self.settings.value("gui/cuttinglines")) )

        if self.settings.value("gui/foldingmarkssave") == "True":
            self.foldingmarks.setChecked( True )
        else:
            self.foldingmarks.setChecked( False )
# alt    self.foldingmarks.setChecked( bool(self.settings.value("gui/foldingmarks")) )

        if self.settings.value("gui/crsdescsave") == "True":
            self.crsdesc.setChecked( True )
        else:
            self.crsdesc.setChecked( False )
# alt    self.crsdesc.setChecked( bool(self.settings.value("gui/crsdescription")) )

        #       Copyright-Verweis ist nicht mehr waehlbar
#        self.copyright.setChecked( self.settings.value("gui/copyright", False).toBool() )




    #--------------------------------------------------------------
    #--------------------------------------------------------------
    # Button "Seriendruck nach Raster" betaetigt
    #--------------------------------------------------------------
    #--------------------------------------------------------------
    @pyqtSignature("on_pushButton_2_pressed()")
    def on_pushButton_2_pressed(self):

        # Aktuell eingestellten Massstab aus dem Hauptfenster übernehmen
        self.serie_grid.mprintScale.setItemText(0,self.printScale.currentText())

        test = self.serie_grid.mbgridtype.findText("--------------------")
        if test == -1:
            self.serie_grid.mbgridtype.insertItem( 0,  QCoreApplication.translate("VogisPrintDialog", "Regular grid" ),   1  )
            self.serie_grid.mbgridtype.insertItem( 1,  QCoreApplication.translate("VogisPrintDialog", "Regular grid (w/o empty grids)" ),   2  )
            self.serie_grid.mbgridtype.insertItem( 0,  "--------------------", -1 )

        self.serie_grid.mbgridtype.setCurrentIndex(0)

        self.serie_grid.label.setText('Ausgabemaßstab für'.decode('utf8') + ' ' + self.printFormat.currentText() + ':')
        self.serie_grid.exec_()
        self.tabIndex = 1

    # Handling für das Erzeugen des Rasters
    def serie_grid_grid_created(self):


        if self.serie_grid.mbmaplayer.currentText() == "":
            #FIXME Translation
            text = QCoreApplication.translate("warning-no-ref-layer", "No reference map layer selected.")
            QMessageBox.warning( None, "", text)
            return



        self.scale = self.serie_grid.mprintScale.currentText().replace('.','')
        #self.scale = self.printScale.currentText()
        self.scale = self.Check_Scale(self.scale)
        if self.scale < 1.0:
            return


        # Hier wird der Raster erzeugt
        if self.serie_grid.mbgridtype.currentIndex() <> 0:
            from doVogisPrintCreateMapBookGrid import CreateMapBookGrid
            d = CreateMapBookGrid(self.iface, self.serie_grid.mbgridtype.itemData(self.serie_grid.mbgridtype.currentIndex()), self.scale, self.printFormat.currentText(), int(self.layout.currentIndex()), self.serie_grid.mbmaplayer.currentText(),self.stand_dkm)

            d.run()
            self.serie_grid.memoryName = d.memoryName

        else:
            text = QCoreApplication.translate("warning-no-raster-type", "No raster type selected.")
            QMessageBox.warning( None, "", text)
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

#  alt   self.settings.setValue( "gui/legend", ( str(self.legend.isChecked()) ) )
#  alt   self.settings.setValue( "gui/cuttinglines", ( str(self.cuttinglines.isChecked()) ) )
#  alt   self.settings.setValue( "gui/foldingmarks", ( str(self.foldingmarks.isChecked()) ) )
#  alt   self.settings.setValue( "gui/crsdescription", ( str(self.crsdesc.isChecked()) ) )



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



#        tttt = self.settings.value("gui/andy")
#        
#        #QMessageBox.about(None, "VogisPrint:247", "self.settings.value in accept() = "  + tttt)




        # Massstab prüfen
        self.scale = self.printScale.currentText().replace('.','')

        self.scale = self.Check_Scale(self.scale)
        if self.scale < 1.0:
            return
        from doVogisPrintCreateSimpleMap import CreateSimpleMap
        copyright = True
        #QMessageBox.about(None, "VogisPrintDialog:388", "stand_dkm = "  + self.stand_dkm)
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

        #preffilename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/VogisMenu/standardlayout/preferences/preferences.xml"))
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
                            print "float error: reading scales"
                    sube = sube.nextSibling()
                n = n.nextSibling()

        except IOError:
            print "error opening preferences.xml"

        return prefs


    #-----------------------------------------------------------------
    # layouts
    #-----------------------------------------------------------------
    def layouts(self):
        layouts = []

        #layoutsfilename = QDir.convertSeparators(QDir.cleanPath(QgsApplication.qgisSettingsDirPath() + "/python/plugins/VogisMenu/standardlayout/layouts/layouts.xml"))
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
                        print "layoutnode.nodeName() = %s" %(layoutnode.nodeName())
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
                            print margins
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
            print "error opening preferences.xml"

        #print "Ende layouts()."

        return layouts



    #-----------------------------------------------------------------
    # Check_Scale()
    #-----------------------------------------------------------------
    def Check_Scale(self, scale):
        #QMessageBox.about(None, "doVogisPrint:658", "scale = %s"  %(scale))

        message = "<FONT COLOR='#000000' SIZE=4>Masstab <FONT COLOR='#000080' SIZE=4>%s<FONT COLOR='#000000' SIZE=4> ungültig!<br>Masstab bitte in der Form 1:10.000 oder 1:10000 oder 10000 eingeben.".decode('utf8') %(scale)
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

    def closeEvent(self,event = None):
        self.serie_grid.close()
    #-----------------------------------------------------------------
    # insertTooltips
    #-----------------------------------------------------------------
    def insertTooltips(self):
        # Tooltips einfuegen

        #---------------------------------------------------------------------
        # Tooltips fuer das Haupt-Fenster
        #---------------------------------------------------------------------
        text = QCoreApplication.translate("tt-Output-Print-Scale", "Print-scale used to render the plots" )
        self.label.setToolTip(text)
        self.printScale.setToolTip(text)

        text = QCoreApplication.translate("tt-mapbook-simple-button", "Creates a single plot." )
        self.pushButton_3.setToolTip(text)

        text = QCoreApplication.translate("tt-mapbook-grid-button", "Creates a user defined grid." )
        self.pushButton_2.setToolTip(text)

        text = QCoreApplication.translate("tt-papersize", "Selection of plot-papersize (e.g. A4)." )
        self.label_2.setToolTip(text)
        self.printFormat.setToolTip(text)

        text = QCoreApplication.translate("tt-layout", "Selection of plot-layout (e.g. portrait)." )
        self.label_5.setToolTip(text)
        self.layout.setToolTip(text)

        text = QCoreApplication.translate("tt-title", "Title of the plot." )
        self.label_3.setToolTip(text)
        self.title.setToolTip(text)

        text = QCoreApplication.translate("tt-subtitle", "Subtitle of the plot." )
        self.label_4.setToolTip(text)
        self.subtitle.setToolTip(text)

        text = QCoreApplication.translate("tt-person", "Author." )
        self.label_6.setToolTip(text)
        self.person.setToolTip(text)

        text = QCoreApplication.translate("tt-cuttinglines", "Prints cuttinglines." )
        self.label_40.setToolTip(text)
        self.cuttinglines.setToolTip(text)

        text = QCoreApplication.translate("tt-foldingmarks", "Prints foldingmarks." )
        self.label_43.setToolTip(text)
        self.foldingmarks.setToolTip(text)

        text = QCoreApplication.translate("tt-crsdesc", "Prints the crs used for this plot." )
        self.label_42.setToolTip(text)
        self.crsdesc.setToolTip(text)

        text = QCoreApplication.translate("tt-legend", "Prints a legend." )
        self.label_39.setToolTip(text)
        self.legend.setToolTip(text)



class VogisPrintSerieGrid(QtGui.QDialog,Ui_VogisPrintSerieGrid):

    def __init__(self,parent,iface): #,iface,pfad = None):
        QtGui.QDialog.__init__(self,parent) #den parent brauchts für einen modalen dialog!!
        Ui_VogisPrintSerieGrid.__init__(self)

        self.setupUi(self)

    def VogisPrintSerieGrid_schliessen(self):
        self.close()
