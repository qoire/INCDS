from pyo import *
import time

s = Server(audio="jack").boot()
s.start()
freqs = midiToHz([60,62,64,65,67,69,71,72])
rnd = Choice(choice=freqs, freq=[3,4])
a = SineLoop(rnd, mul=0.01).out()
b = BrownNoise(mul=0.01).mix(2).out()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()
