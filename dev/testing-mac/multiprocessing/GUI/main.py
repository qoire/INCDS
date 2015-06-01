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

        # Connections for buttons
        self.btnFullScreen.clicked.connect(self.btnFullScreen_clicked)
        self.btnResetAxis.clicked.connect(self.btnResetAxis_clicked)

        # Connections for menuActions
        self.actionFullscreen.triggered.connect(self.actFullScreen_triggered)
        self.actionWindowed.triggered.connect(self.actWindowed_triggered)

        # Configure the plotview (graphicsView)
        self.setPlotAmplitude()

        # Start reciever thread
        self.startRecieverThread()

        # Setup spinBoxes
        self.xspinBoxLower.valueChanged.connect(self.xspinBoxLower_changed)
        self.xspinBoxUpper.valueChanged.connect(self.xspinBoxUpper_changed)
        self.yspinBoxLower.valueChanged.connect(self.yspinBoxLower_changed)
        self.yspinBoxUpper.valueChanged.connect(self.yspinBoxUpper_changed)

        # Define custom reciever handlers
        QtCore.QObject.connect(self.retthread, QtCore.SIGNAL("newData(PyQt_PyObject)"), self.recieverThreadHandler)

    def xspinBoxLower_changed(self):
        plot = self.graphicsView.getPlotItem()
        self.x_lower = self.xspinBoxLower.value()

        if self.x_lower >= self.x_upper:
            self.x_lower = self.x_lower - 1;
            self.xspinBoxLower.setValue(self.x_lower)
            plot.setXRange(self.x_lower, self.x_upper)
        else:
            plot.setXRange(self.x_lower, self.x_upper)

    def xspinBoxUpper_changed(self):
        plot = self.graphicsView.getPlotItem()
        self.x_upper = self.xspinBoxUpper.value()

        if self.x_upper <= self.x_lower:
            self.x_upper = self.x_upper + 1;
            self.xspinBoxUpper.setValue(self.x_upper)
        else:
            plot.setXRange(self.x_lower, self.x_upper)

    def yspinBoxLower_changed(self):
        plot = self.graphicsView.getPlotItem()
        self.y_lower = self.yspinBoxLower.value()

        if self.y_lower >= self.y_upper:
            self.y_lower = self.y_lower - 1;
            self.yspinBoxLower.setValue(self.y_lower)
            plot.setYRange(self.y_lower, self.y_upper)
        else:
            plot.setYRange(self.y_lower, self.y_upper)

    def yspinBoxUpper_changed(self):
        plot = self.graphicsView.getPlotItem()
        self.y_upper = self.yspinBoxUpper.value()

        if self.y_upper <= self.y_lower:
            self.y_upper = self.y_upper + 1;
            self.yspinBoxUpper.setValue(self.y_upper)
        else:
            plot.setXRange(self.y_lower, self.y_upper)

    def setPlotAmplitude(self):
        plot = self.graphicsView.getPlotItem()
        plot.showGrid(x=True, y=True)
        plot.setXRange(0, 0.01)
        plot.setYRange(-1, 1)
        plot.setLabel('bottom', 'Time')
        plot.setLabel('left', 'Amplitude')
        self.curve = self.graphicsView.plot(np.linspace(0, 0, 100))

        # Updated spinboxes to match
        self.xspinBoxLower.setValue(self.x_lower)
        self.xspinBoxUpper.setValue(self.x_upper)
        self.yspinBoxLower.setValue(self.y_lower)
        self.yspinBoxUpper.setValue(self.y_upper)
    
    def btnFullScreen_clicked(self):
        if (not self.isWindowFullScreen):
            self.showFullScreen()
            self.btnFullScreen.setText("Windowed")
            self.isWindowFullScreen = True
        else:
            self.showNormal()
            self.btnFullScreen.setText("Fullscreen")
            self.isWindowFullScreen = False

    def actFullScreen_triggered(self):
        self.showFullScreen()

    def actWindowed_triggered(self):
        self.showNormal()

    def btnResetAxis_clicked(self):
        plotItem = self.graphicsView.getPlotItem()

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

