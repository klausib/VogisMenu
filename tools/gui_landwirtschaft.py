# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_landwirtschaft.ui'
#
# Created: Mon Apr 29 15:49:21 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmLandwirtschaft(object):
    def setupUi(self, frmLandwirtschaft):
        frmLandwirtschaft.setObjectName(_fromUtf8("frmLandwirtschaft"))
        frmLandwirtschaft.resize(319, 298)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmLandwirtschaft)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 230, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmLandwirtschaft)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(170, 230, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.layoutWidget = QtGui.QWidget(frmLandwirtschaft)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 130, 191, 74))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckAlpenVorMaisaesse = QtGui.QCheckBox(self.layoutWidget)
        self.ckAlpenVorMaisaesse.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckAlpenVorMaisaesse.setFont(font)
        self.ckAlpenVorMaisaesse.setObjectName(_fromUtf8("ckAlpenVorMaisaesse"))
        self.ckButtons = QtGui.QButtonGroup(frmLandwirtschaft)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckAlpenVorMaisaesse)
        self.verticalLayout.addWidget(self.ckAlpenVorMaisaesse)
        self.ckBenachteiligteGebiete = QtGui.QCheckBox(self.layoutWidget)
        self.ckBenachteiligteGebiete.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckBenachteiligteGebiete.setFont(font)
        self.ckBenachteiligteGebiete.setObjectName(_fromUtf8("ckBenachteiligteGebiete"))
        self.ckButtons.addButton(self.ckBenachteiligteGebiete)
        self.verticalLayout.addWidget(self.ckBenachteiligteGebiete)
        self.ckBodenklimazahl = QtGui.QCheckBox(self.layoutWidget)
        self.ckBodenklimazahl.setEnabled(True)
        self.ckBodenklimazahl.setObjectName(_fromUtf8("ckBodenklimazahl"))
        self.ckButtons.addButton(self.ckBodenklimazahl)
        self.verticalLayout.addWidget(self.ckBodenklimazahl)
        self.groupBox = QtGui.QGroupBox(frmLandwirtschaft)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 231, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 30, 133, 44))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ckEigentumsverhaeltnisse = QtGui.QCheckBox(self.layoutWidget1)
        self.ckEigentumsverhaeltnisse.setEnabled(True)
        self.ckEigentumsverhaeltnisse.setObjectName(_fromUtf8("ckEigentumsverhaeltnisse"))
        self.ckButtons.addButton(self.ckEigentumsverhaeltnisse)
        self.verticalLayout_2.addWidget(self.ckEigentumsverhaeltnisse)
        self.ckAlpArt = QtGui.QCheckBox(self.layoutWidget1)
        self.ckAlpArt.setEnabled(True)
        self.ckAlpArt.setObjectName(_fromUtf8("ckAlpArt"))
        self.ckButtons.addButton(self.ckAlpArt)
        self.verticalLayout_2.addWidget(self.ckAlpArt)

        self.retranslateUi(frmLandwirtschaft)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmLandwirtschaft.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmLandwirtschaft.close)
        QtCore.QMetaObject.connectSlotsByName(frmLandwirtschaft)

    def retranslateUi(self, frmLandwirtschaft):
        frmLandwirtschaft.setWindowTitle(QtGui.QApplication.translate("frmLandwirtschaft", "Landwirtschaft", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckAlpenVorMaisaesse.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Alpen, Vor- und Maisäße", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBenachteiligteGebiete.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Benachteiligte Gebiete", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBodenklimazahl.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Bodenklimazahl (Ertragswerte)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmLandwirtschaft", "Agrargemeinschaften", None, QtGui.QApplication.UnicodeUTF8))
        self.ckEigentumsverhaeltnisse.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Eigentumsverhältnisse", None, QtGui.QApplication.UnicodeUTF8))
        self.ckAlpArt.setText(QtGui.QApplication.translate("frmLandwirtschaft", "Alp-Art", None, QtGui.QApplication.UnicodeUTF8))

