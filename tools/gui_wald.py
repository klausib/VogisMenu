# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_wald.ui'
#
# Created: Thu Nov 06 10:26:22 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmWald(object):
    def setupUi(self, frmWald):
        frmWald.setObjectName(_fromUtf8("frmWald"))
        frmWald.resize(285, 307)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmWald)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(30, 250, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmWald)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(150, 250, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.layoutWidget = QtGui.QWidget(frmWald)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 20, 219, 201))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckAuwald = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckAuwald.setFont(font)
        self.ckAuwald.setObjectName(_fromUtf8("ckAuwald"))
        self.ckButtons = QtGui.QButtonGroup(frmWald)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckAuwald)
        self.verticalLayout.addWidget(self.ckAuwald)
        self.ckSaatgut = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckSaatgut.setFont(font)
        self.ckSaatgut.setObjectName(_fromUtf8("ckSaatgut"))
        self.ckButtons.addButton(self.ckSaatgut)
        self.verticalLayout.addWidget(self.ckSaatgut)
        self.ckUfergehoelz = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckUfergehoelz.setFont(font)
        self.ckUfergehoelz.setObjectName(_fromUtf8("ckUfergehoelz"))
        self.ckButtons.addButton(self.ckUfergehoelz)
        self.verticalLayout.addWidget(self.ckUfergehoelz)
        self.ckWaldklassifizierung = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckWaldklassifizierung.setFont(font)
        self.ckWaldklassifizierung.setObjectName(_fromUtf8("ckWaldklassifizierung"))
        self.ckButtons.addButton(self.ckWaldklassifizierung)
        self.verticalLayout.addWidget(self.ckWaldklassifizierung)
        self.ckWaldflaecheOek = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckWaldflaecheOek.setFont(font)
        self.ckWaldflaecheOek.setObjectName(_fromUtf8("ckWaldflaecheOek"))
        self.ckButtons.addButton(self.ckWaldflaecheOek)
        self.verticalLayout.addWidget(self.ckWaldflaecheOek)
        self.ckWaldentwicklungsplan = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckWaldentwicklungsplan.setFont(font)
        self.ckWaldentwicklungsplan.setObjectName(_fromUtf8("ckWaldentwicklungsplan"))
        self.ckButtons.addButton(self.ckWaldentwicklungsplan)
        self.verticalLayout.addWidget(self.ckWaldentwicklungsplan)
        self.ckWaldregionen = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckWaldregionen.setFont(font)
        self.ckWaldregionen.setObjectName(_fromUtf8("ckWaldregionen"))
        self.ckButtons.addButton(self.ckWaldregionen)
        self.verticalLayout.addWidget(self.ckWaldregionen)
        self.ckWaldkarte = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ckWaldkarte.setFont(font)
        self.ckWaldkarte.setObjectName(_fromUtf8("ckWaldkarte"))
        self.ckButtons.addButton(self.ckWaldkarte)
        self.verticalLayout.addWidget(self.ckWaldkarte)

        self.retranslateUi(frmWald)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmWald.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmWald.close)
        QtCore.QMetaObject.connectSlotsByName(frmWald)

    def retranslateUi(self, frmWald):
        frmWald.setWindowTitle(QtGui.QApplication.translate("frmWald", "Wald", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmWald", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmWald", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckAuwald.setText(QtGui.QApplication.translate("frmWald", "Auwald", None, QtGui.QApplication.UnicodeUTF8))
        self.ckSaatgut.setText(QtGui.QApplication.translate("frmWald", "Saatgut", None, QtGui.QApplication.UnicodeUTF8))
        self.ckUfergehoelz.setText(QtGui.QApplication.translate("frmWald", "Ufergehölz", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWaldklassifizierung.setText(QtGui.QApplication.translate("frmWald", "Waldklassifizierung aus Orthofotos 2001", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWaldflaecheOek.setText(QtGui.QApplication.translate("frmWald", "Waldfläche aus ÖK50", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWaldentwicklungsplan.setText(QtGui.QApplication.translate("frmWald", "Waldentwicklungsplan", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWaldregionen.setText(QtGui.QApplication.translate("frmWald", "Waldregionen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckWaldkarte.setText(QtGui.QApplication.translate("frmWald", "Waldkarte", None, QtGui.QApplication.UnicodeUTF8))

