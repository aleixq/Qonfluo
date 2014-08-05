from PyQt5.QtCore import pyqtProperty, QVariant
from PyQt5.QtQml import qmlRegisterType, QQmlListProperty
from PyQt5.QtQuick import QQuickItem
# This Class is to implement a python queue to QML to represent the stream datarate in a qml plotter
#
class NetworkData(QQuickItem):
    @pyqtProperty(str)
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        
    @pyqtProperty(QVariant)
    def data(self):
        """
        Gets the List converted in qvariant (http://stackoverflow.com/questions/23504404/pyqtslot-and-return-type-python-list)
        """
        return QVariant(self._values)
    
    @data.setter
    def data(self, value):
        """
        sets the plot with buffer datarate value, it is averaged every 50 takes to calm qml plotter
        """
        #print("data set to %s"%value)
        if len(self._midValues) >49:
            self._values.pop()
            self._values.insert(0,sum(self._midValues)/len(self._midValues))
            self._midValues=[]
        else:
            self._midValues.insert(0,value)
        
    @pyqtProperty(QVariant)
    def labels(self):
        return QVariant(self._labels)   
    
    def __init__(self, parent=None):
        super(NetworkData, self).__init__(parent)

        self._name = ''
        self._labels=[]
        self._values=[]
        self._midValues=[]
        self._values.insert(0,0)
        for val in range(1,50):
            self._values.insert(val,0)
        for val in range(0,len(self._values)):
            self._labels.insert(val,"")