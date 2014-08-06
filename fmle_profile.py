from xml.etree import ElementTree
# http://docs.python.org/library/xml.etree.elementtree.html
class flashmedialiveencoder_profile(object):
    """
        Parses a xml fmle profile 
    Attributes
    ----------
    exitCode: int 
        0 if something goes wrong, 1 if well
    protocols: dict{ 
                    (str) "protocolname" : dict{ 
                                                (str) "url": (str) 
                                                    the url, 
                                                (str)"stream": (str) 
                                                    "the stream token"
                                           },
                }
                protocols represents the protocols available that can be streamed
    input_caps: dict{
                    (str)'audio': dict{ 
                                    (str)'volume': (str)
                                        'the audio volume'
                                    (str)'sample_rate': (str)
                                        'the sample rate' 
                                    (str)'channels': (str) 
                                        'the number of audio channels'
                                  }, 
                    (str)'video': dict{
                                    (str)'width': (str)
                                        'the video width', 
                                    (str)'height': (str)
                                        'the video height', 
                                    (str)'frame_rate': (str)
                                        'the video framerate'
                                  }
                    }
                    input_caps is the desired properties for the input video
     encoder: dict{
                    (str)'audio': dict{
                                        (str)'datarate': (str),
                                            the audio bitstream in kbps
                                        (str)'format': (str)
                                            the audio format
                                      }, 
                    (str)'video': dict{
                                        (str)'datarate': (str), 
                                            the video bitstream in kbps
                                        (str)'format': (str), 
                                            the video format to use
                                        (str)'width': (str), 
                                            the video width
                                        (str)'level': (str), 
                                            the h264 compression level, a specified set of constraints that indicate a degree of required decoder performance for a profile.
                                        (str)'degradequality': (str),
                                            the Degrade quality, degrades the quality of the video by reducing the bit rate until data can be streamed without exceeding the specified RTMP buffer size
                                        (str)'keyframe_frequency': (str), 
                                             The interval at which to insert keyframes
                                        (str)'height': (str)
                                            the video height
                                      }
                    
              }
              the encoder properties

    """ 
    def __init__(self,fileName):
        """
        Constructor
        Returns:
        --------
        exitCode : int
            -1 value indicates correct code, or zero on fail.
        """
        self.exitCode=0
        try:
            self.root = ElementTree.parse(fileName).getroot()
            self.doc= ElementTree.parse(fileName)
            #Recursive tree walking
            #return self.recur_node(self.root, self.operation)                                                                                      
        except  Exception as e:
            # there should be some proper exception handling here
            print( "Error: %s" % str(e) )
            return -1
        self.name= self.doc.findall("./preset/name")[0].text
        self.protocols={}
        for protocol in self.doc.findall("./output/"):
            self.protocols[protocol.tag]={"url": protocol.findall("url")[0].text, "stream":  protocol.findall("stream")[0].text}                    
        self.input_caps={}
        for video in self.doc.findall("./capture/video"):
            self.input_caps["video"]={"width": self.sanitizeToInt(video.findall("size/width")[0].text), "height":  self.sanitizeToInt(video.findall("size/height")[0].text) , "frame_rate": video.findall("frame_rate")[0].text}       
        for audio in self.doc.findall("./capture/audio"):
            self.input_caps["audio"]={"sample_rate": audio.findall("sample_rate")[0].text, "channels":  audio.findall("channels")[0].text , "volume": audio.findall("input_volume")[0].text}                   
        self.encoder={}
        for video in self.doc.findall("./encode/video"):
            self.encoder["video"]={
                "format": video.findall("format")[0].text.lower(),
                "datarate":self.sanitizeToInt(video.findall("datarate")[0].text),
                "width": self.sanitizeToInt(video.findall("outputsize")[0].text.split('x')[0]),
                "height":self.sanitizeToInt(video.findall("outputsize")[0].text.split('x')[1]),
                "keyframe_frequency":video.findall("advanced/keyframe_frequency")[0].text,
                "level":video.findall("advanced/level")[0].text, #http://en.wikipedia.org/wiki/H.264/MPEG-4_AVC#Levels
                "degradequality":video.findall("autoadjust/degradequality/enable")[0].text
            }
        for audio in self.doc.findall("./encode/audio"):
            self.encoder["audio"]={
                "format": audio.findall("format")[0].text.lower(),
                "datarate":audio.findall("datarate")[0].text,
            }
        self.exitCode=1
    def sanitizeToInt(self, text):
        """
        Sometimes ustream offers numbers with ; so convert text with strange chars to int value
        Parameters:
        -----------
        text: str 
            text that will be sanitized
        """
        return text.replace(";","")
        
    def recur_node(self,node, f):
        """Applies function f on given node and goes down recursively to its 
        children.
            
        Parameters:
        -----------
        node:  xml.etree.ElementTree.Element
            the root node
        f: function
            function to be applied on node and its children
            
        """
        if node != None:
            f(node)
            for item in node.getchildren():
                self.recur_node(item, f)
        else:
            return 0


