import sys
import numpy as np
from PyQt4 import QtCore, QtGui
from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): pass
QueueManager.register('get_queue')

class RetrieverThread(QtCore.QThread):
	def __init__(self, graphicsView):
		QtCore.QThread.__init__(self)
		self.graphicsView = graphicsView

	def run(self):
		m = QueueManager(address=('localhost', 50000), authkey='randgen')
		m.connect()
		queue = m.get_queue()
		self.graphicsView.enableAutoRange()
		self.graphicsView.setYRange(-0.5, 0.5)
		self.curve = self.graphicsView.plot(np.linspace(0, 0, 100))
		while True:
			dat_list = queue.get()
			np_array = np.asarray(dat_list)
			self.curve.setData(np_array)

