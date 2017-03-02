# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_progressbar.ui'
#
# Created: Thu Mar 02 15:20:56 2017
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmProgress(object):
    def setupUi(self, frmProgress):
        frmProgress.setObjectName(_fromUtf8("frmProgress"))
        frmProgress.resize(429, 80)
        self.progressBar = QtGui.QProgressBar(frmProgress)
        self.progressBar.setGeometry(QtCore.QRect(20, 22, 391, 31))
        self.progressBar.setProperty(_fromUtf8("value"), 24)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.retranslateUi(frmProgress)
        QtCore.QMetaObject.connectSlotsByName(frmProgress)

    def retranslateUi(self, frmProgress):
        frmProgress.setWindowTitle(QtGui.QApplication.translate("frmProgress", "Ladefortschritt", None, QtGui.QApplication.UnicodeUTF8))

