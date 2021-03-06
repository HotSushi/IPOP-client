import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *#pyqtSlot, SIGNAL, SLOT, QTimer
from ui.login import Ui_Login
import connect
import clientxmpp
import process
import urllib
import json

from Crypto.PublicKey import RSA
from Crypto import Random

class LoginWidget(QtGui.QWidget):
    #Signals
    started = pyqtSignal()
    show_signal = pyqtSignal()
    keyreg = pyqtSignal()
    
    # add layouts
    def __init__(self):
        super(LoginWidget, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        self.setLayout(self.ui.login_uiLayout)
        self.ui.Loginwidget.setLayout(self.ui.loginLayout)
        self.ui.Progresswidget.setLayout(self.ui.progressLayout)
        
        process.init()
        connect.init()
        
        self.connectSignals()
        self.jid = ""
        
        self.ui.hostipTxtbox.setText("127.0.0.1:8000")
        self.ui.xmppTxtbox.setText("alice_sushant@xmpp.jp")
        self.ui.xmppVpnTxtbox.setText("public_server")
        
        # this is a quick-fix, remove completely afterwards
        self.ui.xmppPwTxtbox.hide()

        self.timer = QTimer()
        
        
        #generate new key for the session
        random_generator = Random.new().read
        self.key = RSA.generate(2048, random_generator)   

    def changeView(self):
        xmppTxtbox = self.ui.xmppTxtbox
        xmppPwTxtbox = self.ui.xmppPwTxtbox
        if(xmppTxtbox.displayText().isEmpty()):
            #feature: check if valid Jid
            self.changeStatus('Enter XMPP ID and password')
        else:
            connect.jid = str(xmppTxtbox.displayText())
            connect.jpassword = 'null'
            connect.adminip = str(self.ui.hostipTxtbox.displayText())
            connect.vpnname = str(self.ui.xmppVpnTxtbox.displayText())
            connect.instance.generateURL(connect.adminip)
            if(not connect.instance.checkValid()):
                self.changeStatus('Could not connect')
                return
            self.ui.loginStackedWidget.setCurrentIndex(1)
            self.changeProgress(10, "Server responded")
            self.setSingleShotTimer(self.checkClientJidAvailability)

    def checkClientJidAvailability(self):
        try:
            self.serverjid = connect.instance.getClientJidAvailable(connect.jid)
        except:
            self.changeStatus("Client JID is already in use")
            self.setToLogin()
            return
        self.changeProgress(15, "Client JID available")
        self.setSingleShotTimer(self.getServerJid)
    
    def getServerJid(self):
        try:
            self.serverjid = connect.instance.getServerJid(connect.jid, connect.vpnname)
        except:
            self.changeStatus("Server couldn\'t find the JID")
            self.setToLogin()
            return

        self.changeProgress(25, "Server XMPP ID received")
        self.setSingleShotTimer(self.registerKey)
        #self.setSingleShotTimer(self.startProcess)
        
    def registerKey(self):
        public_key = self.key.publickey().exportKey('PEM')      
                        
        #when key is succesfully registered emit 'keyreg' signal which will call 'getConfiguration()'     
        connect.instance.setPublicKey( connect.jid, connect.vpnname, public_key)
        self.setSingleShotTimer(self.getConfiguration)
        
    def getConfiguration(self):
        self.disconnect(process.ipopprocess,SIGNAL('stopped()'),self.keyreg.emit)
        
    
        self.changeProgress(35, "Key registered")       
        
        enc_data = connect.instance.getConfigData(connect.jid, connect.vpnname)
        data = self.key.decrypt(enc_data)
        connect.instance.storeConfigData(data)
        
        # change /etc/ganglia/gmond.conf if available
        self.changeGmond()
        
        self.changeProgress(50, "Configuration received")
        # sleekxmpp receives admingvpns msgs , best to not initiate it
        if connect.instance.getLocalConfigData('is_admingvpn') == 'yes':
            self.setSingleShotTimer(self.startProcess)
        else:
            self.setSingleShotTimer(self.startClientXMPP)
    
    def startClientXMPP(self):
        #get this from the form
        try:
            clientxmpp.init( connect.jid, connect.jpassword, self.serverjid, connect.instance.getLocalConfigData('xmpp_host'))
        except IOError as err:
            self.changeStatus(str(err))
            self.setToLogin()
            return
        self.changeProgress(70, "Starting Client XMPP")
        self.setSingleShotTimer(self.startProcess)

    def changeGmond(self):
        try:
            with open('/etc/ganglia/gmond.conf','r') as f:
                data = f.read()
        except IOError as err:
            return
        startidx = data.find('udp_send_channel')
        startidx += data[startidx:].find('host')
        startidx += data[startidx:].find('=')

        endidx = startidx + data[startidx:].find('\n')

        hostip = connect.adminip.split(':')[0]
       
        newdata = data[:startidx+1] + " " + hostip + data[endidx:]
        with open('/etc/ganglia/gmond.conf','w') as f:
             f.write(newdata)
        
    def startProcess(self):
        self.changeStatus(" ")

        process.ipopprocess.setAdminGVPN(connect.instance.getLocalConfigData('is_admingvpn') == 'yes')
        process.ipopprocess.start()
    
    def setToLogin(self):
        self.setView(0)  
        
    def setSingleShotTimer(self, functionaddr):
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), functionaddr)
        self.timer.setSingleShot(True)
        self.timer.start(500)
        
    def connectSignals(self):
        connectBtn = self.ui.connectBtn
        connectBtn.connect( connectBtn, SIGNAL("clicked()"), self.changeView )
        self.connect(process.ipopprocess, SIGNAL("controller_started()"), self.started.emit)
        self.keyreg.connect(self.getConfiguration)
        self.show_signal.connect(self.show)


    def changeStatus(self, stringg):
        self.ui.loginstatusLabel.setText(stringg)
    
    def changeProgress(self, percent, text):
        self.ui.progressBar.setValue(percent)
        self.ui.progressLabel.setText(text) 
        
    def setView(self,idx):
        self.ui.loginStackedWidget.setCurrentIndex(idx)
            
         
        
                   
