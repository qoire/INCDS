import sys
import mainwindow #our mainwindow containing definitions for GUI
from PyQt4 import QtCore, QtGui, uic

form_class = uic.loadUiType("mainwindow.ui")[0]

class MainWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.isWindowFullScreen = False
        self.setupUi(self)

        # Connections for buttons
        self.btnFullScreen.clicked.connect(self.btnFullScreen_clicked)
        self.btnResetAxis.clicked.connect(self.btnResetAxis_clicked)

        # Connections for menuActions
        self.actionFullscreen.triggered.connect(self.actFullScreen_triggered)
        self.actionWindowed.triggered.connect(self.actWindowed_triggered)

    
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



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    mainWindow = MainWindowClass()
    mainWindow.show()
    app.exec_()

