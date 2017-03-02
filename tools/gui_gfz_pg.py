# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_gfz_pg.ui'
#
# Created: Thu Mar 02 10:50:00 2017
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmGFZ(object):
    def setupUi(self, frmGFZ):
        frmGFZ.setObjectName(_fromUtf8("frmGFZ"))
        frmGFZ.resize(338, 310)
        self.btnAbbrechen = QtGui.QPushButton(frmGFZ)
        self.btnAbbrechen.setGeometry(QtCore.QRect(100, 260, 121, 31))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.groupBox = QtGui.QGroupBox(frmGFZ)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 311, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btnGFZ = QtGui.QPushButton(self.groupBox)
        self.btnGFZ.setGeometry(QtCore.QRect(90, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGFZ.setFont(font)
        self.btnGFZ.setObjectName(_fromUtf8("btnGFZ"))
        self.groupBox_2 = QtGui.QGroupBox(frmGFZ)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 311, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btnGFZVIId = QtGui.QPushButton(self.groupBox_2)
        self.btnGFZVIId.setGeometry(QtCore.QRect(180, 40, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGFZVIId.setFont(font)
        self.btnGFZVIId.setObjectName(_fromUtf8("btnGFZVIId"))
        self.GfzBwv = QtGui.QRadioButton(self.groupBox_2)
        self.GfzBwv.setGeometry(QtCore.QRect(10, 30, 131, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.GfzBwv.setFont(font)
        self.GfzBwv.setChecked(True)
        self.GfzBwv.setObjectName(_fromUtf8("GfzBwv"))
        self.buttonGroup = QtGui.QButtonGroup(frmGFZ)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.GfzBwv)
        self.btnKompetenzgrenzen = QtGui.QPushButton(self.groupBox_2)
        self.btnKompetenzgrenzen.setGeometry(QtCore.QRect(70, 90, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnKompetenzgrenzen.setFont(font)
        self.btnKompetenzgrenzen.setObjectName(_fromUtf8("btnKompetenzgrenzen"))
        self.ckUeberflutungsflaechen = QtGui.QRadioButton(self.groupBox_2)
        self.ckUeberflutungsflaechen.setGeometry(QtCore.QRect(10, 60, 161, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckUeberflutungsflaechen.setFont(font)
        self.ckUeberflutungsflaechen.setObjectName(_fromUtf8("ckUeberflutungsflaechen"))
        self.buttonGroup.addButton(self.ckUeberflutungsflaechen)

        self.retranslateUi(frmGFZ)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.closeEvent)
        QtCore.QObject.connect(self.btnGFZ, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeGemeinde)
        QtCore.QObject.connect(self.btnGFZVIId, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeGFZWB)
        QtCore.QObject.connect(self.btnKompetenzgrenzen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeKompetenzgrenzen)
        QtCore.QMetaObject.connectSlotsByName(frmGFZ)

    def retranslateUi(self, frmGFZ):
        frmGFZ.setWindowTitle(QtGui.QApplication.translate("frmGFZ", "Gefahrenzonenpläne", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmGFZ", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmGFZ", "Wildbach- und Lawinenverbauung", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGFZ.setText(QtGui.QApplication.translate("frmGFZ", "GFZ Vorarlberg laden", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmGFZ", "Abt. VIId - Wasserwirtschaft", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGFZVIId.setText(QtGui.QApplication.translate("frmGFZ", "Daten laden", None, QtGui.QApplication.UnicodeUTF8))
        self.GfzBwv.setText(QtGui.QApplication.translate("frmGFZ", "Gefahrenzonen BWV", None, QtGui.QApplication.UnicodeUTF8))
        self.btnKompetenzgrenzen.setText(QtGui.QApplication.translate("frmGFZ", "Kompetenzgrenzen  BWV - WLV", None, QtGui.QApplication.UnicodeUTF8))
        self.ckUeberflutungsflaechen.setText(QtGui.QApplication.translate("frmGFZ", "Abflussuntersuchungen BWV", None, QtGui.QApplication.UnicodeUTF8))

