# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_abfall.ui'
#
# Created: Tue Jun 26 14:33:44 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAbfall(object):
    def setupUi(self, frmAbfall):
        frmAbfall.setObjectName(_fromUtf8("frmAbfall"))
        frmAbfall.resize(206, 175)
        self.ButtonAbfallOk = QtGui.QPushButton(frmAbfall)
        self.ButtonAbfallOk.setGeometry(QtCore.QRect(40, 110, 121, 23))
        self.ButtonAbfallOk.setObjectName(_fromUtf8("ButtonAbfallOk"))
        self.ButtonAbfallCancel = QtGui.QPushButton(frmAbfall)
        self.ButtonAbfallCancel.setGeometry(QtCore.QRect(40, 140, 121, 23))
        self.ButtonAbfallCancel.setObjectName(_fromUtf8("ButtonAbfallCancel"))
        self.frame = QtGui.QFrame(frmAbfall)
        self.frame.setGeometry(QtCore.QRect(10, 10, 181, 91))
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName(_fromUtf8("frame"))
        self.layoutWidget = QtGui.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 144, 51))
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
        self.checkButtonsGroup = QtGui.QButtonGroup(frmAbfall)
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

        self.retranslateUi(frmAbfall)
        QtCore.QObject.connect(self.ButtonAbfallOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAbfall.accept)
        QtCore.QObject.connect(self.ButtonAbfallCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAbfall.close)
        QtCore.QMetaObject.connectSlotsByName(frmAbfall)

    def retranslateUi(self, frmAbfall):
        frmAbfall.setWindowTitle(QtGui.QApplication.translate("frmAbfall", "Abfallwirtschaft", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonAbfallOk.setText(QtGui.QApplication.translate("frmAbfall", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonAbfallCancel.setText(QtGui.QApplication.translate("frmAbfall", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox.setText(QtGui.QApplication.translate("frmAbfall", "Deponien", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("frmAbfall", "Altstandorte", None, QtGui.QApplication.UnicodeUTF8))

