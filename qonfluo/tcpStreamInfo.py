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
from PyQt5.QtNetwork import *

class TcpStreamInfo(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.ip="127.0.0.1"
        self.port="14050"     
        interfaces=QNetworkInterface().allInterfaces()
        if len(interfaces) > 1:
            
            self.ip=QNetworkInterface().allInterfaces()[1].addressEntries()[0].ip().toString()        
        layout=QGridLayout(self)
        command = QLineEdit("gst-launch-1.0  tcpclientsrc host=%s port=%s ! decodebin name=d  d. ! autovideosink  d. ! autoaudiosink"%(self.ip, self.port),self)
        command.setReadOnly(True) 
        layout.addWidget(command, 1, 0, 1, 1)
        self.notice=QLabel()
        self.notice.setWordWrap(True)
        layout.addWidget(self.notice, 0, 0, 1, 1)
        self.retranslateUi() 

        
        
    def retranslateUi(self):
        self.notice.setText(self.tr( "Notice that QOnfluo is always streaming to  Tcp Sink. In your case is using %s on port %s. Launching next command somewhere you can relay this stream."%(self.ip, self.port) ))
