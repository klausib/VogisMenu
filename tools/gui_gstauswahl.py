# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_gstauswahl.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmGstauswahl(object):
    def setupUi(self, frmGstauswahl):
        frmGstauswahl.setObjectName("frmGstauswahl")
        frmGstauswahl.resize(331, 66)
        self.label = QtWidgets.QLabel(frmGstauswahl)
        self.label.setGeometry(QtCore.QRect(20, 10, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(frmGstauswahl)
        QtCore.QMetaObject.connectSlotsByName(frmGstauswahl)

    def retranslateUi(self, frmGstauswahl):
        _translate = QtCore.QCoreApplication.translate
        frmGstauswahl.setWindowTitle(_translate("frmGstauswahl", "Ladefortschritt"))
        self.label.setText(_translate("frmGstauswahl", "Grundstücke werden gesucht........"))

