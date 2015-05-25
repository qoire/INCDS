from pyo import *
from multiprocess import BaseManager
pa_list_devices()

class QueueManager(BaseManager): pass
QueueManager.register('get_queue')

s = Server(nchnls=2, duplex=1)
s.boot()
s.start()

inp = Input(chnl=0, mul=1)

#Queue manager
m = QueueManager(address=('', 49998), authkey='randgen')
m.connect()
queue = m.get_queue()

try:
    while True:
        DATA_TABLE = NewTable(length=0.1,chnls=1)
		rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
		time.sleep(0.15)
		queue.put(rec.getTable())
except KeyboardInterrupt:
	audio_rec.stop()
	out_rec.stop()
	s.stop()