import urllib2
import urllib
import json
import os
        
class Connect() : 
    def __init__(self) : 
        self.baseurl = 'http://%s/IPOP/default'
        self.url = ''
               
        
    def generateURL(self, host) : 
        self.url = self.baseurl%(host)
        return self.url    
    
    def checkValid(self):
        try:
            urllib2.urlopen(self.url+'/creategvpn')
        except urllib2.HTTPError, e:
            print(e.code)
            return False
        except urllib2.URLError, e:
            print(e.args)
            return False
        return True
        
    
    def getConfigData(self, jid):
        values = {'type':'getjson','xmppid' : jid}
        data = urllib.urlencode(values)        
        response = urllib2.urlopen(self.url+'/get?'+data)
        return response.read()
        
    def getServerJid(self, jid):
        values = {'type':'getserverjid','xmppid' : jid}
        data = urllib.urlencode(values)        
        response = urllib2.urlopen(self.url+'/get?'+data)
        return response.read()
    
    def setStatus(self, jid, stat):
        values = {'type':'change_status', 'xmppid' : jid, 'status' : stat}
        data = urllib.urlencode(values)        
        response = urllib2.urlopen(self.url+'/set?'+data)
        return response.read()
        
    def storeConfigData(self, response):
        dic = json.loads(response)
        dic ["ganglia_stat"] = "True"
        dic ["ganglia_path"] = os.environ['GANGLIA_DIR']
        with open(os.environ['WORKING_DIR']+'conff.json', 'w') as outfile:
            outfile.write(json.dumps(dic))
        
            
def init():
    global instance, jid, jpassword, serverjid
    instance = Connect()
    
                                
         

