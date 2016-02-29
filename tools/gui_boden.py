# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_boden.ui'
#
# Created: Tue Jun 26 14:44:43 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmBoden(object):
    def setupUi(self, frmBoden):
        frmBoden.setObjectName(_fromUtf8("frmBoden"))
        frmBoden.resize(260, 168)
        self.btnAbbrechen = QtGui.QPushButton(frmBoden)
        self.btnAbbrechen.setGeometry(QtCore.QRect(140, 110, 75, 23))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.btnLaden = QtGui.QPushButton(frmBoden)
        self.btnLaden.setGeometry(QtCore.QRect(40, 110, 75, 23))
        self.btnLaden.setObjectName(_fromUtf8("btnLaden"))
        self.layoutWidget = QtGui.QWidget(frmBoden)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 40, 119, 44))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckDigitaleBodenkarte = QtGui.QCheckBox(self.layoutWidget)
        self.ckDigitaleBodenkarte.setObjectName(_fromUtf8("ckDigitaleBodenkarte"))
        self.ckButtons = QtGui.QButtonGroup(frmBoden)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckDigitaleBodenkarte)
        self.verticalLayout.addWidget(self.ckDigitaleBodenkarte)
        self.ckBodenprofile = QtGui.QCheckBox(self.layoutWidget)
        self.ckBodenprofile.setObjectName(_fromUtf8("ckBodenprofile"))
        self.ckButtons.addButton(self.ckBodenprofile)
        self.verticalLayout.addWidget(self.ckBodenprofile)
        self.btnInfo = QtGui.QPushButton(frmBoden)
        self.btnInfo.setGeometry(QtCore.QRect(190, 50, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setWeight(75)
        font.setBold(True)
        self.btnInfo.setFont(font)
        self.btnInfo.setObjectName(_fromUtf8("btnInfo"))

        self.retranslateUi(frmBoden)
        QtCore.QObject.connect(self.btnLaden, QtCore.SIGNAL(_fromUtf8("clicked()")), frmBoden.laden)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmBoden.abbrechen)
        QtCore.QObject.connect(self.btnInfo, QtCore.SIGNAL(_fromUtf8("clicked()")), frmBoden.infobutton)
        QtCore.QMetaObject.connectSlotsByName(frmBoden)

    def retranslateUi(self, frmBoden):
        frmBoden.setWindowTitle(QtGui.QApplication.translate("frmBoden", "Boden", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmBoden", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLaden.setText(QtGui.QApplication.translate("frmBoden", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ckDigitaleBodenkarte.setText(QtGui.QApplication.translate("frmBoden", "Digitale Bodenkarte", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBodenprofile.setText(QtGui.QApplication.translate("frmBoden", "Bodenprofile", None, QtGui.QApplication.UnicodeUTF8))
        self.btnInfo.setText(QtGui.QApplication.translate("frmBoden", "i", None, QtGui.QApplication.UnicodeUTF8))

