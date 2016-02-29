# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_raumplanung.ui'
#
# Created: Wed Jul 04 15:20:48 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmRaumplanung(object):
    def setupUi(self, frmRaumplanung):
        frmRaumplanung.setObjectName(_fromUtf8("frmRaumplanung"))
        frmRaumplanung.resize(308, 333)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmRaumplanung)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 270, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmRaumplanung)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(160, 270, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.layoutWidget = QtGui.QWidget(frmRaumplanung)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 20, 195, 231))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckGruenzone = QtGui.QCheckBox(self.layoutWidget)
        self.ckGruenzone.setEnabled(True)
        self.ckGruenzone.setObjectName(_fromUtf8("ckGruenzone"))
        self.ckButtons = QtGui.QButtonGroup(frmRaumplanung)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckGruenzone)
        self.verticalLayout.addWidget(self.ckGruenzone)
        self.ckEignungEkz = QtGui.QCheckBox(self.layoutWidget)
        self.ckEignungEkz.setEnabled(True)
        self.ckEignungEkz.setObjectName(_fromUtf8("ckEignungEkz"))
        self.ckButtons.addButton(self.ckEignungEkz)
        self.verticalLayout.addWidget(self.ckEignungEkz)
        self.ckEkz = QtGui.QCheckBox(self.layoutWidget)
        self.ckEkz.setEnabled(True)
        self.ckEkz.setObjectName(_fromUtf8("ckEkz"))
        self.ckButtons.addButton(self.ckEkz)
        self.verticalLayout.addWidget(self.ckEkz)
        self.ckBauflaechen = QtGui.QCheckBox(self.layoutWidget)
        self.ckBauflaechen.setEnabled(True)
        self.ckBauflaechen.setObjectName(_fromUtf8("ckBauflaechen"))
        self.ckButtons.addButton(self.ckBauflaechen)
        self.verticalLayout.addWidget(self.ckBauflaechen)
        self.ckSeveso = QtGui.QCheckBox(self.layoutWidget)
        self.ckSeveso.setEnabled(True)
        self.ckSeveso.setObjectName(_fromUtf8("ckSeveso"))
        self.ckButtons.addButton(self.ckSeveso)
        self.verticalLayout.addWidget(self.ckSeveso)
        self.ckFundzonen = QtGui.QCheckBox(self.layoutWidget)
        self.ckFundzonen.setEnabled(True)
        self.ckFundzonen.setObjectName(_fromUtf8("ckFundzonen"))
        self.ckButtons.addButton(self.ckFundzonen)
        self.verticalLayout.addWidget(self.ckFundzonen)
        self.ckRohstoffplan = QtGui.QCheckBox(self.layoutWidget)
        self.ckRohstoffplan.setEnabled(True)
        self.ckRohstoffplan.setObjectName(_fromUtf8("ckRohstoffplan"))
        self.ckButtons.addButton(self.ckRohstoffplan)
        self.verticalLayout.addWidget(self.ckRohstoffplan)
        self.ckBlauzone = QtGui.QCheckBox(self.layoutWidget)
        self.ckBlauzone.setEnabled(True)
        self.ckBlauzone.setObjectName(_fromUtf8("ckBlauzone"))
        self.ckButtons.addButton(self.ckBlauzone)
        self.verticalLayout.addWidget(self.ckBlauzone)
        self.ckWeisszone = QtGui.QCheckBox(self.layoutWidget)
        self.ckWeisszone.setEnabled(True)
        self.ckWeisszone.setObjectName(_fromUtf8("ckWeisszone"))
        self.ckButtons.addButton(self.ckWeisszone)
        self.verticalLayout.addWidget(self.ckWeisszone)
        self.ckMauerinventar = QtGui.QCheckBox(self.layoutWidget)
        self.ckMauerinventar.setEnabled(True)
        self.ckMauerinventar.setObjectName(_fromUtf8("ckMauerinventar"))
        self.ckButtons.addButton(self.ckMauerinventar)
        self.verticalLayout.addWidget(self.ckMauerinventar)

        self.retranslateUi(frmRaumplanung)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmRaumplanung.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmRaumplanung.close)
        QtCore.QMetaObject.connectSlotsByName(frmRaumplanung)

    def retranslateUi(self, frmRaumplanung):
        frmRaumplanung.setWindowTitle(QtGui.QApplication.translate("frmRaumplanung", "Raumplanung", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmRaumplanung", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmRaumplanung", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckGruenzone.setText(QtGui.QApplication.translate("frmRaumplanung", "Grünzone", None, QtGui.QApplication.UnicodeUTF8))
        self.ckEignungEkz.setText(QtGui.QApplication.translate("frmRaumplanung", "Eignungszonen für Einkaufszentren", None, QtGui.QApplication.UnicodeUTF8))
        self.ckEkz.setText(QtGui.QApplication.translate("frmRaumplanung", "Einkaufszentren", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBauflaechen.setText(QtGui.QApplication.translate("frmRaumplanung", "Bauflächen-Nutzung", None, QtGui.QApplication.UnicodeUTF8))
        self.ckSeveso.setText(QtGui.QApplication.translate("frmRaumplanung", "Seveso II Richtlinie", None, QtGui.QApplication.UnicodeUTF8))
        self.ckFundzonen.setText(QtGui.QApplication.translate("frmRaumplanung", "Archäologische Fundzonen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckRohstoffplan.setText(QtGui.QApplication.translate("frmRaumplanung", "Rohstoffplan", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBlauzone.setText(QtGui.QApplication.translate("frmRaumplanung", "Blauzone", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWeisszone.setText(QtGui.QApplication.translate("frmRaumplanung", "Weißzone", None, QtGui.QApplication.UnicodeUTF8))
        self.ckMauerinventar.setText(QtGui.QApplication.translate("frmRaumplanung", "Mauerinventar", None, QtGui.QApplication.UnicodeUTF8))

