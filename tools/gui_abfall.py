# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_abfall.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmAbfall(object):
    def setupUi(self, frmAbfall):
        frmAbfall.setObjectName("frmAbfall")
        frmAbfall.resize(206, 175)
        self.ButtonAbfallOk = QtWidgets.QPushButton(frmAbfall)
        self.ButtonAbfallOk.setGeometry(QtCore.QRect(40, 110, 121, 23))
        self.ButtonAbfallOk.setObjectName("ButtonAbfallOk")
        self.ButtonAbfallCancel = QtWidgets.QPushButton(frmAbfall)
        self.ButtonAbfallCancel.setGeometry(QtCore.QRect(40, 140, 121, 23))
        self.ButtonAbfallCancel.setObjectName("ButtonAbfallCancel")
        self.frame = QtWidgets.QFrame(frmAbfall)
        self.frame.setGeometry(QtCore.QRect(10, 10, 181, 91))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 144, 51))
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
        self.checkButtonsGroup = QtWidgets.QButtonGroup(frmAbfall)
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

        self.retranslateUi(frmAbfall)
        self.ButtonAbfallOk.clicked.connect(frmAbfall.accept)
        self.ButtonAbfallCancel.clicked.connect(frmAbfall.close)
        QtCore.QMetaObject.connectSlotsByName(frmAbfall)

    def retranslateUi(self, frmAbfall):
        _translate = QtCore.QCoreApplication.translate
        frmAbfall.setWindowTitle(_translate("frmAbfall", "Abfallwirtschaft"))
        self.ButtonAbfallOk.setText(_translate("frmAbfall", "Themen laden"))
        self.ButtonAbfallCancel.setText(_translate("frmAbfall", "Schließen"))
        self.checkBox.setText(_translate("frmAbfall", "Deponien"))
        self.checkBox_2.setText(_translate("frmAbfall", "Altstandorte"))

