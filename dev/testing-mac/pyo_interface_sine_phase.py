#INTERFACE PROGRAM V0.02
#Now takes in a special parameter: debug

from pyo import *
import time

s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.3)
b = Sine(freq=261, phase=0, mul=0.3)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#debug mode
debug_sine=Sine(freq=5,mul=20)

user_phase = 0.0

#initial setup set frequency:
user_freq = float(raw_input('Enter desired frequency:'))
a.setFreq(user_freq)
b.setFreq(user_freq)

try:
    while True:
        try:
            user_phase = raw_input('Enter a new phase value: ')
            if user_phase == 'debug':
                b.setFreq(user_freq+debug_sine)
                a.mul=0
                time.sleep(5)
                #set back to sine
                b.setFreq(user_freq)
                a.mul=0.3
            else:
                user_phase = float(user_phase)

        except ValueError as e:
            print "Please enter a float!"
        if user_phase < 0.0 or user_phase > 1.0:
            print "Please enter a phase within the correct range!"
        else:
            new_phase = 1 - user_phase
            b.setPhase(new_phase)
except KeyboardInterrupt:
    s.stop()
    
