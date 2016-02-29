# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_VogisPrint_Serien_Grid.ui'
#
# Created: Mon Jan 27 16:03:04 2014
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_VogisPrintSerieGrid(object):
    def setupUi(self, VogisPrintSerieGrid):
        VogisPrintSerieGrid.setObjectName(_fromUtf8("VogisPrintSerieGrid"))
        VogisPrintSerieGrid.setEnabled(True)
        VogisPrintSerieGrid.resize(499, 209)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(VogisPrintSerieGrid.sizePolicy().hasHeightForWidth())
        VogisPrintSerieGrid.setSizePolicy(sizePolicy)
        self.groupBox = QtGui.QGroupBox(VogisPrintSerieGrid)
        self.groupBox.setEnabled(True)
        self.groupBox.setGeometry(QtCore.QRect(30, 20, 431, 161))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.gridLayout_5 = QtGui.QGridLayout()
        self.gridLayout_5.setMargin(4)
        self.gridLayout_5.setHorizontalSpacing(34)
        self.gridLayout_5.setObjectName(_fromUtf8("gridLayout_5"))
        self.mbgridtype = QtGui.QComboBox(self.groupBox)
        self.mbgridtype.setObjectName(_fromUtf8("mbgridtype"))
        self.gridLayout_5.addWidget(self.mbgridtype, 0, 1, 1, 1)
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout_5.addWidget(self.label_8, 0, 0, 1, 1)
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout_5.addWidget(self.label_9, 1, 0, 1, 1)
        self.mbmaplayer = QtGui.QComboBox(self.groupBox)
        self.mbmaplayer.setObjectName(_fromUtf8("mbmaplayer"))
        self.gridLayout_5.addWidget(self.mbmaplayer, 1, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setToolTip(_fromUtf8(""))
        self.label.setStatusTip(_fromUtf8(""))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout_5.addWidget(self.label, 2, 0, 1, 1)
        self.mprintScale = QtGui.QComboBox(self.groupBox)
        self.mprintScale.setToolTip(_fromUtf8(""))
        self.mprintScale.setEditable(True)
        self.mprintScale.setMaxVisibleItems(16)
        self.mprintScale.setObjectName(_fromUtf8("mprintScale"))
        self.gridLayout_5.addWidget(self.mprintScale, 2, 1, 1, 1)
        self.gridLayout_3.addLayout(self.gridLayout_5, 0, 0, 1, 1)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnMbGrid = QtGui.QPushButton(self.groupBox)
        self.btnMbGrid.setObjectName(_fromUtf8("btnMbGrid"))
        self.horizontalLayout.addWidget(self.btnMbGrid)
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.buttonClose = QtGui.QPushButton(self.groupBox)
        self.buttonClose.setObjectName(_fromUtf8("buttonClose"))
        self.horizontalLayout.addWidget(self.buttonClose)
        spacerItem2 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.gridLayout_3.addLayout(self.horizontalLayout, 1, 0, 1, 1)

        self.retranslateUi(VogisPrintSerieGrid)
        QtCore.QMetaObject.connectSlotsByName(VogisPrintSerieGrid)

    def retranslateUi(self, VogisPrintSerieGrid):
        VogisPrintSerieGrid.setWindowTitle(QtGui.QApplication.translate("VogisPrintSerieGrid", "VogisPrint - Raster erzeugen", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("VogisPrintSerieGrid", "Grid", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setText(QtGui.QApplication.translate("VogisPrintSerieGrid", "Grid type: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setText(QtGui.QApplication.translate("VogisPrintSerieGrid", "Bezugslayer", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("VogisPrintSerieGrid", "Ausgabemaßstab Format", None, QtGui.QApplication.UnicodeUTF8))
        self.btnMbGrid.setText(QtGui.QApplication.translate("VogisPrintSerieGrid", "Create", None, QtGui.QApplication.UnicodeUTF8))
        self.buttonClose.setText(QtGui.QApplication.translate("VogisPrintSerieGrid", "Schliessen", None, QtGui.QApplication.UnicodeUTF8))

