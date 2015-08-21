import sys
import os
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSignal,QTimer
from monitor import MonitorWidget
from login import LoginWidget
import process
import clientxmpp
import urllib
import json
import connect

global loginapp,tabs

class TabWidget(QtGui.QTabWidget):
    stopped = pyqtSignal()
    hide_signal = pyqtSignal()
    
    def __init__(self):
        super(TabWidget, self).__init__()
        
        self.hide_signal.connect(self.hide)
                
        self.stop = QtGui.QPushButton()
        self.stop.setText("Stop Ipop")
        self.stop.resize(3,2)
        self.addTab(self.stop,"Stop")
        self.stop.clicked.connect(self.stopped.emit)
        
        self.monitorapp = MonitorWidget()
        self.addTab(self.monitorapp,"Monitor")
        
        self.logapp = QtGui.QTextEdit()       
        self.addTab(self.logapp,"Log")

        self.info = QtGui.QLabel()
        self.addTab(self.info,"Info")
        
        self.log_timer = QTimer() 
        self.log_timer.timeout.connect(self.reloadLogs)
        self.log_timer.start(3000)
        
    def reloadLogs(self):
        try:        
            with open(os.environ['WORKING_DIR'] + 'gvpn.log','r') as fi:
                self.logapp.setText(fi.read())
                self.logapp.setReadOnly(True)            
        except IOError:
            return
            pass
            
        info,out = '',''
        try:
            with open(os.environ['WORKING_DIR'] + 'conff.json','r') as finfo:
                info = str(finfo.read())
            dic = json.loads(info)
            for key in sorted(dic.iterkeys()):
                out = out + key +":"+ str(dic[key]) + '\n'
            self.info.setText(out)
        except:
            pass
                
                  
def changeIpCallback():
    # alternative to process.ipopprocess.stop()
    process.ipopprocess.stop_this_inst.emit()
    tabs.hide_signal.emit()
    loginapp.show_signal.emit()
    loginapp.keyreg.emit()
        
        
        
def loggedin():
    tabs.show()
    loginapp.hide()
    try:
        clientxmpp.instance.add_callback('stop_node',tabs.stopped.emit)
        clientxmpp.instance.add_callback('change_ip',changeIpCallback)
    except:
        pass
    connect.instance.setStatus(connect.jid,'running')
    
def loggedout():
    # will error out in case of admin GVPN
    try:
        clientxmpp.instance.disconnect(wait=False)
    except:
        pass
    connect.instance.setStatus(connect.jid,'stopped')
    process.ipopprocess.stop()
    loginapp.setToLogin()
    loginapp.show()
    tabs.hide()
    
     
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    
    try:
        config = json.load(open('config.json','r'))
        os.environ['GANGLIA_DIR'] = config['ganglia_path']
        os.environ['WORKING_DIR'] = config['working_path']
    except IOError:
        print 'config.json file not created'
        exit()
    except KeyError:
        print 'corrupt config.json file'
        exit()       
    
    
    tabs = TabWidget()
    tabs.stopped.connect(loggedout)
    
    loginapp = LoginWidget()
    loginapp.show()
    loginapp.started.connect(loggedin)
    
    sys.exit(app.exec_())
