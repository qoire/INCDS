from pyo import *

s = Server(nchnls=2).boot()
s.start()
s.recstart()

b_phase = 0

a = Sine(freq=261.6, mul=0.05)
b = Sine(freq=261.6, phase=b_phase, mul=0.05)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

 

try:
    while True:
        time.sleep(1)
	
	if b_phase < 0.6:
		b_phase = b_phase + 0.1
		b.setPhase(b_phase)

except KeyboardInterrupt:
    s.stop()
    s.recstop()
