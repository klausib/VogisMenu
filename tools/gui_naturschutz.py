# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'gui_naturschutz.ui'
#
# Created: Thu Sep 15 12:18:07 2016
#      by: PyQt4 UI code generator 4.8.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_frmNaturschutz(object):
    def setupUi(self, frmNaturschutz):
        frmNaturschutz.setObjectName(_fromUtf8("frmNaturschutz"))
        frmNaturschutz.resize(567, 422)
        self.toolBox = QtGui.QToolBox(frmNaturschutz)
        self.toolBox.setGeometry(QtCore.QRect(6, 10, 561, 311))
        self.toolBox.setObjectName(_fromUtf8("toolBox"))
        self.gebietsschutz = QtGui.QWidget()
        self.gebietsschutz.setGeometry(QtCore.QRect(0, 0, 561, 230))
        self.gebietsschutz.setObjectName(_fromUtf8("gebietsschutz"))
        self.layoutWidget = QtGui.QWidget(self.gebietsschutz)
        self.layoutWidget.setGeometry(QtCore.QRect(50, 10, 282, 188))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.gridLayout = QtGui.QGridLayout(self.layoutWidget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.ckNatura2000 = QtGui.QCheckBox(self.layoutWidget)
        self.ckNatura2000.setObjectName(_fromUtf8("ckNatura2000"))
        self.ckButtons = QtGui.QButtonGroup(frmNaturschutz)
        self.ckButtons.setObjectName(_fromUtf8("ckButtons"))
        self.ckButtons.addButton(self.ckNatura2000)
        self.gridLayout.addWidget(self.ckNatura2000, 0, 0, 1, 1)
        self.ckNaturschutzgebiete = QtGui.QCheckBox(self.layoutWidget)
        self.ckNaturschutzgebiete.setObjectName(_fromUtf8("ckNaturschutzgebiete"))
        self.ckButtons.addButton(self.ckNaturschutzgebiete)
        self.gridLayout.addWidget(self.ckNaturschutzgebiete, 1, 0, 1, 1)
        self.ckLandschaftsschutzgebiete = QtGui.QCheckBox(self.layoutWidget)
        self.ckLandschaftsschutzgebiete.setObjectName(_fromUtf8("ckLandschaftsschutzgebiete"))
        self.ckButtons.addButton(self.ckLandschaftsschutzgebiete)
        self.gridLayout.addWidget(self.ckLandschaftsschutzgebiete, 2, 0, 1, 1)
        self.ckPflanzenschutzgebiete = QtGui.QCheckBox(self.layoutWidget)
        self.ckPflanzenschutzgebiete.setObjectName(_fromUtf8("ckPflanzenschutzgebiete"))
        self.ckButtons.addButton(self.ckPflanzenschutzgebiete)
        self.gridLayout.addWidget(self.ckPflanzenschutzgebiete, 3, 0, 1, 1)
        self.ckGeschLandschaftsteil = QtGui.QCheckBox(self.layoutWidget)
        self.ckGeschLandschaftsteil.setObjectName(_fromUtf8("ckGeschLandschaftsteil"))
        self.ckButtons.addButton(self.ckGeschLandschaftsteil)
        self.gridLayout.addWidget(self.ckGeschLandschaftsteil, 4, 0, 1, 1)
        self.ckBiosphaerenpark = QtGui.QCheckBox(self.layoutWidget)
        self.ckBiosphaerenpark.setObjectName(_fromUtf8("ckBiosphaerenpark"))
        self.ckButtons.addButton(self.ckBiosphaerenpark)
        self.gridLayout.addWidget(self.ckBiosphaerenpark, 5, 0, 1, 1)
        self.ckRuhezone = QtGui.QCheckBox(self.layoutWidget)
        self.ckRuhezone.setObjectName(_fromUtf8("ckRuhezone"))
        self.ckButtons.addButton(self.ckRuhezone)
        self.gridLayout.addWidget(self.ckRuhezone, 6, 0, 1, 1)
        self.ckOertlichesSchutzgebiet = QtGui.QCheckBox(self.layoutWidget)
        self.ckOertlichesSchutzgebiet.setObjectName(_fromUtf8("ckOertlichesSchutzgebiet"))
        self.ckButtons.addButton(self.ckOertlichesSchutzgebiet)
        self.gridLayout.addWidget(self.ckOertlichesSchutzgebiet, 7, 0, 1, 1)
        self.toolBox.addItem(self.gebietsschutz, _fromUtf8(""))
        self.inventar = QtGui.QWidget()
        self.inventar.setGeometry(QtCore.QRect(0, 0, 561, 230))
        self.inventar.setObjectName(_fromUtf8("inventar"))
        self.ckBiotopinventar = QtGui.QCheckBox(self.inventar)
        self.ckBiotopinventar.setGeometry(QtCore.QRect(50, 20, 171, 18))
        self.ckBiotopinventar.setObjectName(_fromUtf8("ckBiotopinventar"))
        self.ckButtons.addButton(self.ckBiotopinventar)
        self.groupBox = QtGui.QGroupBox(self.inventar)
        self.groupBox.setGeometry(QtCore.QRect(70, 70, 401, 141))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btnGemeindebericht = QtGui.QPushButton(self.groupBox)
        self.btnGemeindebericht.setGeometry(QtCore.QRect(30, 90, 141, 31))
        self.btnGemeindebericht.setObjectName(_fromUtf8("btnGemeindebericht"))
        self.btnA3Plaene = QtGui.QPushButton(self.groupBox)
        self.btnA3Plaene.setGeometry(QtCore.QRect(210, 90, 141, 31))
        self.btnA3Plaene.setObjectName(_fromUtf8("btnA3Plaene"))
        self.cmbGemeinden = QtGui.QComboBox(self.groupBox)
        self.cmbGemeinden.setGeometry(QtCore.QRect(30, 30, 191, 22))
        self.cmbGemeinden.setObjectName(_fromUtf8("cmbGemeinden"))
        self.btGmdChoice = QtGui.QPushButton(self.groupBox)
        self.btGmdChoice.setGeometry(QtCore.QRect(300, 30, 31, 23))
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
        self.toolBox.addItem(self.inventar, _fromUtf8(""))
        self.page_2 = QtGui.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 561, 230))
        self.page_2.setObjectName(_fromUtf8("page_2"))
        self.layoutWidget1 = QtGui.QWidget(self.page_2)
        self.layoutWidget1.setGeometry(QtCore.QRect(71, 31, 179, 68))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.gridLayout_2 = QtGui.QGridLayout(self.layoutWidget1)
        self.gridLayout_2.setMargin(0)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.ckStreuwiesen_2000 = QtGui.QCheckBox(self.layoutWidget1)
        self.ckStreuwiesen_2000.setObjectName(_fromUtf8("ckStreuwiesen_2000"))
        self.ckButtons.addButton(self.ckStreuwiesen_2000)
        self.gridLayout_2.addWidget(self.ckStreuwiesen_2000, 1, 0, 1, 1)
        self.ckNaturdenkmale = QtGui.QCheckBox(self.layoutWidget1)
        self.ckNaturdenkmale.setObjectName(_fromUtf8("ckNaturdenkmale"))
        self.ckButtons.addButton(self.ckNaturdenkmale)
        self.gridLayout_2.addWidget(self.ckNaturdenkmale, 2, 0, 1, 1)
        self.ckStreuwiesen_2014 = QtGui.QCheckBox(self.layoutWidget1)
        self.ckStreuwiesen_2014.setObjectName(_fromUtf8("ckStreuwiesen_2014"))
        self.ckButtons.addButton(self.ckStreuwiesen_2014)
        self.gridLayout_2.addWidget(self.ckStreuwiesen_2014, 0, 0, 1, 1)
        self.toolBox.addItem(self.page_2, _fromUtf8(""))
        self.line = QtGui.QFrame(frmNaturschutz)
        self.line.setGeometry(QtCore.QRect(0, 340, 571, 16))
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.btnLaden = QtGui.QPushButton(frmNaturschutz)
        self.btnLaden.setGeometry(QtCore.QRect(60, 370, 151, 23))
        self.btnLaden.setObjectName(_fromUtf8("btnLaden"))
        self.btnAbbrechen = QtGui.QPushButton(frmNaturschutz)
        self.btnAbbrechen.setGeometry(QtCore.QRect(330, 370, 141, 23))
        self.btnAbbrechen.setObjectName(_fromUtf8("btnAbbrechen"))

        self.retranslateUi(frmNaturschutz)
        self.toolBox.setCurrentIndex(0)
        QtCore.QObject.connect(self.btnLaden, QtCore.SIGNAL(_fromUtf8("clicked()")), frmNaturschutz.datenladen)
        QtCore.QObject.connect(self.btnAbbrechen, QtCore.SIGNAL(_fromUtf8("clicked()")), frmNaturschutz.closeEvent)
        QtCore.QObject.connect(self.btnGemeindebericht, QtCore.SIGNAL(_fromUtf8("clicked()")), frmNaturschutz.gemeindebericht)
        QtCore.QObject.connect(self.btnA3Plaene, QtCore.SIGNAL(_fromUtf8("clicked()")), frmNaturschutz.a3plaene)
        QtCore.QObject.connect(self.btGmdChoice, QtCore.SIGNAL(_fromUtf8("clicked()")), frmNaturschutz.gmd_choice_toggled)
        QtCore.QObject.connect(self.cmbGemeinden, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(QString)")), frmNaturschutz.auswahlaenderung)
        QtCore.QMetaObject.connectSlotsByName(frmNaturschutz)

    def retranslateUi(self, frmNaturschutz):
        frmNaturschutz.setWindowTitle(QtGui.QApplication.translate("frmNaturschutz", "Naturschutz", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNatura2000.setText(QtGui.QApplication.translate("frmNaturschutz", "NATURA 2000 (Europaschutzgebiet)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNaturschutzgebiete.setText(QtGui.QApplication.translate("frmNaturschutz", "Naturschutzgebiete (inkl. Streuwiesenbiotopverbund)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckLandschaftsschutzgebiete.setText(QtGui.QApplication.translate("frmNaturschutz", "Landschaftsschutzgebiete", None, QtGui.QApplication.UnicodeUTF8))
        self.ckPflanzenschutzgebiete.setText(QtGui.QApplication.translate("frmNaturschutz", "Pflanzenschutzgebiete", None, QtGui.QApplication.UnicodeUTF8))
        self.ckGeschLandschaftsteil.setText(QtGui.QApplication.translate("frmNaturschutz", "Geschützter Landschaftsteil", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBiosphaerenpark.setText(QtGui.QApplication.translate("frmNaturschutz", "Biosphärenparks", None, QtGui.QApplication.UnicodeUTF8))
        self.ckRuhezone.setText(QtGui.QApplication.translate("frmNaturschutz", "Ruhezone", None, QtGui.QApplication.UnicodeUTF8))
        self.ckOertlichesSchutzgebiet.setText(QtGui.QApplication.translate("frmNaturschutz", "Örtliches Schutzgebiet", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.gebietsschutz), QtGui.QApplication.translate("frmNaturschutz", "Gebietsschutz", None, QtGui.QApplication.UnicodeUTF8))
        self.ckBiotopinventar.setText(QtGui.QApplication.translate("frmNaturschutz", "Biotopinventar 2009", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("frmNaturschutz", "Infos (als PDF)", None, QtGui.QApplication.UnicodeUTF8))
        self.btnGemeindebericht.setText(QtGui.QApplication.translate("frmNaturschutz", "Gemeindebericht", None, QtGui.QApplication.UnicodeUTF8))
        self.btnA3Plaene.setText(QtGui.QApplication.translate("frmNaturschutz", "A3 Pläne", None, QtGui.QApplication.UnicodeUTF8))
        self.btGmdChoice.setText(QtGui.QApplication.translate("frmNaturschutz", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.inventar), QtGui.QApplication.translate("frmNaturschutz", "Inventar", None, QtGui.QApplication.UnicodeUTF8))
        self.ckStreuwiesen_2000.setText(QtGui.QApplication.translate("frmNaturschutz", "Evaluierung Streuwiesen (2000)", None, QtGui.QApplication.UnicodeUTF8))
        self.ckNaturdenkmale.setText(QtGui.QApplication.translate("frmNaturschutz", "Naturdenkmale", None, QtGui.QApplication.UnicodeUTF8))
        self.ckStreuwiesen_2014.setText(QtGui.QApplication.translate("frmNaturschutz", "Evaluierung Streuwiesen (2014)", None, QtGui.QApplication.UnicodeUTF8))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), QtGui.QApplication.translate("frmNaturschutz", "Projekte", None, QtGui.QApplication.UnicodeUTF8))
        self.btnLaden.setText(QtGui.QApplication.translate("frmNaturschutz", "Themen laden", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAbbrechen.setText(QtGui.QApplication.translate("frmNaturschutz", "Schließen", None, QtGui.QApplication.UnicodeUTF8))

