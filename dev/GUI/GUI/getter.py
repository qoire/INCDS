from multiprocessing.managers import BaseManager

class QueueManager(BaseManager): pass
QueueManager.register('get_queue')

m = QueueManager(address=('localhost', 50000), authkey='randgen')
m.connect()
queue = m.get_queue()

while True:
	wav_list = queue.get()
	print wav_list