# -*- coding: utf-8 -*-
#!/usr/bin/python


from PyQt4 import QtGui,QtCore

from qgis.core import *
from qgis.gui import *
from gui_ladefortschritt import *

import sys

class LadefortschrittDialog(QtGui.QDialog,Ui_frmLadefortschritt):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        Ui_frmLadefortschritt.__init__(self)



        # Set up the user interface from Designer.
        self.setupUi(self)

