# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wegtafeln.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmWegtafeln(object):
    def setupUi(self, frmWegtafeln):
        frmWegtafeln.setObjectName("frmWegtafeln")
        frmWegtafeln.resize(453, 300)
        self.label = QtWidgets.QLabel(frmWegtafeln)
        self.label.setGeometry(QtCore.QRect(90, 30, 131, 16))
        self.label.setObjectName("label")
        self.btnOK = QtWidgets.QPushButton(frmWegtafeln)
        self.btnOK.setGeometry(QtCore.QRect(330, 90, 75, 23))
        self.btnOK.setObjectName("btnOK")
        self.btnAbbrechen = QtWidgets.QPushButton(frmWegtafeln)
        self.btnAbbrechen.setGeometry(QtCore.QRect(330, 140, 75, 23))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.lstNummern = QtWidgets.QListWidget(frmWegtafeln)
        self.lstNummern.setGeometry(QtCore.QRect(30, 60, 256, 192))
        self.lstNummern.setObjectName("lstNummern")

        self.retranslateUi(frmWegtafeln)
        self.btnAbbrechen.clicked.connect(frmWegtafeln.abbrechen)
        self.btnOK.clicked.connect(frmWegtafeln.zoomtafel)
        QtCore.QMetaObject.connectSlotsByName(frmWegtafeln)

    def retranslateUi(self, frmWegtafeln):
        _translate = QtCore.QCoreApplication.translate
        frmWegtafeln.setWindowTitle(_translate("frmWegtafeln", "Wegtafeln"))
        self.label.setText(_translate("frmWegtafeln", "Tafel Nummer auswählen"))
        self.btnOK.setText(_translate("frmWegtafeln", "OK"))
        self.btnAbbrechen.setText(_translate("frmWegtafeln", "Schließen"))

