from pyo import *
from multiprocessing.managers import BaseManager
from random import randint
pa_list_devices()

#Instantiate BaseManager class for passing information using client
#This is identical to BaseManager server
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

        #Output three possible formats to server
        #1 - Live feed
        a = {'state': "livefeed", 'data': DATA_TABLE.getTable()}
        queue.put(a)

        # Generate phase randomized
        random_phase = randint(0,9)
        a = {'state': "phase", 'data': random_phase}
        queue.put(a)

        # Generate amplitude randomized
        random_amp = randint(0,9)
        a = {'state': "amplitude", 'data': random_amp}
        queue.put(a)

except KeyboardInterrupt:
    out_rec.stop()
    s.stop()