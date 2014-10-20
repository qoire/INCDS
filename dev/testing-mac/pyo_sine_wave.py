from pyo import *
import time

s = Server().boot()
s.start()
s.recstart()
a = Sine(mul=0.1).mix(2).out()

# keep thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.recstop()
    s.stop()
    
