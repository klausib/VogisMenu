# -*- coding: utf-8 -*-
#!/usr/bin/python


from qgis.PyQt import QtGui, QtCore

from qgis.core import *
from qgis.gui import *
from gui_ladefortschritt import *

import sys

class LadefortschrittDialog(QtWidgets.QDialog,Ui_frmLadefortschritt):
    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        Ui_frmLadefortschritt.__init__(self)



        # Set up the user interface from Designer.
        self.setupUi(self)

