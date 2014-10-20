from pyo import *

s = Server(nchnls=2).boot()
s.start()
s.recstart()

a = Sine(freq=261, mul=0.3)
b = Sine(freq=261, phase=0, mul=0.3)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

user_phase = 0.0

try:
    while True:
    	try:
        	user_phase = float(raw_input('Enter a new phase value: '))
        except ValueError as e:
        	print "Please enter a float!"
        if user_phase < 0.0 or user_phase > 1.0:
        	print "Please enter a phase within the correct range!"
        else:
        	new_phase = 1 - user_phase
        	b.setPhase(new_phase)
except KeyboardInterrupt:
    s.stop()
    s.recstop()
    
