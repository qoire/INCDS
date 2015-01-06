import incds_mode
import time
from pyo import *

#MAIN
s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, phase=0, mul=0.5)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

b = incds_mode.INCDS()
b.start()
started = False
while True:
	b.signal = False
	time.sleep(1)



