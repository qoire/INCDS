# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created: Mon May 18 16:33:36 2015
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(780, 519)
        self.centralWidget = QtGui.QWidget(MainWindow)
        self.centralWidget.setObjectName(_fromUtf8("centralWidget"))
        self.gridLayout_4 = QtGui.QGridLayout(self.centralWidget)
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.groupBox_2 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridLayout_3 = QtGui.QGridLayout(self.groupBox_2)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_2 = QtGui.QLabel(self.groupBox_2)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout_3.addWidget(self.label_2, 0, 0, 1, 1)
        self.xspinBoxLower = QtGui.QSpinBox(self.groupBox_2)
        self.xspinBoxLower.setObjectName(_fromUtf8("xspinBoxLower"))
        self.gridLayout_3.addWidget(self.xspinBoxLower, 0, 1, 1, 1)
        self.xspinBoxUpper = QtGui.QSpinBox(self.groupBox_2)
        self.xspinBoxUpper.setObjectName(_fromUtf8("xspinBoxUpper"))
        self.gridLayout_3.addWidget(self.xspinBoxUpper, 1, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox_2)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout_3.addWidget(self.label_3, 2, 0, 1, 1)
        self.yspinBoxLower = QtGui.QSpinBox(self.groupBox_2)
        self.yspinBoxLower.setObjectName(_fromUtf8("yspinBoxLower"))
        self.gridLayout_3.addWidget(self.yspinBoxLower, 2, 1, 1, 1)
        self.yspinBoxUpper = QtGui.QSpinBox(self.groupBox_2)
        self.yspinBoxUpper.setObjectName(_fromUtf8("yspinBoxUpper"))
        self.gridLayout_3.addWidget(self.yspinBoxUpper, 3, 1, 1, 1)
        self.btnAdjustAxis = QtGui.QPushButton(self.groupBox_2)
        self.btnAdjustAxis.setObjectName(_fromUtf8("btnAdjustAxis"))
        self.gridLayout_3.addWidget(self.btnAdjustAxis, 4, 0, 1, 2)
        self.gridLayout_4.addWidget(self.groupBox_2, 0, 0, 1, 1)
        self.groupBox_3 = QtGui.QGroupBox(self.centralWidget)
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox_3)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.cBoxColor = QtGui.QComboBox(self.groupBox_3)
        self.cBoxColor.setObjectName(_fromUtf8("cBoxColor"))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.cBoxColor.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cBoxColor, 0, 0, 1, 1)
        self.cBoxStyle = QtGui.QComboBox(self.groupBox_3)
        self.cBoxStyle.setObjectName(_fromUtf8("cBoxStyle"))
        self.cBoxStyle.addItem(_fromUtf8(""))
        self.cBoxStyle.addItem(_fromUtf8(""))
        self.cBoxStyle.addItem(_fromUtf8(""))
        self.cBoxStyle.addItem(_fromUtf8(""))
        self.gridLayout_2.addWidget(self.cBoxStyle, 1, 0, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox_3, 1, 0, 1, 1)
        self.groupBox = QtGui.QGroupBox(self.centralWidget)
        self.groupBox.setMaximumSize(QtCore.QSize(16777215, 50))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout = QtGui.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.cBoxOutput = QtGui.QComboBox(self.groupBox)
        self.cBoxOutput.setMinimumSize(QtCore.QSize(0, 22))
        self.cBoxOutput.setObjectName(_fromUtf8("cBoxOutput"))
        self.cBoxOutput.addItem(_fromUtf8(""))
        self.cBoxOutput.addItem(_fromUtf8(""))
        self.cBoxOutput.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.cBoxOutput, 0, 4, 1, 1)
        self.btnFullScreen = QtGui.QPushButton(self.groupBox)
        self.btnFullScreen.setMinimumSize(QtCore.QSize(0, 22))
        self.btnFullScreen.setObjectName(_fromUtf8("btnFullScreen"))
        self.gridLayout.addWidget(self.btnFullScreen, 0, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(425, 14, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 22))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 3, 1, 1)
        self.gridLayout_4.addWidget(self.groupBox, 3, 0, 1, 2)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_4.addItem(spacerItem1, 2, 0, 1, 1)
        self.graphicsView = PlotWidget(self.centralWidget)
        self.graphicsView.setObjectName(_fromUtf8("graphicsView"))
        self.gridLayout_4.addWidget(self.graphicsView, 0, 1, 3, 1)
        MainWindow.setCentralWidget(self.centralWidget)
        self.menuBar = QtGui.QMenuBar(MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 780, 21))
        self.menuBar.setObjectName(_fromUtf8("menuBar"))
        self.menuFile = QtGui.QMenu(self.menuBar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.menuHelp = QtGui.QMenu(self.menuBar)
        self.menuHelp.setObjectName(_fromUtf8("menuHelp"))
        MainWindow.setMenuBar(self.menuBar)
        self.mainToolBar = QtGui.QToolBar(MainWindow)
        self.mainToolBar.setObjectName(_fromUtf8("mainToolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.mainToolBar)
        self.statusBar = QtGui.QStatusBar(MainWindow)
        self.statusBar.setObjectName(_fromUtf8("statusBar"))
        MainWindow.setStatusBar(self.statusBar)
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName(_fromUtf8("actionSave"))
        self.actionAbout = QtGui.QAction(MainWindow)
        self.actionAbout.setObjectName(_fromUtf8("actionAbout"))
        self.actionClose = QtGui.QAction(MainWindow)
        self.actionClose.setObjectName(_fromUtf8("actionClose"))
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionClose)
        self.menuHelp.addAction(self.actionAbout)
        self.menuBar.addAction(self.menuFile.menuAction())
        self.menuBar.addAction(self.menuHelp.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.groupBox_2.setTitle(_translate("MainWindow", "Axis", None))
        self.label_2.setText(_translate("MainWindow", "X-Axis", None))
        self.label_3.setText(_translate("MainWindow", "Y-Axis", None))
        self.btnAdjustAxis.setText(_translate("MainWindow", "Adjust Axis", None))
        self.groupBox_3.setTitle(_translate("MainWindow", "Line", None))
        self.cBoxColor.setItemText(0, _translate("MainWindow", "Color (Default)", None))
        self.cBoxColor.setItemText(1, _translate("MainWindow", "Green", None))
        self.cBoxColor.setItemText(2, _translate("MainWindow", "Red", None))
        self.cBoxColor.setItemText(3, _translate("MainWindow", "Blue", None))
        self.cBoxColor.setItemText(4, _translate("MainWindow", "Magenta", None))
        self.cBoxColor.setItemText(5, _translate("MainWindow", "Yellow", None))
        self.cBoxColor.setItemText(6, _translate("MainWindow", "Brown", None))
        self.cBoxStyle.setItemText(0, _translate("MainWindow", "Style (Default)", None))
        self.cBoxStyle.setItemText(1, _translate("MainWindow", "Points", None))
        self.cBoxStyle.setItemText(2, _translate("MainWindow", "Dotted", None))
        self.cBoxStyle.setItemText(3, _translate("MainWindow", "Dash", None))
        self.groupBox.setTitle(_translate("MainWindow", "Output", None))
        self.cBoxOutput.setItemText(0, _translate("MainWindow", "Phase", None))
        self.cBoxOutput.setItemText(1, _translate("MainWindow", "Magnitude", None))
        self.cBoxOutput.setItemText(2, _translate("MainWindow", "Magnitude (from speaker)", None))
        self.btnFullScreen.setText(_translate("MainWindow", "Fullscreen", None))
        self.label.setText(_translate("MainWindow", "Output Display", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))
        self.menuHelp.setTitle(_translate("MainWindow", "Help", None))
        self.actionSave.setText(_translate("MainWindow", "Save", None))
        self.actionAbout.setText(_translate("MainWindow", "About", None))
        self.actionClose.setText(_translate("MainWindow", "Close", None))

from pyqtgraph import PlotWidget
