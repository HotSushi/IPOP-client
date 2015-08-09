import urllib2
import urllib
import json
import os
        
class Connect() :
    def __init__(self) : 
        self.baseurl = 'http://%s/IPOP/default'
        self.url = ''
        self.config = {}            
        
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
        
    def setPublicKey(self, jid, PK):
        values = {'type':'set_public_key','xmppid' : jid, 'public_key':PK}
        data = urllib.urlencode(values)        
        response = urllib2.urlopen(self.url+'/set?'+data)
        return response.read()
    
    def setLog(self,logname,logdata):
        values = {'type':'set','node':jid,'name':logname,'log':logdata}
        data = urllib.urlencode(values)        
        print self.url+'/log?'+data
        response = urllib2.urlopen(self.url+'/log?'+data)
        return response.read()
    
    def getLocalConfigData(self, key):
        return self.config[key]

    def storeConfigData(self, response):
        dic = json.loads(response)
        dic ["ganglia_stat"] = "True"
        dic ["ganglia_path"] = os.environ['GANGLIA_DIR']
        dic ["tincan_logging"] = 2
        dic ["nick"] = dic["xmpp_username"].split('@')[0]

        self.config = dic
        with open(os.environ['WORKING_DIR']+'conff.json', 'w+') as outfile:
            outfile.write(json.dumps(dic))
        
            
def init():
    global instance, jid, jpassword, serverjid, adminip
    instance = Connect()
    
                                
         

