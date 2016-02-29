# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wegtafeln.ui'
#
# Created: Wed Feb 13 13:41:55 2013
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmWegtafeln(object):
    def setupUi(self, frmWegtafeln):
        frmWegtafeln.setObjectName(_fromUtf8("frmWegtafeln"))
        frmWegtafeln.resize(453, 300)
        self.label = QtGui.QLabel(frmWegtafeln)
        self.label.setGeometry(QtCore.QRect(90, 30, 131, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.btnOK = QtGui.QPushButton(frmWegtafeln)
        self.btnOK.setGeometry(QtCore.QRect(330, 90, 75, 23))
        self.btnOK.setObjectName(_fromUtf8("btnOK"))
        self.btnAbbrechen = QtGui.QPushButton(frmWegtafeln)
        self.btnAbbrechen.setGeometry(QtCore.QRect(330, 140, 75, 23))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.lstNummern = QtGui.QListWidget(frmWegtafeln)
        self.lstNummern.setGeometry(QtCore.QRect(30, 60, 256, 192))
        self.lstNummern.setObjectName(_fromUtf8("lstNummern"))

        self.retranslateUi(frmWegtafeln)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmWegtafeln.abbrechen)
        QtCore.QObject.connect(self.btnOK, QtCore.SIGNAL(_fromUtf8("clicked()")), frmWegtafeln.zoomtafel)
        QtCore.QMetaObject.connectSlotsByName(frmWegtafeln)

    def retranslateUi(self, frmWegtafeln):
        frmWegtafeln.setWindowTitle(QtGui.QApplication.translate("frmWegtafeln", "Wegtafeln", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("frmWegtafeln", "Tafel Nummer auswählen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnOK.setText(QtGui.QApplication.translate("frmWegtafeln", "OK", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmWegtafeln", "Schließen", None, QtGui.QApplication.UnicodeUTF8))

