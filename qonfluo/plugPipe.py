# -*- coding: utf-8 -*-

import gi
gi.require_version('Gst', '1.0')
from gi.repository import GObject, Gst
# Needed for window.get_xid(), xvimagesink.set_window_handle(), respectively:
from gi.repository import GdkX11, GstVideo


from PyQt5.QtCore import *
from functools import partial
import time

class PlugPipe(QThread):
    eos=pyqtSignal(str)
    error=pyqtSignal(str,str)
    sync=pyqtSignal(str)
    onPipeTraffic=pyqtSignal(str,int)
    terminated=pyqtSignal()
    def __init__(self, pluginName, parent=None):
        QThread.__init__(self,parent)
        self.test = ''
        self.exiting = False
        self.pluginName = pluginName
        self.setObjectName("qonfluo_"+self.pluginName)
    def passPipe(self,endPoint, pipeline):
        """
        PARAMETERS:
        -----------
        endPoint: Gst.Element
            the sink endpoint of main pipe
        pipeline : str
        """
        self.endPoint = endPoint
        #pipeline= "videotestsrc ! autovideosink" #debug:
        self.pipe=Gst.parse_launch(pipeline)
        #bp 1 - sync respective caps between tcpsink (endpoint) and tcpclient (pipe)
        bus= self.pipe.get_bus()
        bus.add_signal_watch()
        bus.enable_sync_message_emission()
        bus.connect("message::eos", self.onEosMessage)
        bus.connect("message::error", self.onErrorMessage)
        bus.connect("sync-message::element", self.onSyncMessage) 


        #Attach IDentity Part stats
        try:
            queuePlug=self.pipe.get_by_name("queue_stats_%s"%self.pluginName)
            ident=self.pipe.get_by_name("identity_stats_%s"%self.pluginName)
            ident.connect('handoff', partial(self.onHandoff,queuePlug))
        except:
            print("[%s]Plugin claim no stats" %self.pluginName)

    def onEosMessage(self, bus, msg):
        """
        Whenever end of stream present in plugin
        Parameters
        ----------
        bus: Gst.Bus
        msg: Gst.Message
        
        Emits:
        --------
        str: the name of the plugin that get eos
        Emits:
        -------
        terminated thread signal
        """        
        print('[%s]End Of Stream, graceful exit'%self.pluginName)
        self.pipe.set_state(Gst.State.NULL)
        self.eos.emit(self.pluginName)      
        self.terminated.emit()
        self.exiting=True
        

        
        
    def onErrorMessage(self, bus, msg):
        """
        Whenever error present in plugin
        Parameters
        ----------
        bus: Gst.Bus
        msg: Gst.Message
        
        Emits:
        ------
        str: the error message
        str: the name of the plugin
        """        
        err, debug = msg.parse_error()
        self.error.emit(self.pluginName, "[%s]Error: %s \n\tDEBUG:%s" % (self.pluginName, err, debug) )
        #self.pipe.set_state(Gst.State.NULL)
        
        
    def onSyncMessage(self, bus, message):
        """
        When plugin play gets synced
        Parameters
        ----------
        pluginName: str
            the name of the plugin that gets the error
        bus: Gst.Bus
        msg: Gst.Message
        Emits:
        -----
        str: the plugin name that gets synced
        """        
        print(message.get_structure().get_name())
        print(message.src.name)
        self.sync.emit(self.pluginName)

    def onHandoff(self, queuePlug, element, buf):
        """
        new identity handoff, so propagate the current buffer kbps of queuePlug to everywhere. We use identity to get handoffs and queue to get buffer level transformed in kbps to plot this via QML and plugin 
        Parameters
        ----------
        queuePlug: Gst.Element
            the queue element used to get kbps
        element: Gst.Element
            the identity element we use to trigger data input 
        Emits:
        ------
        str: plugin name
        int: the kbps 
        """
        props=queuePlug.props
        if props.current_level_bytes > 0:
            rate=props.current_level_bytes*8.0/1000.0
            time=props.current_level_time/1000000000.0
            if not time == 0:
                kbps=rate/time
            else:
                kbps=0
            if kbps >1:
                self.onPipeTraffic.emit(self.pluginName, kbps)
        data=buf.extract_dup(0,buf.get_size())
        databytes='on_handoff - %d bytes' % len(data)

    def requestChangeCaps(self, pad, unused):
        """
        Callback when caps are set for the shmsink element's
        sink pad. We then keep in memory these caps to serve to client.
        Tries to get specific capsfilter in the pipe and change the caps of that filter prior of encoder source to new caps.
        SHMSINK cruft

        """        
        caps=pad.props.caps
        if caps is None or not caps.is_fixed():
            return
        else:
            print ("Caps are %s" % (caps))
            
            capps=self.pipe.get_by_name("plugin_caps_%s"%self.pluginName)
            try:
                capps.set_property("caps",caps)
                print("[%s] Setting plugin caps to %s"%(self.pluginName, capps.get_property("caps").to_string()))                
            except:
                print("[%s]no need to define plugin caps or non existent"%self.pluginName)
  
    def stopPlay(self):
        """
        Stops the pipe.
        """
        self.pipe.send_event(Gst.Event.new_eos())
    def run(self):
        """
        QThread main
        """
        self.pipe.set_state(Gst.State.PLAYING)
        while self.exiting==False:
             time.sleep(1)
