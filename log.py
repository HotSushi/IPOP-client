from PyQt4 import QtCore
from PyQt4.QtCore import QTimer
import connect
import os
import time

class LogUpdater():

    def __init__(self,filename,time_in_seconds):
        self.filename = filename
        self.timer = QTimer()
        self.timer.timeout.connect(self.upload)
        self.timer.start(time_in_seconds*1000)
        self.PDATA = 0
    
    def upload(self):
        logdata = self.getLatestData()
        if not logdata:
            return
        logdata = self.process(logdata)
        connect.instance.setLog(self.filename,logdata)

    def currenttime(self):
        return time.strftime("%Y-%m-%d %H:%M:%S")

    def getLatestData(self):
        with open(os.environ['WORKING_DIR'] +self.filename,'r') as gl:
            DATA = gl.read()
            gl.close()
        NDATA = DATA[self.PDATA:]
        self.PDATA = len(DATA)
        if not NDATA:
            return False
        return NDATA
    
    def process(self,data):
        if self.filename == 'gvpn.log':
            return "="*5 + self.currenttime() + "="*5 + data
        elif self.filename == 'ipop.log':
            splitlist = data.split('\n')
            data = "\n".join(splitlist[::-1])
            return data


    def __del__(self):
        self.timer.stop()
        del self.timer
        del self.filename
