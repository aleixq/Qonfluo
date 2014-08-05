# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamcontrols.ui'
#
# Created: Mon Jun 30 21:08:43 2014
#      by: PyQt5 UI code generator 5.2.1
#

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtCore import pyqtSignal
import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst


class BasePlugin(QObject):
    startStreamSig = pyqtSignal(['QString','QString']) #the signal emmitted when startStream Buttton is in True State
    stopStreamSig = pyqtSignal(['QString']) #the signal emmitted when startStream Buttton is in False State
    def __init__(self,name):
        super().__init__()
        #the Name of the plugin and also the name of the tab
        self.pluginName=name
        
        self.buffers=[]
        
        #The baseWidget, so the one that will be fitted in the tab
        self.baseWidget=QWidget() #We need this as plugin
        
        #The protocol used, alias of the name of the plugin
        self._protocol=name
        
        #The appsrc element 
        self._source=None
        
        #The Gst Pipeline
        self._pipeline=None

        
        #Stream Toggle Button
        self.startStream=QPushButton("Stream!")
        self.startStream.setCheckable(True)
        
        #Remember to call self.connectStream() again if new button created if you want to autoconnect button to handler
        self.connectStream()
        
    def connectStream(self):
        """
        This will be the action to connect the stream button to the handler
        """
        self.startStream.toggled.connect(self.handleToggleStream)
        
    def getPlayBin(self):
        """
        Returns the pipeline to be injected through appsink tee 
        """
        return "appsrc name=%s ! queue ! fakesink " % self.pluginName
    def getSource(self):
        """
        Gets the stored source
        """
        return self._source
    def setSource(self,source):
        """
        Stores the source of the pipeline
        """
        self._source=source
    def getPipeline(self):
        """
        Gets the stored pipeline(real gst)
        """
        return self._pipeline
    def setPipeline(self,pipeline):
        """
        Stores the source of the pipeline (real gst)
        """
        self._pipeline=pipeline       
    def handleToggleStream(self,state):
        """
        Will handle the Stream! button depending state
        """
        if state:
            self.startStreamSig.emit(self.pluginName, self.getPlayBin())
        else:
            self.stopStreamSig.emit(self.pluginName)    
    
    source=property(getSource,setSource)
    pipeline=property(getPipeline,setPipeline)