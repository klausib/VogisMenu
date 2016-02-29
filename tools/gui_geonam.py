# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_geonam.ui'
#
# Created: Tue Jun 26 14:04:58 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmGeonam(object):
    def setupUi(self, frmGeonam):
        frmGeonam.setObjectName(_fromUtf8("frmGeonam"))
        frmGeonam.resize(334, 384)
        self.lstGeonam = QtGui.QListView(frmGeonam)
        self.lstGeonam.setGeometry(QtCore.QRect(20, 65, 291, 187))
        self.lstGeonam.setObjectName(_fromUtf8("lstGeonam"))
        self.linSuche = QtGui.QLineEdit(frmGeonam)
        self.linSuche.setGeometry(QtCore.QRect(20, 40, 291, 20))
        self.linSuche.setObjectName(_fromUtf8("linSuche"))
        self.btnAnzeigen = QtGui.QPushButton(frmGeonam)
        self.btnAnzeigen.setEnabled(False)
        self.btnAnzeigen.setGeometry(QtCore.QRect(110, 266, 121, 27))
        self.btnAnzeigen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnAnzeigen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnAnzeigen.setObjectName(_fromUtf8("btnAnzeigen"))
        self.btnLoeschen = QtGui.QPushButton(frmGeonam)
        self.btnLoeschen.setGeometry(QtCore.QRect(110, 298, 121, 27))
        self.btnLoeschen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnLoeschen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnLoeschen.setObjectName(_fromUtf8("btnLoeschen"))
        self.btnAbbrechen = QtGui.QPushButton(frmGeonam)
        self.btnAbbrechen.setGeometry(QtCore.QRect(110, 330, 121, 27))
        self.btnAbbrechen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnAbbrechen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))

        self.retranslateUi(frmGeonam)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGeonam.abbrechen)
        QtCore.QObject.connect(self.linSuche, QtCore.SIGNAL(_fromUtf8("textChanged(QString)")), frmGeonam.imlistenfeldsuchen)
        QtCore.QObject.connect(self.btnLoeschen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGeonam.geonamClear)
        QtCore.QObject.connect(self.btnAnzeigen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGeonam.geonamZoom)
        QtCore.QObject.connect(self.lstGeonam, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), frmGeonam.AuswahlAktiviert)
        QtCore.QObject.connect(frmGeonam, QtCore.SIGNAL(_fromUtf8("destroyed()")), frmGeonam.grafikreturn)
        QtCore.QMetaObject.connectSlotsByName(frmGeonam)

    def retranslateUi(self, frmGeonam):
        frmGeonam.setWindowTitle(QtGui.QApplication.translate("frmGeonam", "Geonam Suche", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAnzeigen.setText(QtGui.QApplication.translate("frmGeonam", "in View darstellen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLoeschen.setText(QtGui.QApplication.translate("frmGeonam", "in View löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmGeonam", "Schließen", None, QtGui.QApplication.UnicodeUTF8))

