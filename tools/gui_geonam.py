# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_geonam.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmGeonam(object):
    def setupUi(self, frmGeonam):
        frmGeonam.setObjectName("frmGeonam")
        frmGeonam.resize(334, 384)
        self.lstGeonam = QtWidgets.QListView(frmGeonam)
        self.lstGeonam.setGeometry(QtCore.QRect(20, 65, 291, 187))
        self.lstGeonam.setObjectName("lstGeonam")
        self.linSuche = QtWidgets.QLineEdit(frmGeonam)
        self.linSuche.setGeometry(QtCore.QRect(20, 40, 291, 20))
        self.linSuche.setObjectName("linSuche")
        self.btnAnzeigen = QtWidgets.QPushButton(frmGeonam)
        self.btnAnzeigen.setEnabled(False)
        self.btnAnzeigen.setGeometry(QtCore.QRect(110, 266, 121, 27))
        self.btnAnzeigen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnAnzeigen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnAnzeigen.setObjectName("btnAnzeigen")
        self.btnLoeschen = QtWidgets.QPushButton(frmGeonam)
        self.btnLoeschen.setGeometry(QtCore.QRect(110, 298, 121, 27))
        self.btnLoeschen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnLoeschen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnLoeschen.setObjectName("btnLoeschen")
        self.btnAbbrechen = QtWidgets.QPushButton(frmGeonam)
        self.btnAbbrechen.setGeometry(QtCore.QRect(110, 330, 121, 27))
        self.btnAbbrechen.setMinimumSize(QtCore.QSize(121, 27))
        self.btnAbbrechen.setMaximumSize(QtCore.QSize(121, 27))
        self.btnAbbrechen.setObjectName("btnAbbrechen")

        self.retranslateUi(frmGeonam)
        self.btnAbbrechen.clicked.connect(frmGeonam.abbrechen)
        self.linSuche.textChanged['QString'].connect(frmGeonam.imlistenfeldsuchen)
        self.btnLoeschen.clicked.connect(frmGeonam.geonamClear)
        self.btnAnzeigen.clicked.connect(frmGeonam.geonamZoom)
        self.lstGeonam.clicked['QModelIndex'].connect(frmGeonam.AuswahlAktiviert)
        frmGeonam.destroyed.connect(frmGeonam.grafikreturn)
        QtCore.QMetaObject.connectSlotsByName(frmGeonam)

    def retranslateUi(self, frmGeonam):
        _translate = QtCore.QCoreApplication.translate
        frmGeonam.setWindowTitle(_translate("frmGeonam", "Geonam Suche"))
        self.btnAnzeigen.setText(_translate("frmGeonam", "in View darstellen"))
        self.btnLoeschen.setText(_translate("frmGeonam", "in View löschen"))
        self.btnAbbrechen.setText(_translate("frmGeonam", "Schließen"))

