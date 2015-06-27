from PyQt4 import QtCore
from PyQt4.QtCore import pyqtSignal,pyqtSlot, SLOT, SIGNAL,QProcess

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
        
        
    def startIPOP(self):
        self.ipop_process.setWorkingDirectory("/home/hotsushi/game/ipoptemp/")
        self.ipop_process.start("gksudo", ['./script.sh']);
        self.ipop_process.readyRead.connect(self.ipop_started.emit)
    
    def startGVPN(self):
        self.controller_process.setWorkingDirectory("/home/hotsushi/game/ipoptemp/")
        self.controller_process.setStandardOutputFile('/home/hotsushi/game/ipoptemp/LOG.txt')
        self.controller_process.setStandardErrorFile('/home/hotsushi/game/ipoptemp/ERROR.txt')
        self.controller_process.start("./gvpn_controller.py",['-c','conff.json']);
        self.controller_process.started.connect(self.controller_started.emit)
        self.controller_process.started.connect(self.started.emit)
        
    def start(self):
        self.startIPOP()
        self.running = True    
    
    def stop(self):
        self.stopIPOP()
    
    def stopIPOP(self):
        self.ipop_kill_process.start("gksudo",['pkill','ipop-tincan-x86'])
        self.ipop_kill_process.finished.connect(self.ipop_stopped.emit)
    
    def stopGVPN(self):
        self.controller_process.kill()
        self.controller_stopped.emit()
        self.stopped.emit()        
        self.running = False
    
    def makeConnections(self):
        self.connect(self, SIGNAL("ipop_started()"), self.startGVPN)
        self.connect(self, SIGNAL("ipop_stopped()"), self.stopGVPN)
        self.connect(self, SIGNAL("stop_this_inst()"), self.stop)
        
def init():
    global ipopprocess
    ipopprocess = IPOPProcess()   
    
    
