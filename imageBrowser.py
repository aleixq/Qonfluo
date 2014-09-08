#
# <one line to give the program's name and a brief idea of what it does.>
# Copyright (C) 2014  kinta <kinta@communia.org>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# 
#
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QImage,QPixmap, QPalette
class ImageBrowser(QWidget):
    imageSet=pyqtSignal([str])
    XSet=pyqtSignal([int])
    YSet=pyqtSignal([int])
    alphaSet=pyqtSignal([int])
    sizeSet=pyqtSignal([str])
    def __init__(self):
        QWidget.__init__(self)
        layout=QGridLayout(self)
        self.monitor=QLabel()
        self.monitor.setSizePolicy( QSizePolicy.Ignored, QSizePolicy.Ignored );
        self.monitor.setScaledContents(True)
        scrollArea = QScrollArea()
        scrollArea.setBackgroundRole(QPalette.Dark)
        scrollArea.setWidget(self.monitor)            
        
        #filename = source.get_property("location")
        #image=QImage(filename)
        #image=image.scaledToHeight(60)
        
        #self.monitor.setPixmap(QPixmap.fromImage(image));   
        self.monitor.adjustSize()
        layout.addWidget(scrollArea,0,0,1,6)
        
        #Enable Control
        self.enabledDev=QCheckBox("Enabled")
        
        self.enabledDev.setChecked(True)
        self.enabledDev.stateChanged.connect(self.toggleDevice)
        layout.addWidget(self.enabledDev, 1, 0, 1, 6)        
        #Alpha Control
        self.sliderAlpha = QSlider(Qt.Horizontal, self)
        self.sliderAlpha.setFocusPolicy(Qt.StrongFocus)
        self.sliderAlpha.setTickPosition(QSlider.TicksBothSides)
        self.sliderAlpha.setSliderPosition(100)
        self.sliderAlpha.setTickInterval(10)
        self.sliderAlpha.setSingleStep(1)
        self.sliderAlpha.valueChanged.connect(self.twAlpha)
        alphaLabel=QLabel("<small>Alpha</small>")
        layout.addWidget(alphaLabel, 2, 0, 1, 1)
        layout.addWidget(self.sliderAlpha, 2, 1, 1, 5)
        
        
        #X position
        self.sliderX = QSlider(Qt.Horizontal, self)
        self.sliderX.setFocusPolicy(Qt.StrongFocus)
        self.sliderX.setTickPosition(QSlider.TicksBothSides)
        self.sliderX.setTickInterval(10)
        self.sliderX.setSingleStep(1)
        self.sliderX.valueChanged.connect(self.twX)
        XLabel=QLabel("<small>X</small>")
        layout.addWidget(XLabel, 3, 0, 1, 1)
        layout.addWidget(self.sliderX, 3, 1, 1, 5)

        #Y position
        self.sliderY = QSlider(Qt.Horizontal, self)
        self.sliderY.setFocusPolicy(Qt.StrongFocus)
        self.sliderY.setTickPosition(QSlider.TicksBothSides)
        self.sliderY.setTickInterval(10)
        self.sliderY.setSingleStep(1)
        self.sliderY.valueChanged.connect( self.twY )
        YLabel=QLabel("<small>Y</small>")
        layout.addWidget(YLabel, 4, 0, 1, 1)
        layout.addWidget(self.sliderY, 4, 1, 1, 5)
        
       
        #Z-order
        self.zorders= QSpinBox(self)
        #self.zorders.setValue(devindex+1)
        ZLabel=QLabel("<small>Z</small>")
        layout.addWidget(ZLabel, 5, 0, 1, 3)
        layout.addWidget(self.zorders, 5, 3, 1, 3)
        self.zorders.valueChanged.connect(self.twZ )
        #self.sinks.set_property("zorder", devindex+1) #SET INITIAL Z-ORDER

        #formats combo
        self.comboSize= QComboBox(self)
        self.comboSize.setEditable(True)        
        layout.addWidget(self.comboSize, 6, 1, 1, 5)
        self.comboSize.activated.connect(self.twSize)
        labelSize=QLabel("Size")
        layout.addWidget(labelSize, 6, 0, 1, 1)
        
        pass
    def setImage(self,fileName=None):
        """
        Sets the image overlay
        """
        if not fileName:
            fileName, _ = QFileDialog.getOpenFileName(self)
        self.imageSet.emit(fileName)
    def setMaximums(self,XAndY):
        """
        Sets the maximum of resolution to be able to set position x and y , util when canvas size changes
        """
        (width,height)=XAndY
        self.sliderX.setMaximum(int(width)/10)
        self.sliderY.setMaximum(int(height)/10)             
    def twAlpha(self,value):
        """
        Tweaks Alpha property to @value for image
        Parameters
        ----------
        value: int
            the value of the qslider
        """
        self.alphaSet.emit(value)
    def twZ(self,value):
        """
        Tweaks Z order property to @value for image
        """
        self.Zset.emit(value)
    def twSize(self,value):
        """
        Tweaks input Resolution property to @value for image
        Parameters
        ----------
        value: str
            the size value of the qcombobox    
        """       
        self.sizeSet.emit(value)


    def twX(self,value):
        """
        Tweaks X property to @value for image
        Parameters
        ----------
        value: int
            the x value of the qslider
        """
        self.XSet.emit(value)
    def twY(self,value):
        """
        Tweaks Y property to @value for image
        Parameters
        ----------
        value: int
            the y value of the qslider
        devindex:str
            the index of the video device        
        """
        self.YSet.emit(value)
    def toggleDevice(self,value):
        """
        toggles(hides or shows) the image whenever checkbox gets toggled by user
        Parameters
        ----------
        value: int
            the value of the qcheckbox
        """       
        
        #self.player.unlink(self.player.get_by_name("vsrc"+str(devindex)))#TODO is necessary to remove pad ???
        if value==0:
            self.sinks[devindex].set_property("alpha", 0)            
        if value==2:
            self.sinks[devindex].set_property("alpha", self.sliderAlpha[devindex].sliderPosition()/100)
        
