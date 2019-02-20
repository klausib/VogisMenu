# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_topo.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmTopo(object):
    def setupUi(self, frmTopo):
        frmTopo.setObjectName("frmTopo")
        frmTopo.resize(694, 913)
        self.textView = QtWidgets.QTextEdit(frmTopo)
        self.textView.setGeometry(QtCore.QRect(20, 20, 651, 831))
        self.textView.setLineWrapMode(QtWidgets.QTextEdit.FixedPixelWidth)
        self.textView.setLineWrapColumnOrWidth(500)
        self.textView.setObjectName("textView")
        self.btnText = QtWidgets.QPushButton(frmTopo)
        self.btnText.setGeometry(QtCore.QRect(170, 870, 161, 31))
        self.btnText.setObjectName("btnText")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmTopo)
        self.ButtonBlattschnitteCancel.setEnabled(True)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(410, 870, 111, 31))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")

        self.retranslateUi(frmTopo)
        self.btnText.clicked.connect(frmTopo.drucken_text)
        self.ButtonBlattschnitteCancel.clicked.connect(frmTopo.closeEvent)
        QtCore.QMetaObject.connectSlotsByName(frmTopo)

    def retranslateUi(self, frmTopo):
        _translate = QtCore.QCoreApplication.translate
        frmTopo.setWindowTitle(_translate("frmTopo", "Topographie LVA Punkte"))
        self.btnText.setText(_translate("frmTopo", "Topographie Drucken"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmTopo", "Schließen"))

