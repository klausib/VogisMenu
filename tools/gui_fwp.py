# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_fwp.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmFWP(object):
    def setupUi(self, frmFWP):
        frmFWP.setObjectName("frmFWP")
        frmFWP.resize(297, 419)
        self.lstGemeinden = QtWidgets.QListView(frmFWP)
        self.lstGemeinden.setGeometry(QtCore.QRect(20, 10, 256, 191))
        self.lstGemeinden.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.lstGemeinden.setObjectName("lstGemeinden")
        self.btnFWP = QtWidgets.QPushButton(frmFWP)
        self.btnFWP.setGeometry(QtCore.QRect(90, 270, 111, 31))
        self.btnFWP.setObjectName("btnFWP")
        self.btnBZ = QtWidgets.QPushButton(frmFWP)
        self.btnBZ.setGeometry(QtCore.QRect(90, 310, 111, 31))
        self.btnBZ.setObjectName("btnBZ")
        self.btnAbbrechen = QtWidgets.QPushButton(frmFWP)
        self.btnAbbrechen.setGeometry(QtCore.QRect(90, 380, 111, 23))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.btGmdChoice = QtWidgets.QPushButton(frmFWP)
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
        self.btGmdChoice.setObjectName("btGmdChoice")
        self.btnVorarlberg = QtWidgets.QPushButton(frmFWP)
        self.btnVorarlberg.setGeometry(QtCore.QRect(70, 210, 111, 23))
        self.btnVorarlberg.setObjectName("btnVorarlberg")

        self.retranslateUi(frmFWP)
        self.btnAbbrechen.clicked.connect(frmFWP.closeEvent)
        self.btGmdChoice.clicked.connect(frmFWP.gmd_choice_toggled)
        self.btnFWP.clicked.connect(frmFWP.ladeGemeinde)
        self.lstGemeinden.clicked['QModelIndex'].connect(frmFWP.auswahlaenderung)
        self.btnBZ.clicked.connect(frmFWP.ladeBZ)
        self.btnVorarlberg.clicked.connect(frmFWP.landesflaeche)
        QtCore.QMetaObject.connectSlotsByName(frmFWP)

    def retranslateUi(self, frmFWP):
        _translate = QtCore.QCoreApplication.translate
        frmFWP.setWindowTitle(_translate("frmFWP", "Flächenwidmung"))
        self.btnFWP.setText(_translate("frmFWP", "FWP laden"))
        self.btnBZ.setText(_translate("frmFWP", "Beschränkungszonen"))
        self.btnAbbrechen.setText(_translate("frmFWP", "Schließen"))
        self.btGmdChoice.setText(_translate("frmFWP", "+"))
        self.btnVorarlberg.setText(_translate("frmFWP", "Landesfläche Vlbg."))

