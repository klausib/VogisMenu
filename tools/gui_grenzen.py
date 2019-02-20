# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_grenzen.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmGrenzen(object):
    def setupUi(self, frmGrenzen):
        frmGrenzen.setObjectName("frmGrenzen")
        frmGrenzen.resize(303, 209)
        self.groupBox = QtWidgets.QGroupBox(frmGrenzen)
        self.groupBox.setGeometry(QtCore.QRect(30, 10, 231, 121))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 191, 92))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckPolitischeGrenzen = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckPolitischeGrenzen.setObjectName("ckPolitischeGrenzen")
        self.buttonGroup = QtWidgets.QButtonGroup(frmGrenzen)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.ckPolitischeGrenzen)
        self.verticalLayout.addWidget(self.ckPolitischeGrenzen)
        self.ckKatastralgrenzen = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckKatastralgrenzen.setObjectName("ckKatastralgrenzen")
        self.buttonGroup.addButton(self.ckKatastralgrenzen)
        self.verticalLayout.addWidget(self.ckKatastralgrenzen)
        self.ckZaehlsprengel = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckZaehlsprengel.setObjectName("ckZaehlsprengel")
        self.buttonGroup.addButton(self.ckZaehlsprengel)
        self.verticalLayout.addWidget(self.ckZaehlsprengel)
        self.ckGemeinden = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckGemeinden.setObjectName("ckGemeinden")
        self.buttonGroup.addButton(self.ckGemeinden)
        self.verticalLayout.addWidget(self.ckGemeinden)
        self.btnAbbrechen = QtWidgets.QPushButton(frmGrenzen)
        self.btnAbbrechen.setGeometry(QtCore.QRect(170, 150, 81, 31))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.btnLaden = QtWidgets.QPushButton(frmGrenzen)
        self.btnLaden.setGeometry(QtCore.QRect(40, 150, 81, 31))
        self.btnLaden.setObjectName("btnLaden")

        self.retranslateUi(frmGrenzen)
        self.btnLaden.clicked.connect(frmGrenzen.laden)
        self.btnAbbrechen.clicked.connect(frmGrenzen.abbrechen)
        QtCore.QMetaObject.connectSlotsByName(frmGrenzen)

    def retranslateUi(self, frmGrenzen):
        _translate = QtCore.QCoreApplication.translate
        frmGrenzen.setWindowTitle(_translate("frmGrenzen", "Grenzen"))
        self.groupBox.setTitle(_translate("frmGrenzen", "Vorarlberg"))
        self.ckPolitischeGrenzen.setText(_translate("frmGrenzen", "Politische Grenzen"))
        self.ckKatastralgrenzen.setText(_translate("frmGrenzen", "Katastralgrenzen"))
        self.ckZaehlsprengel.setText(_translate("frmGrenzen", "Zählsprengel"))
        self.ckGemeinden.setText(_translate("frmGrenzen", "Gemeinden"))
        self.btnAbbrechen.setText(_translate("frmGrenzen", "Schließen"))
        self.btnLaden.setText(_translate("frmGrenzen", "Themen laden"))

