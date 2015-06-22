import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal
from monitor import MonitorWidget
from login import LoginWidget
import urllib
import json

loginapp = ''
tabs = ''

class TabWidget(QtGui.QTabWidget):
    stopped = pyqtSignal()
    
    def __init__(self):
        super(TabWidget, self).__init__()
                
        self.stop = QtGui.QPushButton()
        self.stop.setText("Stop Ipop")
        self.stop.resize(3,2)
        self.addTab(self.stop,"Stop")
        self.stop.clicked.connect(self.stopped.emit)
        
        self.monitorapp = MonitorWidget()
        self.addTab(self.monitorapp,"Monitor")
        
        self.logapp = QtGui.QTextEdit()        
        with open('/home/hotsushi/game/ipoptemp/ERROR.txt','r') as fi:
            self.logapp.setText(fi.read())
            self.logapp.setReadOnly(True)            
        self.addTab(self.logapp,"Log")
        
        self.info = QtGui.QLabel()
        info,out = '',''
        with open('/home/hotsushi/game/ipoptemp/conff.json','r') as finfo:
            info = str(finfo.read())
        dic = json.loads(info)
        for key in sorted(dic.iterkeys()):
            out = out + key +":"+ str(dic[key]) + '\n'
        self.info.setText(out)
        self.addTab(self.info,"Info")        
                  
        
        
        
def loggedin():
    tabs.show()
    loginapp.hide()
    
def loggedout():
    loginapp.stop()
    loginapp.show()
    tabs.hide()
    
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    tabs = TabWidget()
    tabs.stopped.connect(loggedout)
    
    #should return qprocess
    loginapp = LoginWidget()
    loginapp.show()
    loginapp.started.connect(loggedin)
    
    
    
    
    sys.exit(app.exec_())
