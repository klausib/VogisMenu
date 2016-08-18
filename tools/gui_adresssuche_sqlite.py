# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_adresssuche_sqlite.ui'
#
# Created: Tue Jun 28 14:54:39 2016
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmAdresssuche(object):
    def setupUi(self, frmAdresssuche):
        frmAdresssuche.setObjectName(_fromUtf8("frmAdresssuche"))
        frmAdresssuche.resize(671, 416)
        self.schliessen = QtGui.QPushButton(frmAdresssuche)
        self.schliessen.setGeometry(QtCore.QRect(450, 330, 101, 31))
        self.schliessen.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.schliessen.setAutoDefault(False)
        self.schliessen.setObjectName(_fromUtf8("schliessen"))
        self.groupBox = QtGui.QGroupBox(frmAdresssuche)
        self.groupBox.setGeometry(QtCore.QRect(20, 300, 361, 91))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.layoutWidget = QtGui.QWidget(self.groupBox)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 157, 51))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.checkBox_3 = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_3.setFont(font)
        self.checkBox_3.setChecked(True)
        self.checkBox_3.setObjectName(_fromUtf8("checkBox_3"))
        self.buttonGroup = QtGui.QButtonGroup(frmAdresssuche)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.checkBox_3)
        self.verticalLayout.addWidget(self.checkBox_3)
        self.checkBox_2 = QtGui.QCheckBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.checkBox_2.setFont(font)
        self.checkBox_2.setObjectName(_fromUtf8("checkBox_2"))
        self.buttonGroup.addButton(self.checkBox_2)
        self.verticalLayout.addWidget(self.checkBox_2)
        self.ButtonAdressenOk = QtGui.QPushButton(self.groupBox)
        self.ButtonAdressenOk.setGeometry(QtCore.QRect(210, 30, 121, 31))
        self.ButtonAdressenOk.setAutoDefault(False)
        self.ButtonAdressenOk.setObjectName(_fromUtf8("ButtonAdressenOk"))
        self.groupBox_2 = QtGui.QGroupBox(frmAdresssuche)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 10, 621, 281))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.lstNummer = QtGui.QListView(self.groupBox_2)
        self.lstNummer.setGeometry(QtCore.QRect(430, 40, 150, 192))
        self.lstNummer.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.lstNummer.setObjectName(_fromUtf8("lstNummer"))
        self.lstGemeinde = QtGui.QListView(self.groupBox_2)
        self.lstGemeinde.setGeometry(QtCore.QRect(20, 80, 150, 151))
        self.lstGemeinde.setObjectName(_fromUtf8("lstGemeinde"))
        self.laden = QtGui.QPushButton(self.groupBox_2)
        self.laden.setGeometry(QtCore.QRect(190, 240, 111, 31))
        self.laden.setAutoDefault(False)
        self.laden.setObjectName(_fromUtf8("laden"))
        self.pushButton = QtGui.QPushButton(self.groupBox_2)
        self.pushButton.setGeometry(QtCore.QRect(310, 240, 111, 31))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.lstStrasse = QtGui.QListView(self.groupBox_2)
        self.lstStrasse.setGeometry(QtCore.QRect(200, 80, 201, 151))
        self.lstStrasse.setObjectName(_fromUtf8("lstStrasse"))
        self.groupBox_3 = QtGui.QGroupBox(self.groupBox_2)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 401, 51))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.leStrasse = QtGui.QLineEdit(self.groupBox_3)
        self.leStrasse.setGeometry(QtCore.QRect(10, 20, 381, 21))
        self.leStrasse.setObjectName(_fromUtf8("leStrasse"))

        self.retranslateUi(frmAdresssuche)
        QtCore.QObject.connect(self.laden, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAdresssuche.accept)
        QtCore.QObject.connect(self.schliessen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAdresssuche.closeEvent)
        QtCore.QObject.connect(self.lstNummer, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), frmAdresssuche.lstNummerKlicked)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAdresssuche.adrClear)
        QtCore.QObject.connect(self.ButtonAdressenOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmAdresssuche.themenLaden)
        QtCore.QObject.connect(self.leStrasse, QtCore.SIGNAL(_fromUtf8("returnPressed()")), frmAdresssuche.strassensuche)
        QtCore.QMetaObject.connectSlotsByName(frmAdresssuche)

    def retranslateUi(self, frmAdresssuche):
        frmAdresssuche.setWindowTitle(QtGui.QApplication.translate("frmAdresssuche", "Adresssuche", None, QtGui.QApplication.UnicodeUTF8))
        self.schliessen.setText(QtGui.QApplication.translate("frmAdresssuche", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmAdresssuche", "Adresslayer laden", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_3.setText(QtGui.QApplication.translate("frmAdresssuche", "Adressen Gemeinde", None, QtGui.QApplication.UnicodeUTF8))
        self.checkBox_2.setText(QtGui.QApplication.translate("frmAdresssuche", "Adressen Landesfläche", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonAdressenOk.setText(QtGui.QApplication.translate("frmAdresssuche", "Thema laden", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmAdresssuche", "Adressen suchen und anzeigen", None, QtGui.QApplication.UnicodeUTF8))
        self.laden.setText(QtGui.QApplication.translate("frmAdresssuche", "in View darstellen", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton.setText(QtGui.QApplication.translate("frmAdresssuche", "in View löschen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmAdresssuche", "Strassensuche Landesweit", None, QtGui.QApplication.UnicodeUTF8))

