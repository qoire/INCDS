
from pyo import *
import time

print pa_list_devices()

s = Server(nchnls=2, duplex=1)
s.setInputDevice(3)
s.setOutputDevice(1)
s.boot()
s.start()
a = Input(chnl=0, mul=.7)
b = Delay(a, delay=.25, feedback=.5, mul=.5).mix(2).out()

try:
	while True:
		time.sleep(1)

except KeyboardInterrupt:
	s.stop()