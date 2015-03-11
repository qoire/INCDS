from pyo import *

s = Server(nchnls=2).boot()

#sndinfo
#s.recordOptions(dur=5, filename="./output/sine.wav")
#a = Sine(freq=261, mul=1).out()
#d = Sine(freq=900, mul=0.5).out()
b = Sine(freq=450, mul=0.5).out()
s.start()

time.sleep(120)
s.stop()
