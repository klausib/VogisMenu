# -*- coding: latin1 -*-

class Decoration():
    def __init__(self, type):
        self.type = type
        self.affinity_x = "left"
        self.affinity_y = "top"
        self.offset_x = 0
        self.offset_y = 0
        self.height = 0
        self.width = 0
        self.fontsize = 12
        self.text = ""
        self.picture = ""
        self.rotation = 0
        self.fontfamily = "Bitstream Vera Sans"
        
    def setAffinityX(self,  affx):
        self.affinity_x = affx
        
    def setAffinityY(self,  affy):
        self.affinity_y = affy        
    
    def setOffsetX(self,  x):
        self.offset_x = x
        
    def setOffsetY(self,  y):
        self.offset_y = y
        
    def setHeight(self,  h):
        self.height = h
        
    def setWidth(self,  w):
        self.width = w
        
    def setText(self,  text):
        self.text = text
    
    def setFontSize(self,  s):
        self.fontsize = s
        
    def setFontFamily(self,  font):
        self.fontfamily = font
        
    def setRotation(self,  r):
        self.rotation = r
        
    def setPicture(self,  p):
        self.picture = p
        
    def getType(self):
        return self.type        
        
    def getAffinityX(self):
        return self.affinity_x
        
    def getAffinityY(self):
        return self.affinity_y

    def getOffsetX(self):
        return self.offset_x
        
    def getOffsetY(self):
        return self.offset_y       
        
    def getHeight(self):
        return self.height
        
    def getWidth(self):
        return self.width
        
    def getFontSize(self):
        return self.fontsize
        
    def getFontFamily(self):
        return self.fontfamily
        
    def getText(self):
        return unicode(self.text)
        
    def getPicture(self):
        return unicode(self.picture)
        
    def getRotation(self):
        return self.rotation
