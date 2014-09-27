#! /usr/bin/env python3
# DEBUG with  GST_DEBUG=*:5
# DEBUG rtmpsink with just GST_DEBUG=rtmpsink:6
# to file: GST_DEBUG=*:5 qonfluo.py  > debug.log  2>&1
#

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst

# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo

from PyQt5.QtWidgets import QMainWindow, QWidget, QDockWidget, QApplication,QMenuBar,QGridLayout,QToolBar,QStatusBar,QVBoxLayout, QAction,QMenu,QLabel, QSlider,QCheckBox,QComboBox,QSpinBox,QFileDialog, QGraphicsDropShadowEffect
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage,QPixmap, QPalette,QIcon
from functools import partial
from qonfluo.plugPipe import PlugPipe

from qonfluo.streamControls import *


from qonfluo.rtmpPlugin import *
from qonfluo.recPlugin import *
from qonfluo.textBrowser import *
from qonfluo.imageBrowser import *

import argparse

import os
import sys


VERSION=0.1
SHMSINK=False #If using shmsink audio gets delayed and not functional... setting to False will use tcpserversink
PORT=14050

    
def getDataDir(toJoin):
    #TODO FIXME in qonfluo package
    libpath=os.environ['XDG_DATA_DIRS'].split(':')
    #Qt way to get it: QStandardPaths.standardLocations(QStandardPaths.GenericDataLocation)
    data_path=""
    for libpath in libpath:
        if os.path.exists(os.path.join(libpath,'qonfluo')):
            data_path=os.path.join(libpath,'qonfluo') 
    return os.path.join(data_path,toJoin) 

