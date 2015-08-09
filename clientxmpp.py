from sleekxmpp import ClientXMPP
from sleekxmpp.exceptions import IqError, IqTimeout


class ClientXmppBot(ClientXMPP):

    def __init__(self, jid, password, server_jid):
        ClientXMPP.__init__(self, jid, password)

        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("message", self.message)
        self.server_jid = server_jid
        self.msgcallback = {}
        
        
    def session_start(self, event):
        self.send_presence()
        self.get_roster()
        # Handle Errors

    # received_key_ack: upon key received by server
    # stop_node: server wants the node to shut down
    # change_ip: server wants to change ip
    def add_callback(self, function_name, function_addr):
        self.msgcallback[function_name] = function_addr        
        
    #server asks for public_key by sending 'get_key', should reply with the public key
    def message(self, msg):
        if msg['type'] in ('chat', 'normal'):
            msgs = msg['body'].split(' ',1)
            
            if msgs[0] == 'get_key':
                self.send_message(mto = self.server_jid, mbody = 'register '+ self.jid + ' ' + self.pk)
            elif msgs[0] == 'received_key_ack':
                if 'received_key_ack' in self.msgcallback.keys():
                    self.msgcallback['received_key_ack']()
            elif msgs[0] == 'stop_node':
                if 'stop_node' in self.msgcallback.keys():
                    self.msgcallback['stop_node']()
            elif msgs[0] == 'change_ip':
                if 'change_ip' in self.msgcallback.keys():
                    self.msgcallback['change_ip']()
            else:
                print "unformated msg",msgs

def init(jid, jp, s_jid, x_host):
    global instance
    instance = ClientXmppBot(jid, jp, s_jid)
    
    #if any character in x_host is alpha
    is_ip = True
    for c in x_host:
        if c.isalpha():
            is_ip = False
            break

    if not is_ip:
        if not instance.connect(reattempt=False):
            raise IOError('Could not connect to xmpp server')
    else:
        #create tuple (xmpp_host_ip,port)  ,default ejabberd port = 5280 
        if ':' in x_host:
            x_host_tuple = tuple(x_host.split(':'))
        else:
            x_host_tuple = (x_host,'5280')

        if not instance.connect(address=x_host_tuple, reattempt=False):
            raise IOError('Could not connect to xmpp server')    
    instance.process(block=False)               


'''
if __name__ == '__main__':
    xmpp = ClientBot('bob_sushant@xmpp.jp', 'bob123','alice_sushant@xmpp.jp','PUBLICKEYBLAHBLAHBLAH')
    xmpp.connect()
    xmpp.process(block=False)
    xmpp.send_key_server()
'''
