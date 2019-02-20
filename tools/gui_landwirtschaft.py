# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_landwirtschaft.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmLandwirtschaft(object):
    def setupUi(self, frmLandwirtschaft):
        frmLandwirtschaft.setObjectName("frmLandwirtschaft")
        frmLandwirtschaft.resize(319, 298)
        self.ButtonBlattschnitteOk = QtWidgets.QPushButton(frmLandwirtschaft)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 230, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName("ButtonBlattschnitteOk")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmLandwirtschaft)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(170, 230, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")
        self.layoutWidget = QtWidgets.QWidget(frmLandwirtschaft)
        self.layoutWidget.setGeometry(QtCore.QRect(60, 130, 191, 74))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckAlpenVorMaisaesse = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckAlpenVorMaisaesse.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckAlpenVorMaisaesse.setFont(font)
        self.ckAlpenVorMaisaesse.setObjectName("ckAlpenVorMaisaesse")
        self.ckButtons = QtWidgets.QButtonGroup(frmLandwirtschaft)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.setExclusive(False)
        self.ckButtons.addButton(self.ckAlpenVorMaisaesse)
        self.verticalLayout.addWidget(self.ckAlpenVorMaisaesse)
        self.ckBenachteiligteGebiete = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBenachteiligteGebiete.setEnabled(True)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckBenachteiligteGebiete.setFont(font)
        self.ckBenachteiligteGebiete.setObjectName("ckBenachteiligteGebiete")
        self.ckButtons.addButton(self.ckBenachteiligteGebiete)
        self.verticalLayout.addWidget(self.ckBenachteiligteGebiete)
        self.ckBodenklimazahl = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBodenklimazahl.setEnabled(True)
        self.ckBodenklimazahl.setObjectName("ckBodenklimazahl")
        self.ckButtons.addButton(self.ckBodenklimazahl)
        self.verticalLayout.addWidget(self.ckBodenklimazahl)
        self.groupBox = QtWidgets.QGroupBox(frmLandwirtschaft)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 231, 91))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(20, 30, 133, 44))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ckEigentumsverhaeltnisse = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckEigentumsverhaeltnisse.setEnabled(True)
        self.ckEigentumsverhaeltnisse.setObjectName("ckEigentumsverhaeltnisse")
        self.ckButtons.addButton(self.ckEigentumsverhaeltnisse)
        self.verticalLayout_2.addWidget(self.ckEigentumsverhaeltnisse)
        self.ckAlpArt = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckAlpArt.setEnabled(True)
        self.ckAlpArt.setObjectName("ckAlpArt")
        self.ckButtons.addButton(self.ckAlpArt)
        self.verticalLayout_2.addWidget(self.ckAlpArt)

        self.retranslateUi(frmLandwirtschaft)
        self.ButtonBlattschnitteOk.clicked.connect(frmLandwirtschaft.accept)
        self.ButtonBlattschnitteCancel.clicked.connect(frmLandwirtschaft.close)
        QtCore.QMetaObject.connectSlotsByName(frmLandwirtschaft)

    def retranslateUi(self, frmLandwirtschaft):
        _translate = QtCore.QCoreApplication.translate
        frmLandwirtschaft.setWindowTitle(_translate("frmLandwirtschaft", "Landwirtschaft"))
        self.ButtonBlattschnitteOk.setText(_translate("frmLandwirtschaft", "Themen laden"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmLandwirtschaft", "Schließen"))
        self.ckAlpenVorMaisaesse.setText(_translate("frmLandwirtschaft", "Alpen, Vor- und Maisäße"))
        self.ckBenachteiligteGebiete.setText(_translate("frmLandwirtschaft", "Benachteiligte Gebiete"))
        self.ckBodenklimazahl.setText(_translate("frmLandwirtschaft", "Bodenklimazahl (Ertragswerte)"))
        self.groupBox.setTitle(_translate("frmLandwirtschaft", "Agrargemeinschaften"))
        self.ckEigentumsverhaeltnisse.setText(_translate("frmLandwirtschaft", "Eigentumsverhältnisse"))
        self.ckAlpArt.setText(_translate("frmLandwirtschaft", "Alp-Art"))

