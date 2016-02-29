# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_landnutzung.ui'
#
# Created: Thu Jun 28 13:51:10 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmLandnutzung(object):
    def setupUi(self, frmLandnutzung):
        frmLandnutzung.setObjectName(_fromUtf8("frmLandnutzung"))
        frmLandnutzung.resize(428, 146)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmLandnutzung)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(80, 100, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmLandnutzung)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(220, 100, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.layoutWidget = QtGui.QWidget(frmLandnutzung)
        self.layoutWidget.setGeometry(QtCore.QRect(40, 20, 347, 61))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckLnVlbg = QtGui.QCheckBox(self.layoutWidget)
        self.ckLnVlbg.setEnabled(False)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckLnVlbg.setFont(font)
        self.ckLnVlbg.setObjectName(_fromUtf8("ckLnVlbg"))
        self.ckButtons = QtGui.QButtonGroup(frmLandnutzung)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckLnVlbg)
        self.verticalLayout.addWidget(self.ckLnVlbg)
        self.ckLnRheintal = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.ckLnRheintal.setFont(font)
        self.ckLnRheintal.setObjectName(_fromUtf8("ckLnRheintal"))
        self.ckButtons.addButton(self.ckLnRheintal)
        self.verticalLayout.addWidget(self.ckLnRheintal)

        self.retranslateUi(frmLandnutzung)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmLandnutzung.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmLandnutzung.close)
        QtCore.QMetaObject.connectSlotsByName(frmLandnutzung)

    def retranslateUi(self, frmLandnutzung):
        frmLandnutzung.setWindowTitle(QtGui.QApplication.translate("frmLandnutzung", "Landnutzung", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmLandnutzung", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmLandnutzung", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.ckLnVlbg.setText(QtGui.QApplication.translate("frmLandnutzung", "Landnutzungsklassifizierung aus Orthophotos 2001/2002", None, QtGui.QApplication.UnicodeUTF8))
        self.ckLnRheintal.setText(QtGui.QApplication.translate("frmLandnutzung", "Landnutzungskartierung Rheintal 2004/2005", None, QtGui.QApplication.UnicodeUTF8))

