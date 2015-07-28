from multiprocessing.managers import BaseManager
import Queue
queue = Queue.PriorityQueue(maxsize=1)

class QueueManager(BaseManager):
	pass

QueueManager.register('get_queue', callable=lambda:queue)
queue_manager = QueueManager(address=('localhost', 50000), authkey='randgen')
queue_server = queue_manager.get_server()
queue_server.serve_forever()