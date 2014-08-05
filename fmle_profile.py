from xml.etree import ElementTree
# http://docs.python.org/library/xml.etree.elementtree.html
class flashmedialiveencoder_profile(object):
    """
        Parses a xml fmle profile 
        
    """ 
    def __init__(self,fileName):
        self.exitCode=-1
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
        print(self.name)
        print(self.protocols)        
        print(self.input_caps)
        print(self.encoder)
        self.exitCode=1
    def sanitizeToInt(self, text):
        """
        Sometimes ustream offers numbers with ; so convert text with strange chars to int value
        """
        return text.replace(";","")

    def operation(self,node):
        """Just a sample function that prints the tag of a node."""
        #print(node.tag)
        #print(node)
        
    def recur_node(self,node, f):
        """Applies function f on given node and goes down recursively to its 
        children.
            
        Keyword arguments:
        node - the root node
        f - function to be applied on node and its children
            
        """
        if node != None:
            f(node)
            for item in node.getchildren():
                self.recur_node(item, f)
        else:
            return 0


