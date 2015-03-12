from pyo import *
pa_list_devices()
max_in = pa_get_input_max_channels(1)
max_out = pa_get_output_max_channels(2)
print max_in
print max_out

print "pa_get_default_input:" + str(pa_get_default_input())
print "pa_get_default_output:" + str(pa_get_default_output())
