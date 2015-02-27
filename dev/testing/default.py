from pyo import *

s = Server(audio="jack", nchnls=2).boot()
s.start()
s.recstart()

a = Sine(freq=261.6, mul=0.05)
b = Sine(freq=261.6, phase=0, mul=0.05)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()


try:
    while True:
        user_phase = raw_input('Enter a new phase value: ')
        if user_phase < 0 | user_phase > 0:
        	print "please enter a phase within the correct range!"
        else:
        	new_phase = 1 - user_phase
        	b.setPhase(new_phase)
except KeyboardInterrupt:
    s.stop()
    s.recstop()
