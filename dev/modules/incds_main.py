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

# wave location
WAVE_LOCATION = "./output/temp.wav"

# create new functions to detect devices

#MAIN
s = Server(nchnls=2, duplex=1).boot()
s.start()
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, mul=0)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#debug mode
debug_sine=Sine(freq=5,mul=20)

#set up server
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
            
            #set back to sine
            b.setFreq(global_var.user_freq)
            a.mul=0.3

            #change debug mode to false
            in_dict[_DEBUG] = 0

        # Auto mode implemented
        if in_dict[_AUTO]:
            #Automode steps:
            #   1.Accept input from microphone
            #   2.Run through DFT
            #   3.Examine output in table format
            #   4.Take Average
            #   5.Determine best course of action
            if not auto_started:
                auto_thread = incds_mode.INCDS(WAVE_LOCATION, in_dict[_FREQ])
                auto_thread.start()
                auto_started = True
        else:
            # MANUAL MODE
            #   1. Get instructions from queue
            #   2. Execute
            #   3. Tell queue it's done

            if auto_started:
                auto_thread.signal = False
                auto_started = False

            a.setFreq(in_dict[_FREQ])
            b.setFreq(in_dict[_FREQ])
            phase_float = float(in_dict[_PHASE])/360
            b.setPhase(1 - phase_float)

            # set the magnitudes properly
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

        # finish task
        #global_var.network_queue.task_done()
except KeyboardInterrupt:
    s.stop()
    
