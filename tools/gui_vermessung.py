# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_vermessung.ui'
#
# Created: Tue Dec 11 16:16:57 2012
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmVermessung(object):
    def setupUi(self, frmVermessung):
        frmVermessung.setObjectName(_fromUtf8("frmVermessung"))
        frmVermessung.resize(578, 345)
        self.ButtonBlattschnitteOk = QtGui.QPushButton(frmVermessung)
        self.ButtonBlattschnitteOk.setEnabled(True)
        self.ButtonBlattschnitteOk.setGeometry(QtCore.QRect(120, 300, 111, 31))
        self.ButtonBlattschnitteOk.setObjectName(_fromUtf8("ButtonBlattschnitteOk"))
        self.ButtonBlattschnitteCancel = QtGui.QPushButton(frmVermessung)
        self.ButtonBlattschnitteCancel.setEnabled(True)
        self.ButtonBlattschnitteCancel.setGeometry(QtCore.QRect(330, 300, 111, 31))
        self.ButtonBlattschnitteCancel.setObjectName(_fromUtf8("ButtonBlattschnitteCancel"))
        self.progressBar = QtGui.QProgressBar(frmVermessung)
        self.progressBar.setGeometry(QtCore.QRect(20, 270, 551, 23))
        self.progressBar.setProperty(_fromUtf8("value"), 0)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.groupBox_3 = QtGui.QGroupBox(frmVermessung)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 20, 311, 231))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setCheckable(False)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.lstPolgem = QtGui.QListView(self.groupBox_3)
        self.lstPolgem.setGeometry(QtCore.QRect(10, 20, 131, 191))
        self.lstPolgem.setLocale(QtCore.QLocale(QtCore.QLocale.German, QtCore.QLocale.Austria))
        self.lstPolgem.setEditTriggers(QtGui.QAbstractItemView.CurrentChanged|QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed)
        self.lstPolgem.setTabKeyNavigation(False)
        self.lstPolgem.setObjectName(_fromUtf8("lstPolgem"))
        self.layoutWidget = QtGui.QWidget(self.groupBox_3)
        self.layoutWidget.setGeometry(QtCore.QRect(150, 20, 161, 101))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.ckPolygonpunkte = QtGui.QCheckBox(self.layoutWidget)
        self.ckPolygonpunkte.setChecked(False)
        self.ckPolygonpunkte.setObjectName(_fromUtf8("ckPolygonpunkte"))
        self.buttonGroup = QtGui.QButtonGroup(frmVermessung)
        self.buttonGroup.setObjectName(_fromUtf8("buttonGroup"))
        self.buttonGroup.addButton(self.ckPolygonpunkte)
        self.verticalLayout.addWidget(self.ckPolygonpunkte)
        self.ckNivellement = QtGui.QCheckBox(self.layoutWidget)
        self.ckNivellement.setChecked(False)
        self.ckNivellement.setObjectName(_fromUtf8("ckNivellement"))
        self.buttonGroup.addButton(self.ckNivellement)
        self.verticalLayout.addWidget(self.ckNivellement)
        self.ckTriangulierungspunkte = QtGui.QCheckBox(self.layoutWidget)
        self.ckTriangulierungspunkte.setChecked(False)
        self.ckTriangulierungspunkte.setObjectName(_fromUtf8("ckTriangulierungspunkte"))
        self.buttonGroup.addButton(self.ckTriangulierungspunkte)
        self.verticalLayout.addWidget(self.ckTriangulierungspunkte)
        self.ckEinschaltpunkte = QtGui.QCheckBox(self.layoutWidget)
        self.ckEinschaltpunkte.setChecked(False)
        self.ckEinschaltpunkte.setObjectName(_fromUtf8("ckEinschaltpunkte"))
        self.buttonGroup.addButton(self.ckEinschaltpunkte)
        self.verticalLayout.addWidget(self.ckEinschaltpunkte)
        self.groupBox = QtGui.QGroupBox(self.groupBox_3)
        self.groupBox.setGeometry(QtCore.QRect(150, 160, 151, 61))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btGmdChoice = QtGui.QPushButton(self.groupBox)
        self.btGmdChoice.setGeometry(QtCore.QRect(60, 20, 31, 31))
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
        self.groupBox_4 = QtGui.QGroupBox(frmVermessung)
        self.groupBox_4.setGeometry(QtCore.QRect(330, 20, 221, 231))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.groupBox_4.setFont(font)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.layoutWidget1 = QtGui.QWidget(self.groupBox_4)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 196, 131))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.ckIllwerke = QtGui.QCheckBox(self.layoutWidget1)
        self.ckIllwerke.setChecked(False)
        self.ckIllwerke.setObjectName(_fromUtf8("ckIllwerke"))
        self.buttonGroup.addButton(self.ckIllwerke)
        self.verticalLayout_2.addWidget(self.ckIllwerke)
        self.ckNaniv = QtGui.QCheckBox(self.layoutWidget1)
        self.ckNaniv.setChecked(False)
        self.ckNaniv.setObjectName(_fromUtf8("ckNaniv"))
        self.buttonGroup.addButton(self.ckNaniv)
        self.verticalLayout_2.addWidget(self.ckNaniv)
        self.ckOniv = QtGui.QCheckBox(self.layoutWidget1)
        self.ckOniv.setChecked(False)
        self.ckOniv.setObjectName(_fromUtf8("ckOniv"))
        self.buttonGroup.addButton(self.ckOniv)
        self.verticalLayout_2.addWidget(self.ckOniv)
        self.ckLva = QtGui.QCheckBox(self.layoutWidget1)
        self.ckLva.setChecked(False)
        self.ckLva.setObjectName(_fromUtf8("ckLva"))
        self.buttonGroup.addButton(self.ckLva)
        self.verticalLayout_2.addWidget(self.ckLva)
        self.ckUmrisspolygone = QtGui.QCheckBox(self.layoutWidget1)
        self.ckUmrisspolygone.setChecked(False)
        self.ckUmrisspolygone.setObjectName(_fromUtf8("ckUmrisspolygone"))
        self.buttonGroup.addButton(self.ckUmrisspolygone)
        self.verticalLayout_2.addWidget(self.ckUmrisspolygone)
        self.groupBox_2 = QtGui.QGroupBox(self.groupBox_4)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 160, 191, 61))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.btTopo = QtGui.QPushButton(self.groupBox_2)
        self.btTopo.setGeometry(QtCore.QRect(70, 20, 31, 31))
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
        self.btTopo.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btTopo.setFont(font)
        self.btTopo.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btTopo.setCheckable(True)
        self.btTopo.setChecked(False)
        self.btTopo.setObjectName(_fromUtf8("btTopo"))

        self.retranslateUi(frmVermessung)
        QtCore.QObject.connect(self.ButtonBlattschnitteOk, QtCore.SIGNAL(_fromUtf8("clicked()")), frmVermessung.accept)
        QtCore.QObject.connect(self.ButtonBlattschnitteCancel, QtCore.SIGNAL(_fromUtf8("clicked()")), frmVermessung.closeEvent)
        QtCore.QObject.connect(self.btGmdChoice, QtCore.SIGNAL(_fromUtf8("clicked()")), frmVermessung.gmd_choice_toggled)
        QtCore.QObject.connect(self.lstPolgem, QtCore.SIGNAL(_fromUtf8("clicked(QModelIndex)")), frmVermessung.auswahlaenderung)
        QtCore.QObject.connect(self.btTopo, QtCore.SIGNAL(_fromUtf8("clicked()")), frmVermessung.topo_choice_toggled)
        QtCore.QObject.connect(self.ckUmrisspolygone, QtCore.SIGNAL(_fromUtf8("clicked()")), frmVermessung.uncheck)
        QtCore.QMetaObject.connectSlotsByName(frmVermessung)

    def retranslateUi(self, frmVermessung):
        frmVermessung.setWindowTitle(QtGui.QApplication.translate("frmVermessung", "Vermessung", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteOk.setText(QtGui.QApplication.translate("frmVermessung", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.ButtonBlattschnitteCancel.setText(QtGui.QApplication.translate("frmVermessung", "Schließen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_3.setTitle(QtGui.QApplication.translate("frmVermessung", "Datenauswahl - Gemeinde", None, QtGui.QApplication.UnicodeUTF8))
        self.ckPolygonpunkte.setText(QtGui.QApplication.translate("frmVermessung", "VKW Polygonpunkte", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNivellement.setText(QtGui.QApplication.translate("frmVermessung", "Nivellement (BEV)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckTriangulierungspunkte.setText(QtGui.QApplication.translate("frmVermessung", "Triangulierungspunkte (BEV)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckEinschaltpunkte.setText(QtGui.QApplication.translate("frmVermessung", "Einschaltpunkte (BEV)", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmVermessung", "Gemeinde auswählen", None, QtGui.QApplication.UnicodeUTF8))
        self.btGmdChoice.setText(QtGui.QApplication.translate("frmVermessung", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_4.setTitle(QtGui.QApplication.translate("frmVermessung", "Datenauswahl - Landesfläche", None, QtGui.QApplication.UnicodeUTF8))
        self.ckIllwerke.setText(QtGui.QApplication.translate("frmVermessung", "Illwerke Flusssteine (Landesfläche)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNaniv.setText(QtGui.QApplication.translate("frmVermessung", "Nachgereihtes Nivellement", None, QtGui.QApplication.UnicodeUTF8))
        self.ckOniv.setText(QtGui.QApplication.translate("frmVermessung", "Ortsnivellements", None, QtGui.QApplication.UnicodeUTF8))
        self.ckLva.setText(QtGui.QApplication.translate("frmVermessung", "LVG Punkte (Landesfläche)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckUmrisspolygone.setText(QtGui.QApplication.translate("frmVermessung", "LVG Vermessungen: Umrisspolygone", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox_2.setTitle(QtGui.QApplication.translate("frmVermessung", "LVA Punkte: Topografie abfragen", None, QtGui.QApplication.UnicodeUTF8))
        self.btTopo.setText(QtGui.QApplication.translate("frmVermessung", "+", None, QtGui.QApplication.UnicodeUTF8))

