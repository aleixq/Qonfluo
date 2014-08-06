# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'streamcontrols.ui'
#
# Created: Mon Jun 30 21:08:43 2014
#      by: PyQt5 UI code generator 5.2.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtQuick import QQuickView
from basePlugin import *
from networkData import *


class RtmpPlugin(BasePlugin):
    """
    subclass of BasePlugin to stream to rtmp server
    """
    def __init__(self,name):
        super().__init__(name)
        self.pluginName=name
        self.pageRtmp = QWidget()        
        self.baseWidget=self.pageRtmp #We need this as plugin
        self.setupUi(self.pageRtmp)
        self._protocol="rtmp"
        self.profile="main"
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
        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.comboOutputSize)
        self.labelLevel = QLabel(self.groupBox)
        self.labelLevel.setObjectName("labelLevel")
        self.formLayout_2.setWidget(10, QFormLayout.LabelRole, self.labelLevel)
        self.spinLevel = QDoubleSpinBox(self.groupBox)
        self.spinLevel.setMaximum(5.2)
        self.spinLevel.setProperty("value", 3.0)
        self.spinLevel.setObjectName("spinLevel")
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
        self.comboDatarate.setMaximum(20000)
        self.comboDatarate.setProperty("value", 650)
        self.comboDatarate.setObjectName("comboDatarate")
        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.comboDatarate)
        
        
        self.labelKeyframeFreq = QLabel(self.groupBox)
        self.labelKeyframeFreq.setObjectName("KeyframeFreq")
        self.formLayout_2.setWidget(9, QFormLayout.LabelRole, self.labelKeyframeFreq)        
        self.comboKeyframeFreq = QSpinBox(self.groupBox)
        self.comboKeyframeFreq.setMaximum(9)
        self.comboKeyframeFreq.setProperty("value", 5)
        self.comboKeyframeFreq.setObjectName("comboKeyframeFreq")
        self.formLayout_2.setWidget(9, QFormLayout.FieldRole, self.comboKeyframeFreq)
        
        self.inPageLayout.addWidget(self.groupBox, 0, 0, 3, 1)
        
        
        
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
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboFormatAudio)
        self.labelAudioDatarate = QLabel(self.groupBox_2)
        self.labelAudioDatarate.setObjectName("labelAudioDatarate")
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.labelAudioDatarate)
        self.comboAudioDatarate = QSpinBox(self.groupBox_2)
        self.comboAudioDatarate.setMaximum(512)
        self.comboAudioDatarate.setProperty("value", 128)
        self.comboAudioDatarate.setObjectName("comboAudioDatarate")
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.comboAudioDatarate)
        self.inPageLayout.addWidget(self.groupBox_2, 0, 1, 1, 1)
        self.startStream=QPushButton("Stream!")
        self.startStream.setSizePolicy ( QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.startStream.setCheckable(True)
        self.inPageLayout.addWidget(self.startStream, 1, 1, 1, 1)
        
        #DATARATE PLOTTER
        #Implementation via QProgressBar also in 
        
        #self.bufferStream=QProgressBar()
        #self.bufferStream.setFormat("%v kbps")#If this you need to set maximum, maybe as: self.setMaxBufLevel(int(datarate)+int(self.getAudioDatarate()))
        
        #Implementation via QML 
        self.addQMLcontainer() #put qquickview on widget       
        
        self.retranslateUi(Form)
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
        self.inPageLayout.addWidget(container,2,1,1,1)
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
        self.comboFormat.setItemText(1, _translate("Form", "vp6"))
        self.comboFormat.setItemText(2, _translate("Form", "vp8"))
        self.labelDatarate.setText(_translate("Form", "datarate"))
        self.labelOutputSize.setText(_translate("Form", "outputsize"))
        self.comboOutputSize.setItemText(0, _translate("Form", "1280x720"))
        self.labelKeyframeFreq.setText(_translate("Form", "Keyframe frequency"))
        self.labelLevel.setText(_translate("Form", "level"))
        self.checkDegradequality.setText(_translate("Form", "degradequality"))
        self.labelRtmpStream.setText(_translate("Form", "stream"))
        self.labelRtmpUrl.setText(_translate("Form", "url"))
        self.groupBox_2.setTitle(_translate("Form", "Audio"))
        self.labelFormatAudio.setText(_translate("Form", "format"))
        self.comboFormatAudio.setItemText(0, _translate("Form", "aac"))
        self.labelAudioDatarate.setText(_translate("Form", "datarate"))        


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
        Overrrides generic fakesink Playbin 
        """
        location="%s/%s live=true flashver=FMLE/3.0(compatible;FMSc/1.0)"%(self.rtmpUrl,self.rtmpStream)
        
        videoencoder="x264enc bitrate="+str(self.datarate)+" key-int-max="+str(self.keyframeFreq)+" bframes=0 byte-stream=false aud=true tune=zerolatency ! h264parse !  queue ! \
        video/x-h264,level=(string)"+str(self.level)+",profile=(string)"+self.profile+", width=(int)"+self.outputSize[0]+", height=(int)"+self.outputSize[1]+" "
                
        if self.audioFormat=="aac":
            audioencoder="pulsesrc ! queue ! audioconvert ! voaacenc bitrate="+str(self.audioDatarate*1000)+" ! aacparse ! audio/mpeg,mpegversion=4,stream-format=raw "
        if self.audioFormat=="mp3":
            audioencoder="pulsesrc ! queue ! audioconvert ! lamemp3enc bitrate="+str(self.audioDatarate)+" ! mpegaudioparse             "
        
        
        pipe="%s ! queue ! %s_mux. %s ! queue ! flvmux streamable=true  name=%s_mux ! queue name=queue_%s ! identity name=ident_%s sync=true ! rtmpsink location='%s' "%(videoencoder, self.pluginName,audioencoder, self.pluginName, self.pluginName, self.pluginName, location)
        
        
        #OPTION SHMSINK
        shmsrcPipeline="shmsrc socket-path=/tmp/%s name=source do-timestamp=true is-live=true ! queue leaky=2 max-size-buffers=2 !  capsfilter name=plugin_caps_%s  ! videoscale ! videoconvert ! %s"%(self.pluginName,self.pluginName, pipe)
        #shmsrcPipeline="shmsrc socket-path=/tmp/%s name=source do-timestamp=true is-live=true ! queue leaky=2 max-size-buffers=2 !  capsfilter name=plugin_caps_%s !  queue name=queue_%s ! identity name=ident_%s ! xvimagesink "%(self.pluginName,self.pluginName,self.pluginName,self.pluginName) #DEBUG
        print(shmsrcPipeline)
        return shmsrcPipeline
        
        #OPTION UDPSRC
        return "udpsrc  name=source port=1234 ! application/x-rtp, payload=127 !  rtph264depay !  avdec_h264 ! videoscale ! videoconvert ! xvimagesink "#+pipe
    
    
        #OPTION APPSRC
        #self._recording_pipeline ="appsrc name=source   block=true is-live=true ! filesink location=test.mp4" 
        #return self._recording_pipeline  #TO DEBUG 
        return "appsrc  block=true is-live=true  name=source ! capsfilter name=apps_1_caps ! videoconvert ! videoscale ! videorate ! "+pipe
    
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







    