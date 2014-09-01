from pyo import *
import time

s = Server(audio="jack").boot()
s.start()
mod = Sine(freq=32, mul=50)
a = Sine(freq=mod, mul=0.01).mix(3).out()

# keep thread alive
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()
    
