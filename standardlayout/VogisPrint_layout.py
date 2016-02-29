# -*- coding: latin1 -*-
import VogisPrint_decoration

class Layout():
    def __init__(self,  id):
        self.id = id
        self.orientation = "portrait"
        self.margins = [0,  0,  0,  0,  0]
        self.decorations = []

    def setOrientation(self,  ori):
        self.orientation = ori

    def setMargins(self, m):
        self.margins = m

    def addDecoration(self,  d):
        self.decorations.append(d)

    def getID(self):
        return self.id

    def getOrientation(self):
        return self.orientation

    def getMargins(self):
        #print "VogisPrint_layout.py:27 self.margins: "
        #print self.margins
        margins = {'margin-top': self.margins[1],  'margin-right': self.margins[2],  'margin-bottom': self.margins[3],  'margin-left': self.margins[4]}
        return margins

    def getDecorations(self):
        return self.decorations
