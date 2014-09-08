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
from PyQt5.QtCore import * #QFile, QTextStream, 
#from PyQt5.QtGui import QFileDialog

class TextBrowser(QWidget):
    broadcastString=pyqtSignal([str])
    broadcastFont=pyqtSignal([str,str,int,int])
    def __init__(self,sourceElement):
        QWidget.__init__(self)
        self.sourceElement=sourceElement
        layout=QGridLayout(self)
        
        self.fontPicker = QFontComboBox()
        self.fontSize = QSpinBox()
        self.fontSize.setMaximum(99)
        self.fontSize.setValue(12)
        self.fontSize.setToolTip(self.tr("Font size"))
        self.textList = QListWidget()
        self.textList.setSortingEnabled(False)
        self.emptyText= QListWidgetItem()
        self.textList.addItem(self.emptyText)
        self.emptyText.setText("")
        self.textAdder = QLineEdit()
        self.textAdder.setToolTip(self.tr("Write string and press enter to append to string list launcher"))
        self.textAdder.setClearButtonEnabled(True)
        self.textAdderButton=QPushButton(self.tr("Add string"))
        self.textAdderButton.setEnabled(False)
        self.halign=QComboBox()
        self.valign=QComboBox()
        self.halign.addItem(self.tr("left"),0)
        self.halign.addItem(self.tr("center"),1)
        self.halign.addItem(self.tr("right"),2)
        self.valign.addItem(self.tr("baseline"),0)
        self.valign.addItem(self.tr("bottom"),1)
        self.valign.addItem(self.tr("top"),2)
        self.valign.addItem(self.tr("center"),4)
        self.halign.setCurrentIndex(1)
        self.valign.setCurrentIndex(0)
       
        layout.addWidget(self.textList,0,0,1,2)
        layout.addWidget(self.textAdder,1,0,1,1)
        layout.addWidget(self.textAdderButton,1,1,1,1)
        layout.addWidget(self.fontPicker,2,0,1,1)
        layout.addWidget(self.fontSize,2,1,1,1)
        layout.addWidget(self.halign,3,0,1,1)
        layout.addWidget(self.valign,3,1,1,1)
        
        self.textAdder.returnPressed.connect(self.addString)
        self.textAdder.textChanged.connect(self.enableAddString)
        self.textAdderButton.clicked.connect(self.addString)
        self.textList.setContextMenuPolicy(Qt.CustomContextMenu)
        self.textList.customContextMenuRequested.connect(self.editItem)
        self.textList.itemDoubleClicked.connect(self.sendString)
        self.fontSize.valueChanged.connect(self.sendFont)
        self.fontPicker.currentFontChanged.connect(self.sendFont)
        self.halign.currentIndexChanged.connect(self.sendFont)
        self.valign.currentIndexChanged.connect(self.sendFont)
        self.broadcastString.connect(self.twText)
        self.broadcastFont.connect(self.twTextProps)
    def enableAddString(self,text):
        """
        Enables button if text is not empty
        Parameters:
        -----------
        text: str
        """
        self.textAdderButton.setEnabled(len(text)>0)
    def editItem(self,pos):
        """
        Set Item Editable 
        Parameters:
        -----------
        pos: QPos
        """
        item=self.textList.itemAt(pos)
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsEditable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled) #Set momentary editable
        self.textList.editItem(item)
        item.setFlags(Qt.ItemIsSelectable|Qt.ItemIsDragEnabled|Qt.ItemIsUserCheckable|Qt.ItemIsEnabled) # Unset Editable
    def sendString(self,item):
        """
        Sends string to mainwindow to be included to Gst textOverlay (item not used)
        """
        self.broadcastString.emit(item.text())
    def sendFont(self,value):
        """
        Sends Font Props (family, size, position) to Gst textOverlay (value not used)
        """        
        valign=self.valign.itemData( self.valign.currentIndex() ) 
        halign=self.halign.itemData( self.halign.currentIndex() ) 
        self.broadcastFont.emit(self.fontPicker.currentFont().family(),str(self.fontSize.value()), valign, halign)
    def addString(self):
        """
        Adds String to text List to be selected (double click sends to canvas
        """
        newString=QListWidgetItem(self.textAdder.text())
        newString.setToolTip(self.tr("Double click to launch, Right Click to edit"))
        self.textList.addItem(newString)
        self.textAdder.clear()
    def addStringsFromFile(self,fileName=None):
        """
        Add txt File lines to text List to be selected  (double click sends to canvas
        """
        if not fileName:
            fileUrl,_= QFileDialog.getOpenFileUrl(self.parent(),caption=self.tr("Open text file"), directory=QStandardPaths.standardLocations(QStandardPaths.HomeLocation)[0], filter="*.txt")
            fileName=fileUrl.toLocalFile() 
        if fileName:
            f = QFile(fileName)
            print(f)
            print(fileName)
  
            if f.open(QFile.ReadOnly | QFile.Text):
                stream = QTextStream(f)        
                row = 1
                while not stream.atEnd():
                    line = stream.readLine()
                    
                    self.textList.insertItem(row, line) 
                    row+=1
                    
                f.close()
                   
    def twText(self,text):
        """
        Tweaks the Text properties setting text overlay to @text 
        Parameters:
        -----------
        text: str 
        """
        self.sourceElement.set_property("text",text)
    def twTextProps(self,font,size,valign,halign):
        """
        Tweaks the Text properties setting text font overlay to @font and size to @size
        Parameters:
        -----------
        font: str 
        size: str
        """
        self.sourceElement.set_property("font-desc","%s %s"%(font,size))
        self.sourceElement.set_property("valignment",valign)
        self.sourceElement.set_property("halignment",halign)
