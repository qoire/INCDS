#INCDS main

from pyo import *
import time
import socket
import threading
import SocketServer
import json
import network_handler
import global_var
import incds_mode

#static
_FREQ = 'freq'
_PHASE = 'phase'
_AUTO = 'auto'
_DEBUG = 'debug'
_SHUTDOWN = 'shutdown'
_MAG1 = 'mag1'
_MAG2 = 'mag2'
_MUTE1 = 'mute1'
_MUTE2 = 'mute2'
_RESET = 'reset'
_SWITCH = 'switch'

# Initialization
s = Server(nchnls=2, duplex=1)
s.setOutputDevice(1)
s.setInputDevice(3)
s.boot()
s.setVerbosity(1)

# Setup output
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, mul=0.5)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

# Setup Inputs
inp = Input(chnl=0,mul=1)
s.start()

# Filtered input
fil_inp = Biquadx(inp, freq=650, q=5, type=2, stages=7)

# Debug mode setup
debug_sine=Sine(freq=5,mul=20)

# Server setup
HOST, PORT = '', 9999
network_handler.startInterfaceServer(HOST, PORT)

auto_started = False

try:
    while True:
        
        in_dict = global_var.network_queue.get()

        if in_dict[_DEBUG]:
            b.setFreq(global_var.user_freq+debug_sine)
            a.mul=0
            time.sleep(5)
            
            # Set back to sine
            b.setFreq(global_var.user_freq)
            a.mul=0.3

            # Change debug mode to false
            in_dict[_DEBUG] = 0

        # Auto mode implemented
        if (in_dict[_AUTO] == 1):
            if not auto_started:
                auto_thread = incds_mode.INCDS(in_dict[_FREQ], in_dict[_MAG2], fil_inp, a, b)
                auto_thread.start()
                auto_started = True
        elif (in_dict[_AUTO] == 0):
            if auto_started:
                auto_thread.signal = False
                auto_started = False

            a.setFreq(in_dict[_FREQ])
            b.setFreq(in_dict[_FREQ])
            phase_float = float(in_dict[_PHASE])/360
            b.setPhase(phase_float)

            # Set the magnitudes properly
            if in_dict[_MUTE1]:
                a.mul = 0
            else:
                a.mul = float(in_dict[_MAG1])/1000

            if in_dict[_MUTE2]:
                b.mul = 0
            else:
                b.mul = float(in_dict[_MAG2])/1000

        if in_dict[_SHUTDOWN]:
            raise KeyboardInterrupt

        # Finish task
        # global_var.network_queue.task_done()
except KeyboardInterrupt:
    s.stop()
    
