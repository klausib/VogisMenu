# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_gfz.ui'
#
# Created: Mon Feb 16 10:58:02 2015
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmGFZ(object):
    def setupUi(self, frmGFZ):
        frmGFZ.setObjectName(_fromUtf8("frmGFZ"))
        frmGFZ.resize(354, 595)
        self.btnAbbrechen = QtGui.QPushButton(frmGFZ)
        self.btnAbbrechen.setGeometry(QtCore.QRect(120, 530, 121, 31))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))
        self.groupBox = QtGui.QGroupBox(frmGFZ)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 311, 281))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btnGFZ = QtGui.QPushButton(self.groupBox)
        self.btnGFZ.setGeometry(QtCore.QRect(100, 232, 111, 31))
        self.btnGFZ.setObjectName(_fromUtf8("btnGFZ"))
        self.btGmdChoice = QtGui.QPushButton(self.groupBox)
        self.btGmdChoice.setGeometry(QtCore.QRect(210, 190, 31, 23))
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
        self.btGmdChoice.setObjectName(_fromUtf8("btGmdChoice"))
        self.lstGemeinden = QtGui.QListView(self.groupBox)
        self.lstGemeinden.setGeometry(QtCore.QRect(30, 20, 256, 161))
        self.lstGemeinden.setObjectName(_fromUtf8("lstGemeinden"))
        self.btnVorarlberg = QtGui.QPushButton(self.groupBox)
        self.btnVorarlberg.setGeometry(QtCore.QRect(50, 190, 111, 23))
        self.btnVorarlberg.setObjectName(_fromUtf8("btnVorarlberg"))
        self.groupBox_2 = QtGui.QGroupBox(frmGFZ)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 310, 311, 201))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btnGFZVIId = QtGui.QPushButton(self.groupBox_2)
        self.btnGFZVIId.setGeometry(QtCore.QRect(170, 100, 111, 23))
        self.btnGFZVIId.setObjectName(_fromUtf8("btnGFZVIId"))
        self.GfzBwv = QtGui.QRadioButton(self.groupBox_2)
        self.GfzBwv.setGeometry(QtCore.QRect(20, 100, 131, 18))
        self.GfzBwv.setChecked(True)
        self.GfzBwv.setObjectName(_fromUtf8("GfzBwv"))
        self.buttonGroup = QtGui.QButtonGroup(frmGFZ)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.GfzBwv)
        self.btnKompetenzgrenzen = QtGui.QPushButton(self.groupBox_2)
        self.btnKompetenzgrenzen.setGeometry(QtCore.QRect(70, 150, 161, 31))
        self.btnKompetenzgrenzen.setObjectName(_fromUtf8("btnKompetenzgrenzen"))

        self.retranslateUi(frmGFZ)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.closeEvent)
        QtCore.QObject.connect(self.btnGFZ, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeGemeinde)
        QtCore.QObject.connect(self.btGmdChoice, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.gmd_choice_toggled)
        QtCore.QObject.connect(self.lstGemeinden, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), frmGFZ.auswahlaenderung)
        QtCore.QObject.connect(self.btnGFZVIId, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeGFZWB)
        QtCore.QObject.connect(self.btnKompetenzgrenzen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.ladeKompetenzgrenzen)
        QtCore.QObject.connect(self.btnVorarlberg, QtCore.SIGNAL(_fromUtf8("clicked()")), frmGFZ.landesflaeche)
        QtCore.QMetaObject.connectSlotsByName(frmGFZ)

    def retranslateUi(self, frmGFZ):
        frmGFZ.setWindowTitle(QtGui.QApplication.translate("frmGFZ", "Gefahrenzonenpläne", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmGFZ", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmGFZ", "Wildbach- und Lawinenverbauung", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGFZ.setText(QtGui.QApplication.translate("frmGFZ", "GFZ laden", None, QtGui.QApplication.UnicodeUTF8))
        self.btGmdChoice.setText(QtGui.QApplication.translate("frmGFZ", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.btnVorarlberg.setText(QtGui.QApplication.translate("frmGFZ", "Landesfläche Vlbg.", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmGFZ", "Abt. VIId - Wasserwirtschaft", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGFZVIId.setText(QtGui.QApplication.translate("frmGFZ", "GFZ laden", None, QtGui.QApplication.UnicodeUTF8))
        self.GfzBwv.setText(QtGui.QApplication.translate("frmGFZ", "Gefahrenzonen BWV", None, QtGui.QApplication.UnicodeUTF8))
        self.btnKompetenzgrenzen.setText(QtGui.QApplication.translate("frmGFZ", "Betreuungsbereich WLV - BWV", None, QtGui.QApplication.UnicodeUTF8))

