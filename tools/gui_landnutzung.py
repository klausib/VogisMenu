# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_landnutzung.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmLandnutzung(object):
    def setupUi(self, frmLandnutzung):
        frmLandnutzung.setObjectName("frmLandnutzung")
        frmLandnutzung.resize(428, 146)
        self.ButtonBlattschnitteOk = QtWidgets.QPushButton(frmLandnutzung)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(80, 100, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName("ButtonBlattschnitteOk")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmLandnutzung)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(220, 100, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")
        self.layoutWidget = QtWidgets.QWidget(frmLandnutzung)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 347, 61))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckLnRheintal = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckLnRheintal.setFont(font)
        self.ckLnRheintal.setObjectName("ckLnRheintal")
        self.ckButtons = QtWidgets.QButtonGroup(frmLandnutzung)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.setExclusive(False)
        self.ckButtons.addButton(self.ckLnRheintal)
        self.verticalLayout.addWidget(self.ckLnRheintal)

        self.retranslateUi(frmLandnutzung)
        self.ButtonBlattschnitteOk.clicked.connect(frmLandnutzung.accept)
        self.ButtonBlattschnitteCancel.clicked.connect(frmLandnutzung.close)
        QtCore.QMetaObject.connectSlotsByName(frmLandnutzung)

    def retranslateUi(self, frmLandnutzung):
        _translate = QtCore.QCoreApplication.translate
        frmLandnutzung.setWindowTitle(_translate("frmLandnutzung", "Landnutzung"))
        self.ButtonBlattschnitteOk.setText(_translate("frmLandnutzung", "Themen laden"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmLandnutzung", "Schließen"))
        self.ckLnRheintal.setText(_translate("frmLandnutzung", "Landnutzungskartierung Rheintal 2004/2005"))

