# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_grenzen.ui'
#
# Created: Wed Dec 19 09:45:02 2012
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
        frmGrenzen.resize(303, 271)
        self.groupBox = QtGui.QGroupBox(frmGrenzen)
        self.groupBox.setGeometry(QtCore.QRect(30, 10, 241, 121))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 113, 88))
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
        self.groupBox_2.setGeometry(QtCore.QRect(30, 140, 241, 51))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.ckLaendergrenzen = QtGui.QCheckBox(self.groupBox_2)
        self.ckLaendergrenzen.setGeometry(QtCore.QRect(10, 20, 111, 18))
        self.ckLaendergrenzen.setObjectName(_fromUtf8("ckLaendergrenzen"))
        self.buttonGroup.addButton(self.ckLaendergrenzen)
        self.btnAbbrechen = QtGui.QPushButton(frmGrenzen)
        self.btnAbbrechen.setGeometry(QtCore.QRect(170, 210, 81, 31))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.btnLaden = QtGui.QPushButton(frmGrenzen)
        self.btnLaden.setGeometry(QtCore.QRect(40, 210, 81, 31))
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
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmGrenzen", "Österreich", None, QtGui.QApplication.UnicodeUTF8))
        self.ckLaendergrenzen.setText(QtGui.QApplication.translate("frmGrenzen", "Länder Grenzen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmGrenzen", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLaden.setText(QtGui.QApplication.translate("frmGrenzen", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))

