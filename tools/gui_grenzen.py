# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_grenzen.ui'
#
# Created: Thu Aug 18 15:20:15 2016
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmGrenzen(object):
    def setupUi(self, frmGrenzen):
        frmGrenzen.setObjectName(_fromUtf8("frmGrenzen"))
        frmGrenzen.resize(303, 347)
        self.groupBox = QtGui.QGroupBox(frmGrenzen)
        self.groupBox.setGeometry(QtCore.QRect(30, 10, 241, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 113, 92))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckPolitischeGrenzen = QtGui.QCheckBox(self.layoutWidget)
        self.ckPolitischeGrenzen.setObjectName(_fromUtf8("ckPolitischeGrenzen"))
        self.buttonGroup = QtGui.QButtonGroup(frmGrenzen)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.ckPolitischeGrenzen)
        self.verticalLayout.addWidget(self.ckPolitischeGrenzen)
        self.ckKatastralgrenzen = QtGui.QCheckBox(self.layoutWidget)
        self.ckKatastralgrenzen.setObjectName(_fromUtf8("ckKatastralgrenzen"))
        self.buttonGroup.addButton(self.ckKatastralgrenzen)
        self.verticalLayout.addWidget(self.ckKatastralgrenzen)
        self.ckZaehlsprengel = QtGui.QCheckBox(self.layoutWidget)
        self.ckZaehlsprengel.setObjectName(_fromUtf8("ckZaehlsprengel"))
        self.buttonGroup.addButton(self.ckZaehlsprengel)
        self.verticalLayout.addWidget(self.ckZaehlsprengel)
        self.ckGemeinden = QtGui.QCheckBox(self.layoutWidget)
        self.ckGemeinden.setObjectName(_fromUtf8("ckGemeinden"))
        self.buttonGroup.addButton(self.ckGemeinden)
        self.verticalLayout.addWidget(self.ckGemeinden)
        self.groupBox_2 = QtGui.QGroupBox(frmGrenzen)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 140, 241, 131))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.verticalLayoutWidget = QtGui.QWidget(self.groupBox_2)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(20, 20, 160, 92))
        self.verticalLayoutWidget.setObjectName(_fromUtf8("verticalLayoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ckOGemeinden = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.ckOGemeinden.setObjectName(_fromUtf8("ckOGemeinden"))
        self.buttonGroup.addButton(self.ckOGemeinden)
        self.verticalLayout_2.addWidget(self.ckOGemeinden)
        self.ckOBezirke = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.ckOBezirke.setObjectName(_fromUtf8("ckOBezirke"))
        self.buttonGroup.addButton(self.ckOBezirke)
        self.verticalLayout_2.addWidget(self.ckOBezirke)
        self.ckOBundeslaender = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.ckOBundeslaender.setObjectName(_fromUtf8("ckOBundeslaender"))
        self.buttonGroup.addButton(self.ckOBundeslaender)
        self.verticalLayout_2.addWidget(self.ckOBundeslaender)
        self.ckONachbarlaender = QtGui.QCheckBox(self.verticalLayoutWidget)
        self.ckONachbarlaender.setObjectName(_fromUtf8("ckONachbarlaender"))
        self.buttonGroup.addButton(self.ckONachbarlaender)
        self.verticalLayout_2.addWidget(self.ckONachbarlaender)
        self.btnAbbrechen = QtGui.QPushButton(frmGrenzen)
        self.btnAbbrechen.setGeometry(QtCore.QRect(180, 290, 81, 31))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.btnLaden = QtGui.QPushButton(frmGrenzen)
        self.btnLaden.setGeometry(QtCore.QRect(50, 290, 81, 31))
        self.btnLaden.setObjectName(_fromUtf8("btnLaden"))

        self.retranslateUi(frmGrenzen)
        QtCore.QObject.connect(self.btnLaden, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGrenzen.laden)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGrenzen.abbrechen)
        QtCore.QMetaObject.connectSlotsByName(frmGrenzen)

    def retranslateUi(self, frmGrenzen):
        frmGrenzen.setWindowTitle(QtGui.QApplication.translate("frmGrenzen", "Grenzen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmGrenzen", "Vorarlberg", None, QtGui.QApplication.UnicodeUTF8))
        self.ckPolitischeGrenzen.setText(QtGui.QApplication.translate("frmGrenzen", "Politische Grenzen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckKatastralgrenzen.setText(QtGui.QApplication.translate("frmGrenzen", "Katastralgrenzen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckZaehlsprengel.setText(QtGui.QApplication.translate("frmGrenzen", "Zählsprengel", None, QtGui.QApplication.UnicodeUTF8))
        self.ckGemeinden.setText(QtGui.QApplication.translate("frmGrenzen", "Gemeinden", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmGrenzen", "Österreich und Umgebung", None, QtGui.QApplication.UnicodeUTF8))
        self.ckOGemeinden.setText(QtGui.QApplication.translate("frmGrenzen", "Österreich Gemeinden", None, QtGui.QApplication.UnicodeUTF8))
        self.ckOBezirke.setText(QtGui.QApplication.translate("frmGrenzen", "Österreich Bezirke", None, QtGui.QApplication.UnicodeUTF8))
        self.ckOBundeslaender.setText(QtGui.QApplication.translate("frmGrenzen", "Österreich Bundesländer", None, QtGui.QApplication.UnicodeUTF8))
        self.ckONachbarlaender.setText(QtGui.QApplication.translate("frmGrenzen", "Österreich Nachbarländer", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmGrenzen", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLaden.setText(QtGui.QApplication.translate("frmGrenzen", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))

