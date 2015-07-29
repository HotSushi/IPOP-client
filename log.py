from PyQt4 import QtCore
from PyQt4.QtCore import QTimer
import connect
import os
import time

KB_5 = 5 * (2**10)
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
        #if data to be sent is greater than 5 KB, then send last 5 KB
        if len(DATA)-self.PDATA > KB_5:
            NDATA = DATA[-KB_5:]
        else:
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
