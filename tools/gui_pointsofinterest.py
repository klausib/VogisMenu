# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_pointsofinterest.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmPointsofInterest(object):
    def setupUi(self, frmPointsofInterest):
        frmPointsofInterest.setObjectName("frmPointsofInterest")
        frmPointsofInterest.resize(308, 191)
        self.ButtonBlattschnitteOk = QtWidgets.QPushButton(frmPointsofInterest)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 140, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName("ButtonBlattschnitteOk")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmPointsofInterest)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(180, 140, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")
        self.groupBox = QtWidgets.QGroupBox(frmPointsofInterest)
        self.groupBox.setGeometry(QtCore.QRect(40, 20, 231, 91))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 148, 44))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ckBergspitzen = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBergspitzen.setEnabled(True)
        self.ckBergspitzen.setObjectName("ckBergspitzen")
        self.ckButtons = QtWidgets.QButtonGroup(frmPointsofInterest)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.setExclusive(False)
        self.ckButtons.addButton(self.ckBergspitzen)
        self.verticalLayout_2.addWidget(self.ckBergspitzen)
        self.ckNamengut = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckNamengut.setEnabled(True)
        self.ckNamengut.setObjectName("ckNamengut")
        self.ckButtons.addButton(self.ckNamengut)
        self.verticalLayout_2.addWidget(self.ckNamengut)

        self.retranslateUi(frmPointsofInterest)
        self.ButtonBlattschnitteOk.clicked.connect(frmPointsofInterest.accept)
        self.ButtonBlattschnitteCancel.clicked.connect(frmPointsofInterest.close)
        QtCore.QMetaObject.connectSlotsByName(frmPointsofInterest)

    def retranslateUi(self, frmPointsofInterest):
        _translate = QtCore.QCoreApplication.translate
        frmPointsofInterest.setWindowTitle(_translate("frmPointsofInterest", "Points of Interest"))
        self.ButtonBlattschnitteOk.setText(_translate("frmPointsofInterest", "Themen laden"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmPointsofInterest", "Schließen"))
        self.groupBox.setTitle(_translate("frmPointsofInterest", "Punktthemen"))
        self.ckBergspitzen.setText(_translate("frmPointsofInterest", "Bergspitzen (aus ÖK)"))
        self.ckNamengut.setText(_translate("frmPointsofInterest", "Namengut"))

