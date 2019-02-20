# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_ladefortschritt.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmLadefortschritt(object):
    def setupUi(self, frmLadefortschritt):
        frmLadefortschritt.setObjectName("frmLadefortschritt")
        frmLadefortschritt.resize(429, 80)
        self.label = QtWidgets.QLabel(frmLadefortschritt)
        self.label.setGeometry(QtCore.QRect(20, 10, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")

        self.retranslateUi(frmLadefortschritt)
        QtCore.QMetaObject.connectSlotsByName(frmLadefortschritt)

    def retranslateUi(self, frmLadefortschritt):
        _translate = QtCore.QCoreApplication.translate
        frmLadefortschritt.setWindowTitle(_translate("frmLadefortschritt", "Ladefortschritt"))
        self.label.setText(_translate("frmLadefortschritt", "Daten werden vom VOGIS Laufwerk geladen..."))

