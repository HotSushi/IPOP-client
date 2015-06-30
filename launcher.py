import os
import sys
from PyQt4 import QtCore,QtGui
from PyQt4.QtCore import pyqtSignal,pyqtSlot, SLOT, SIGNAL,QProcess    

if __name__ == "__main__":
    
    ipop_client = QProcess()
    if os.getuid() == 0:
        print 'sudo rights'
        launched = ipop_client.startDetached("sudo", ['python','test.py','&']);
        #app.exit()
    else:
        print 'non sudo rights'
        launched = ipop_client.startDetached("gksudo", ['python','test.py','&']);
    
    print launched    
    #sys.exit(app.exec_())
