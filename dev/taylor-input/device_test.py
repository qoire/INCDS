from pyo import *
pa_list_devices()
max_in = pa_get_input_max_channels(1)
max_out = pa_get_output_max_channels(2)
print max_in
print max_out

print "pa_get_default_input:" + str(pa_get_default_input())
print "pa_get_default_output:" + str(pa_get_default_output())

maxchnl = min(max_in, max_out)

s = Server(nchnls=2, duplex=1)
s.boot().start()


a = Sine(freq=450, mul=0.02)
b = Sine(freq=261.6, mul=0.02)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(a, outs=2, pan=0, spread=0).out()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()
    s.recstop()