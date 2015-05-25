from pyo import *
from multiprocessing.managers import BaseManager
pa_list_devices()

class QueueManager(BaseManager): pass
QueueManager.register('get_queue')

s = Server(nchnls=2, duplex=1)
s.boot()
s.start()

inp = Input(chnl=0, mul=1)

#Queue manager
m = QueueManager(address=('', 50000), authkey='randgen')
m.connect()
queue = m.get_queue()

try:
    while True:
        DATA_TABLE = NewTable(length=0.01,chnls=1)
        rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.015)
        queue.put(DATA_TABLE.getTable())
except KeyboardInterrupt:
    out_rec.stop()
    s.stop()