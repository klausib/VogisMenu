# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_fischerei.ui'
#
# Created: Fri Dec 13 16:19:02 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmFischerei(object):
    def setupUi(self, frmFischerei):
        frmFischerei.setObjectName(_fromUtf8("frmFischerei"))
        frmFischerei.resize(279, 142)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmFischerei)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 90, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmFischerei)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(150, 90, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.layoutWidget = QtGui.QWidget(frmFischerei)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 201, 51))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckFischereireviere = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckFischereireviere.setFont(font)
        self.ckFischereireviere.setObjectName(_fromUtf8("ckFischereireviere"))
        self.ckButtons = QtGui.QButtonGroup(frmFischerei)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckFischereireviere)
        self.verticalLayout.addWidget(self.ckFischereireviere)

        self.retranslateUi(frmFischerei)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFischerei.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFischerei.close)
        QtCore.QMetaObject.connectSlotsByName(frmFischerei)

    def retranslateUi(self, frmFischerei):
        frmFischerei.setWindowTitle(QtGui.QApplication.translate("frmFischerei", "Fischerei", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmFischerei", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmFischerei", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckFischereireviere.setText(QtGui.QApplication.translate("frmFischerei", "Fischereireviere", None, QtGui.QApplication.UnicodeUTF8))

