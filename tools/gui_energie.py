# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_energie.ui'
#
# Created: Tue Jun 26 15:55:51 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmEnergie(object):
    def setupUi(self, frmEnergie):
        frmEnergie.setObjectName(_fromUtf8("frmEnergie"))
        frmEnergie.resize(248, 155)
        self.ButtonEnergieOk = QtGui.QPushButton(frmEnergie)
        self.ButtonEnergieOk.setGeometry(QtCore.QRect(10, 110, 101, 23))
        self.ButtonEnergieOk.setObjectName(_fromUtf8("ButtonEnergieOk"))
        self.ButtonEnergieCancel = QtGui.QPushButton(frmEnergie)
        self.ButtonEnergieCancel.setGeometry(QtCore.QRect(130, 110, 101, 23))
        self.ButtonEnergieCancel.setObjectName(_fromUtf8("ButtonEnergieCancel"))
        self.frame = QtGui.QFrame(frmEnergie)
        self.frame.setGeometry(QtCore.QRect(10, 10, 221, 91))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.layoutWidget = QtGui.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 185, 51))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox.setFont(font)
        self.checkBox.setChecked(True)
        self.checkBox.setObjectName(_fromUtf8("checkBox"))
        self.checkButtonsGroup = QtGui.QButtonGroup(frmEnergie)
        self.checkButtonsGroup.setObjectName(_fromUtf8("checkButtonsGroup"))
        self.checkButtonsGroup.addButton(self.checkBox)
        self.verticalLayout.addWidget(self.checkBox)
        self.checkBox_2 = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.checkButtonsGroup.addButton(self.checkBox_2)
        self.verticalLayout.addWidget(self.checkBox_2)

        self.retranslateUi(frmEnergie)
        QtCore.QObject.connect(self.ButtonEnergieOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmEnergie.accept)
        QtCore.QObject.connect(self.ButtonEnergieCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmEnergie.close)
        QtCore.QMetaObject.connectSlotsByName(frmEnergie)

    def retranslateUi(self, frmEnergie):
        frmEnergie.setWindowTitle(QtGui.QApplication.translate("frmEnergie", "Energieversorgung", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonEnergieOk.setText(QtGui.QApplication.translate("frmEnergie", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonEnergieCancel.setText(QtGui.QApplication.translate("frmEnergie", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("frmEnergie", "Energieversorgung: GAS", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("frmEnergie", "Energieversorgung: STROM", None, QtGui.QApplication.UnicodeUTF8))

