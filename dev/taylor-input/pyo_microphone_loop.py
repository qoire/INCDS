from pyo import *

s = Server(nchnls=2, duplex=1).boot()
s.setVerbosity(1)
a = Sine(freq=450, mul=0.8)
b = Sine(freq=450, mul=0)

p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#setup input
inp = Input(chnl=0, mul=1)

#DATA_TABLE
data_table = NewTable(length=0.2,chnls=1)
rec = TableRec(inp, data_table, fadetime=0).play()
s.start()

try:
	while True:
		time.sleep(1)
		print rec['trig']
		#print data_table.getTable()
except KeyboardInterrupt:
	s.stop()