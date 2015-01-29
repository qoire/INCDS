from pyo import *


pa_list_devices()
print "Default input:", pa_get_default_input()
s = Server(duplex=1).boot()
s.start()

inp = Input(chnl=0, mul=1) # chnl=[0,1] for stereo input
indel = Delay(inp, delay=.25, feedback=0.5).out()

try:
	while True:
		pass
except KeyboardInterrupt:
	s.stop()