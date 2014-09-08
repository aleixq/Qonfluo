# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamcontrols.ui'
#
# Created: Mon Jun 30 21:08:43 2014
#      by: PyQt5 UI code generator 5.2.1
#

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon
from tcpStreamInfo import TcpStreamInfo

class StreamControls(object):
    """
    this class is the root of the plugins it has all plugins and also it is the responsable of adding a tab each time a plugin is added
    
    Attributes
    ----------
    plugins: dict{ (str)"pluginName": BasePlugin } 
        the dictionary of the plugin objects
    
    """
    def __init__(self):
        self.baseWidget=QWidget()
        self.setupUi(self.baseWidget)
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
        
    def addNotice(self):
        """
        Add notice about tcp streaming
        """
        self.tabWidget.addTab(TcpStreamInfo(), "Info")
    def addPlugin(self,plugin):
        """
        Adds a new widget that will be putted in a new tab
        PARAMETERS
        -----------
        plugin: BasePlugin
            the plugin to be added as a new tab
        """
        _translate = QCoreApplication.translate
        self.tabWidget.addTab(plugin.baseWidget, plugin.pluginName)
        self.plugins[plugin.pluginName]=plugin
        self.tabWidget.setTabText(self.tabWidget.indexOf(plugin.baseWidget), _translate("Form", plugin.pluginName))
    def bufferStall(self,plugin):
        """
        Reacts on some buffer stopped
        PARAMETERS
        ----------
        plugin : BasePlugin
            the plugin the buffer belongs
        """
        #CHANGE ICON YELLOW or RED LED...
        icon=self.tabWidget.style().standardIcon(  QStyle.SP_MessageBoxWarning )
        self.tabWidget.setTabIcon(  self.tabWidget.indexOf(plugin.baseWidget), icon )
        
    def fineStream(self,plugin):
        """
        Tells tabwidget that buffer is feeding ok
        PARAMETERS
        ----------
        plugin : BasePlugin
            the plugin the buffer belongs 
        """
        #CHANGE ICON YELLOW or RED LED...
        icon=self.tabWidget.style().standardIcon(QStyle.SP_MediaPlay)
        self.tabWidget.setTabIcon(  self.tabWidget.indexOf(plugin.baseWidget), icon  )
    def bufferStop(self,plugin):
        """
        Tells tabwidget that buffer is normally stopped
        PARAMETERS
        ----------
        plugin : BasePlugin
            the plugin the buffer belongs 
        """
        #Clears the icon...
        icon=QIcon()
        self.tabWidget.setTabIcon(  self.tabWidget.indexOf(plugin.baseWidget), icon  )        
