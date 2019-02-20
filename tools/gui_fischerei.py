# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_fischerei.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmFischerei(object):
    def setupUi(self, frmFischerei):
        frmFischerei.setObjectName("frmFischerei")
        frmFischerei.resize(279, 142)
        self.ButtonBlattschnitteOk = QtWidgets.QPushButton(frmFischerei)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 90, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName("ButtonBlattschnitteOk")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmFischerei)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(150, 90, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")
        self.layoutWidget = QtWidgets.QWidget(frmFischerei)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 201, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckFischereireviere = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckFischereireviere.setFont(font)
        self.ckFischereireviere.setObjectName("ckFischereireviere")
        self.ckButtons = QtWidgets.QButtonGroup(frmFischerei)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.setExclusive(False)
        self.ckButtons.addButton(self.ckFischereireviere)
        self.verticalLayout.addWidget(self.ckFischereireviere)

        self.retranslateUi(frmFischerei)
        self.ButtonBlattschnitteOk.clicked.connect(frmFischerei.accept)
        self.ButtonBlattschnitteCancel.clicked.connect(frmFischerei.close)
        QtCore.QMetaObject.connectSlotsByName(frmFischerei)

    def retranslateUi(self, frmFischerei):
        _translate = QtCore.QCoreApplication.translate
        frmFischerei.setWindowTitle(_translate("frmFischerei", "Fischerei"))
        self.ButtonBlattschnitteOk.setText(_translate("frmFischerei", "Themen laden"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmFischerei", "Schließen"))
        self.ckFischereireviere.setText(_translate("frmFischerei", "Fischereireviere"))

