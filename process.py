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
        self.controller_process.start("./gvpn_controller.py",['-c','conff.json']);
        self.controller_process.started.connect(self.controller_started.emit)
        self.controller_process.started.connect(self.started.emit)
        self.gvpnlogupdater = LogUpdater('gvpn.log',60)
        self.heartbeat.start(HEARTBEAT_CYCLE)

    def beat(self):
        connect.instance.setStatus(connect.jid,'running')
    
        
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
        del self.gvpnlogupdater
        self.stopped.emit()        
        self.running = False
        self.heartbeat.stop()
    
    def makeConnections(self):
        self.connect(self, SIGNAL("ipop_started()"), self.startGVPN)
        self.connect(self, SIGNAL("ipop_stopped()"), self.stopGVPN)
        self.connect(self, SIGNAL("stop_this_inst()"), self.stop)
        
def init():
    global ipopprocess
    ipopprocess = IPOPProcess()   
    
    
