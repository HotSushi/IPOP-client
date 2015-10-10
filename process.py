import os
from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal,pyqtSlot, SLOT, SIGNAL,QProcess,QTimer
from log import LogUpdater
import connect
#time in seconds
HEARTBEAT_CYCLE = 8
    
class IPOPProcess(QtCore.QObject):
    #Signals
    ipop_started = pyqtSignal()
    controller_started = pyqtSignal()
    ipop_stopped = pyqtSignal()
    controller_stopped = pyqtSignal()
    started = pyqtSignal()
    stopped = pyqtSignal()
    stop_this_inst = pyqtSignal()
    
    is_admingvpn = False

    def __init__(self):
        super(IPOPProcess, self).__init__()
        self.ipop_process = QProcess()
        self.controller_process = QProcess()
        self.ipop_kill_process = QProcess()
        self.running = False
        self.makeConnections()
        self.heartbeat = QTimer()
        self.heartbeat.timeout.connect(self.beat)
        
    def startIPOP(self):
        self.ipop_process.setWorkingDirectory(os.environ['WORKING_DIR'])
        self.ipop_process.start("sudo", ['./script.sh']);
        self.ipop_process.readyRead.connect(self.ipop_started.emit)
        self.ipoplogupdater = LogUpdater('ipop.log',60)
        
    def startGVPN(self):
        self.controller_process.setWorkingDirectory(os.environ['WORKING_DIR'])
        #self.controller_process.setStandardOutputFile(os.environ['WORKING_DIR'] + 'LOG.txt')
        self.controller_process.setStandardErrorFile(os.environ['WORKING_DIR'] + 'gvpn.log')
        if self.is_admingvpn:
            self.controller_process.start("./admin_gvpn.py",['-c','conff.json']);
        else:
            self.controller_process.start("./gvpn_controller.py",['-c','conff.json']);
        self.controller_process.started.connect(self.controller_started.emit)
        self.controller_process.started.connect(self.started.emit)
        self.gvpnlogupdater = LogUpdater('gvpn.log',60)
        self.heartbeat.start(HEARTBEAT_CYCLE)

    def beat(self):
        try:
            connect.instance.setStatus(connect.jid, connect.vpnname, 'running')
        except:
            return
    
        
    def start(self):
        self.startIPOP()
        self.running = True    
    
    def stop(self):
        self.stopIPOP()
    
    def stopIPOP(self):
        self.ipop_kill_process.start("sudo",['pkill','ipop-tincan-x86'])
        del self.ipoplogupdater
        self.ipop_kill_process.finished.connect(self.ipop_stopped.emit)
    
    def stopGVPN(self):
        self.controller_process.kill()
        self.controller_stopped.emit()
        try:
            del self.gvpnlogupdater
        except AttributeError:
            pass  # gives out error while restarting IPOP due to changed IP
        self.stopped.emit()        
        self.running = False
        self.heartbeat.stop()

    def setAdminGVPN(self, is_admingvpn = False):
        self.is_admingvpn = is_admingvpn
    
    def makeConnections(self):
        self.connect(self, SIGNAL("ipop_started()"), self.startGVPN)
        self.connect(self, SIGNAL("ipop_stopped()"), self.stopGVPN)
        self.connect(self, SIGNAL("stop_this_inst()"), self.stop)
        
def init():
    global ipopprocess
    ipopprocess = IPOPProcess()   
    
    
