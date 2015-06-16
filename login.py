import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import *#pyqtSlot, SIGNAL, SLOT, QTimer
from ui.login import Ui_Login
from connect import Connect
from clientxmpp import ClientXmppBot
import urllib

from Crypto.PublicKey import RSA
from Crypto import Random

class LoginWidget(QtGui.QWidget):
    #Signals
    keyreg = pyqtSignal()
    
    # add layouts
    def __init__(self):
        super(LoginWidget, self).__init__()
        self.ui = Ui_Login()
        self.ui.setupUi(self)
        
        self.setLayout(self.ui.login_uiLayout)
        self.ui.Loginwidget.setLayout(self.ui.loginLayout)
        self.ui.Progresswidget.setLayout(self.ui.progressLayout)
        
        self.connectSignals()
        self.Connect = Connect()
        self.jid = ""
        
        self.ui.hostipTxtbox.setText("127.0.0.1:8000")
        self.ui.xmppTxtbox.setText("bob_sushant@xmpp.jp")
        self.ui.xmppPwTxtbox.setText("bob123")
        self.timer = QTimer()
        
        self.ipopproc = QProcess()
        
        #generate new key for the session
        random_generator = Random.new().read
        self.key = RSA.generate(2048, random_generator)
        
        

    def changeView(self):
        xmppTxtbox = self.ui.xmppTxtbox
        xmppPwTxtbox = self.ui.xmppPwTxtbox
        if(xmppTxtbox.displayText().isEmpty() or xmppPwTxtbox.displayText().isEmpty()):
            #feature: check if valid Jid
            self.changeStatus('Enter XMPP ID and password')
        else:
            self.jid = xmppTxtbox.displayText()
            self.jpassword = xmppPwTxtbox.displayText()
            self.Connect.generateURL(self.ui.hostipTxtbox.displayText())
            if(not self.Connect.checkValid()):
                self.changeStatus('Could not connect')
                return
            self.ui.loginStackedWidget.setCurrentIndex(1)
            self.changeProgress(10, "Server responded")
            self.setSingleShotTimer(self.getServerJid)
            
    def getServerJid(self):
        self.serverjid = self.Connect.getServerJid()
        self.changeProgress(25, "Server XMPP ID received")
        self.setSingleShotTimer(self.registerKey)

    
    def registerKey(self):
        public_key = self.key.publickey().exportKey('PEM')
        #get this from the form
        self.xmpp = ClientXmppBot( self.jid, self.jpassword, self.serverjid, public_key)
        self.xmpp.connect()
        self.xmpp.process(block=False)
        self.xmpp.add_callback('received_key_ack', self.registerKeyCB)
        self.xmpp.send_key_server()
        
    
    #when key is succesfully     
    def registerKeyCB(self):
        #otherwise it would be called from non-qt thread
        self.keyreg.emit()
        self.xmpp.disconnect()
              
        
        
    @pyqtSlot()
    def getConfiguration(self):
        self.changeProgress(35, "Key registered")       
        
        enc_data = self.Connect.getConfigData(self.jid)
        data = self.key.decrypt(enc_data)
        self.Connect.storeConfigData(data)
        
        self.changeProgress(50, "Configuration received")
        self.setSingleShotTimer(self.startIpop)
        
        
    def startIpop(self):
        self.changeProgress(75, "Starting IPOP")
        #fix-this
        self.ipopproc.setWorkingDirectory("/home/hotsushi/game/ipoptemp/")
        options = QStringList()
        options << "-c" << "./ipop-tincan-x86_64 1> out.log 2> err.log &"
        self.ipopproc.start("/bin/sh", options);
        
        
    def setSingleShotTimer(self, functionaddr):
        self.timer = QTimer()
        self.timer.connect(self.timer, SIGNAL("timeout()"), functionaddr)
        self.timer.setSingleShot(True)
        self.timer.start(500)
        
    def connectSignals(self):
        connectBtn = self.ui.connectBtn
        connectBtn.connect( connectBtn, SIGNAL("clicked()"), self.changeView )      
        self.keyreg.connect(self.getConfiguration)

    def changeStatus(self, stringg):
        self.ui.loginstatusLabel.setText(stringg)
    
    def changeProgress(self, percent, text):
        self.ui.progressBar.setValue(percent)
        self.ui.progressLabel.setText(text)      
        
                   
