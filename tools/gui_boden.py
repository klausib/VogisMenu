# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_boden.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmBoden(object):
    def setupUi(self, frmBoden):
        frmBoden.setObjectName("frmBoden")
        frmBoden.resize(260, 168)
        self.btnAbbrechen = QtWidgets.QPushButton(frmBoden)
        self.btnAbbrechen.setGeometry(QtCore.QRect(140, 110, 75, 23))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.btnLaden = QtWidgets.QPushButton(frmBoden)
        self.btnLaden.setGeometry(QtCore.QRect(40, 110, 75, 23))
        self.btnLaden.setObjectName("btnLaden")
        self.layoutWidget = QtWidgets.QWidget(frmBoden)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 40, 119, 44))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckDigitaleBodenkarte = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckDigitaleBodenkarte.setObjectName("ckDigitaleBodenkarte")
        self.ckButtons = QtWidgets.QButtonGroup(frmBoden)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.addButton(self.ckDigitaleBodenkarte)
        self.verticalLayout.addWidget(self.ckDigitaleBodenkarte)
        self.ckBodenprofile = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBodenprofile.setObjectName("ckBodenprofile")
        self.ckButtons.addButton(self.ckBodenprofile)
        self.verticalLayout.addWidget(self.ckBodenprofile)
        self.btnInfo = QtWidgets.QPushButton(frmBoden)
        self.btnInfo.setGeometry(QtCore.QRect(190, 50, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btnInfo.setFont(font)
        self.btnInfo.setObjectName("btnInfo")

        self.retranslateUi(frmBoden)
        self.btnLaden.clicked.connect(frmBoden.laden)
        self.btnAbbrechen.clicked.connect(frmBoden.abbrechen)
        self.btnInfo.clicked.connect(frmBoden.infobutton)
        QtCore.QMetaObject.connectSlotsByName(frmBoden)

    def retranslateUi(self, frmBoden):
        _translate = QtCore.QCoreApplication.translate
        frmBoden.setWindowTitle(_translate("frmBoden", "Boden"))
        self.btnAbbrechen.setText(_translate("frmBoden", "Schließen"))
        self.btnLaden.setText(_translate("frmBoden", "Themen laden"))
        self.ckDigitaleBodenkarte.setText(_translate("frmBoden", "Digitale Bodenkarte"))
        self.ckBodenprofile.setText(_translate("frmBoden", "Bodenprofile"))
        self.btnInfo.setText(_translate("frmBoden", "i"))

