# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_ladefortschritt.ui'
#
# Created: Thu Jan 17 10:50:24 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmLadefortschritt(object):
    def setupUi(self, frmLadefortschritt):
        frmLadefortschritt.setObjectName(_fromUtf8("frmLadefortschritt"))
        frmLadefortschritt.resize(429, 80)
        self.label = QtGui.QLabel(frmLadefortschritt)
        self.label.setGeometry(QtCore.QRect(20, 10, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(frmLadefortschritt)
        QtCore.QMetaObject.connectSlotsByName(frmLadefortschritt)

    def retranslateUi(self, frmLadefortschritt):
        frmLadefortschritt.setWindowTitle(QtGui.QApplication.translate("frmLadefortschritt", "Ladefortschritt", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmLadefortschritt", "Daten werden vom VOGIS Laufwerk geladen...", None, QtGui.QApplication.UnicodeUTF8))

