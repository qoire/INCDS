from pyo import *

s = Server().boot()
s.start()
b = Sine(mul=0.3, freq=261).mix(2)
lfo = Sine(freq=[.250, .261], mul=1000, add=0)
f = Biquadx(b, freq=lfo, q=5, type=2, stages=5).out()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()