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
    """
    The base to subclass new plugins, it is an abstraction. 
    
    Attributes:
    -----------
    pluginName: str 
        the name of the plugin
    args: dict
        the additional args to pass to plugin
    protocol: str 
        the name of the protocol (alias of the pluginName)
    baseWidget: QWidget
        the one that will be fitted in the tab
    source: Gst.Element
        the source of the plugin side pipeline
    pipeline: Gst.PlayBin
        the plugin side pipeline
    startStream: QPushButton
        the button that will trigger the action of connectStream. Remember to call again the function connectStream if new button is created if you want to autoconnect button to handler
    state: int 
        the state of the plugin: 0 stopped, -1 stalled, 1 running
    
        
    """
    startStreamSig = pyqtSignal(['QString','QString']) #the signal emmitted when startStream Buttton is in True State
    stopStreamSig = pyqtSignal(['QString']) #the signal emmitted when startStream Buttton is in False State
    bufferStop = pyqtSignal() #Signal emitted when buffer is not filling because normal stop
    bufferStart = pyqtSignal() #Signal emitted when buffer is filling normally
    bufferStall = pyqtSignal() #Signal emitted when buffer has stalled, for example network disconnected
    def __init__(self, name, args, parent):
        """
        PARAMETERS:
        -----------
        name: str
            the plugin name
        args: dict
            the list of args to include to plugin
        parent: str 
            the mainwindow Object which contains GST playbins, and also window gui elements             
        """
        super().__init__(parent)
        #the Name of the plugin and also the name of the tab
        self.pluginName=name
        
        self.settings=QSettings('communia','qonfluo/'+self.pluginName)
        
        self.buffers=[]
        
        #The baseWidget, so the one that will be fitted in the tab
        self.baseWidget=QWidget() #We need this as plugin
        
        #The protocol used, alias of the name of the plugin
        self._protocol=name
        
        #The appsrc element 
        self._source=None
        
        #The Gst Pipeline
        self._pipeline=None
        
        #The additional args in list type:
        self.args=args
        
        #The state of the plugin: 0 stopped, -1 stalled, 1 running
        self._state=0
        
        #Stream Toggle Button
        self.startStream=QPushButton("Stream!")
        self.startStream.setCheckable(True)
        
        #Remember to call self.connectStream() again if new button created if you want to autoconnect button to handler
        self.connectStream()
    def writeSettings(self):
        """
        Defines the plugin conf file, implementing again will offer the mechanism to save the settings for each plugin, open the settings and attaching is out of scope
        """
        print("TODO save it")
        
        print(self.settings.fileName())
        self.settings.setValue('TODO','TODO')
        
    def getMenu(self,parent):
        """
        Sets the menu that will
        PARAMETERS:
        -----------
            parent: QMenuBar
                the menubar parent where menu will grow up
        RETURNS:
        -------
        QMenu object or None if not needed
        """
        menu=QMenu("BasePlugin",parent)
        actionOpenFME = QAction("Base plugin sample", self, shortcut="Ctrl+B",
                statusTip="base sample to be reimplemented",triggered=__str__)
        menu.addAction(actionOpenFME)
        
        return None
    
    def connectStream(self):
        """
        This will be the action to connect the stream button to the handler
        """
        self.startStream.toggled.connect(self.handleToggleStream)
        
    def getPlayBin(self):
        """
        Returns the pipeline to be injected through appsink tee if using queue named queue_stats_%pluginName% preceded by  identity named identity_stats_%spluginName% it will be used to collect stats. It's used in some plugins to estimate the used bandwidth if both elements are feeding the sink. Main pipeline sink Caps can be get automatically from main pipeline plugin sink using capsfilter name=plugin_caps_%pluginname%, useful if using shmsrc instead of tcpclientsrc
        """
        return "shmsrc name=%s ! queue name=queue_stats_%s ! identity name=identity_stats_%s sync=true ! fakesink " % self.pluginName
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
            self.state=1
        else:
            self.stopStreamSig.emit(self.pluginName)    
            self.state=0
    def bufferStopped(self):
        """
        invoked when buffer must be filled and it cannot
        """
        self.state=-1

    def setState(self,state):
        """
        Sets the streaming state of the plugin
        PARAMETERS:
        ----------
        state: int
            The code of the streaming buffer state 0 stopped, 1 playing, -1 stalled
        """
        self._state=state
        if self._state==0:
            self.bufferStop.emit()
            print("[%s] Buffer stopped..."%self.pluginName)
        if self._state==1:
            self.bufferStart.emit()
            print("[%s] Buffer filling started..."%self.pluginName)
        if self._state==-1:
            self.bufferStall.emit()
            print("[%s] Buffer stalled..."%self.pluginName)
    def getState(self):
        """
        Gets the streaming state of the plugin
        RETURNS:
        -------
        state: int
            The code of the streaming buffer state 0 stopped, 1 playing, -1 stalled        
        """
        return self._state
    
    source=property(getSource,setSource)
    pipeline=property(getPipeline,setPipeline)
    state=property(getState,setState)