import sys
from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4.QtGui import *
from ui.monitor import Ui_Monitor
from graph import GangliaGraph
#
from login import LoginWidget
import urllib

class TempForm(QtGui.QMainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self,parent)
        self.ui = Ui_Monitor()
        self.ui.setupUi(self)
        self.connectSignals()
        self.graphobj = GangliaGraph()
        
    
    def connectSignals(self):
        durationCB = self.ui.durationComboBox
        graphTypeCB = self.ui.graphTypeComboBox
        durationCB.connect( durationCB, SIGNAL("currentIndexChanged(int)"), self.changeGraph )
        graphTypeCB.connect( graphTypeCB, SIGNAL("currentIndexChanged(int)"), self.changeGraph )        
    
    def changeGraph(self):
        duridx = self.ui.durationComboBox.currentIndex()
        graphtypeidx = self.ui.graphTypeComboBox.currentIndex()
        image = self.graphobj.getGraph(duridx , graphtypeidx)
        self.ui.graphImage.setPixmap(QtGui.QPixmap(image))
        
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    #myapp = TempForm()
    #myapp.show()
    myapp = LoginWidget()
    myapp.show()
    sys.exit(app.exec_())
