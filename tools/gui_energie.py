# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_energie.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmEnergie(object):
    def setupUi(self, frmEnergie):
        frmEnergie.setObjectName("frmEnergie")
        frmEnergie.resize(248, 155)
        self.ButtonEnergieOk = QtWidgets.QPushButton(frmEnergie)
        self.ButtonEnergieOk.setGeometry(QtCore.QRect(10, 110, 101, 23))
        self.ButtonEnergieOk.setObjectName("ButtonEnergieOk")
        self.ButtonEnergieCancel = QtWidgets.QPushButton(frmEnergie)
        self.ButtonEnergieCancel.setGeometry(QtCore.QRect(130, 110, 101, 23))
        self.ButtonEnergieCancel.setObjectName("ButtonEnergieCancel")
        self.frame = QtWidgets.QFrame(frmEnergie)
        self.frame.setGeometry(QtCore.QRect(10, 10, 221, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 185, 51))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName("checkBox")
        self.checkButtonsGroup = QtWidgets.QButtonGroup(frmEnergie)
        self.checkButtonsGroup.setObjectName("checkButtonsGroup")
        self.checkButtonsGroup.setExclusive(False)
        self.checkButtonsGroup.addButton(self.checkBox)
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName("checkBox_2")
        self.checkButtonsGroup.addButton(self.checkBox_2)
        self.verticalLayout.addWidget(self.checkBox_2)

        self.retranslateUi(frmEnergie)
        self.ButtonEnergieOk.clicked.connect(frmEnergie.accept)
        self.ButtonEnergieCancel.clicked.connect(frmEnergie.close)
        QtCore.QMetaObject.connectSlotsByName(frmEnergie)

    def retranslateUi(self, frmEnergie):
        _translate = QtCore.QCoreApplication.translate
        frmEnergie.setWindowTitle(_translate("frmEnergie", "Energieversorgung"))
        self.ButtonEnergieOk.setText(_translate("frmEnergie", "Themen laden"))
        self.ButtonEnergieCancel.setText(_translate("frmEnergie", "Schließen"))
        self.checkBox.setText(_translate("frmEnergie", "Energieversorgung: GAS"))
        self.checkBox_2.setText(_translate("frmEnergie", "Energieversorgung: STROM"))

