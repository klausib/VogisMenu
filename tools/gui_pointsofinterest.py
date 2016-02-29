# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_pointsofinterest.ui'
#
# Created: Thu Jun 28 15:14:51 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmPointsofInterest(object):
    def setupUi(self, frmPointsofInterest):
        frmPointsofInterest.setObjectName(_fromUtf8("frmPointsofInterest"))
        frmPointsofInterest.resize(308, 191)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmPointsofInterest)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 140, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmPointsofInterest)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(180, 140, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.groupBox = QtGui.QGroupBox(frmPointsofInterest)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 231, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 148, 44))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ckBergspitzen = QtGui.QCheckBox(self.layoutWidget)
        self.ckBergspitzen.setEnabled(True)
        self.ckBergspitzen.setObjectName(_fromUtf8("ckBergspitzen"))
        self.ckButtons = QtGui.QButtonGroup(frmPointsofInterest)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckBergspitzen)
        self.verticalLayout_2.addWidget(self.ckBergspitzen)
        self.ckNamengut = QtGui.QCheckBox(self.layoutWidget)
        self.ckNamengut.setEnabled(True)
        self.ckNamengut.setObjectName(_fromUtf8("ckNamengut"))
        self.ckButtons.addButton(self.ckNamengut)
        self.verticalLayout_2.addWidget(self.ckNamengut)

        self.retranslateUi(frmPointsofInterest)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmPointsofInterest.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmPointsofInterest.close)
        QtCore.QMetaObject.connectSlotsByName(frmPointsofInterest)

    def retranslateUi(self, frmPointsofInterest):
        frmPointsofInterest.setWindowTitle(QtGui.QApplication.translate("frmPointsofInterest", "Points of Interest", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmPointsofInterest", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmPointsofInterest", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmPointsofInterest", "Punktthemen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBergspitzen.setText(QtGui.QApplication.translate("frmPointsofInterest", "Bergspitzen (aus ÖK)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNamengut.setText(QtGui.QApplication.translate("frmPointsofInterest", "Namengut", None, QtGui.QApplication.UnicodeUTF8))

