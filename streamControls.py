# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamcontrols.ui'
#
# Created: Mon Jun 30 21:08:43 2014
#      by: PyQt5 UI code generator 5.2.1
#

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *



class StreamControls(object):
    def __init__(self):
        self.baseWidget=QWidget()
        self.setupUi(self.baseWidget)
        self._protocol="rtmp"
        self.plugins={}
    def setupUi(self, Form):
        Form.setObjectName("Form")
        self.gridLayout = QGridLayout(Form)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QTabWidget(Form)
        self.tabWidget.setObjectName("tabWidget")
        
        self.gridLayout.addWidget(self.tabWidget, 1, 1, 1, 1)
        
        self.tabWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(Form)
    def addPlugin(self,plugin):
        """
        Adds a new widget that will be putted in a new tab
        """
        _translate = QCoreApplication.translate
        self.tabWidget.addTab(plugin.baseWidget, plugin.pluginName)
        self.plugins[plugin.pluginName]=plugin
        self.tabWidget.setTabText(self.tabWidget.indexOf(plugin.baseWidget), _translate("Form", plugin.pluginName))
