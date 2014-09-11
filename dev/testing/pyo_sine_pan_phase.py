from pyo import *

s = Server(audio="jack", nchnls=2).boot()
s.start()
s.recstart()

a = Sine(freq=261.6, mul=0.05)
b = Sine(freq=261.6, phase=180, mul=0.05)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()



try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()
    s.recstop()
