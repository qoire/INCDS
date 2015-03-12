from pyo import *
pa_list_devices()

s = Server(nchnls=2, duplex=1)
s.setOutputDevice(1)
s.boot()
s.start()

sine_out = Sine(freq=261, mul=0.2).out()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()