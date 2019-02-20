# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_gfz_pg.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmGFZ(object):
    def setupUi(self, frmGFZ):
        frmGFZ.setObjectName("frmGFZ")
        frmGFZ.resize(338, 310)
        self.btnAbbrechen = QtWidgets.QPushButton(frmGFZ)
        self.btnAbbrechen.setGeometry(QtCore.QRect(100, 260, 121, 31))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.groupBox = QtWidgets.QGroupBox(frmGFZ)
        self.groupBox.setGeometry(QtCore.QRect(10, 10, 311, 81))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.btnGFZ = QtWidgets.QPushButton(self.groupBox)
        self.btnGFZ.setGeometry(QtCore.QRect(90, 30, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGFZ.setFont(font)
        self.btnGFZ.setObjectName("btnGFZ")
        self.groupBox_2 = QtWidgets.QGroupBox(frmGFZ)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 110, 311, 131))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.btnGFZVIId = QtWidgets.QPushButton(self.groupBox_2)
        self.btnGFZVIId.setGeometry(QtCore.QRect(180, 40, 111, 23))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnGFZVIId.setFont(font)
        self.btnGFZVIId.setObjectName("btnGFZVIId")
        self.GfzBwv = QtWidgets.QRadioButton(self.groupBox_2)
        self.GfzBwv.setGeometry(QtCore.QRect(10, 30, 131, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.GfzBwv.setFont(font)
        self.GfzBwv.setChecked(True)
        self.GfzBwv.setObjectName("GfzBwv")
        self.buttonGroup = QtWidgets.QButtonGroup(frmGFZ)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.GfzBwv)
        self.btnKompetenzgrenzen = QtWidgets.QPushButton(self.groupBox_2)
        self.btnKompetenzgrenzen.setGeometry(QtCore.QRect(70, 90, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.btnKompetenzgrenzen.setFont(font)
        self.btnKompetenzgrenzen.setObjectName("btnKompetenzgrenzen")
        self.ckUeberflutungsflaechen = QtWidgets.QRadioButton(self.groupBox_2)
        self.ckUeberflutungsflaechen.setGeometry(QtCore.QRect(10, 60, 161, 18))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckUeberflutungsflaechen.setFont(font)
        self.ckUeberflutungsflaechen.setObjectName("ckUeberflutungsflaechen")
        self.buttonGroup.addButton(self.ckUeberflutungsflaechen)

        self.retranslateUi(frmGFZ)
        self.btnAbbrechen.clicked.connect(frmGFZ.closeEvent)
        self.btnGFZ.clicked.connect(frmGFZ.ladeGemeinde)
        self.btnGFZVIId.clicked.connect(frmGFZ.ladeGFZWB)
        self.btnKompetenzgrenzen.clicked.connect(frmGFZ.ladeKompetenzgrenzen)
        QtCore.QMetaObject.connectSlotsByName(frmGFZ)

    def retranslateUi(self, frmGFZ):
        _translate = QtCore.QCoreApplication.translate
        frmGFZ.setWindowTitle(_translate("frmGFZ", "Gefahrenzonenpläne"))
        self.btnAbbrechen.setText(_translate("frmGFZ", "Schließen"))
        self.groupBox.setTitle(_translate("frmGFZ", "Wildbach- und Lawinenverbauung"))
        self.btnGFZ.setText(_translate("frmGFZ", "GFZ Vorarlberg laden"))
        self.groupBox_2.setTitle(_translate("frmGFZ", "Abt. VIId - Wasserwirtschaft"))
        self.btnGFZVIId.setText(_translate("frmGFZ", "Daten laden"))
        self.GfzBwv.setText(_translate("frmGFZ", "Gefahrenzonen BWV"))
        self.btnKompetenzgrenzen.setText(_translate("frmGFZ", "Kompetenzgrenzen  BWV - WLV"))
        self.ckUeberflutungsflaechen.setText(_translate("frmGFZ", "Abflussuntersuchungen BWV"))

