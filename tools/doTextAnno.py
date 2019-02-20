# -*- coding: utf-8 -*-
#!/usr/bin/python


from qgis.PyQt import QtGui, QtCore, QtSql

from qgis.core import *
from qgis.gui import *
from gui_geonam import *
#from globale_variablen import *     #Die Adresse der Listen importieren: Modulübergreifende globale Variablen sind so möglich


from ProjektImport import *
import sys
import string

class draw_text_class():
    def __init__(self,mc,text_u,props,punkti,offset):


        #wieder nur lokale Variable....
        self.mc=mc
        self.text=text_u
        self.props=props
        self.punkti=punkti
        self.offset=offset
        self.gen_var = None

         # Annotation Manager! Um die Annotations
        # mit dem Annotation Tool dann auch löschen zu können!!!
        self.am = QgsProject.instance().annotationManager()

    def gen(self):

        # Tip: Style Exportieren, im XML stehen dann die Properties, dort einfach rausnehmen
        #damit man weiß was es für Properties gibt!!
        #diese props gelten für das Kreuzchen das auf die Adresskoordinate gesetzt wird
        props = { 'color' : '255,0,0', 'color_border' : '255,0,0' , 'name' : 'cross', 'size' : '4' }

        # Ein textgrafikobjekt für die Textdarstellung erzeugen
        text = QtGui.QTextDocument()

        # Das Fontobjekt fürs Textobjekt
        font = QtGui.QFont()
        font.setPointSize(12)
        text.setDefaultFont(font)
        text.setHtml("<font color = \"#FF0000\">" + self.text + "</font>")

        # Benötigte Framgröße
        frame_groesse = text.size()

        # DAS objekt um Kreuzchen und Text zu zeichnen
        textAnno = QgsTextAnnotation(self.mc)
        textAnno.setFrameSize(frame_groesse)   # ohne Framgröße keine Darstellung im Drucklayout
        textAnno.setMapPosition(self.punkti)
        textAnno.setFrameOffsetFromReferencePoint(self.offset)

        # Hintergrund und Rahmen sollen weiss sein
        fs = textAnno.fillSymbol()
        sl = fs.symbolLayer(0)
        sl.setFillColor(QtGui.QColor(255,255,255))
        sl.setStrokeColor(QtGui.QColor(255,255,255))
        fs.setOpacity(0.8)


        textAnno.setDocument(text)  #Text zuweisen

        # textAnno.setMarkerSymbol geht nicht!!
        # deshalb so: wir wollen nicht den Standardknödel
        # sondern ein rotes Kreuzchen
        s = textAnno.markerSymbol() #1. das eingestellte Marker Symbol holen
        # Die neuen Properties...
        slr = QgsSymbolLayerRegistry()
        slm = slr.symbolLayerMetadata("SimpleMarker").createSymbolLayer(props)   #in der Schleife sonst Probleme im Qgis
        s.changeSymbolLayer(0,slm)   #2. das neue Symbol zuweisen

        # Und unbedingt auch zum Annotation Manager,
        # sonst können sie mit dem Annotation Tool nicht gelöscht werden!!
        self.am.addAnnotation(textAnno)

        # Den Text dem Map Canvas hinzufügen nicht vergessen!
        return QgsMapCanvasAnnotationItem(textAnno,self.mc)

