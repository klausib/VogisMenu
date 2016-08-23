# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_gstauswahl.ui'
#
# Created: Tue Aug 23 10:10:55 2016
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmGstauswahl(object):
    def setupUi(self, frmGstauswahl):
        frmGstauswahl.setObjectName(_fromUtf8("frmGstauswahl"))
        frmGstauswahl.resize(331, 66)
        self.label = QtGui.QLabel(frmGstauswahl)
        self.label.setGeometry(QtCore.QRect(20, 10, 401, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setWeight(75)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))

        self.retranslateUi(frmGstauswahl)
        QtCore.QMetaObject.connectSlotsByName(frmGstauswahl)

    def retranslateUi(self, frmGstauswahl):
        frmGstauswahl.setWindowTitle(QtGui.QApplication.translate("frmGstauswahl", "Ladefortschritt", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmGstauswahl", "Grundstücke werden gesucht........", None, QtGui.QApplication.UnicodeUTF8))

