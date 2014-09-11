from pyo import *

s = Server(audio="jack").boot()
s.start()

a = Noise(mul=0.01)
lfo = Sine(freq=1, mul=0.5, add=0.5)
p = Pan(a, outs=2, pan=lfo).out()


try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()