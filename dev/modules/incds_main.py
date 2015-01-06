#INCDS main

from pyo import *
import time
import socket
import threading
import SocketServer
import json
import network_handler
import global_var

#static
_FREQUENCY = 'freq'
_PHASE = 'phase'
_AUTO = 'auto'
_DEBUG = 'debug'

#initialize hash

#MAIN
s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, phase=0, mul=0.5)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#debug mode
debug_sine=Sine(freq=5,mul=20)

#set up server
HOST, PORT = '', 9999
network_handler.startInterfaceServer(HOST, PORT)

try:
    while True:
        in_dict = global_var.network_queue.get()

        if in_dict[_DEBUG] == "True":
            b.setFreq(global_var.user_freq+debug_sine)
            a.mul=0
            time.sleep(5)
            
            #set back to sine
            b.setFreq(global_var.user_freq)
            a.mul=0.3

            #change debug mode to false
            in_dict[_DEBUG] = "False"

        # Auto mode implemented
        if in_dict[_AUTO] == "True":
            #Automode steps:
            #   1.Accept input from microphone
            #   2.Run through DFT
            #   3.Examine output in table format
            #   4.Take Average
            #   5.Determine best course of action
            
            hello_world = 1
        else:
            # MANUAL MODE
            #   1. Get instructions from queue
            #   2. Execute
            #   3. Tell queue it's done

            a.setFreq(in_dict['freq'])
            b.setFreq(in_dict['freq'])
            phase_float = float(in_dict['phase'])/360

            b.setPhase(1 - phase_float)

        # finish task
        global_var.network_queue.task_done()
except KeyboardInterrupt:
    s.stop()
    
