from PyQt4 import QtGui
from PyQt4.QtGui import QImage
import urllib
import connect

class GangliaGraph() : 
    def __init__(self) : 
        self.url = 'http://%s/ganglia/graph.php?'
        self.values = {
            'r' : 'hour',
            'z' : 'small',
            'c' : 'my cluster',
            'h' : 'localhost',
            'm' : 'graphname',
            'vl' : 'verticalaxis',
            'ti' : 'title'            
            }
        self.durationMap = {
            0 : 'hour',
            1 : '2hr',
            2 : '5hr',
            3 : 'day',
            4 : 'week',
            5 : 'month',
            6 : 'year'
            }
        self.graphtypeMap = {
            0 : 'peer_bytes_recv_-',
            1 : 'peer_bytes_sent_-',
            2 : 'peer_conn_age_-',
            3 : 'peer_status_-',
            4 : 'peer_xmpp_time_-'
            }
        
        
    def generateURL(self) :
        try: 
            return self.url%(connect.adminip.split(':')[0]) + urllib.urlencode(self.values)    
        except:
            return self.url
    
    def setValues(self, duration, graphtype) : 
        self.values['r'] = self.durationMap[duration]
        #fix-this
        self.values['m'] = self.graphtypeMap[graphtype] + '172.31.0.102'        
        if graphtype == 0 : 
            self.values['vl'] = 'Bytes/Second'
            self.values['ti'] = 'Bytes received'
        elif graphtype == 1 : 
            self.values['vl'] = 'Bytes/Second'
            self.values['ti'] = 'Bytes sent'
        elif graphtype == 2 : 
            self.values['vl'] = 'Seconds'
            self.values['ti'] = 'Connection age'
        elif graphtype == 3 : 
            self.values['vl'] = 'On/Off'
            self.values['ti'] = 'Status'
        elif graphtype == 4 : 
            self.values['vl'] = 'Seconds'
            self.values['ti'] = 'Xmpp time'
        else : 
            pass

    
    def getGraph(self, duration, graphtype) : 
        self.setValues(duration, graphtype)
        url = self.generateURL()
        try:
            imgdata = urllib.urlopen(url).read()
            image = QtGui.QImage()
            image.loadFromData(imgdata)
        except:
            return QtGui.QImage()
        return image
                                
         

