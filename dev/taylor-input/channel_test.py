from pyo import *

#print pa_list_devices()
s = Server()
s.setInputDevice(3)
s.setOutputDevice(3)
s.boot()

