# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_siedlungsgebiete.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmSiedlungsgebiete(object):
    def setupUi(self, frmSiedlungsgebiete):
        frmSiedlungsgebiete.setObjectName("frmSiedlungsgebiete")
        frmSiedlungsgebiete.resize(273, 298)
        self.ButtonBlattschnitteOk = QtWidgets.QPushButton(frmSiedlungsgebiete)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(20, 220, 101, 23))
        self.ButtonBlattschnitteOk.setObjectName("ButtonBlattschnitteOk")
        self.ButtonBlattschnitteCancel = QtWidgets.QPushButton(frmSiedlungsgebiete)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(150, 220, 101, 23))
        self.ButtonBlattschnitteCancel.setObjectName("ButtonBlattschnitteCancel")
        self.groupBox = QtWidgets.QGroupBox(frmSiedlungsgebiete)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 231, 181))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 30, 195, 71))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckSiedlungsgebiete = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckSiedlungsgebiete.setEnabled(True)
        self.ckSiedlungsgebiete.setObjectName("ckSiedlungsgebiete")
        self.ckButtons = QtWidgets.QButtonGroup(frmSiedlungsgebiete)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.setExclusive(False)
        self.ckButtons.addButton(self.ckSiedlungsgebiete)
        self.verticalLayout.addWidget(self.ckSiedlungsgebiete)
        self.ckSiedlungsentwicklung = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckSiedlungsentwicklung.setEnabled(True)
        self.ckSiedlungsentwicklung.setObjectName("ckSiedlungsentwicklung")
        self.ckButtons.addButton(self.ckSiedlungsentwicklung)
        self.verticalLayout.addWidget(self.ckSiedlungsentwicklung)

        self.retranslateUi(frmSiedlungsgebiete)
        self.ButtonBlattschnitteOk.clicked.connect(frmSiedlungsgebiete.accept)
        self.ButtonBlattschnitteCancel.clicked.connect(frmSiedlungsgebiete.close)
        QtCore.QMetaObject.connectSlotsByName(frmSiedlungsgebiete)

    def retranslateUi(self, frmSiedlungsgebiete):
        _translate = QtCore.QCoreApplication.translate
        frmSiedlungsgebiete.setWindowTitle(_translate("frmSiedlungsgebiete", "Siedlungen"))
        self.ButtonBlattschnitteOk.setText(_translate("frmSiedlungsgebiete", "Themen laden"))
        self.ButtonBlattschnitteCancel.setText(_translate("frmSiedlungsgebiete", "Schließen"))
        self.groupBox.setTitle(_translate("frmSiedlungsgebiete", "Vorarlberg"))
        self.ckSiedlungsgebiete.setText(_translate("frmSiedlungsgebiete", "Siedlungsgebiete mit Einwohnern"))
        self.ckSiedlungsentwicklung.setText(_translate("frmSiedlungsgebiete", "Siedlungsentwicklung Rheintal"))

