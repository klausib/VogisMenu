# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_options.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmOptions(object):
    def setupUi(self, frmOptions):
        frmOptions.setObjectName("frmOptions")
        frmOptions.resize(349, 187)
        self.ButtonSave = QtWidgets.QPushButton(frmOptions)
        self.ButtonSave.setGeometry(QtCore.QRect(120, 150, 101, 23))
        self.ButtonSave.setObjectName("ButtonSave")
        self.layoutWidget = QtWidgets.QWidget(frmOptions)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 270, 77))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckCRS = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckCRS.setFont(font)
        self.ckCRS.setObjectName("ckCRS")
        self.verticalLayout.addWidget(self.ckCRS)
        self.ckEncoding = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckEncoding.setFont(font)
        self.ckEncoding.setObjectName("ckEncoding")
        self.verticalLayout.addWidget(self.ckEncoding)
        self.ckDb = QtWidgets.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckDb.setFont(font)
        self.ckDb.setChecked(True)
        self.ckDb.setObjectName("ckDb")
        self.verticalLayout.addWidget(self.ckDb)
        self.ButtonPath = QtWidgets.QPushButton(frmOptions)
        self.ButtonPath.setGeometry(QtCore.QRect(230, 110, 81, 23))
        self.ButtonPath.setObjectName("ButtonPath")
        self.lblPath = QtWidgets.QLabel(frmOptions)
        self.lblPath.setGeometry(QtCore.QRect(40, 100, 181, 37))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.lblPath.setFont(font)
        self.lblPath.setObjectName("lblPath")

        self.retranslateUi(frmOptions)
        QtCore.QMetaObject.connectSlotsByName(frmOptions)

    def retranslateUi(self, frmOptions):
        _translate = QtCore.QCoreApplication.translate
        frmOptions.setWindowTitle(_translate("frmOptions", "VOGIS - Menü Einstellungen"))
        self.ButtonSave.setText(_translate("frmOptions", "OK"))
        self.ckCRS.setText(_translate("frmOptions", "Koordinatenbezugssystem aus Projektdatei"))
        self.ckEncoding.setText(_translate("frmOptions", "Codierung Shapefiles aus Projektdatei"))
        self.ckDb.setText(_translate("frmOptions", "Vektorlayer aus Geodatenbank"))
        self.ButtonPath.setText(_translate("frmOptions", "Pfad Ändern"))
        self.lblPath.setText(_translate("frmOptions", "Path"))

