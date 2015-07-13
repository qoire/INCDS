import sys
import mainwindow #our mainwindow containing definitions for GUI
import multiprocessing
import retrieverthread
import numpy as np
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("mainwindow.ui")[0]

class MainWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.isWindowFullScreen = False
        self.setupUi(self)

        # Setup shared variables
        self.x_lower = 0
        self.x_upper = 10
        self.y_lower = 0
        self.y_upper = 10

        # Connections for menuActions
        self.actionFullscreen.triggered.connect(self.actFullScreen_triggered)
        self.actionWindowed.triggered.connect(self.actWindowed_triggered)

        # Configure the plotview (graphicsView)
        self.setPlotAmplitude()

        # Start reciever thread
        self.startRecieverThread()

        # Define custom reciever handlers
        QtCore.QObject.connect(self.retthread, QtCore.SIGNAL("newData(PyQt_PyObject)"), self.recieverThreadHandler)

    def setPlotAmplitude(self):
        plot = self.graphicsView.getPlotItem()
        plot.showGrid(x=True, y=True)
        plot.setXRange(0, 0.01)
        plot.setYRange(-0.5, 0.5)
        plot.setLabel('bottom', 'Time')
        plot.setLabel('left', 'Amplitude')
        self.curve = self.graphicsView.plot(np.linspace(0, 0, 100))

    def actFullScreen_triggered(self):
        self.showFullScreen()

    def actWindowed_triggered(self):
        self.showNormal()

# Thread handler section
    def startRecieverThread(self):
        self.retthread = retrieverthread.RetrieverThread(self.graphicsView)
        self.retthread.start()

    def recieverThreadHandler(self, npdata):
        time_calc = np.linspace(0, 0.01, npdata.size)
        self.curve.setData(x=time_calc, y=npdata)

if __name__ == "__main__":
    # Implement thread for recieving information


    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindowClass()
    mainWindow.show()
    app.exec_()

