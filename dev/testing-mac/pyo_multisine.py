from pyo import *
import time

s = Server().boot()
s.start()
s.recstart()
a = Sine(freq=261, mul=0.2).mix(2).out()
b = Sine(freq=400, mul=0.2).mix(2).out()
c = Sine(freq=600, mul=0.2).mix(2).out()

# keep thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.recstop()
    s.stop()