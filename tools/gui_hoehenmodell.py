# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_hoehenmodell.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmHoehenmodell(object):
    def setupUi(self, frmHoehenmodell):
        frmHoehenmodell.setObjectName("frmHoehenmodell")
        frmHoehenmodell.resize(326, 705)
        self.btnAbbrechen = QtWidgets.QPushButton(frmHoehenmodell)
        self.btnAbbrechen.setGeometry(QtCore.QRect(170, 660, 81, 31))
        self.btnAbbrechen.setObjectName("btnAbbrechen")
        self.btnLaden = QtWidgets.QPushButton(frmHoehenmodell)
        self.btnLaden.setGeometry(QtCore.QRect(50, 660, 81, 31))
        self.btnLaden.setObjectName("btnLaden")
        self.toolBox = QtWidgets.QToolBox(frmHoehenmodell)
        self.toolBox.setGeometry(QtCore.QRect(10, 20, 311, 451))
        self.toolBox.setFrameShape(QtWidgets.QFrame.Panel)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox.setObjectName("toolBox")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_2.setObjectName("page_2")
        self.groupBox_5 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_5.setGeometry(QtCore.QRect(20, 10, 241, 161))
        self.groupBox_5.setObjectName("groupBox_5")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_5)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 247, 68))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.ckBLaserIsolinien_04 = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBLaserIsolinien_04.setChecked(False)
        self.ckBLaserIsolinien_04.setObjectName("ckBLaserIsolinien_04")
        self.ckButtons = QtWidgets.QButtonGroup(frmHoehenmodell)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.addButton(self.ckBLaserIsolinien_04)
        self.verticalLayout_6.addWidget(self.ckBLaserIsolinien_04)
        self.ckBLaserIsolinien_11 = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBLaserIsolinien_11.setChecked(False)
        self.ckBLaserIsolinien_11.setObjectName("ckBLaserIsolinien_11")
        self.ckButtons.addButton(self.ckBLaserIsolinien_11)
        self.verticalLayout_6.addWidget(self.ckBLaserIsolinien_11)
        self.cmbBlattschnitt = QtWidgets.QComboBox(self.groupBox_5)
        self.cmbBlattschnitt.setGeometry(QtCore.QRect(10, 120, 161, 22))
        self.cmbBlattschnitt.setObjectName("cmbBlattschnitt")
        self.btnBlattschnitt = QtWidgets.QPushButton(self.groupBox_5)
        self.btnBlattschnitt.setGeometry(QtCore.QRect(190, 120, 31, 23))
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
        self.btnBlattschnitt.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btnBlattschnitt.setFont(font)
        self.btnBlattschnitt.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btnBlattschnitt.setCheckable(True)
        self.btnBlattschnitt.setChecked(False)
        self.btnBlattschnitt.setObjectName("btnBlattschnitt")
        self.groupBox_8 = QtWidgets.QGroupBox(self.page_2)
        self.groupBox_8.setGeometry(QtCore.QRect(20, 200, 241, 111))
        self.groupBox_8.setObjectName("groupBox_8")
        self.layoutWidget_5 = QtWidgets.QWidget(self.groupBox_8)
        self.layoutWidget_5.setGeometry(QtCore.QRect(10, 20, 296, 91))
        self.layoutWidget_5.setObjectName("layoutWidget_5")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget_5)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.ckB5LaserIsolinien = QtWidgets.QCheckBox(self.layoutWidget_5)
        self.ckB5LaserIsolinien.setCheckable(True)
        self.ckB5LaserIsolinien.setChecked(False)
        self.ckB5LaserIsolinien.setObjectName("ckB5LaserIsolinien")
        self.ckButtons.addButton(self.ckB5LaserIsolinien)
        self.verticalLayout_7.addWidget(self.ckB5LaserIsolinien)
        self.ckOEKIsolinien = QtWidgets.QCheckBox(self.layoutWidget_5)
        self.ckOEKIsolinien.setCheckable(True)
        self.ckOEKIsolinien.setChecked(False)
        self.ckOEKIsolinien.setObjectName("ckOEKIsolinien")
        self.ckButtons.addButton(self.ckOEKIsolinien)
        self.verticalLayout_7.addWidget(self.ckOEKIsolinien)
        self.ckUMGIsolinien = QtWidgets.QCheckBox(self.layoutWidget_5)
        self.ckUMGIsolinien.setCheckable(True)
        self.ckUMGIsolinien.setChecked(False)
        self.ckUMGIsolinien.setObjectName("ckUMGIsolinien")
        self.ckButtons.addButton(self.ckUMGIsolinien)
        self.verticalLayout_7.addWidget(self.ckUMGIsolinien)
        self.toolBox.addItem(self.page_2, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 309, 395))
        self.page.setObjectName("page")
        self.groupBox = QtWidgets.QGroupBox(self.page)
        self.groupBox.setGeometry(QtCore.QRect(10, 0, 291, 71))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 297, 52))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckVBEVumgebung = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckVBEVumgebung.setAutoExclusive(True)
        self.ckVBEVumgebung.setObjectName("ckVBEVumgebung")
        self.ckButtons.addButton(self.ckVBEVumgebung)
        self.verticalLayout.addWidget(self.ckVBEVumgebung)
        self.ckHSZentraleuropa = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckHSZentraleuropa.setAutoExclusive(True)
        self.ckHSZentraleuropa.setObjectName("ckHSZentraleuropa")
        self.ckButtons.addButton(self.ckHSZentraleuropa)
        self.verticalLayout.addWidget(self.ckHSZentraleuropa)
        self.toolBox_2 = QtWidgets.QToolBox(self.page)
        self.toolBox_2.setGeometry(QtCore.QRect(10, 80, 291, 301))
        self.toolBox_2.setFrameShape(QtWidgets.QFrame.Box)
        self.toolBox_2.setFrameShadow(QtWidgets.QFrame.Plain)
        self.toolBox_2.setObjectName("toolBox_2")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_3.setObjectName("page_3")
        self.groupBox_6 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_6.setGeometry(QtCore.QRect(11, 11, 251, 71))
        self.groupBox_6.setObjectName("groupBox_6")
        self.layoutWidget_2 = QtWidgets.QWidget(self.groupBox_6)
        self.layoutWidget_2.setGeometry(QtCore.QRect(10, 20, 242, 52))
        self.layoutWidget_2.setObjectName("layoutWidget_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget_2)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ckVLaserVegetation_04 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.ckVLaserVegetation_04.setAutoExclusive(True)
        self.ckVLaserVegetation_04.setObjectName("ckVLaserVegetation_04")
        self.ckButtons.addButton(self.ckVLaserVegetation_04)
        self.verticalLayout_2.addWidget(self.ckVLaserVegetation_04)
        self.ckVDgmVegetation_04 = QtWidgets.QCheckBox(self.layoutWidget_2)
        self.ckVDgmVegetation_04.setAutoExclusive(True)
        self.ckVDgmVegetation_04.setObjectName("ckVDgmVegetation_04")
        self.ckButtons.addButton(self.ckVDgmVegetation_04)
        self.verticalLayout_2.addWidget(self.ckVDgmVegetation_04)
        self.groupBox_7 = QtWidgets.QGroupBox(self.page_3)
        self.groupBox_7.setGeometry(QtCore.QRect(10, 90, 251, 148))
        self.groupBox_7.setObjectName("groupBox_7")
        self.layoutWidget_4 = QtWidgets.QWidget(self.groupBox_7)
        self.layoutWidget_4.setGeometry(QtCore.QRect(10, 20, 242, 52))
        self.layoutWidget_4.setObjectName("layoutWidget_4")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget_4)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ckVLaserGelaende_04 = QtWidgets.QCheckBox(self.layoutWidget_4)
        self.ckVLaserGelaende_04.setAutoExclusive(True)
        self.ckVLaserGelaende_04.setObjectName("ckVLaserGelaende_04")
        self.ckButtons.addButton(self.ckVLaserGelaende_04)
        self.verticalLayout_4.addWidget(self.ckVLaserGelaende_04)
        self.ckVDgmGelaende_04 = QtWidgets.QCheckBox(self.layoutWidget_4)
        self.ckVDgmGelaende_04.setAutoExclusive(True)
        self.ckVDgmGelaende_04.setObjectName("ckVDgmGelaende_04")
        self.ckButtons.addButton(self.ckVDgmGelaende_04)
        self.verticalLayout_4.addWidget(self.ckVDgmGelaende_04)
        self.layoutWidget_3 = QtWidgets.QWidget(self.groupBox_7)
        self.layoutWidget_3.setGeometry(QtCore.QRect(10, 70, 296, 80))
        self.layoutWidget_3.setObjectName("layoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ckVNeigungGrad_04 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.ckVNeigungGrad_04.setEnabled(True)
        self.ckVNeigungGrad_04.setAutoExclusive(True)
        self.ckVNeigungGrad_04.setObjectName("ckVNeigungGrad_04")
        self.ckButtons.addButton(self.ckVNeigungGrad_04)
        self.verticalLayout_3.addWidget(self.ckVNeigungGrad_04)
        self.ckVNeigungProzent_04 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.ckVNeigungProzent_04.setEnabled(True)
        self.ckVNeigungProzent_04.setAutoExclusive(True)
        self.ckVNeigungProzent_04.setObjectName("ckVNeigungProzent_04")
        self.ckButtons.addButton(self.ckVNeigungProzent_04)
        self.verticalLayout_3.addWidget(self.ckVNeigungProzent_04)
        self.ckVExposition_04 = QtWidgets.QCheckBox(self.layoutWidget_3)
        self.ckVExposition_04.setEnabled(True)
        self.ckVExposition_04.setAutoExclusive(True)
        self.ckVExposition_04.setObjectName("ckVExposition_04")
        self.ckButtons.addButton(self.ckVExposition_04)
        self.verticalLayout_3.addWidget(self.ckVExposition_04)
        self.toolBox_2.addItem(self.page_3, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 289, 245))
        self.page_4.setObjectName("page_4")
        self.groupBox_9 = QtWidgets.QGroupBox(self.page_4)
        self.groupBox_9.setGeometry(QtCore.QRect(11, 1, 251, 71))
        self.groupBox_9.setObjectName("groupBox_9")
        self.layoutWidget_6 = QtWidgets.QWidget(self.groupBox_9)
        self.layoutWidget_6.setGeometry(QtCore.QRect(10, 20, 257, 52))
        self.layoutWidget_6.setObjectName("layoutWidget_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget_6)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ckVLaserVegetation_11 = QtWidgets.QCheckBox(self.layoutWidget_6)
        self.ckVLaserVegetation_11.setAutoExclusive(True)
        self.ckVLaserVegetation_11.setObjectName("ckVLaserVegetation_11")
        self.ckButtons.addButton(self.ckVLaserVegetation_11)
        self.verticalLayout_5.addWidget(self.ckVLaserVegetation_11)
        self.ckVDgmVegetation_11 = QtWidgets.QCheckBox(self.layoutWidget_6)
        self.ckVDgmVegetation_11.setAutoExclusive(True)
        self.ckVDgmVegetation_11.setObjectName("ckVDgmVegetation_11")
        self.ckButtons.addButton(self.ckVDgmVegetation_11)
        self.verticalLayout_5.addWidget(self.ckVDgmVegetation_11)
        self.groupBox_10 = QtWidgets.QGroupBox(self.page_4)
        self.groupBox_10.setGeometry(QtCore.QRect(10, 80, 251, 148))
        self.groupBox_10.setObjectName("groupBox_10")
        self.layoutWidget_7 = QtWidgets.QWidget(self.groupBox_10)
        self.layoutWidget_7.setGeometry(QtCore.QRect(10, 20, 242, 52))
        self.layoutWidget_7.setObjectName("layoutWidget_7")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.layoutWidget_7)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ckVLaserGelaende_11 = QtWidgets.QCheckBox(self.layoutWidget_7)
        self.ckVLaserGelaende_11.setAutoExclusive(True)
        self.ckVLaserGelaende_11.setObjectName("ckVLaserGelaende_11")
        self.ckButtons.addButton(self.ckVLaserGelaende_11)
        self.verticalLayout_8.addWidget(self.ckVLaserGelaende_11)
        self.ckVDgmGelaende_11 = QtWidgets.QCheckBox(self.layoutWidget_7)
        self.ckVDgmGelaende_11.setAutoExclusive(True)
        self.ckVDgmGelaende_11.setObjectName("ckVDgmGelaende_11")
        self.ckButtons.addButton(self.ckVDgmGelaende_11)
        self.verticalLayout_8.addWidget(self.ckVDgmGelaende_11)
        self.layoutWidget_8 = QtWidgets.QWidget(self.groupBox_10)
        self.layoutWidget_8.setGeometry(QtCore.QRect(10, 70, 296, 80))
        self.layoutWidget_8.setObjectName("layoutWidget_8")
        self.verticalLayout_9 = QtWidgets.QVBoxLayout(self.layoutWidget_8)
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.ckVNeigungGrad_11 = QtWidgets.QCheckBox(self.layoutWidget_8)
        self.ckVNeigungGrad_11.setEnabled(True)
        self.ckVNeigungGrad_11.setAutoExclusive(True)
        self.ckVNeigungGrad_11.setObjectName("ckVNeigungGrad_11")
        self.ckButtons.addButton(self.ckVNeigungGrad_11)
        self.verticalLayout_9.addWidget(self.ckVNeigungGrad_11)
        self.ckVNeigungProzent_11 = QtWidgets.QCheckBox(self.layoutWidget_8)
        self.ckVNeigungProzent_11.setEnabled(True)
        self.ckVNeigungProzent_11.setAutoExclusive(True)
        self.ckVNeigungProzent_11.setObjectName("ckVNeigungProzent_11")
        self.ckButtons.addButton(self.ckVNeigungProzent_11)
        self.verticalLayout_9.addWidget(self.ckVNeigungProzent_11)
        self.ckVExposition_11 = QtWidgets.QCheckBox(self.layoutWidget_8)
        self.ckVExposition_11.setEnabled(True)
        self.ckVExposition_11.setAutoExclusive(True)
        self.ckVExposition_11.setObjectName("ckVExposition_11")
        self.ckButtons.addButton(self.ckVExposition_11)
        self.verticalLayout_9.addWidget(self.ckVExposition_11)
        self.toolBox_2.addItem(self.page_4, "")
        self.toolBox.addItem(self.page, "")
        self.groupBox_2 = QtWidgets.QGroupBox(frmHoehenmodell)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 482, 251, 161))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.btHoehenabfrage = QtWidgets.QPushButton(self.groupBox_2)
        self.btHoehenabfrage.setGeometry(QtCore.QRect(140, 40, 31, 31))
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
        self.btHoehenabfrage.setPalette(palette)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.btHoehenabfrage.setFont(font)
        self.btHoehenabfrage.setFocusPolicy(QtCore.Qt.StrongFocus)
        self.btHoehenabfrage.setCheckable(True)
        self.btHoehenabfrage.setChecked(False)
        self.btHoehenabfrage.setObjectName("btHoehenabfrage")
        self.label = QtWidgets.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(100, 10, 131, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.leX = QtWidgets.QLineEdit(self.groupBox_2)
        self.leX.setGeometry(QtCore.QRect(10, 50, 71, 20))
        self.leX.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leX.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leX.setObjectName("leX")
        self.leY = QtWidgets.QLineEdit(self.groupBox_2)
        self.leY.setGeometry(QtCore.QRect(10, 90, 71, 20))
        self.leY.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leY.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leY.setObjectName("leY")
        self.leZ = QtWidgets.QLineEdit(self.groupBox_2)
        self.leZ.setGeometry(QtCore.QRect(10, 130, 71, 20))
        self.leZ.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.leZ.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.leZ.setObjectName("leZ")
        self.label_2 = QtWidgets.QLabel(self.groupBox_2)
        self.label_2.setGeometry(QtCore.QRect(10, 30, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.groupBox_2)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self.groupBox_2)
        self.label_4.setGeometry(QtCore.QRect(10, 110, 51, 20))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.btnAbbrechen_2 = QtWidgets.QPushButton(self.groupBox_2)
        self.btnAbbrechen_2.setGeometry(QtCore.QRect(100, 100, 131, 41))
        self.btnAbbrechen_2.setObjectName("btnAbbrechen_2")
        self.line = QtWidgets.QFrame(frmHoehenmodell)
        self.line.setGeometry(QtCore.QRect(0, 471, 321, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.retranslateUi(frmHoehenmodell)
        self.toolBox.setCurrentIndex(1)
        self.toolBox_2.setCurrentIndex(1)
        self.btnLaden.clicked.connect(frmHoehenmodell.laden)
        self.btnAbbrechen.clicked.connect(frmHoehenmodell.closeEvent)
        self.btHoehenabfrage.clicked.connect(frmHoehenmodell.hoehenklick)
        self.btnBlattschnitt.clicked.connect(frmHoehenmodell.hoehenklick)
        self.btnAbbrechen_2.clicked.connect(frmHoehenmodell.hoeheClear)
        QtCore.QMetaObject.connectSlotsByName(frmHoehenmodell)

    def retranslateUi(self, frmHoehenmodell):
        _translate = QtCore.QCoreApplication.translate
        frmHoehenmodell.setWindowTitle(_translate("frmHoehenmodell", "Digitales Geländemodell"))
        self.btnAbbrechen.setText(_translate("frmHoehenmodell", "Schließen"))
        self.btnLaden.setText(_translate("frmHoehenmodell", "Thema laden"))
        self.groupBox_5.setTitle(_translate("frmHoehenmodell", "Blattschnitt"))
        self.ckBLaserIsolinien_04.setText(_translate("frmHoehenmodell", "1m-Höhenschichtenlinien\n"
"(Lasermodell 2002-04, ab 1:25000)"))
        self.ckBLaserIsolinien_11.setText(_translate("frmHoehenmodell", "50cm-Höhenschichtenlinien\n"
"(Lasermodell 2011, ab 1:25000)"))
        self.btnBlattschnitt.setText(_translate("frmHoehenmodell", "+"))
        self.groupBox_8.setTitle(_translate("frmHoehenmodell", "Landesfläche"))
        self.ckB5LaserIsolinien.setText(_translate("frmHoehenmodell", "5m-Höhenschichtenlinien (Vlbg.)\n"
"(ab 1:25000)"))
        self.ckOEKIsolinien.setText(_translate("frmHoehenmodell", "OEK50-Höhenschichtenlinien (Vlbg.)\n"
"(ab 1:50000)"))
        self.ckUMGIsolinien.setText(_translate("frmHoehenmodell", "50m-Höhenschichtenlinien (Vlbg. + Umg.)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("frmHoehenmodell", "Höhenschichtenlinien"))
        self.groupBox.setTitle(_translate("frmHoehenmodell", "Schummerungen Vorarlberg und Umgebung"))
        self.ckVBEVumgebung.setText(_translate("frmHoehenmodell", "Schummerung 5m Aufl. (Vlbg. und Umg.)"))
        self.ckHSZentraleuropa.setText(_translate("frmHoehenmodell", "Schummerung 50m Aufl. (Zentraleuropa)"))
        self.groupBox_6.setTitle(_translate("frmHoehenmodell", "Oberflächenmodell"))
        self.ckVLaserVegetation_04.setText(_translate("frmHoehenmodell", "Schummerung 1m Auflösung"))
        self.ckVDgmVegetation_04.setText(_translate("frmHoehenmodell", "Rasterhöhenmodell 1m Auflösung"))
        self.groupBox_7.setTitle(_translate("frmHoehenmodell", "Geländemodell"))
        self.ckVLaserGelaende_04.setText(_translate("frmHoehenmodell", "Schummerung 1m Auflösung"))
        self.ckVDgmGelaende_04.setText(_translate("frmHoehenmodell", "Rasterhöhenmodell 1m Auflösung"))
        self.ckVNeigungGrad_04.setText(_translate("frmHoehenmodell", "Geländeneigung in Grad 5m Auflösung"))
        self.ckVNeigungProzent_04.setText(_translate("frmHoehenmodell", "Geländeneigung in Prozent 5m Auflösung"))
        self.ckVExposition_04.setText(_translate("frmHoehenmodell", "Geländeexposition (Orientierung) 5m Aufl."))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_3), _translate("frmHoehenmodell", "Laserscanning Höhenmodelle Vlbg (2002-04)"))
        self.groupBox_9.setTitle(_translate("frmHoehenmodell", "Oberflächenmodell"))
        self.ckVLaserVegetation_11.setText(_translate("frmHoehenmodell", "Schummerung 50cm Auflösung"))
        self.ckVDgmVegetation_11.setText(_translate("frmHoehenmodell", "Rasterhöhenmodell 50cm Auflösung"))
        self.groupBox_10.setTitle(_translate("frmHoehenmodell", "Geländemodell"))
        self.ckVLaserGelaende_11.setText(_translate("frmHoehenmodell", "Schummerung 50cm Auflösung"))
        self.ckVDgmGelaende_11.setText(_translate("frmHoehenmodell", "Rasterhöhenmodell 50cm Auflösung"))
        self.ckVNeigungGrad_11.setText(_translate("frmHoehenmodell", "Geländeneigung in Grad 5m Auflösung"))
        self.ckVNeigungProzent_11.setText(_translate("frmHoehenmodell", "Geländeneigung in Prozent 5m Auflösung"))
        self.ckVExposition_11.setText(_translate("frmHoehenmodell", "Geländeexposition (Orientierung) 5m Aufl."))
        self.toolBox_2.setItemText(self.toolBox_2.indexOf(self.page_4), _translate("frmHoehenmodell", "Laserscanning Höhenmodelle Vlbg (2011)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("frmHoehenmodell", "Rastermodelle"))
        self.groupBox_2.setTitle(_translate("frmHoehenmodell", "Höhenmarken (Modell 2011)"))
        self.btHoehenabfrage.setText(_translate("frmHoehenmodell", "+"))
        self.label.setText(_translate("frmHoehenmodell", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Höhenmarkierung zeichnen</span></p></body></html>"))
        self.label_2.setText(_translate("frmHoehenmodell", "Rechtswert:"))
        self.label_3.setText(_translate("frmHoehenmodell", "Hochwert:"))
        self.label_4.setText(_translate("frmHoehenmodell", "Hoehe:"))
        self.btnAbbrechen_2.setText(_translate("frmHoehenmodell", "Hoehenmarkierungen\n"
"entfernen"))

