# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\bamc\AppData\Roaming\QGIS\QGIS3\profiles\default\python\plugins\VogisMenu\tools\gui_wasser.ui'
#
# Created by: PyQt5 UI code generator 5.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_frmWasser(object):
    def setupUi(self, frmWasser):
        frmWasser.setObjectName("frmWasser")
        frmWasser.resize(362, 499)
        self.toolBox = QtWidgets.QToolBox(frmWasser)
        self.toolBox.setGeometry(QtCore.QRect(0, 0, 361, 431))
        self.toolBox.setFrameShape(QtWidgets.QFrame.Panel)
        self.toolBox.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.toolBox.setObjectName("toolBox")
        self.toolBoxPage1 = QtWidgets.QWidget()
        self.toolBoxPage1.setGeometry(QtCore.QRect(0, 0, 359, 159))
        self.toolBoxPage1.setObjectName("toolBoxPage1")
        self.layoutWidget = QtWidgets.QWidget(self.toolBoxPage1)
        self.layoutWidget.setGeometry(QtCore.QRect(30, 30, 151, 68))
        self.layoutWidget.setObjectName("layoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.ckQuellen = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckQuellen.setObjectName("ckQuellen")
        self.ckButtons = QtWidgets.QButtonGroup(frmWasser)
        self.ckButtons.setObjectName("ckButtons")
        self.ckButtons.addButton(self.ckQuellen)
        self.verticalLayout.addWidget(self.ckQuellen)
        self.ckBrunnen = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckBrunnen.setObjectName("ckBrunnen")
        self.ckButtons.addButton(self.ckBrunnen)
        self.verticalLayout.addWidget(self.ckBrunnen)
        self.ckSchutzSchongebiete = QtWidgets.QCheckBox(self.layoutWidget)
        self.ckSchutzSchongebiete.setObjectName("ckSchutzSchongebiete")
        self.ckButtons.addButton(self.ckSchutzSchongebiete)
        self.verticalLayout.addWidget(self.ckSchutzSchongebiete)
        self.toolBox.addItem(self.toolBoxPage1, "")
        self.toolBoxPage2 = QtWidgets.QWidget()
        self.toolBoxPage2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.toolBoxPage2.setObjectName("toolBoxPage2")
        self.layoutWidget1 = QtWidgets.QWidget(self.toolBoxPage2)
        self.layoutWidget1.setGeometry(QtCore.QRect(21, 11, 259, 116))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.ckGWWaermepumpen = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckGWWaermepumpen.setObjectName("ckGWWaermepumpen")
        self.ckButtons.addButton(self.ckGWWaermepumpen)
        self.verticalLayout_2.addWidget(self.ckGWWaermepumpen)
        self.ckErdwaermeanlagen = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckErdwaermeanlagen.setObjectName("ckErdwaermeanlagen")
        self.ckButtons.addButton(self.ckErdwaermeanlagen)
        self.verticalLayout_2.addWidget(self.ckErdwaermeanlagen)
        self.ckKuehlwasseranlagenGW = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckKuehlwasseranlagenGW.setObjectName("ckKuehlwasseranlagenGW")
        self.ckButtons.addButton(self.ckKuehlwasseranlagenGW)
        self.verticalLayout_2.addWidget(self.ckKuehlwasseranlagenGW)
        self.ckKuehlwasseranlagenOG = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckKuehlwasseranlagenOG.setObjectName("ckKuehlwasseranlagenOG")
        self.ckButtons.addButton(self.ckKuehlwasseranlagenOG)
        self.verticalLayout_2.addWidget(self.ckKuehlwasseranlagenOG)
        self.ckWeitereAnlagen = QtWidgets.QCheckBox(self.layoutWidget1)
        self.ckWeitereAnlagen.setObjectName("ckWeitereAnlagen")
        self.ckButtons.addButton(self.ckWeitereAnlagen)
        self.verticalLayout_2.addWidget(self.ckWeitereAnlagen)
        self.toolBox.addItem(self.toolBoxPage2, "")
        self.toolBoxPage3 = QtWidgets.QWidget()
        self.toolBoxPage3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.toolBoxPage3.setObjectName("toolBoxPage3")
        self.layoutWidget2 = QtWidgets.QWidget(self.toolBoxPage3)
        self.layoutWidget2.setGeometry(QtCore.QRect(20, 10, 246, 116))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget2)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.ckKraftwerke = QtWidgets.QCheckBox(self.layoutWidget2)
        self.ckKraftwerke.setObjectName("ckKraftwerke")
        self.ckButtons.addButton(self.ckKraftwerke)
        self.verticalLayout_3.addWidget(self.ckKraftwerke)
        self.ckSonstigeBetriebe = QtWidgets.QCheckBox(self.layoutWidget2)
        self.ckSonstigeBetriebe.setObjectName("ckSonstigeBetriebe")
        self.ckButtons.addButton(self.ckSonstigeBetriebe)
        self.verticalLayout_3.addWidget(self.ckSonstigeBetriebe)
        self.ckGeschiebe = QtWidgets.QCheckBox(self.layoutWidget2)
        self.ckGeschiebe.setObjectName("ckGeschiebe")
        self.ckButtons.addButton(self.ckGeschiebe)
        self.verticalLayout_3.addWidget(self.ckGeschiebe)
        self.ckSonstigeAnlagen = QtWidgets.QCheckBox(self.layoutWidget2)
        self.ckSonstigeAnlagen.setObjectName("ckSonstigeAnlagen")
        self.ckButtons.addButton(self.ckSonstigeAnlagen)
        self.verticalLayout_3.addWidget(self.ckSonstigeAnlagen)
        self.toolBox.addItem(self.toolBoxPage3, "")
        self.toolBoxPage4 = QtWidgets.QWidget()
        self.toolBoxPage4.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.toolBoxPage4.setObjectName("toolBoxPage4")
        self.layoutWidget3 = QtWidgets.QWidget(self.toolBoxPage4)
        self.layoutWidget3.setGeometry(QtCore.QRect(20, 20, 146, 92))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.ckKommunaleKlaeranlagen = QtWidgets.QCheckBox(self.layoutWidget3)
        self.ckKommunaleKlaeranlagen.setObjectName("ckKommunaleKlaeranlagen")
        self.ckButtons.addButton(self.ckKommunaleKlaeranlagen)
        self.verticalLayout_4.addWidget(self.ckKommunaleKlaeranlagen)
        self.ckKleinklaeranlagen = QtWidgets.QCheckBox(self.layoutWidget3)
        self.ckKleinklaeranlagen.setObjectName("ckKleinklaeranlagen")
        self.ckButtons.addButton(self.ckKleinklaeranlagen)
        self.verticalLayout_4.addWidget(self.ckKleinklaeranlagen)
        self.ckBetrieblicheKlaeranlagen = QtWidgets.QCheckBox(self.layoutWidget3)
        self.ckBetrieblicheKlaeranlagen.setObjectName("ckBetrieblicheKlaeranlagen")
        self.ckButtons.addButton(self.ckBetrieblicheKlaeranlagen)
        self.verticalLayout_4.addWidget(self.ckBetrieblicheKlaeranlagen)
        self.ckOeffentlicheTankstellen = QtWidgets.QCheckBox(self.layoutWidget3)
        self.ckOeffentlicheTankstellen.setObjectName("ckOeffentlicheTankstellen")
        self.ckButtons.addButton(self.ckOeffentlicheTankstellen)
        self.verticalLayout_4.addWidget(self.ckOeffentlicheTankstellen)
        self.toolBox.addItem(self.toolBoxPage4, "")
        self.toolBoxPage5 = QtWidgets.QWidget()
        self.toolBoxPage5.setGeometry(QtCore.QRect(0, 0, 359, 159))
        self.toolBoxPage5.setObjectName("toolBoxPage5")
        self.layoutWidget4 = QtWidgets.QWidget(self.toolBoxPage5)
        self.layoutWidget4.setGeometry(QtCore.QRect(30, 10, 184, 140))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.ckNiederschlagmessstellen = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ckNiederschlagmessstellen.setObjectName("ckNiederschlagmessstellen")
        self.ckButtons.addButton(self.ckNiederschlagmessstellen)
        self.verticalLayout_5.addWidget(self.ckNiederschlagmessstellen)
        self.ckOberflaechenwassermessstellen = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ckOberflaechenwassermessstellen.setObjectName("ckOberflaechenwassermessstellen")
        self.ckButtons.addButton(self.ckOberflaechenwassermessstellen)
        self.verticalLayout_5.addWidget(self.ckOberflaechenwassermessstellen)
        self.ckGrundwassermessstellen = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ckGrundwassermessstellen.setObjectName("ckGrundwassermessstellen")
        self.ckButtons.addButton(self.ckGrundwassermessstellen)
        self.verticalLayout_5.addWidget(self.ckGrundwassermessstellen)
        self.ckQuellenmessstellen = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ckQuellenmessstellen.setObjectName("ckQuellenmessstellen")
        self.ckButtons.addButton(self.ckQuellenmessstellen)
        self.verticalLayout_5.addWidget(self.ckQuellenmessstellen)
        self.ckGrundwasserfelder = QtWidgets.QCheckBox(self.layoutWidget4)
        self.ckGrundwasserfelder.setObjectName("ckGrundwasserfelder")
        self.ckButtons.addButton(self.ckGrundwasserfelder)
        self.verticalLayout_5.addWidget(self.ckGrundwasserfelder)
        self.toolBox.addItem(self.toolBoxPage5, "")
        self.page_4 = QtWidgets.QWidget()
        self.page_4.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_4.setObjectName("page_4")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.page_4)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 10, 184, 101))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.ckEzFliessgewaesser = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ckEzFliessgewaesser.setObjectName("ckEzFliessgewaesser")
        self.ckButtons.addButton(self.ckEzFliessgewaesser)
        self.verticalLayout_8.addWidget(self.ckEzFliessgewaesser)
        self.ckEzOberflaechenwasserMesstellen = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ckEzOberflaechenwasserMesstellen.setObjectName("ckEzOberflaechenwasserMesstellen")
        self.ckButtons.addButton(self.ckEzOberflaechenwasserMesstellen)
        self.verticalLayout_8.addWidget(self.ckEzOberflaechenwasserMesstellen)
        self.ckEzQuellen = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ckEzQuellen.setObjectName("ckEzQuellen")
        self.ckButtons.addButton(self.ckEzQuellen)
        self.verticalLayout_8.addWidget(self.ckEzQuellen)
        self.ckEzWasserscheideRheinDonau = QtWidgets.QCheckBox(self.verticalLayoutWidget)
        self.ckEzWasserscheideRheinDonau.setObjectName("ckEzWasserscheideRheinDonau")
        self.ckButtons.addButton(self.ckEzWasserscheideRheinDonau)
        self.verticalLayout_8.addWidget(self.ckEzWasserscheideRheinDonau)
        self.toolBox.addItem(self.page_4, "")
        self.page = QtWidgets.QWidget()
        self.page.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page.setObjectName("page")
        self.layoutWidget5 = QtWidgets.QWidget(self.page)
        self.layoutWidget5.setGeometry(QtCore.QRect(20, 20, 325, 140))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.ckGewaessernetz2017Vlbg = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2017Vlbg.setObjectName("ckGewaessernetz2017Vlbg")
        self.ckButtons.addButton(self.ckGewaessernetz2017Vlbg)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2017Vlbg)
        self.ckGewaessernetz2017Umgebung = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2017Umgebung.setObjectName("ckGewaessernetz2017Umgebung")
        self.ckButtons.addButton(self.ckGewaessernetz2017Umgebung)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2017Umgebung)
        self.ckGewaessernetz2012Vlbg = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2012Vlbg.setObjectName("ckGewaessernetz2012Vlbg")
        self.ckButtons.addButton(self.ckGewaessernetz2012Vlbg)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2012Vlbg)
        self.ckGewaessernetz2012Umgebung = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2012Umgebung.setObjectName("ckGewaessernetz2012Umgebung")
        self.ckButtons.addButton(self.ckGewaessernetz2012Umgebung)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2012Umgebung)
        self.ckGewaessernetz2000Vlbg = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2000Vlbg.setEnabled(True)
        self.ckGewaessernetz2000Vlbg.setObjectName("ckGewaessernetz2000Vlbg")
        self.ckButtons.addButton(self.ckGewaessernetz2000Vlbg)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2000Vlbg)
        self.ckGewaessernetz2000Umgebung = QtWidgets.QCheckBox(self.layoutWidget5)
        self.ckGewaessernetz2000Umgebung.setEnabled(True)
        self.ckGewaessernetz2000Umgebung.setObjectName("ckGewaessernetz2000Umgebung")
        self.ckButtons.addButton(self.ckGewaessernetz2000Umgebung)
        self.verticalLayout_6.addWidget(self.ckGewaessernetz2000Umgebung)
        self.toolBox.addItem(self.page, "")
        self.page_5 = QtWidgets.QWidget()
        self.page_5.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_5.setObjectName("page_5")
        self.ckGewaesserbewirtschaftungsplan2015 = QtWidgets.QCheckBox(self.page_5)
        self.ckGewaesserbewirtschaftungsplan2015.setGeometry(QtCore.QRect(20, 20, 323, 17))
        self.ckGewaesserbewirtschaftungsplan2015.setObjectName("ckGewaesserbewirtschaftungsplan2015")
        self.ckButtons.addButton(self.ckGewaesserbewirtschaftungsplan2015)
        self.toolBox.addItem(self.page_5, "")
        self.page_3 = QtWidgets.QWidget()
        self.page_3.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_3.setObjectName("page_3")
        self.layoutWidget6 = QtWidgets.QWidget(self.page_3)
        self.layoutWidget6.setGeometry(QtCore.QRect(50, 10, 170, 134))
        self.layoutWidget6.setObjectName("layoutWidget6")
        self.formLayout = QtWidgets.QFormLayout(self.layoutWidget6)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout.setObjectName("formLayout")
        self.ckDirekteinleitungen = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckDirekteinleitungen.setObjectName("ckDirekteinleitungen")
        self.ckButtons.addButton(self.ckDirekteinleitungen)
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ckDirekteinleitungen)
        self.ckKontinuumsunterbrechungen = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckKontinuumsunterbrechungen.setObjectName("ckKontinuumsunterbrechungen")
        self.ckButtons.addButton(self.ckKontinuumsunterbrechungen)
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.ckKontinuumsunterbrechungen)
        self.ckSohleBoeschung = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckSohleBoeschung.setObjectName("ckSohleBoeschung")
        self.ckButtons.addButton(self.ckSohleBoeschung)
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.ckSohleBoeschung)
        self.ckStrukturzustand = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckStrukturzustand.setObjectName("ckStrukturzustand")
        self.ckButtons.addButton(self.ckStrukturzustand)
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.ckStrukturzustand)
        self.ckUfervegetation = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckUfervegetation.setObjectName("ckUfervegetation")
        self.ckButtons.addButton(self.ckUfervegetation)
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.ckUfervegetation)
        self.ckAbflussregime = QtWidgets.QCheckBox(self.layoutWidget6)
        self.ckAbflussregime.setObjectName("ckAbflussregime")
        self.ckButtons.addButton(self.ckAbflussregime)
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.ckAbflussregime)
        self.toolBox.addItem(self.page_3, "")
        self.page_2 = QtWidgets.QWidget()
        self.page_2.setGeometry(QtCore.QRect(0, 0, 98, 28))
        self.page_2.setObjectName("page_2")
        self.btnSeen = QtWidgets.QPushButton(self.page_2)
        self.btnSeen.setGeometry(QtCore.QRect(280, 105, 25, 25))
        font = QtGui.QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.btnSeen.setFont(font)
        self.btnSeen.setObjectName("btnSeen")
        self.layoutWidget7 = QtWidgets.QWidget(self.page_2)
        self.layoutWidget7.setGeometry(QtCore.QRect(20, 3, 256, 141))
        self.layoutWidget7.setObjectName("layoutWidget7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.layoutWidget7)
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.ckBodenseeAlles = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckBodenseeAlles.setEnabled(True)
        self.ckBodenseeAlles.setObjectName("ckBodenseeAlles")
        self.ckButtons.addButton(self.ckBodenseeAlles)
        self.verticalLayout_7.addWidget(self.ckBodenseeAlles)
        self.ckBodenseeWasserflaeche = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckBodenseeWasserflaeche.setEnabled(True)
        self.ckBodenseeWasserflaeche.setObjectName("ckBodenseeWasserflaeche")
        self.ckButtons.addButton(self.ckBodenseeWasserflaeche)
        self.verticalLayout_7.addWidget(self.ckBodenseeWasserflaeche)
        self.ckBodensee25m = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckBodensee25m.setEnabled(True)
        self.ckBodensee25m.setObjectName("ckBodensee25m")
        self.ckButtons.addButton(self.ckBodensee25m)
        self.verticalLayout_7.addWidget(self.ckBodensee25m)
        self.ckBodensee5m = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckBodensee5m.setEnabled(True)
        self.ckBodensee5m.setObjectName("ckBodensee5m")
        self.ckButtons.addButton(self.ckBodensee5m)
        self.verticalLayout_7.addWidget(self.ckBodensee5m)
        self.ckBodenseeUferlinie = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckBodenseeUferlinie.setEnabled(True)
        self.ckBodenseeUferlinie.setObjectName("ckBodenseeUferlinie")
        self.ckButtons.addButton(self.ckBodenseeUferlinie)
        self.verticalLayout_7.addWidget(self.ckBodenseeUferlinie)
        self.ckSeen = QtWidgets.QCheckBox(self.layoutWidget7)
        self.ckSeen.setEnabled(True)
        self.ckSeen.setObjectName("ckSeen")
        self.ckButtons.addButton(self.ckSeen)
        self.verticalLayout_7.addWidget(self.ckSeen)
        self.toolBox.addItem(self.page_2, "")
        self.pushButton = QtWidgets.QPushButton(frmWasser)
        self.pushButton.setGeometry(QtCore.QRect(30, 450, 101, 23))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(frmWasser)
        self.pushButton_2.setGeometry(QtCore.QRect(230, 450, 101, 23))
        self.pushButton_2.setObjectName("pushButton_2")

        self.retranslateUi(frmWasser)
        self.pushButton_2.clicked.connect(frmWasser.abbrechen)
        self.pushButton.clicked.connect(frmWasser.datenladen)
        self.btnSeen.clicked.connect(frmWasser.infobuttton)
        QtCore.QMetaObject.connectSlotsByName(frmWasser)

    def retranslateUi(self, frmWasser):
        _translate = QtCore.QCoreApplication.translate
        frmWasser.setWindowTitle(_translate("frmWasser", "Themenbereich Wasser"))
        self.ckQuellen.setText(_translate("frmWasser", "Quellen"))
        self.ckBrunnen.setText(_translate("frmWasser", "Brunnen"))
        self.ckSchutzSchongebiete.setText(_translate("frmWasser", "Schutz- und Schongebiete"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage1), _translate("frmWasser", "Wasserversorgung"))
        self.ckGWWaermepumpen.setText(_translate("frmWasser", "Grundwasserwärme-Pumpen"))
        self.ckErdwaermeanlagen.setText(_translate("frmWasser", "Erdwärmeanlagen"))
        self.ckKuehlwasseranlagenGW.setText(_translate("frmWasser", "Kühlwasseranlagen Grundwasser"))
        self.ckKuehlwasseranlagenOG.setText(_translate("frmWasser", "Kühlwasseranlagen Oberflächengewässer"))
        self.ckWeitereAnlagen.setText(_translate("frmWasser", "weitere Grundwasseranlagen (z.B. Versickerung)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage2), _translate("frmWasser", "Thermische Nutzung"))
        self.ckKraftwerke.setText(_translate("frmWasser", "Kraftwerke"))
        self.ckSonstigeBetriebe.setText(_translate("frmWasser", "Betriebe (z.B. Beschneiungsanlagen)"))
        self.ckGeschiebe.setText(_translate("frmWasser", "Geschieberückhalteeinrichtungen"))
        self.ckSonstigeAnlagen.setText(_translate("frmWasser", " Anlagen an Gewässern (z.B. Entnahmen)"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage3), _translate("frmWasser", "Wassernutzung / Schutzwasserbau"))
        self.ckKommunaleKlaeranlagen.setText(_translate("frmWasser", "Kommunale Kläranlagen"))
        self.ckKleinklaeranlagen.setText(_translate("frmWasser", "Kleinkläranalgen"))
        self.ckBetrieblicheKlaeranlagen.setText(_translate("frmWasser", "Betriebliche Kläranlagen"))
        self.ckOeffentlicheTankstellen.setText(_translate("frmWasser", "Öffentliche Tankstellen"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage4), _translate("frmWasser", "Abwasserentsorgung / Gefährdung"))
        self.ckNiederschlagmessstellen.setText(_translate("frmWasser", "Niederschlag-Messstellen"))
        self.ckOberflaechenwassermessstellen.setText(_translate("frmWasser", "Oberflächenwasser-Messstellen"))
        self.ckGrundwassermessstellen.setText(_translate("frmWasser", "Grundwasser-Messstellen"))
        self.ckQuellenmessstellen.setText(_translate("frmWasser", "Quellen-Messstellen"))
        self.ckGrundwasserfelder.setText(_translate("frmWasser", "Grundwasserfelder"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.toolBoxPage5), _translate("frmWasser", "Hydrographie"))
        self.ckEzFliessgewaesser.setText(_translate("frmWasser", "Fließgewässer"))
        self.ckEzOberflaechenwasserMesstellen.setText(_translate("frmWasser", "Oberflächenwasser - Messstellen"))
        self.ckEzQuellen.setText(_translate("frmWasser", "Quellen"))
        self.ckEzWasserscheideRheinDonau.setText(_translate("frmWasser", "Rhein Donau Wasserscheide"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_4), _translate("frmWasser", "Einzugsgebiete"))
        self.ckGewaessernetz2017Vlbg.setText(_translate("frmWasser", "Gewässernetz 2017 Vorarlberg"))
        self.ckGewaessernetz2017Umgebung.setText(_translate("frmWasser", "Gewässernetz 2017 Vorarlberg + Umgebung"))
        self.ckGewaessernetz2012Vlbg.setText(_translate("frmWasser", "Gewässernetz 2012 Vorarlberg"))
        self.ckGewaessernetz2012Umgebung.setText(_translate("frmWasser", "Gewaessernetz 2012 Vorarlberg + Umgebung"))
        self.ckGewaessernetz2000Vlbg.setText(_translate("frmWasser", "Gewässernetz 2000 Vorarlberg"))
        self.ckGewaessernetz2000Umgebung.setText(_translate("frmWasser", "Gewaessernetz 2000 Vorarlberg + Umgebung"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page), _translate("frmWasser", "Fließgewässer Netz (FGW)"))
        self.ckGewaesserbewirtschaftungsplan2015.setText(_translate("frmWasser", "NGP 2015"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_5), _translate("frmWasser", "Nationaler Gewässerbewirtschaftungsplan"))
        self.ckDirekteinleitungen.setText(_translate("frmWasser", "Direkteinleitungen"))
        self.ckKontinuumsunterbrechungen.setText(_translate("frmWasser", "Kontinuumsunterbrechungen"))
        self.ckSohleBoeschung.setText(_translate("frmWasser", "Sohle Böschung"))
        self.ckStrukturzustand.setText(_translate("frmWasser", "Strukturzustand"))
        self.ckUfervegetation.setText(_translate("frmWasser", "Ufervegetation"))
        self.ckAbflussregime.setText(_translate("frmWasser", "Abflussregime"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_3), _translate("frmWasser", "Fließgewässer Strukturgüte"))
        self.btnSeen.setText(_translate("frmWasser", "i"))
        self.ckBodenseeAlles.setText(_translate("frmWasser", "Bodensee -> alles"))
        self.ckBodenseeWasserflaeche.setText(_translate("frmWasser", "Bodensee -> nur Wasserfläche"))
        self.ckBodensee25m.setText(_translate("frmWasser", "Bodensee -> nur 25m Tiefenlinien"))
        self.ckBodensee5m.setText(_translate("frmWasser", "Bodensee -> nur 5m Tiefenlinien"))
        self.ckBodenseeUferlinie.setText(_translate("frmWasser", "Bodensee -> nur Uferlinie"))
        self.ckSeen.setText(_translate("frmWasser", "Andere Seen u. stehende Gewässer Vorarlbergs"))
        self.toolBox.setItemText(self.toolBox.indexOf(self.page_2), _translate("frmWasser", "Stehende Gewässer"))
        self.pushButton.setText(_translate("frmWasser", "Themen Laden"))
        self.pushButton_2.setText(_translate("frmWasser", "Schließen"))

