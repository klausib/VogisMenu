# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_VogisPrint_Serien_Grid.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_VogisPrintSerieGrid(object):
    def setupUi(self, VogisPrintSerieGrid):
        VogisPrintSerieGrid.setObjectName("VogisPrintSerieGrid")
        VogisPrintSerieGrid.setEnabled(True)
        VogisPrintSerieGrid.resize(499, 209)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VogisPrintSerieGrid.sizePolicy().hasHeightForWidth())
        VogisPrintSerieGrid.setSizePolicy(sizePolicy)
        self.groupBox = QtWidgets.QGroupBox(VogisPrintSerieGrid)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 431, 161))
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_5 = QtWidgets.QGridLayout()
        self.gridLayout_5.setContentsMargins(4, 4, 4, 4)
        self.gridLayout_5.setHorizontalSpacing(34)
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.mbgridtype = QtWidgets.QComboBox(self.groupBox)
        self.mbgridtype.setObjectName("mbgridtype")
        self.gridLayout_5.addWidget(self.mbgridtype, 0, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.groupBox)
        self.label_8.setObjectName("label_8")
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.groupBox)
        self.label_9.setObjectName("label_9")
        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)
        self.mbmaplayer = QtWidgets.QComboBox(self.groupBox)
        self.mbmaplayer.setObjectName("mbmaplayer")
        self.gridLayout_5.addWidget(self.mbmaplayer, 1, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setToolTip("")
        self.label.setStatusTip("")
        self.label.setObjectName("label")
        self.gridLayout_5.addWidget(self.label, 2, 0, 1, 1)
        self.mprintScale = QtWidgets.QComboBox(self.groupBox)
        self.mprintScale.setToolTip("")
        self.mprintScale.setEditable(True)
        self.mprintScale.setMaxVisibleItems(16)
        self.mprintScale.setObjectName("mprintScale")
        self.gridLayout_5.addWidget(self.mprintScale, 2, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnMbGrid = QtWidgets.QPushButton(self.groupBox)
        self.btnMbGrid.setObjectName("btnMbGrid")
        self.horizontalLayout.addWidget(self.btnMbGrid)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonClose = QtWidgets.QPushButton(self.groupBox)
        self.buttonClose.setObjectName("buttonClose")
        self.horizontalLayout.addWidget(self.buttonClose)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(VogisPrintSerieGrid)
        self.buttonClose.clicked.connect(VogisPrintSerieGrid.VogisPrintSerieGrid_schliessen)
        QtCore.QMetaObject.connectSlotsByName(VogisPrintSerieGrid)

    def retranslateUi(self, VogisPrintSerieGrid):
        _translate = QtCore.QCoreApplication.translate
        VogisPrintSerieGrid.setWindowTitle(_translate("VogisPrintSerieGrid", "VogisPrint - Raster erzeugen"))
        self.groupBox.setTitle(_translate("VogisPrintSerieGrid", "Grid"))
        self.label_8.setText(_translate("VogisPrintSerieGrid", "Grid type: "))
        self.label_9.setText(_translate("VogisPrintSerieGrid", "Bezugslayer"))
        self.label.setText(_translate("VogisPrintSerieGrid", "Ausgabemaßstab Format"))
        self.btnMbGrid.setText(_translate("VogisPrintSerieGrid", "Create"))
        self.buttonClose.setText(_translate("VogisPrintSerieGrid", "Schliessen"))

