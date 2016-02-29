# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_siedlungsgebiete.ui'
#
# Created: Tue Jan 14 16:41:44 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmSiedlungsgebiete(object):
    def setupUi(self, frmSiedlungsgebiete):
        frmSiedlungsgebiete.setObjectName(_fromUtf8("frmSiedlungsgebiete"))
        frmSiedlungsgebiete.resize(273, 298)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmSiedlungsgebiete)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(20, 220, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmSiedlungsgebiete)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(150, 220, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.groupBox = QtGui.QGroupBox(frmSiedlungsgebiete)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 231, 181))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 195, 71))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckSiedlungsgebiete = QtGui.QCheckBox(self.layoutWidget)
        self.ckSiedlungsgebiete.setEnabled(True)
        self.ckSiedlungsgebiete.setObjectName(_fromUtf8("ckSiedlungsgebiete"))
        self.ckButtons = QtGui.QButtonGroup(frmSiedlungsgebiete)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckSiedlungsgebiete)
        self.verticalLayout.addWidget(self.ckSiedlungsgebiete)
        self.ckSiedlungsentwicklung = QtGui.QCheckBox(self.layoutWidget)
        self.ckSiedlungsentwicklung.setEnabled(True)
        self.ckSiedlungsentwicklung.setObjectName(_fromUtf8("ckSiedlungsentwicklung"))
        self.ckButtons.addButton(self.ckSiedlungsentwicklung)
        self.verticalLayout.addWidget(self.ckSiedlungsentwicklung)

        self.retranslateUi(frmSiedlungsgebiete)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmSiedlungsgebiete.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmSiedlungsgebiete.close)
        QtCore.QMetaObject.connectSlotsByName(frmSiedlungsgebiete)

    def retranslateUi(self, frmSiedlungsgebiete):
        frmSiedlungsgebiete.setWindowTitle(QtGui.QApplication.translate("frmSiedlungsgebiete", "Siedlungen", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmSiedlungsgebiete", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmSiedlungsgebiete", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmSiedlungsgebiete", "Vorarlberg", None, QtGui.QApplication.UnicodeUTF8))
        self.ckSiedlungsgebiete.setText(QtGui.QApplication.translate("frmSiedlungsgebiete", "Siedlungsgebiete mit Einwohnern", None, QtGui.QApplication.UnicodeUTF8))
        self.ckSiedlungsentwicklung.setText(QtGui.QApplication.translate("frmSiedlungsgebiete", "Siedlungsentwicklung Rheintal", None, QtGui.QApplication.UnicodeUTF8))