class VideoMixerConsole(QMainWindow):
    """
    QMainWindow 
    
    
    Attributes
    ----------
    deviceControls: dict{(int)"devvideoID":QWidget}
        Dictionary containing each main Widget for each v4l2 device    
    devicesGridLayout:dict{(int)"devvideoID":QGridLayout}
        Dictionary containing each gridLayout for each v4l2 device
    
    sinks:dict{(int)"devvideoID": GstVideoMixer2Pad}
        The dictionary containing each sink to Gst.mix
    sources:dict{(int)"devvideoID":Gst.Pad}
        The dictionary containing each video (v4l2src) source
    inputs: list[int]
        The list containing all the indexes of sources
    apps:dict{"pluginName":GstShmSink}
        The dictionary containing the sinks in main pipeline for each plugin
    appPipes: dict{"pluginName":Gst.Pipeline}
        The dictionary containing each Gst.Pipeline per plugin
    appPipesStrings:dict
        The dictionary containing each string per plugin
    monitors:dict{(int)"devvideoID":QWidget}
        Dictionary containing each Widget that will embed the monitor video canvas for each v4l2 device
    monitors_xid: dict{"monitorWin"+str((int)devindex):int}
        Dictionary containing each Widget WinID for each v4l2 device
    enabledDev: dict{(int)"devvideoID":QChackBox}
        Dictionary containing each enabling CheckBox for each v4l2 device
    sliderX:dict{(int)"devvideoID":QSlider}
        Dictionary containing each slider for X coord for each v4l2 device    
    sliderY:dict{(int)"devvideoID":QSlider}
        Dictionary containing each slider for Y coord for each v4l2 device       
    sliderAlpha:dict{(int)"devvideoID":QSlider}
        Dictionary containing each slider for Alpha for each v4l2 device       
    comboSize:dict{(int)"devvideoID":QCombobox}
        Dictionary containing each Combobox with sizes for each v4l2 device   
    zorders:dict{(int)"devvideoID":QSpinBox}
        Dictionary containing each Z Order spinbox for each v4l2 device           
    xid: int
        The main master pipeline mix Qwidget winId
    player: Gst.Pipeline
        The main master pipeline
    bus: Gst.Bus
        The main master pipeline Bus
    streamControls: StreamControls
        The object containing the stream controls of plugins
    startimage: str 
        The path to image to overlay
    textControl: TextBrowser
        The text overlay control widget
    imageControl: ImageControl
        The image overlay control widget
    """
    def __init__(self):
        super(VideoMixerConsole,self).__init__()
        self.settings=QSettings()
        container = QWidget()
        self.gridLayout = QGridLayout(container)                                                     
        self.gridLayout.setObjectName("gridLayout")        
        self.setCentralWidget(container)
        self.backCanvas=QWidget(self)
        self.backCanvas.setStyleSheet("border:1px solid #444;background-color:#bbb;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:1 rgba(100, 100, 100, 255), stop:0 rgba(150, 150, 150, 255));")
        self.gridLayout.addWidget(self.backCanvas, 0, 0, 1, 1)
        #self.canvasWin.setGeometry(QRect(530, 20, 256, 192))
        
        self.gridLayoutCanvas = QGridLayout(self.backCanvas)
        self.canvasWin=QWidget(self.backCanvas)
        self.canvasWin.setObjectName("canvasWin")
        self.canvasWin.setAttribute(0, 1); # AA_ImmediateWidgetCreation == 0
        self.canvasWin.setAttribute(3, 1); # AA_NativeWindow == 3
        self.canvasWin.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.canvasWin.setStyleSheet("border:0px solid black;background:transparent;")
        self.canvasWin.setContentsMargins(100, 100, 100, 100)   
        self.canvasW=1920
        self.canvasH=1080
        
        self.gridLayoutCanvas.addWidget(self.canvasWin, 0, 0, 1, 1)
        self.xid=self.canvasWin.winId()
        

        #MENUS
        
        self.menuBar = QMenuBar(self)
        self.menuBar.setGeometry(QRect(0, 0, 1331, 150))
        self.menuBar.setObjectName("menuBar")
        
        self.menuMenu = QMenu(self.menuBar)
        self.menuMenu.setObjectName("menuMenu")
        self.menuHelp = QMenu(self.menuBar)
        self.menuHelp.setObjectName("menuHelp")
      
        self.mainToolBar = QToolBar("ToolBar",self)
        self.addToolBar(self.mainToolBar)
        self.statusBar=QStatusBar(self)
        self.setStatusBar(self.statusBar)
        
        self.actionOpenConf = QAction("O&pen configuration", self, shortcut="Ctrl+O",
                statusTip="Open configuration", triggered=partial(self.openSettings,True) )
        self.actionSaveConf = QAction("S&ave configuration", self, shortcut="Ctrl+S",
                statusTip="Saves the current configuration", triggered=partial(self.writeSettings,True) )
        
        
        self.actionSetImage=QAction(self)
        self.actionSetImage.setObjectName("Set image overlay")

        self.actionSetText=QAction(self)
        self.actionSetText.setObjectName("Get text overlay")
        
        self.actionQuit = QAction("E&xit", self, shortcut="Ctrl+Q",
                statusTip="Exit the application", triggered=self.close)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout = QAction(self)
        self.actionAbout.setObjectName("actionAbout")
        self.actionAboutQt = QAction(self)
        self.actionAboutQt.setObjectName("actionAboutQt")
        self.menuMenu.addAction(self.actionOpenConf)
        self.menuMenu.addAction(self.actionSaveConf)
        self.menuMenu.addAction(self.actionSetImage)    
        self.menuMenu.addAction(self.actionSetText)
        self.menuMenu.addAction(self.actionQuit)
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAboutQt)
        self.menuBar.addAction(self.menuMenu.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())
        plugSeparator=QAction("Plugins:",self)
        plugSeparator.setEnabled(False)
        self.menuBar.addAction(plugSeparator)
        self.menuBar.addSeparator()


        self.actionAbout.triggered.connect(self.about)
        self.actionAboutQt.triggered.connect(self.aboutQt)
        
        

        #Canvas size controls
        self.dockWidgetCanvas = QDockWidget("Canvas params",self)
        self.dockWidgetCanvasContent=QWidget()
        self.canvasVerticalLayout=QVBoxLayout(self.dockWidgetCanvasContent)
        self.addDockWidget(Qt.DockWidgetArea(2), self.dockWidgetCanvas)
        self.addCanvasControls()
        self.dockWidgetCanvas.setWidget(self.dockWidgetCanvasContent)

        #Nth video parameter
        self.dockWidget_2 = QDockWidget("Video Inputs",self)
        self.dockWidgetContents_2 = QWidget()
        self.devicesVerticalLayout=QHBoxLayout(self.dockWidgetContents_2)
        self.addDockWidget(Qt.DockWidgetArea(8), self.dockWidget_2)
        
        #Stream controls
        self.dockWidgetStream = QDockWidget("Stream params",self)
        self.dockWidgetStreamContent=QWidget()
        self.streamVerticalLayout=QVBoxLayout(self.dockWidgetStreamContent)
        self.addDockWidget(Qt.DockWidgetArea(8), self.dockWidgetStream)
        self.appTimers = {} 
        self.addStreamControls()
        self.dockWidgetStream.setWidget(self.dockWidgetStreamContent)
        

        
        #Additional Artifacts
        self.dockWidget_artsI = QDockWidget("Image O/L",self)
        self.dockWidgetContents_artsI = QWidget()
        self.artsVerticalLayoutI=QVBoxLayout(self.dockWidgetContents_artsI)
        self.addDockWidget(Qt.DockWidgetArea(1), self.dockWidget_artsI)
        #Additional Artifacts II
        self.dockWidget_artsII = QDockWidget("Text O/L",self)
        self.dockWidgetContents_artsII = QWidget()
        self.artsVerticalLayoutII=QVBoxLayout(self.dockWidgetContents_artsII)
        self.tabifyDockWidget(self.dockWidget_artsI,self.dockWidget_artsII)
        
        self.deviceControls={}
        self.devicesGridLayout={}
        self.sinks={}
        self.sources={}
        self.inputs=[]
        
        self.plugEndpoints={}
        self.appPipes={}
        self.appPipesStrings={}
        
        self.monitors={}
        self.monitors_xid={}
        self.enabledDev={}
        self.switchers={}
        self.sliderX={}
        self.sliderY={}
        self.sliderAlpha={}
        self.comboSize={}
        self.zorders={}
        self.constrainers={}
               
        self.FMEprofile=False
        self.startimage=getDataDir("images/empty.png") #NOTE: Should be in QStandardPaths.standardLocations(QStandardPaths.DataLocation) when packaged
        
        self.dockWidget_2.setWidget(self.dockWidgetContents_2)   
        self.dockWidget_artsI.setWidget(self.dockWidgetContents_artsI)
        self.dockWidget_artsII.setWidget(self.dockWidgetContents_artsII)
        
        self.setMenuBar(self.menuBar)
 
        self.show()
        self.retranslateUi()

    def retranslateUi(self):
        """
        Translates the Ui
        """
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "Qonfluo"))
        self.menuMenu.setTitle(_translate("MainWindow", "Menu"))
        self.menuHelp.setTitle(_translate("MainWindow", "Help"))
        self.actionSetImage.setText(_translate("MainWindow","Set image overlay"))
        self.actionSetText.setText(_translate("MainWindow","Get text overlay"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout.setText(_translate("MainWindow", "About"))
        self.actionAboutQt.setText(_translate("MainWindow", "About Qt"))
    def writeSettings(self,saveToFile=False):
        """
        Writes the current state of inputs, images, canvas, etc. and  finally fires the writeSettings method for each plugin
        PARAMETERS:
        -----------
        saveToFile: bool
            if save to custom file is need
        """
        if saveToFile:
            fileName, _ = QFileDialog.getSaveFileUrl(self,caption=self.tr("Save File"), directory=QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0])
            if fileName:
                print("Saving configuration as %s"%fileName.toString())
                settings=QSettings(fileName.toLocalFile() , QSettings.IniFormat)
                if not settings.isWritable():
                    QMessageBox.critical(self,"Bad,Bad","Could Not save the file in %s, check you can do that there"%fileName.toLocalFile())
                    return
            else:
                return
        else:
            settings=self.settings
        settings.clear()
        settings.beginGroup("mainwindow")
        settings.setValue('size', self.size())
        settings.setValue('pos', self.pos())
        settings.setValue('version',VERSION)
        settings.endGroup()
        settings.beginGroup("canvas")
        settings.setValue('size',self.canvasSize.currentText())
        settings.endGroup()
        settings.beginGroup("background")
        settings.setValue('size',self.backgroundSize.currentText())
        settings.endGroup()        
        settings.beginGroup("Artifacts")
        settings.beginGroup("ImageOverlay")
        settings.setValue('alpha',self.imageControl.sliderAlpha.value())
        settings.setValue('x',self.imageControl.sliderX.value())
        settings.setValue('y',self.imageControl.sliderY.value())
        settings.setValue('size',self.imageControl.comboSize.currentText())    
        if self.player:
            m = self.player.get_by_name ("imageOverlay_96")
            filename=m.get_property("location")
            settings.setValue('file',filename)
        settings.setValue('enabled',self.imageControl.enabledDev.checkState())  
        settings.endGroup()        
        settings.endGroup()
        
        #Inputs Settings
        settings.beginGroup('Inputs')
        for video in self.videoDevs:
            vid=self.videoDevs[video]['id']
            interface=self.videoDevs[video]['interface']
            settings.beginGroup(interface)
            settings.setValue('alpha',self.sliderAlpha[vid].value())
            settings.setValue('x',self.sliderX[vid].value())
            settings.setValue('y',self.sliderY[vid].value())
            settings.setValue('z',self.zorders[vid].value()) 
            settings.setValue('size',self.comboSize[vid].currentText())
            settings.setValue('enabled',self.enabledDev[vid].checkState())            
            settings.endGroup()
        settings.endGroup()
        
        for plugin in self.streamControls.plugins:
            self.streamControls.plugins[plugin].writeSettings()
            
    def openSettings(self,fromFile=False):
        """
        Opens a configuration of state of inputs, images, canvas, etc.
        PARAMETERS:
        -----------
        saveToFile: bool
            if save to custom file is need
        """
        if fromFile:
            fileName, _ = QFileDialog.getOpenFileUrl(self,caption=self.tr("Open File"), directory=QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0])
            if fileName:
                print("Saving configuration as %s"%fileName.toString())
                settings=QSettings(fileName.toLocalFile() , QSettings.IniFormat)
            else:
                return
        else:
            settings=self.settings
        settings.beginGroup("mainwindow")
        self.resize(settings.value("size", QSize(1280, 720)))
        self.move(settings.value('pos', self.pos()))
        settings.endGroup()
        settings.beginGroup("canvas")
        #self.setCanvasSize(self.canvasSize.findText( settings.value('size',self.canvasSize.currentText())))
        self.canvasSize.setCurrentText( settings.value('size',self.canvasSize.currentText() )  )
        settings.endGroup()
        settings.beginGroup("background")
        #self.setBackgroundSize( self.backgroundSize.findText( settings.value('size',self.backgroundSize.currentText()) ) )
        self.backgroundSize.setCurrentText( settings.value('size',self.backgroundSize.currentText() )  )
        settings.endGroup()        
        settings.beginGroup("Artifacts")
        settings.beginGroup("ImageOverlay")
        
        self.imageControl.sliderAlpha.setValue(int( settings.value('alpha',self.imageControl.sliderAlpha.value()) )) 
        self.imageControl.sliderX.setValue(int( settings.value('x',self.imageControl.sliderX.value()) ) )
        self.imageControl.sliderY.setValue(int( settings.value('y',self.imageControl.sliderY.value()) ) )
        self.imageControl.comboSize.setCurrentText( settings.value('size',self.imageControl.comboSize.currentText()) ) 
        self.imageControl.enabledDev.setChecked( bool(settings.value('enabled',self.imageControl.enabledDev.checkState()) ) )  
        m = self.player.get_by_name ("imageOverlay_96")
        filename=m.get_property("location")        
        self.imageControl.setImage(settings.value('file', filename ))
        settings.endGroup()        
        settings.endGroup()
        
        #Inputs Settings
        settings.beginGroup('Inputs')
        for video in self.videoDevs:
            vid=self.videoDevs[video]['id']
            interface=self.videoDevs[video]['interface']

            if interface in settings.childGroups():
                print("found present interface in settings")
                settings.beginGroup(interface)            
                self.sliderAlpha[vid].setValue(int( settings.value('alpha',self.sliderAlpha[vid].value()) )) 
                self.sliderX[vid].setValue(int( settings.value('x',self.sliderX[vid].value()) ) )
                self.sliderY[vid].setValue(int( settings.value('y',self.sliderY[vid].value()) ) )
                self.zorders[vid].setValue(int( settings.value('z',self.zorders[vid].value()) ) )
                self.comboSize[vid].setCurrentText( settings.value('size',self.comboSize[vid].currentText()) ) 
                self.enabledDev[vid].setChecked( bool(settings.value('enabled',self.enabledDev[vid].checkState())) )                  
                settings.endGroup()
        settings.endGroup()        
        
    def closeEvent(self, event):
        """
        Reacts when users press exit.
        Parameters:
        -----------
        event: QCloseEvent
        """
        
        if not self.isStreaming():
            self.player.send_event(Gst.Event.new_eos())            
            #self.bus.disconnect_by_func(self.on_eos_message)
            #self.bus.disconnect_by_func(self.on_error_message)
            #self.bus.disconnect_by_func(self.on_sync_message)
            #self.bus.remove_signal_watch()
            #self.bus.set_sync_handler(None)
            ##TODO disconnect apps buses and monitors
            ##self.player.set_state(Gst.State.NULL)
            #self.bus = None
            #self.player = None            
            self.writeSettings()
            event.accept()
        else:
            QMessageBox.critical(self,"Pipe is streaming","Could not exit application while streaming, stop pipe before")
            event.ignore()  
    def isStreaming(self):
        """
        Asks if it is streaming
        """
        return self.player.current_state == Gst.State.PLAYING                        
            
    def listDevs(self):
        """
        Creates and return a list of all devices that v4l2 has created, and also fulfills the dictionary adding relevant info about each device
        """
        vds={}
        videoId=0
        if args.devices:
            wishDevs=args.devices.split(",")
        else:
            wishDevs=[None]
        for vd in os.listdir("/sys/class/video4linux/"):
            if not wishDevs==[None] and vd not in wishDevs:
                continue
            with open('/sys/class/video4linux/'+vd+'/name','r') as f: interf = f.read()
            vds[vd]={
                'interface': interf,
                'id': videoId,
                
                #TODO: add metainfo about v4l2
                }
            videoId=videoId+1
        return vds
    def addStreamControls(self):
        """
        Add Streaming Controls
        """
        self.streamControls=StreamControls()
        self.streamVerticalLayout.addWidget(self.streamControls.baseWidget)
        
        #Add plugins:
        
        for plugDesc in PLUGINS:
            plugin=plugDesc['class'](plugDesc['name'],plugDesc['args'],parent=self)
            self.streamControls.addPlugin(plugin)
            #Connect the start and stop buttons
            plugin.startStreamSig.connect(self.connectApp)
            plugin.stopStreamSig.connect(self.stopApp)
            self.appTimers[plugDesc['name']] = QTimer()
            self.appTimers[plugDesc['name']].timeout.connect(plugin.bufferStopped)  
            plugin.bufferStall.connect(partial(self.streamControls.bufferStall,plugin)) # Change Led color
            plugin.bufferStart.connect(partial(self.streamControls.fineStream,plugin)) # Change Led color
            plugin.bufferStop.connect(partial(self.streamControls.bufferStop,plugin)) # Change Led color
            #Add plugin menu if any
            menu=plugin.getMenu(self.menuBar)
            if menu:
                self.menuBar.addMenu(menu)
                self.menuBar.addAction(menu.menuAction())
        self.streamControls.addNotice()
    def addCanvasControls(self):
        """
        Add canvas controls
        """
        self.canvasControls=QWidget(self.dockWidgetCanvas)
        self.canvasCtlGridLayout=QGridLayout(self.canvasControls)
        
        #Start Pipe control
        self.enablePipe=QCheckBox("Start Pipe")
        self.enablePipe.stateChanged.connect(partial( self.togglePipe ))
        self.canvasCtlGridLayout.addWidget(self.enablePipe, 0, 0, 1, 3)
        
        #Canvas Size Control
        self.canvasSizeLabel=QLabel("Canvas size")
        self.canvasCtlGridLayout.addWidget(self.canvasSizeLabel, 1, 0, 1, 1)
        self.canvasSize=QComboBox(self)
        self.canvasSize.setEditable(True)
        self.canvasCtlGridLayout.addWidget(self.canvasSize, 1, 1, 1, 2)
        self.fillCanvasSizes(False)
        self.canvasSize.currentIndexChanged.connect(partial( self.setCanvasSize) )
        
        #Background (layer1)Size Control
        self.backgroundSizeLabel=QLabel("Background size")
        self.canvasCtlGridLayout.addWidget(self.backgroundSizeLabel, 2, 0, 1, 1)
        self.backgroundSize=QComboBox(self)
        self.backgroundSize.activated.connect(partial( self.setBackgroundSize) )
        self.canvasCtlGridLayout.addWidget(self.backgroundSize, 2, 1, 1, 2)
        self.fillBackgroundSizes(False)
       
        
        self.canvasVerticalLayout.addWidget(self.canvasControls)
        
    def fillCanvasSizes(self,discover):
        """
        fills the allowed canvas background size specified by @value and if it is not depending upon the discovering streamsink, THIS IS THE GENERAL STREAM CAPS that will be tee'd
        Parameters:
        -----------
        discover: bool
            If it must discover the backgrounds sizes or not (TODO)             
        """
        canvasSizes=[
             {1920:1080},
             {1366:768},
             {1366:720},
             {1280:720},
             {960:540},
             {848:480},
             {640:480},
             {640:360},
             {424:240},
             {352:288},
             {320:240},
             {176:144},
             {160:120},
            ]
        if discover==False:
            for s in canvasSizes:
                (width,height)=s.popitem()
                self.canvasSize.addItem( "%sx%s"% (width, height),
                QVariant("video/x-raw, format=(string)I420, pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, framerate=(fraction)30/1,width=(int)%s,height=(int)%s"%(width, height))
                )
        else:
            bg=self.player.get_by_name("backgroundsrc")
            print ("#TODO: create discover depending on sink") #TODO DISCOVER SIZES self.comboSize[devindex].addItem( "%sx%s"% (width, height) , QVariant(caps.get_structure(i).to_string()))
    def fillBackgroundSizes(self,discover):
        """
        fills the allowed canvas background size specified by @value and if it is not depending upon the discovering streamsink
        Parameters:
        -----------
        discover: bool
            If it must discover the backgrounds sizes or not (TODO)          
        """
        backgroundSizes=[
             {1920:1080},
             {1366:768},
             {1366:720},
             {1280:720},
             {960:540},
             {848:480},
             {640:480},
             {640:360},
             {424:240},
             {352:288},
             {320:240},
             {176:144},
             {160:120},
            ]
        if discover==False:
            for s in backgroundSizes:
                (width,height)=s.popitem()
                self.backgroundSize.addItem( "%sx%s"% (width,height) ,QVariant("video/x-raw,width=(int)%s,height=(int)%s"%(width, height)))                    
        else:
            print ("#TODO: create discover depending on sink") #TODO DISCOVER SIZES QVariant(caps.get_structure(i).to_string()))            
    def canvas_send_back(self):
        """
        Send the background to background
        """
        self.testSink.set_property("zorder", 0)          
    def addCanvasSize(self,width,height):
        """
        Adds a new canvas size checking if exists, and selecting this new size after. Useful for example when constraining canvas sizes from a plugin.
        PARAMETERS:
        -----------
        width: int
        height:int
        """
        if self.canvasSize.findText("%sx%s"%(width,height) )== -1:
            self.canvasSize.addItem( "%sx%s"% (width, height) , QVariant("video/x-raw,format=(string)I420, pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, framerate=(fraction)30/1, width=(int)%s,height=(int)%s"% (width, height) ))
            self.canvasSize.setCurrentIndex(self.canvasSize.findText("%sx%s"%(width,height) ) ) 
        else:
            self.canvasSize.setCurrentIndex(self.canvasSize.findText("%sx%s"%(width,height) ) )        
    def setCanvasSize(self,value):
        """
        Sets the canvas size specified by @value
        Parameters:
        -----------
        value: int
            the size value of the qcombobox        
        """
        #First make sure to set every caps that we input but size to common
        for videodev in self.videoDevs:
            devindex=self.videoDevs[videodev]['id']        
            self.twSize(self.comboSize[devindex].currentIndex(),devindex)
        
        
        if hasattr(self, "player"):
            bg=self.player.get_by_name("backgroundsrc").srcpad    
            print ("setting canvas box to %s" % self.canvasSize.itemData(value) )
            newCapString=self.canvasSize.itemData(value)
            #Check if its a new user input value if it is use some hardcoded values
            if not newCapString: 
                wxh=self.canvasSize.currentText().split("x")
                width=wxh[0]
                height=wxh[1]
                newCapString= "video/x-raw, format=(string)I420, pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, width=(int)%s, height=(int)%s,framerate=(fraction)30/1" %(width,height) #Hard coding 30/1 to simplify and is mostly used                 
            #Pass the new coordinates maximums to source controls:
            (width,height)=self.canvasSize.currentText().split("x")
            for sourceid in self.inputs:
                self.sliderX[sourceid].setMaximum(int(width)/10)
                self.sliderY[sourceid].setMaximum(int(height)/10)      
            self.imageControl.setMaximums((width,height))
            
            #Set  main caps
            self.canvasW=int(width)
            self.canvasH=int(height)
            
            #Finally set the new canvas caps    
            newCaps=Gst.caps_from_string(newCapString)
            if (bg.query_accept_caps(newCaps) ):
                self.canvasCaps.set_property("caps",newCaps)
    def setBackgroundSize(self,value):
        """
        Sets the background size specified by @value
        Parameters:
        -----------
        value: int
            the value of the qslider        
        """
        bg=self.player.get_by_name("backgroundsrc").srcpad    
        print ("setting background to (layer 1) %s" % self.backgroundSize.itemData(value) )
        newCapString=self.backgroundSize.itemData(value)
        #Check if its a new user input value if it is use some hardcoded values
        if not newCapString: 
            wxh=self.backgroundSize.currentText().split("x")
            width=wxh[0]
            height=wxh[1]
            newCapString= "video/x-raw, format=(string)I420, pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, width=(int)%s, height=(int)%s,framerate=(fraction)30/1" %(width,height) #Hard coding 30/1 to simplify and is mostly used           
        newCaps=Gst.caps_from_string(newCapString)
        if (bg.query_accept_caps(newCaps) ):
            self.player.get_by_name("bgcaps").set_property("caps",newCaps)        

    def addVideoControls(self):
        """
        Adds all the controls  for each scanned video devices
        """
        for videodev in sorted(self.videoDevs):
            self.addSourceControl(self.videoDevs[videodev]['id'],self.videoDevs[videodev]['interface'])

    def addSourceControl(self,devindex,name):
        """
        Add controls for @devindex source
        Parameters
        ----------
        devindex:int
            the index of the source (if video equals to video device)
            98 in case of image
        name: string
            the name of the source
        """
        m = self.player.get_by_name ("mix")
        self.sinks[devindex]=m.get_static_pad("sink_"+str(devindex))
        source=self.player.get_by_name ("vsrc"+str(devindex))
        self.sources[devindex]=source.srcpad
        self.inputs.append(devindex)
        nonStandardInputs=[96,97,98]

        self.deviceControls[devindex]=QWidget(self.dockWidgetContents_2)
        self.devicesGridLayout[devindex] =QGridLayout(self.deviceControls[devindex])
        sourceName=QLabel(name)
        self.devicesGridLayout[devindex].addWidget(sourceName,0,0,1,6)
        
        if not devindex in nonStandardInputs :
            #sets the Monitor of Video
            destinationSpace=self.devicesVerticalLayout
            self.monitors[devindex]=QWidget()
            self.monitors[devindex].setMinimumSize(160, 120);
            self.monitors[devindex].setStyleSheet("border:1px solid #444;background-color:#bbb;background: qlineargradient(spread:pad, x1:0, y1:0, x2:0, y2:1, stop:1 rgba(100, 100, 100, 255), stop:0 rgba(150, 150, 150, 255));")
            self.monitors_xid["monitorWin"+str(devindex)]=self.monitors[devindex].winId()
            self.devicesGridLayout[devindex].addWidget(self.monitors[devindex], 1, 0, 1, 6)
        
        #Enable Control
        self.enabledDev[devindex]=QCheckBox("Enabled")
        
        self.enabledDev[devindex].setChecked(True)
        self.enabledDev[devindex].stateChanged.connect(partial( self.toggleDevice, devindex=devindex ))
        self.devicesGridLayout[devindex].addWidget(self.enabledDev[devindex], 2, 0, 1, 6)
        
        #Switch properties to other device
        if not devindex in nonStandardInputs and len(self.videoDevs)>1:
            switchLabel=QLabel("switch props with")
            self.devicesGridLayout[devindex].addWidget(switchLabel, 3, 0, 1, 1)
            videoDevs=[(str(self.videoDevs[x]['interface']),str(self.videoDevs[x]['id'])) for x in self.videoDevs if self.videoDevs[x]['id'] != devindex]
            self.switchers[devindex]=QComboBox()
            [self.switchers[devindex].addItem(interf,idv) for interf,idv in videoDevs]
            self.switchers[devindex].activated[int].connect(partial( self.switchDevices, devindex ) )
            self.devicesGridLayout[devindex].addWidget(self.switchers[devindex], 3, 1, 1, 5 )
        

        #Alpha Control
        self.sliderAlpha[devindex] = QSlider(Qt.Horizontal, self)
        self.sliderAlpha[devindex].setFocusPolicy(Qt.StrongFocus)
        self.sliderAlpha[devindex].setTickPosition(QSlider.TicksBothSides)
        self.sliderAlpha[devindex].setSliderPosition(100)
        self.sliderAlpha[devindex].setTickInterval(10)
        self.sliderAlpha[devindex].setSingleStep(1)
        self.sliderAlpha[devindex].valueChanged.connect(partial(self.twAlpha, devindex=devindex) )
        alphaLabel=QLabel("<small>Alpha</small>")
        self.devicesGridLayout[devindex].addWidget(alphaLabel, 4, 0, 1, 1)
        self.devicesGridLayout[devindex].addWidget(self.sliderAlpha[devindex], 4, 1, 1, 5)
        
        
        #X position
        self.sliderX[devindex] = QSlider(Qt.Horizontal, self)
        self.sliderX[devindex].setFocusPolicy(Qt.StrongFocus)
        self.sliderX[devindex].setTickPosition(QSlider.TicksBothSides)
        self.sliderX[devindex].setTickInterval(10)
        self.sliderX[devindex].setSingleStep(1)
        self.sliderX[devindex].valueChanged.connect(partial( self.twX, devindex=devindex ))
        XLabel=QLabel("<small>X</small>")
        self.devicesGridLayout[devindex].addWidget(XLabel, 5, 0, 1, 1)
        self.devicesGridLayout[devindex].addWidget(self.sliderX[devindex], 5, 1, 1, 5)

        #Y position
        self.sliderY[devindex] = QSlider(Qt.Horizontal, self)
        self.sliderY[devindex].setFocusPolicy(Qt.StrongFocus)
        self.sliderY[devindex].setTickPosition(QSlider.TicksBothSides)
        self.sliderY[devindex].setTickInterval(10)
        self.sliderY[devindex].setSingleStep(1)
        self.sliderY[devindex].valueChanged.connect(partial( self.twY, devindex=devindex ))
        YLabel=QLabel("<small>Y</small>")
        self.devicesGridLayout[devindex].addWidget(YLabel, 6, 0, 1, 1)
        self.devicesGridLayout[devindex].addWidget(self.sliderY[devindex], 6, 1, 1, 5)
        
       
        #Z-order
        self.zorders[devindex]= QSpinBox(self)
        self.zorders[devindex].setValue(devindex+1)
        ZLabel=QLabel("<small>Z</small>")
        self.devicesGridLayout[devindex].addWidget(ZLabel, 8, 0, 1, 3)
        self.devicesGridLayout[devindex].addWidget(self.zorders[devindex], 8, 3, 1, 3)
        self.zorders[devindex].valueChanged.connect(partial( self.twZ, devindex=devindex ) )
        self.sinks[devindex].set_property("zorder", devindex+1) #SET INITIAL Z-ORDER

        #formats combo
        self.comboSize[devindex]= QComboBox(self)
        self.comboSize[devindex].setEditable(True)     
        self.comboSize[devindex].setToolTip(self.tr("Write size in format weightxheight (for example: 1920x1080) to change resolution"))
        if not devindex in nonStandardInputs:
            self.devicesGridLayout[devindex].addWidget(self.comboSize[devindex], 9, 1, 1, 4)
        else:
            self.devicesGridLayout[devindex].addWidget(self.comboSize[devindex], 9, 1, 1, 5)
        self.comboSize[devindex].activated.connect(partial( self.twSize, devindex=devindex ) )
        labelSize=QLabel("Size")
        self.devicesGridLayout[devindex].addWidget(labelSize, 9, 0, 1, 1)
        #Constrain button
        if not devindex in nonStandardInputs:
            self.constrainers[devindex]= QPushButton("^")
            self.constrainers[devindex].setToolTip(self.tr("Pushes the actual video size to canvas size"))
            self.constrainers[devindex].setMaximumWidth(50)
            self.constrainers[devindex].setMaximumHeight(50)
            self.devicesGridLayout[devindex].addWidget(self.constrainers[devindex], 9, 5, 1, 1)
            self.constrainers[devindex].clicked.connect(partial( self.constrainToDevice, devindex=devindex ) )        

        destinationSpace.addWidget(self.deviceControls[devindex])  

    def addTextOverlay(self):
        """
        Adds the text overlay
        """
        devindex=97
        source=self.player.get_by_name ("textOverlay_"+str(devindex))
        
        self.deviceControls[devindex]=QWidget(self.dockWidgetContents_2)
        self.devicesGridLayout[devindex] =QGridLayout(self.deviceControls[devindex])
        sourceName=QLabel("Text Overlay")
        self.devicesGridLayout[devindex].addWidget(sourceName,0,0,1,6)

        destinationSpace=self.artsVerticalLayoutII
        
        self.textControl=TextBrowser(source)
        self.actionSetText.triggered.connect(self.textControl.addStringsFromFile)
        
        self.devicesGridLayout[devindex].addWidget(self.textControl,1,0,1,6)
        destinationSpace.addWidget(self.deviceControls[devindex]) 
    def addImageOverlay(self):
        """
        Adds Image overlay
        """
        devindex=96
        source=self.player.get_by_name ("imageOverlay_"+str(devindex))
        
        self.deviceControls[devindex]=QWidget(self.dockWidgetContents_2)
        self.devicesGridLayout[devindex] =QGridLayout(self.deviceControls[devindex])
        sourceName=QLabel("Image Overlay")
        self.devicesGridLayout[devindex].addWidget(sourceName,0,0,1,6)

        destinationSpace=self.artsVerticalLayoutI
        
        self.imageControl=ImageBrowser(source)
        self.imageControl.setImage(source.get_property("location"))        
        self.actionSetImage.triggered.connect(self.imageControl.setImage)

        self.devicesGridLayout[devindex].addWidget(self.imageControl,1,0,1,6)
        destinationSpace.addWidget(self.deviceControls[devindex])             
    def constrainToDevice(self,devindex):
        """
        Constrain the canvas to this device resizing canvas and z-order to the device specified by devindex
        Parameters
        ----------
        devindex:int
            the index of the source (if video equals to video device)
        
        """
        (width,height)=self.comboSize[devindex].currentText().split("x")
        self.twX(0,devindex)
        self.twY(0,devindex)
        self.twZ(99,devindex)
        
        if self.canvasSize.findText("%sx%s"%(width,height) )== -1:
            self.canvasSize.addItem( "%sx%s"% (width, height) , QVariant("video/x-raw,format=(string)I420, pixel-aspect-ratio=(fraction)1/1, interlace-mode=(string)progressive, framerate=(fraction)30/1, width=(int)%s,height=(int)%s"% (width, height) ))
            self.canvasSize.setCurrentIndex(self.canvasSize.findText("%sx%s"%(width,height) ) ) 
        else:
            self.canvasSize.setCurrentIndex(self.canvasSize.findText("%sx%s"%(width,height) ) )        
    def get_caps(self):
        """
        Gets capabilities for each videodevice and adds i420 caps to combobox 
        """
        for videodev in self.videoDevs:
            devindex=self.videoDevs[videodev]['id']
            source=self.player.get_by_name ("vsrc"+str(devindex))
            self.sources[devindex]=source.srcpad
            caps = self.sources[devindex].query_caps(None)
            capsS=self.sources[devindex].query_caps(None).to_string()
            print ("adding i420 capabilities for device %s to combo (only I420 will be added):" % videodev) #We hard code I420 format (the most common) to simplify user choices...
            for i in range(caps.get_size()):
                format=caps.get_structure(i).get_string('format')
                if format == "I420":
                    (success, width) = caps.get_structure(i).get_int('width')
                    (success, height) = caps.get_structure(i).get_int('height')
                    # To get list of caps to be in some combobox (not in any specific scope, just for coding)
                    #a="""self.backgroundSize.addItem( \"%%sx%%s\"%% ("%s", "%s") ,"""%(width,height)
                    #b="""QVariant("video/x-raw,width=(int)%s,height=(int)%s"))"""%(width,height)
                    #print( a+b )
                    self.comboSize[devindex].addItem( "%sx%s"% (width, height) , QVariant(caps.get_structure(i).to_string()))
                    print('\t[+] %s' % caps.get_structure(i).to_string())
                else:
                    print('\t[-] %s' % caps.get_structure(i).to_string())
    def twAlpha(self,value,devindex):
        """
        Tweaks Alpha property to @value for device with id @devindex
        Parameters
        ----------
        value: int
            the value of the qslider
        devindex:str
            the index of the video device            
        """
        self.sinks[devindex].set_property ("alpha", value/100)
    def twZ(self,value,devindex):
        """
        Tweaks Z order property to @value for device with id @devindex
        """
        self.sinks[devindex].set_property ("zorder", value)
    def twSize(self,value,devindex):
        """
        Tweaks input Resolution property to @value for device with id @devindex
        http://gstreamer-devel.966125.n4.nabble.com/How-to-get-the-real-capabilities-of-a-v4l2src-element-td999291.html
        Parameters
        ----------
        value: str
            the size value of the qcombobox
        devindex:str
            the index of the video device            
        """        
        if value == -1:
            return
        prev_state=self.player.get_state(0)[1]
        self.player.set_state(Gst.State.READY)
        print ("choosing %s" % self.comboSize[devindex].itemData(value) )
        (width,height)=self.comboSize[devindex].currentText().split("x")
        newCapString=self.comboSize[devindex].itemData(value) #TODO get string correctly (as below)
        newCapString= "video/x-raw, format=(string)I420, width=(int)%s, height=(int)%s,framerate=(fraction)30/1" %(width,height) #Hard coding 30/1 to simplify and is mostly used
        print ("setting %s" % newCapString )
        newCaps=Gst.caps_from_string(newCapString)
        self.player.get_by_name("vcaps2"+str(devindex)).set_property("caps",newCaps)
        caps_event=Gst.Event.new_caps(  newCaps  )
        self.player.set_state(prev_state)        
        return         

    def twX(self,value,devindex):
        """
        Tweaks X property to @value for device with id @devindex
        Parameters
        ----------
        value: int
            the x value of the qslider
        devindex:str
            the index of the video device            
        """
        if (value*10<self.canvasW):
            self.sinks[devindex].set_property ("xpos", value*10)  
    def twY(self,value,devindex):
        """
        Tweaks Y property to @value for device with id @devindex
        Parameters
        ----------
        value: int
            the y value of the qslider
        devindex:str
            the index of the video device        
        """
        if (value*10<self.canvasH):
            self.sinks[devindex].set_property ("ypos", value*10)  
        
    def toggleDevice(self,value,devindex):
        """
        toggles(hides or shows) the device specified by devindex whenever device checkbox gets toggled by user
        Parameters
        ----------
        value: int
            the value of the qcheckbox
        devindex:str
            the index of the video device
        """       
        
        #self.player.unlink(self.player.get_by_name("vsrc"+str(devindex)))#TODO is necessary to remove pad ???
        if value==0:
            self.sinks[devindex].set_property("alpha", 0)            
        if value==2:
            self.sinks[devindex].set_property("alpha", self.sliderAlpha[devindex].sliderPosition()/100)
        
    def switchDevices(self,fromDev, value ):
        """
        switches props between to devices
        Parameters:
        -----------
        value: str
            the index of the selecte item in videoswitcher combobox 
        fromDev: str
            the index of the video devices from where we take props
        """
        print(self.sliderX)
        toDev=int(self.switchers[fromDev].itemData(value))
        print("switching values %s -> %s"%(fromDev, toDev))
        ( aAlpha, aX, aY, aZ ) =( self.sliderAlpha[fromDev].value(),self.sliderX[fromDev].value(),self.sliderY[fromDev].value(),self.zorders[fromDev].value() )
        ( bAlpha,bX,bY,bZ ) =(   self.sliderAlpha[toDev].value(),self.sliderX[toDev].value(),self.sliderY[toDev].value(),self.zorders[toDev].value()  )
        self.sliderAlpha[toDev].setValue(aAlpha)
        self.sliderX[toDev].setValue(aX)
        self.sliderY[toDev].setValue(aY)
        self.zorders[toDev].setValue(aZ)
        self.sliderAlpha[fromDev].setValue(bAlpha)
        self.sliderX[fromDev].setValue(bX)
        self.sliderY[fromDev].setValue(bY)
        self.zorders[fromDev].setValue(bZ)
        
    def togglePipe(self,value):
        """
        toggles the main pipe whenever enablepipe checkbox gets toggled by user
        Parameters
        ----------
        value: int
            the value of the qcheckbox
        """         
        if value==0:
            self.player.send_event(Gst.Event.new_eos())   
            for pipe in self.appPipes:
                self.appPipes[pipe].stopPlay()
        if value==2:
            #QTimer.singleShot(100,self.startPipe) # Add delay to put pipe on
            self.player.set_state(Gst.State.PAUSED)
            self.player.set_state(Gst.State.PLAYING)

    def setUpGst(self):
        """
        Creates the gstreamer playbin then add the controls
        """
        self.videoDevs=self.listDevs()
        pipe={}
        textoverlay="""textoverlay  shaded-background=TRUE auto-resize=TRUE font-desc="Sans 12" name=textOverlay_97 """ #Text overlay
        imageoverlay="""gdkpixbufoverlay name=imageOverlay_96 location="%s"  """%self.startimage 

        #PIPES EXAMPLES:
        #rec="tee name=rec ! vp8enc threads=4 keyframe-max-dist=5  ! queue ! rec_mux. pulsesrc do-timestamp=true ! queue ! audioconvert ! vorbisenc  ! queue !  matroskamux writing-app=qonfluo name=rec_mux ! filesink location=/tmp/test.mp4 rec. ! queue ! "
        
        #udpMirror = "tee name=stream ! queue ! x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink host=127.0.0.1 port=1234  stream. ! queue ! " 
        # Stream delivered at gst-launch-1.0 udpsrc port=1234 ! "application/x-rtp, payload=127" ! rtph264depay !  avdec_h264 ! xvimagesink sync=false
        
        #appMirrorI="tee name=appteei ! queue ! appsink name=app1 appteei. ! queue ! "
        #appMirrorII="tee name=appteeii ! queue ! valve name=valve drop=False !  x264enc pass=qual quantizer=20 tune=zerolatency ! rtph264pay ! udpsink name=app2 host=127.0.0.1 port=1234 appteeii. ! queue ! "

        #appMirrorIII="tee name=appteeiii ! queue ! valve name=valveiii drop=False ! shmsink name=app3 socket-path=/tmp/appiii shm-size=10000000 wait-for-connection=false sync=false appteeiii. ! queue ! "        
        # EOE        
        branches=[]
        if SHMSINK:
            for mirror in PLUGINS:
                pluginName=mirror['name']
                try:
                    os.remove('/tmp/%s'%pluginName)
                except:
                    print('no tmp file %s to delete'%pluginName)     
                branches.append("""
                    tee name=plugtee_%s ! 
                        queue ! valve name=valve_%s drop=False ! shmsink name=plugin_%s socket-path=/tmp/%s shm-size=47923200 wait-for-connection=false plugtee_%s. ! queue ! """ % (tuple( [mirror['name']]*5 )) )
        if not SHMSINK:
            branches.append("""
                tee name=plugtee_%s ! 
                        queue leaky=2 ! videoconvert ! jpegenc ! %smux.
                        pulsesrc ! audioconvert ! %smux.
                    matroskamux name=%smux streamable=true !  
                    tcpserversink name=plugin_%s host=0.0.0.0 port=%s sync-method=2 recover-policy=keyframe sync=false
                plugtee_%s. ! queue ! 
                """ % (tuple( ["tcp"]*5)+(PORT,"tcp")) )
                
        pipe[0]= """
        videomixer name=mix background=black ! videoconvert ! videoscale ! capsfilter name=canvascaps ! %s ! %s !
        %s 
        %s
        xvimagesink sync=false name="previewsink"
        videotestsrc pattern=17 foreground-color=0xff000000  name="backgroundsrc"  ! videorate name="bgrate" ! videoscale name="bgscale" ! capsfilter name="bgcaps" ! queue  max-size-bytes=100000000 max-size-time=0  ! mix.sink_99
        """ % (textoverlay, imageoverlay,  " ".join(branches),"") #(rec, udpMirror)
               
        sinkN=0
        for vd in sorted(self.videoDevs):
            pipe[vd]="""
            v4l2src device="/dev/"""+vd+"""" name=vsrc"""+str(sinkN)+"""  !   
            tee name=monitor_"""+str(sinkN)+""" ! videoscale ! queue ! xvimagesink  sync=false name=monitorWin"""+str(sinkN)+""" monitor_"""+str(sinkN)+""". !  
            videoscale name=vscale"""+str(sinkN)+""" ! videorate name =vrate"""+str(sinkN)+""" ! capsfilter name=vcaps2"""+str(sinkN)+""" !   queue   max-size-bytes=100000000 max-size-time=0 max-size-buffers=0 min-threshold-time=50000000 !   mix.sink_"""+str(sinkN)+ """
            """ 
            sinkN=sinkN+1

        print("  ".join(pipe.values()))
        self.player = Gst.parse_launch ("  ".join(pipe.values()) )
        self.addVideoControls() #Add video inputs
        self.addImageOverlay() # Add image overlay
        self.addTextOverlay() #Add textoverlay
        
        #Common elements, such as canvas, videomixer, outputs...
        m = self.player.get_by_name ("mix")
        self.previewWin=self.player.get_by_name("previewsink")
        self.canvasCaps=self.player.get_by_name("canvascaps")
        self.testSink=m.get_static_pad("sink_99")        
        
        #Track inputs caps changes
        m.get_static_pad('sink_99').connect('notify::caps', self._onNotifyCaps) # Background caps change track
        for vd in self.videoDevs:
            devindex=self.videoDevs[vd]['id']
            m.get_static_pad('sink_%s'%devindex).connect('notify::caps', self._onNotifyCaps)        
                    
            
        self.bus = self.player.get_bus()
        self.bus.add_signal_watch()
        self.bus.enable_sync_message_emission()
        self.bus.connect("message::eos", self.on_eos_message)
        self.bus.connect("message::error", self.on_error_message)
        self.bus.connect("sync-message::element", self.on_sync_message)

    def on_eos_message(self, bus, msg):
        """
        Whenever end of stream present in main pipeline
        Parameters
        ----------
        bus: Gst.Bus
        msg: Gst.Message
        """         
        print('on_eos(): eos message in main pipeline')
        self.player.set_state(Gst.State.NULL)

    def on_error_message(self, bus, msg):
        """
        Whenever error present in main pipeline
        Parameters
        ----------
        bus: Gst.Bus
        msg: Gst.Message
        """           
        err, debug = msg.parse_error()
        print("Error: %s" % err, debug )
        self.player.set_state(Gst.State.NULL)
        self.enablePipe.setChecked(False)

    def on_sync_message(self, bus, message):
        """
        When main pipeline play gets synced
        Parameters
        ----------
        bus: Gst.Bus
        message: Gst.Message
        """             
        print(message.get_structure().get_name())
        print(message.src.name)
        if message.get_structure().get_name() == 'prepare-window-handle':
            message.src.set_property('force-aspect-ratio', True)
            if message.src.name=="previewsink":    
                message.src.set_window_handle(self.xid)
            else: # like message.src.name=="monitorWin0": 
                message.src.set_window_handle(self.monitors_xid[message.src.name])
                
    def stopApp(self,pluginName):
        """
        stops the plugin remote pipeline
        Parameters
        ----------
        pluginName: str        
        """
        print("[%s] stopping plugin pipeline"% pluginName)
        self.appPipes[pluginName].stopPlay()
        self.appTimers[pluginName].stop()
        
    def connectApp(self,pluginName, pipeline):
        """
        Connects and Launches the remote pipeline, getting correct caps from local shmsink.
        Parameters
        ----------
        pluginName: str
            the name of the plugin to stop
        pipeline: str
            the pipeline string
        """        
        #Check if pipeline is exactly the same and no needs to re-create...
        if pluginName in self.appPipes and pluginName in self.appPipesStrings:
            if self.appPipesStrings[pluginName]==pipeline:
                print("[%s]pipeline marchin' already, putting back to play state"%pluginName)
                self.appPipes[pluginName].start()
                return True
            else:
                print("New Pipeline definitions create everything")                  
                
        #PluginPipeline Creation and connection       
        print("[%s]-----Parsing App pipeline-----"% pluginName)        
        
        self.appPipes[pluginName]=PlugPipe(pluginName) #Thread containing Gstreamer Pipe
        self.appPipesStrings[pluginName]=pipeline # Define String Pipeline to detects future changes
        
        if SHMSINK:
            self.plugEndpoints[pluginName]=self.player.get_by_name("plugin_%s"%str(pluginName)) #SHMSINK cruft
        else:
            self.plugEndpoints[pluginName]=self.player.get_by_name("plugin_tcp")          
        
        #Connect the notifications of changings caps from plugEndpoint to plugin pipeline
        for prop in GObject.list_properties(self.plugEndpoints[pluginName].get_static_pad('sink')):
            print("[%s] plugin connected searching caps in %s"%(pluginName,prop.name))
            if prop.name=='caps':
                print("[%s] plugEndpoint caps are: %s " % (pluginName,self.plugEndpoints[pluginName].get_static_pad('sink').props.caps.to_string()))
                
        self.plugEndpoints[pluginName].get_static_pad('sink').connect('notify::caps', self.appPipes[pluginName].requestChangeCaps) 
        
        
        self.appPipes[pluginName].passPipe(self.plugEndpoints[pluginName],pipeline) # The GST.Pipeline Thread Constructor
        #Set Caps based on shmsink (if needed)
        self.appPipes[pluginName].requestChangeCaps(self.plugEndpoints[pluginName].get_static_pad('sink'),None) # SHMSINK cruft
        
        #Connect the plugin notifications
        self.appPipes[pluginName].eos.connect(self.onEosMessagePlugins)
        self.appPipes[pluginName].error.connect(self.onErrorMessagePlugins)
        self.appPipes[pluginName].sync.connect(self.onSyncMessagePlugins)
        self.appPipes[pluginName].onPipeTraffic.connect(self.onHandoffPlugins)
        
        #Fulfill the Gui plugin object to get some link with Gst thread- not needed and possibly CRUFT
        #self.streamControls.plugins[pluginName].source = self.appPipes[pluginName].get_by_name("source")
        #self.streamControls.plugins[pluginName].pipeline = self.appPipes[pluginName]         

        
        self.appPipes[pluginName].start()        
        return True


    def _onNotifyCaps(self, pad, unused):
        """
        Callback when caps are set for the main player's sink element's
        sink.
        """        

        caps=pad.props.caps
        if caps is None or not caps.is_fixed():
            return
        else:
            print (" %s Caps are %s" % (pad.get_name(),caps.to_string()))            
            return 
         


    def onHandoffPlugins(self, pluginName, kbps):
        """
        new identity handoff, so propagate the current buffer kbps of queuePlug to everywhere. We use identity to get handoffs and queue to get buffer level transformed in kbps to plot this via QML and plugin 
        Parameters
        ----------
        pluginName: str
            the name of the plugin that has handoff  
        kbps: int 
            the quantity of kbps detected.
        """
        self.appTimers[pluginName].stop()
        if self.streamControls.plugins[pluginName].state==-1:
            self.streamControls.plugins[pluginName].state=1
        if kbps>0:
            self.streamControls.plugins[pluginName].bufferLevel=kbps

        self.appTimers[pluginName].start(3000)
        
    def onEosMessagePlugins(self, pluginName):
        """
        Whenever end of stream present present in any plugin
        Parameters
        ----------
        pluginName: str
            the name of the plugin that gets the error
        """        
        print('End Of Stream in plugin %s'%pluginName)
        self.statusBar.showMessage("End of Stream in plugin %s:" % (pluginName))
        self.appTimers[pluginName].stop()
        self.streamControls.plugins[pluginName].state=0
        #Remove zombie thread???
       

        
        
    def onErrorMessagePlugins(self, pluginName, error):
        """
        Whenever error present in any plugin
        Parameters
        ----------
        pluginName: str
            the name of the plugin that gets the error
        """        
        print(error)
        self.statusBar.showMessage(error)
        self.streamControls.plugins[pluginName].startStream.setChecked(False)
        
    def onSyncMessagePlugins(self,pluginName):
        """
        When plugin play gets synced
        Parameters
        ----------
        pluginName: str
            the name of the plugin that gets the error
        """        
        print("[%s] Synced ! "%pluginName)

    def startPrev(self):
        """
        Puts the main player in ready state waiting for user interaction
        """         
        self.player.set_state(Gst.State.READY)
        
        self.get_caps()
        #TODO init method that:
        self.canvas_send_back()        
        self.setCanvasSize( self.canvasSize.currentIndex() )
        #self.fillCanvasSizes(True)#TODO refresh and discover valid and negotiated sizes

            
    def format_time(self, value):
        """
        Formats the value in usable time format
        Parameters
        ----------
        value: str
            the time to be formatted
        """
        seconds = value / Gst.SECOND
        return '%02d:%02d' % (seconds / 60, seconds % 60)
    def aboutQt(self):
        QMessageBox.aboutQt(self,"About Qt")
    def about(self):
        QMessageBox.about(self, "About Qonfluo", "<h2>Qonfluo</h2>\nis a video mixer dashboard to stream to any Gst Sink, by now (via rtmp plugin) is capable to stream to rtmp server such as justin.tv, bambuser, ustream, youtube...<br/> sources:<a href='https://github.com/aleixq/Qonfluo'>https://github.com/aleixq/Qonfluo</a> <br/> Copyright: Aleix quintana 2014")



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--fmle", dest="fmle", help="FMLE file to import") #NOTE This implies using rtmp plugin
    parser.add_argument("-n", "--netplothidden", help="If qml network plotting must be hidden", action="store_true") #NOTE This implies using rtmp plugin
    parser.add_argument("-d", "--devices", dest="devices", help="The video devices id that must be used (ex: video0,video2)") #
    args = parser.parse_args()


    PLUGINS=[
            {'name':'rtmp','class':RtmpPlugin,'args':{"notPlot":args.netplothidden}},
            {'name':'rec','class':RecPlugin,'args':{}},
            ]

    #if args.netplothidden:
        #PLUGINS[0]['args'].append("notPlot")    
        
    GObject.threads_init()
    Gst.init(None)
    app = QApplication(sys.argv)

    app.setOrganizationName("communia")
    app.setOrganizationDomain("communia.org")
    app.setApplicationName("qonfluo/qonfluo")
    app.setWindowIcon(QIcon.fromTheme("qonfluo",QIcon(getDataDir("qonfluo.svg"))))
    
    video = VideoMixerConsole()
    video.setUpGst()
    video.startPrev()
    if args.fmle:
        video.importFME(fmeFile=os.getcwd()+'/'+args.fmle)
    sys.exit(app.exec_())
