# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamcontrols.ui'
#
# Created: Mon Jun 30 21:08:43 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! 
# TODO(AKA Known Issues):
# * When streaming to rtmp server and network gets disconnected it's not possible to change plugin pipeline state to other than PLAY , if so it locks all whole application until network comes back.


from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQuick import QQuickView
from basePlugin import *
from networkData import *
from fmle_profile import *
from lib.dicttoxml import dicttoxml
from xml.dom.minidom import parseString

class RtmpPlugin(BasePlugin):
    """
    subclass of BasePlugin to stream to rtmp server
    
    ATTRIBUTES:
    -----------
    FMEprofile: str
        Wether or not a profile is included as argument to load automatically (TODO)
    """
    def __init__(self, name, args, parent=None):
        """
        Constructor.
        PARAMETERS:
        -----------
        name: str 
            the plugin name
        args: dict
            the list of args to include to plugin
        parent: str 
            the mainwindow Object which contains GST playbins, and also window gui elements             
        """
        super().__init__(name,args,parent)
        self.pluginName=name
        self.pageRtmp = QWidget()        
        self.baseWidget=self.pageRtmp #We need this as plugin
        self.setupUi(self.pageRtmp)
        self._protocol="rtmp"
        self.profile="main"
        self.args=args
        self.uid=0 #identifier to change something in pipeline and disable pause state 
        super().connectStream()
        
    def setupUi(self, Form):
        #plugin RTMP
        self.pageRtmp.setGeometry(QRect(0, 0, 937, 460))
        self.pageRtmp.setObjectName("page")
        self.inPageLayout = QGridLayout(self.pageRtmp)
        self.inPageLayout.setObjectName("inPageLayout")
        self.groupBox = QGroupBox(self.pageRtmp)
        self.groupBox.setObjectName("groupBox")
        self.formLayout_2 = QFormLayout(self.groupBox)
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout_2.setObjectName("formLayout_2")
        self.editRtmpUrl = QLineEdit(self.groupBox)
        self.editRtmpUrl.setObjectName("editRtmpUrl")
        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.editRtmpUrl)
        self.labelFormat = QLabel(self.groupBox)
        self.labelFormat.setObjectName("labelFormat")
        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.labelFormat)
        self.comboFormat = QComboBox(self.groupBox)
        self.comboFormat.setObjectName("comboFormat")
        self.comboFormat.addItem("")
        self.comboFormat.addItem("")
        self.comboFormat.addItem("")        
        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.comboFormat)
        self.labelDatarate = QLabel(self.groupBox)
        self.labelDatarate.setObjectName("labelDatarate")
        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.labelDatarate)
        self.labelOutputSize = QLabel(self.groupBox)
        self.labelOutputSize.setObjectName("labelOutputSize")
        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.labelOutputSize)
        self.comboOutputSize = QComboBox(self.groupBox)
        self.comboOutputSize.setObjectName("comboOutputSize")
        self.comboOutputSize.addItem("")
        self.comboOutputSize.addItem("")
        self.comboOutputSize.setEditable(True)
        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.comboOutputSize)
        self.labelLevel = QLabel(self.groupBox)
        self.labelLevel.setObjectName("labelLevel")
        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.labelLevel)
        self.spinLevel = QSpinBox(self.groupBox)
        self.spinLevel.setMaximum(63)
        self.spinLevel.setProperty("value", 0)
        self.spinLevel.setObjectName("spinLevel")
        self.spinLevel.setToolTip("0 for default")        
        self.formLayout_2.setWidget(10, QFormLayout.FieldRole, self.spinLevel)
        self.checkDegradequality = QCheckBox(self.groupBox)
        self.checkDegradequality.setObjectName("checkDegradequality")
        self.formLayout_2.setWidget(11, QFormLayout.FieldRole, self.checkDegradequality)
        self.editRtmpStream = QLineEdit(self.groupBox)
        self.editRtmpStream.setObjectName("editRtmpStream")
        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.editRtmpStream)
        self.labelRtmpStream = QLabel(self.groupBox)
        self.labelRtmpStream.setObjectName("labelRtmpStream")
        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.labelRtmpStream)
        self.labelRtmpUrl = QLabel(self.groupBox)
        self.labelRtmpUrl.setObjectName("labelRtmpUrl")
        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.labelRtmpUrl)
        self.comboDatarate = QSpinBox(self.groupBox)
        self.comboDatarate.setMaximum(102400)
        self.comboDatarate.setProperty("value", 650)
        self.comboDatarate.setObjectName("comboDatarate")
        self.comboDatarate.setToolTip("0 for default")        
        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.comboDatarate)
        
        
        self.labelKeyframeFreq = QLabel(self.groupBox)
        self.labelKeyframeFreq.setObjectName("KeyframeFreq")
        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.labelKeyframeFreq)        
        self.comboKeyframeFreq = QSpinBox(self.groupBox)
        self.comboKeyframeFreq.setMaximum(9)
        self.comboKeyframeFreq.setProperty("value", 5)
        self.comboKeyframeFreq.setObjectName("comboKeyframeFreq")
        self.comboKeyframeFreq.setToolTip("0 for default")        
        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.comboKeyframeFreq)
        
        self.inPageLayout.addWidget(self.groupBox, 1, 0, 3, 1)
        
        
        
        self.groupBox_2 = QGroupBox(self.pageRtmp)
        self.groupBox_2.setObjectName("groupBox_2")
        self.formLayout = QFormLayout(self.groupBox_2)
        self.formLayout.setFieldGrowthPolicy(QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName("formLayout")
        self.labelFormatAudio = QLabel(self.groupBox_2)
        self.labelFormatAudio.setObjectName("labelFormatAudio")
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.labelFormatAudio)
        self.comboFormatAudio = QComboBox(self.groupBox_2)
        self.comboFormatAudio.setObjectName("comboFormatAudio")
        self.comboFormatAudio.addItem("")
        self.comboFormatAudio.addItem("")
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboFormatAudio)
        self.labelAudioDatarate = QLabel(self.groupBox_2)
        self.labelAudioDatarate.setObjectName("labelAudioDatarate")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelAudioDatarate)
        self.comboAudioDatarate = QSpinBox(self.groupBox_2)
        self.comboAudioDatarate.setMaximum(512)
        self.comboAudioDatarate.setProperty("value", 128)
        self.comboAudioDatarate.setObjectName("comboAudioDatarate")
        self.comboAudioDatarate.setToolTip("0 for default")            
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboAudioDatarate)
        self.inPageLayout.addWidget(self.groupBox_2, 1, 1, 1, 1)
        self.startStream=QPushButton("Stream!")
        self.startStream.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.startStream.setCheckable(True)
        self.inPageLayout.addWidget(self.startStream, 2, 1, 1, 1)
        
        #self.forceStop=QPushButton("Force Stop!")
        #self.forceStop.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
        #self.inPageLayout.addWidget(self.forceStop, 3, 1, 1, 1)
        #self.forceStop.clicked.connect(self.forceStopPipe)
        
        self.presetWidget=QWidget()
        self.formLayoutPreset=QFormLayout(self.presetWidget)
        self.editPresetName= QLineEdit(self.presetWidget)
        self.editPresetName.setObjectName("editPresetName")
        self.labelPreset = QLabel(self.presetWidget)
        self.labelPreset.setObjectName("labelPreset")        
        self.formLayoutPreset.setWidget(0, QFormLayout.FieldRole, self.editPresetName)
        self.formLayoutPreset.setWidget(0, QFormLayout.LabelRole, self.labelPreset)
        self.inPageLayout.addWidget(self.presetWidget, 0, 0, 1, 1)
        
        
        self.bufferStall.connect(self.disableByStall)
        self.bufferStart.connect(self.enableByBufferStart)
        
                                   
        #DATARATE PLOTTER
        #Implementation via QProgressBar also in 
        
        #self.bufferStream=QProgressBar()
        #self.bufferStream.setFormat("%v kbps")#If this you need to set maximum, maybe as: self.setMaxBufLevel(int(datarate)+int(self.getAudioDatarate()))
        
        #Implementation via QML 
        if not self.args["notPlot"]:
            self.addQMLcontainer() #put qquickview on widget
        self.retranslateUi(Form)
        self.comboFormat.currentTextChanged.connect(self.negotiateAVMux)
        QMetaObject.connectSlotsByName(Form)

    def addQMLcontainer(self):
        """
        Adds the Network QML Graph 
        """
        self.qmlBufLevel=QQuickView()
        self.qmlBufLevel.setResizeMode(QQuickView.SizeRootObjectToView)
        qmlRegisterType(NetworkData, 'GstMix.NetworkData', 1, 0, 'NetworkDataNodes')
        self.qmlBufLevel.setSource(QUrl.fromLocalFile('qml/osc.qml'))
        self.qmlRootObject = self.qmlBufLevel.rootObject()
        self.chart=self.qmlRootObject.findChild(QObject,name="chart_line")
        self.networkData=self.qmlRootObject.findChild(QObject,name="nodes")
        
        container = QWidget.createWindowContainer(self.qmlBufLevel)        
        self.inPageLayout.addWidget(container,3,1,1,1)
        self.bufLevelChanged.connect(self.onBufLevelChanged)
        
    def onBufLevelChanged(self,level):
        """
        Buffer has changed so populate to qml plotter
        """
        self.networkData.setProperty("data",int(level))
        QMetaObject.invokeMethod(self.chart,"updateLine", Qt.AutoConnection)
        
    def retranslateUi(self, Form):
        _translate = QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.groupBox.setTitle(_translate("Form", "Video"))
        self.labelFormat.setText(_translate("Form", "format"))
        self.comboFormat.setItemText(0, _translate("Form", "h.264"))
        self.comboFormat.setItemText(1, _translate("Form", "MP2"))
        self.comboFormat.setItemText(2, _translate("Form", "VP8"))
        self.labelDatarate.setText(_translate("Form", "datarate"))
        self.labelOutputSize.setText(_translate("Form", "outputsize"))
        self.comboOutputSize.setItemText(0, _translate("Form", "canvas size"))
        self.comboOutputSize.setItemText(1, _translate("Form", "1280x720"))
        self.labelKeyframeFreq.setText(_translate("Form", "Keyframe frequency"))
        self.labelLevel.setText(_translate("Form", "level"))
        self.checkDegradequality.setText(_translate("Form", "degradequality"))
        self.labelRtmpStream.setText(_translate("Form", "stream"))
        self.labelRtmpUrl.setText(_translate("Form", "url"))
        self.groupBox_2.setTitle(_translate("Form", "Audio"))
        self.labelFormatAudio.setText(_translate("Form", "format"))
        self.comboFormatAudio.setItemText(0, _translate("Form", "aac"))
        self.comboFormatAudio.setItemText(1, _translate("Form", "ogg"))        
        self.labelAudioDatarate.setText(_translate("Form", "datarate"))
        self.labelPreset.setText(_translate("Form", "Preset name"))
        #self.actionOpenFME.setText(_translate("Form", "Open FME profile"))
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
        menu=QMenu("Rtmp",parent)
        self.actionOpenFME = QAction("Open f&me", self, shortcut="Ctrl+F",
                statusTip="open fme",triggered=self.importFME)
        self.actionSaveFME = QAction("Save f&me", self, shortcut="Ctrl+W",
                statusTip="save fme",triggered=self.exportFME)
        menu.addAction(self.actionOpenFME)
        menu.addAction(self.actionSaveFME)
        
        return menu

    def importFME(self, fmeFile=None):
        """
        Open filechooser to get FME profile
        """
        if fmeFile:
            if not os.path.exists(fmeFile):
                raise argparse.ArgumentError(None,"%s does not exist"%fmeFile)
            fileName=fmeFile
        else:
            fileName, _ = QFileDialog.getOpenFileName()
        if fileName:
            self.fmle=flashmedialiveencoder_profile(fileName)
            if self.fmle.exitCode:
                self.fillCapsFromFME()
    def fillCapsFromFME(self):
        """
        Fills the correct constrains to succes with streaming
        """
        self.presetName=self.fmle.name
        (width,height)=(self.fmle.encoder["video"]["width"],self.fmle.encoder["video"]["height"])
        print("[RTMP]setting canvas to : %s x %s by FMLE profile demand"%(width,height) )
        self.parent().addCanvasSize(width,height)
        #We are gonna set the stream controls based on fmle    
        self.protocol=next( iter(self.fmle.protocols.keys()))
        self.videoFormat=self.fmle.encoder['video']['format']
        self.rtmpUrl=self.fmle.protocols[self.protocol]["url"]
        self.rtmpStream=self.fmle.protocols[self.protocol]["stream"]
        self.datarate=self.fmle.encoder['video']['datarate']
        self.outputSize=(self.fmle.encoder['video']['width'],self.fmle.encoder['video']['height'])
        self.level=self.fmle.encoder['video']['level']
        self.keyframeFreq=self.fmle.encoder['video']['keyframe_frequency']
        self.degradeQuality=self.fmle.encoder['video']['degradequality']
        self.audioFormat=self.fmle.encoder['audio']['format']
        self.audioDatarate=self.fmle.encoder['audio']['datarate']
    def exportFME(self):
        """
        exports current state to xml
        """
        #Preset: preset/name
        out={
            "flashmedialiveencoder_profile":{
                "preset":{
                    "name":self.presetName
                },
                "output":{
                    "rtmp":{
                        "url":self.rtmpUrl,
                        "stream":self.rtmpStream
                    }
                },
                "encode":{
                    "video":{
                                "format":self.videoFormat,
                                "datarate":self.datarate,
                                "advanced":
                                    {
                                        "profile":"Main",
                                        "level":self.level,
                                        "keyframe_frequency":"%s Seconds"%self.keyframeFreq
                                    }
                    },
                    "audio":{
                                    "format":self.audioFormat,
                                    "datarate":self.audioDatarate
                    }
                }
            }
        }
        if self.degradeQuality:
            out["flashmedialiveencoder_profile"]["encode"]["video"]["autoadjust"]={"degradequality":{"enable":"true"}}
        if len(self.outputSize)==2:
            out["flashmedialiveencoder_profile"]["encode"]["video"]['outputsize']="%sx%s"%(self.outputSize[0],self.outputSize[1])
        else:
            out["flashmedialiveencoder_profile"]["encode"]["video"]['outputsize']="%s"%(self.outputSize[0])           
        xml = dicttoxml.dicttoxml(out,attr_type=False,root=False)
        dom = parseString(xml)
        fileName = QFileDialog.getSaveFileName(self.parent(), 'Save FMLE xml profile', directory=QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0], filter='*.xml')
        if fileName:
            try:
                fname = open(fileName[0], 'w')
                fname.write(dom.toprettyxml())
                fname.close()            
            except BaseException as e: 
                 QMessageBox.critical(self.parent(),"Bad,Bad","Could Not save the file, check:\n %s" % str(e))
    
    def negotiateAVMux(self,vformat):
        """
        Negotiates formats in muxers so it is consistent, no Gst magic here...
        PARAMETERS:
        -----------
        vformat: str 
            the video format that user has chosen
        """
        
        if vformat=="VP8": self.setAudioFormat("ogg")
        if vformat=="h.264":self.setAudioFormat("aac")
        if vformat=="MP2":self.setAudioFormat("aac")
        if vformat != "h.264": QMessageBox.critical(self.parent(),"Bad,Bad","By now only <b>h264</b> in a <b>flv</b> can be used to stream to rtmp sink.Check <a href=\"http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gst-plugins-bad-plugins/html/gst-plugins-bad-plugins-rtmpsink.html\">rtmpsink docs</a>. Please choose <b> h264</b>")
        
    def setPresetName(self, presetName):
        """
        Sets the stream preset Name.
        """
        self.editPresetName.setText(presetName)
    def getPresetName(self):
        """
        Sets the stream preset Name.
        """
        return self.editPresetName.text()
                
    def setProtocol(self, protocol):
        """
        Sets the stream protocol (this is RTMP). More to come...(hope)
        """
        self._protocol='rtmp'
        
    def getProtocol(self):
        """
        Gets the stream protocol (this is RTMP). More to come...(hope)
        """
        return self._protocol
    
    def setRtmpUrl(self,url):
        """
        Sets the rtmp url
        """
        print("setting to "+url)
        self.editRtmpUrl.setText(url)
        return self.editRtmpUrl.text()
    def setRtmpStream(self,stream):
        """
        Sets the Rtmp Stream
        """
        self.editRtmpStream.setText(stream)
        return self.editRtmpStream.text()    
    def setFormat(self,formatValue):
        """
        Sets Video format
        """
        if self.comboFormat.findText(formatValue)== -1:
            self.comboFormat.addItem(formatValue) #TODO accept other formats and change fields...
        self.comboFormat.setCurrentIndex(self.comboFormat.findText(formatValue ) )
                                         
                                         
        return self.comboFormat.currentText()
    def setDatarate(self,datarate):
        """
        Sets video datarate
        """
        self.comboDatarate.setValue(int(datarate)) 
        return self.comboDatarate.value()
    def setOutputSize(self,size):
        """
        Sets the output size
        """
        (width,height)=(size[0],size[1])
        if self.comboOutputSize.findText("%sx%s"%(width,height) )== -1:
            self.comboOutputSize.addItem("%sx%s"%(width,height), QVariant("video/x-raw,width=(int)%s,height=(int)%s"%(width, height)))
        self.comboOutputSize.setCurrentIndex(self.comboOutputSize.findText("%sx%s"%(width,height) ) )
        return self.comboOutputSize.currentText()
    def setLevel(self,level):
        """
        Sets the h264 compression level, a specified set of constraints that indicate a degree of required decoder performance for a profile.
        """
        self.spinLevel.setValue(float(level))
        return self.spinLevel.value()
    def setKeyframeFreq(self,freq):
        """
        Sets the Keyframe Frequency,     The interval at which to insert keyframes. The default is 5 seconds, which means a keyframe is inserted every 5 seconds.


        """
        freq=[int(s) for s in freq.split() if s.isdigit()] # Extracts integers, the first will be the one
        self.comboKeyframeFreq.setValue(freq[0])
        return self.comboKeyframeFreq.value()      
    def setDegradeQuality(self,quality):
        """
        Sets the Degrade quality 
        This setting degrades the quality of the video by reducing the bit rate until data can be streamed without exceeding the specified RTMP buffer size. 
        """
        quality=quality.capitalize()
        quality=(quality=="True")
        self.checkDegradequality.setCheckState(quality)
        return self.checkDegradequality.checkState()

    def setAudioFormat(self, formatValue):
        """
        Sets the Audio format
        """
        if self.comboFormatAudio.findText(formatValue)== -1:
            self.comboFormatAudio.addItem(formatValue) #TODO accept other formats and change fields...
        self.comboFormatAudio.setCurrentIndex(self.comboFormatAudio.findText(formatValue ) )
                                         
        return self.comboFormatAudio.currentText()        
    def setAudioDatarate(self,datarate):
        """
        Sets Audio data rate
        """
        self.comboAudioDatarate.setValue(int(datarate))
        return self.comboAudioDatarate.value()   
    def getRtmpUrl(self):
        """
        Gets the rtmp url
        """
        return self.editRtmpUrl.text()
    def getRtmpStream(self):
        """
        Gets the Rtmp Stream
        """
        return self.editRtmpStream.text()    
    def getFormat(self):
        """
        Gets Video format
        """
        return self.comboFormat.currentText()
    def getDatarate(self):
        """
        Gets video datarate
        """
        return self.comboDatarate.value()
    def getOutputSize(self):
        """
        Gets the output size
        """
        return self.comboOutputSize.currentText().split("x")
    def getLevel(self):
        """
        Gets the h264 compression level, a specified set of constraints that indicate a degree of required decoder performance for a profile.
        """
        return self.spinLevel.value()   
    def getKeyframeFreq(self):
        """
        Gets the Keyframe Frequency,     The interval at which to insert keyframes. The default is 5 seconds, which means a keyframe is inserted every 5 seconds.


        """
        return self.comboKeyframeFreq.value()      
    def getDegradeQuality(self):
        """
        Gets the Degrade quality 
        This getting degrades the quality of the video by reducing the bit rate until data can be streamed without exceeding the specified RTMP buffer size. 
        """
        return self.checkDegradequality.checkState()
    def getAudioFormat(self):
        """
        Gets the Audio format
        """
        return self.comboFormatAudio.currentText()
    def getAudioDatarate(self):
        """
        Gets Audio data rate
        """
        return self.comboAudioDatarate.value()

    def getPlayBin(self):
        """
        Overrrides generic fakesink Playbin. Main pipeline sink Caps can be get automatically from main pipeline plugin sink using capsfilter name=plugin_caps_%pluginname%, useful if using shmsrc instead of tcpclientsrc
        """
        location="%s/%s live=true flashver=FMLE/3.0(compatible;FMSc/1.0)"%(self.rtmpUrl,self.rtmpStream)
        filesink="""queue name=queue_stats_%s ! identity name=identity_stats_%s sync=true ! rtmpsink location='%s'"""%(self.pluginName, self.pluginName, location)
        #Audio Encoder
        if self.audioFormat=="aac":
            audioencoder=" d. ! audioconvert ! voaacenc bitrate="+str(self.audioDatarate*1000)+" ! aacparse ! audio/mpeg,mpegversion=4,stream-format=raw "
        if self.audioFormat=="mp3":
            audioencoder="d. ! queue ! audioconvert ! lamemp3enc bitrate="+str(self.audioDatarate*1000)+" ! mpegaudioparse"
        if self.audioFormat=="ogg":
            audioencoder="d. ! audioconvert ! vorbisenc bitrate="+str(self.audioDatarate*1000)+" ! vorbisparse"        
        
        if self.videoFormat== "h.264":
            #x264Enc in FLV
            h264options=[]
            if self.keyframeFreq >0: h264options.append("key-int-max=%s"%str(self.keyframeFreq))
            if self.datarate >0: h264options.append("bitrate=%s"%str(self.datarate)) 
            #NOTE Profile and Level caps are not used here nor anywhere, just size 
            h264parseOptions=["video/x-h264"]
            if self.outputSize[0] !="canvas size": h264parseOptions.append("width=(int)%s,height=(int)%s"%(self.outputSize[0],self.outputSize[1] ) )
            #if self.level>0: h264parseOptions.append("level=(string)%s.0" %str(self.level)) 
            h264videoencoder="x264enc tune=zerolatency  bframes=0 byte-stream=false aud=true  speed-preset=ultrafast %s ! h264parse ! queue ! %s"%(" ". join (h264options), ",". join (h264parseOptions))
            h264pipe="%s ! queue ! %s_mux. %s ! queue !  flvmux  streamable=true name=%s_mux ! %s "%(h264videoencoder, self.pluginName,  audioencoder, self.pluginName, filesink)
            videoencoder=h264videoencoder
            pipe=h264pipe
            
        if self.videoFormat== "MP2":
            mp2options=[]
            if self.keyframeFreq >0: mp2options.append("max-key-interval=%s"%str(self.keyframeFreq))
            if self.datarate >0: mp2options.append("bitrate=%s"%str(self.datarate)) 
            mp2parseOptions=["video/mpeg,version=(int)2"]
            if self.outputSize[0] !="canvas size": mp2parseOptions.append(" width=(int)%s,height=(int)%s"%(self.outputSize[0],self.outputSize[1] ) )
            #if self.level>0: mp2parseOptions.append("level=%s" %str(self.level)) #No Level option...
            
            mp2videoencoder="avenc_mpeg2video %s ! mpegvideoparse ! queue ! %s"%(" ". join (mp2options), ",". join (mp2parseOptions))
            mp2pipe="%s ! queue ! %s_mux. %s ! queue !  avimux  name=%s_mux ! %s "%(mp2videoencoder, self.pluginName,  audioencoder, self.pluginName, filesink)
                       
            videoencoder=mp2videoencoder
            pipe=mp2pipe
        if self.videoFormat=="VP8":
            #VP8 and ogg in Matroska
            vp8options=[]
            if self.keyframeFreq >0: vp8options.append("keyframe-max-dist=%s"%str(self.keyframeFreq))
            if self.datarate >0: vp8options.append("target-bitrate=%s"%str(self.datarate*1000)) 
            if self.outputSize[0] !="canvas size": vp8options.append(" width=%s height=%s "%(self.outputSize[0],self.outputSize[1] ) )
            if self.level>0: vp8options.append("cq-level=%s" %str(self.level))
            
            vp8videoencoder=" vp8enc deadline=1 %s " %(" ". join (vp8options)) #" theoraenc"
            vp8pipe="%s ! queue ! %s_mux. %s ! queue !  %s_mux. matroskamux streamable=true writing-app=qonfluo name=%s_mux ! %s  "%(vp8videoencoder, self.pluginName, audioencoder, self.pluginName , self.pluginName, filesink )
            
            videoencoder=vp8videoencoder
            pipe=vp8pipe
        
        tcpsrcPipeline="""tcpclientsrc host=127.0.0.1 port=14050 name=source  ! decodebin name=d  d. ! queue leaky=2 max-size-buffers=2 !  videoscale name=change%s ! videoconvert ! %s     
        """%( str(self.uid), pipe) #Do-timestamp gets timestamp from source, not viable in tcpclientsrc
        print(tcpsrcPipeline)
        self.uid=self.uid+1        
        return tcpsrcPipeline
        #OPTION UDPSRC
        return "udpsrc  name=source port=1234 ! application/x-rtp, payload=127 !  rtph264depay !  avdec_h264 ! videoscale ! videoconvert ! xvimagesink "#+pipe

    
    def getBufLevel(self):
        """
        Gets the level of Stream buffer Progress Bar
        """        
        return self.bufferStream.value()
    def setBufLevel(self,level):
        """
        Sets the level of Stream buffer Progress Bar
        """
        self.bufLevelChanged.emit(level) #emits the signal new buffer level
        #self.bufferStream.setValue(level) #for QProgressBar
        
    def setMaxBufLevel(self,maxLevel):
        """
        Sets the maximum level of Stream buffer Progress Bar
        """
        self.bufferStream.setMaximum(maxLevel)

    def disableByStall(self):
        """
        invoked when buffer must be filled and it cannot
        """
        print("TODO ALERT: May be not Streaming!!! Feed buffer stopped")
        #self.startStream.setDisabled(True)
        #self.startStream.setChecked(False)
        
    def enableByBufferStart(self):
        """
        invoked when buffer is fed
        """
        self.startStream.setDisabled(False)
        
    presetName=property(getPresetName,setPresetName)
    rtmpUrl=property(getRtmpUrl,setRtmpUrl)
    rtmpStream=property(getRtmpStream,setRtmpStream)
    videoFormat=property(getFormat,setFormat) #TODO
    datarate=property(getDatarate,setDatarate)
    outputSize=property(getOutputSize,setOutputSize)
    level=property(getLevel,setLevel)
    keyframeFreq=property(getKeyframeFreq,setKeyframeFreq)
    degradeQuality=property(getDegradeQuality,setDegradeQuality)#TODO
    audioFormat=property(getAudioFormat,setAudioFormat)
    audioDatarate=property(getAudioDatarate,setAudioDatarate)
    protocol=property(getProtocol,setProtocol)    
    currentPipe=property(getPlayBin)
    bufferLevel=property(getBufLevel,setBufLevel)
    bufLevelChanged = pyqtSignal(int)







    
