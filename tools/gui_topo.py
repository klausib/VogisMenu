# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_topo.ui'
#
# Created: Fri Dec 06 14:56:37 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmTopo(object):
    def setupUi(self, frmTopo):
        frmTopo.setObjectName(_fromUtf8("frmTopo"))
        frmTopo.resize(703, 913)
        self.textView = QtGui.QTextEdit(frmTopo)
        self.textView.setGeometry(QtCore.QRect(40, 20, 631, 831))
        self.textView.setLineWrapMode(QtGui.QTextEdit.FixedPixelWidth)
        self.textView.setLineWrapColumnOrWidth(500)
        self.textView.setObjectName(_fromUtf8("textView"))
        self.btnText = QtGui.QPushButton(frmTopo)
        self.btnText.setGeometry(QtCore.QRect(170, 870, 161, 31))
        self.btnText.setObjectName(_fromUtf8("btnText"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmTopo)
        self.ButtonBlattschnitteCancel.setEnabled(True)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(410, 870, 111, 31))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))

        self.retranslateUi(frmTopo)
        QtCore.QObject.connect(self.btnText, QtCore.SIGNAL(_fromUtf8("clicked()")), frmTopo.drucken_text)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmTopo.closeEvent)
        QtCore.QMetaObject.connectSlotsByName(frmTopo)

    def retranslateUi(self, frmTopo):
        frmTopo.setWindowTitle(QtGui.QApplication.translate("frmTopo", "Topographie LVA Punkte", None, QtGui.QApplication.UnicodeUTF8))
        self.btnText.setText(QtGui.QApplication.translate("frmTopo", "Topographie Drucken", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmTopo", "Schließen", None, QtGui.QApplication.UnicodeUTF8))

