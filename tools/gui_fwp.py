# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_fwp.ui'
#
# Created: Mon Feb 16 10:56:13 2015
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmFWP(object):
    def setupUi(self, frmFWP):
        frmFWP.setObjectName(_fromUtf8("frmFWP"))
        frmFWP.resize(297, 419)
        self.lstGemeinden = QtGui.QListView(frmFWP)
        self.lstGemeinden.setGeometry(QtCore.QRect(20, 10, 256, 191))
        self.lstGemeinden.setSelectionBehavior(QtGui.QAbstractItemView.SelectItems)
        self.lstGemeinden.setObjectName(_fromUtf8("lstGemeinden"))
        self.btnFWP = QtGui.QPushButton(frmFWP)
        self.btnFWP.setGeometry(QtCore.QRect(90, 270, 111, 31))
        self.btnFWP.setObjectName(_fromUtf8("btnFWP"))
        self.btnBZ = QtGui.QPushButton(frmFWP)
        self.btnBZ.setGeometry(QtCore.QRect(90, 310, 111, 31))
        self.btnBZ.setObjectName(_fromUtf8("btnBZ"))
        self.btnAbbrechen = QtGui.QPushButton(frmFWP)
        self.btnAbbrechen.setGeometry(QtCore.QRect(90, 380, 111, 23))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.btGmdChoice = QtGui.QPushButton(frmFWP)
        self.btGmdChoice.setGeometry(QtCore.QRect(220, 210, 31, 23))
        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(255, 0, 127))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.ButtonText, brush)
        brush = QtGui.QBrush(QtGui.QColor(106, 104, 100))
        brush.setStyle(QtCore.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.ButtonText, brush)
        self.btGmdChoice.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btGmdChoice.setFont(font)
        self.btGmdChoice.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btGmdChoice.setCheckable(True)
        self.btGmdChoice.setChecked(False)
        self.btGmdChoice.setObjectName(_fromUtf8("btGmdChoice"))
        self.btnVorarlberg = QtGui.QPushButton(frmFWP)
        self.btnVorarlberg.setGeometry(QtCore.QRect(70, 210, 111, 23))
        self.btnVorarlberg.setObjectName(_fromUtf8("btnVorarlberg"))

        self.retranslateUi(frmFWP)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFWP.closeEvent)
        QtCore.QObject.connect(self.btGmdChoice, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFWP.gmd_choice_toggled)
        QtCore.QObject.connect(self.btnFWP, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFWP.ladeGemeinde)
        QtCore.QObject.connect(self.lstGemeinden, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), frmFWP.auswahlaenderung)
        QtCore.QObject.connect(self.btnBZ, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFWP.ladeBZ)
        QtCore.QObject.connect(self.btnVorarlberg, QtCore.SIGNAL(_fromUtf8("clicked()")), frmFWP.landesflaeche)
        QtCore.QMetaObject.connectSlotsByName(frmFWP)

    def retranslateUi(self, frmFWP):
        frmFWP.setWindowTitle(QtGui.QApplication.translate("frmFWP", "Flächenwidmung", None, QtGui.QApplication.UnicodeUTF8))
        self.btnFWP.setText(QtGui.QApplication.translate("frmFWP", "FWP laden", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBZ.setText(QtGui.QApplication.translate("frmFWP", "Beschränkungszonen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmFWP", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.btGmdChoice.setText(QtGui.QApplication.translate("frmFWP", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btnVorarlberg.setText(QtGui.QApplication.translate("frmFWP", "Landesfläche Vlbg.", None, QtGui.QApplication.UnicodeUTF8))

