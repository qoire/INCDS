from pyo import *
import time

s = Server(nchnls=2, duplex=1)
s.setInputDevice(4)
s.setOutputDevice(2)
s.boot()
s.start()
a = Sine(mul=0.01).mix(2).out()

# keep thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.recstop()
    s.stop()
    
