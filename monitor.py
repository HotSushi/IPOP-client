from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import pyqtSlot,SIGNAL,SLOT
from PyQt4.QtGui import *
from ui.monitor import Ui_Monitor
from graph import GangliaGraph

class MonitorWidget(QtGui.QWidget):
    def __init__(self):
        super(MonitorWidget, self).__init__()
        self.ui = Ui_Monitor()
        self.ui.setupUi(self)
        self.ui.graphImage.setScaledContents(True)
        self.setLayout(self.ui.monitorLayout)
        
        self.connectSignals()
        self.graphobj = GangliaGraph()    
        
        self.changeGraph()
        
    
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

