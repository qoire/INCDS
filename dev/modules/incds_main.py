#INCDS main

from pyo import *
import time
import socket
import threading
import SocketServer
import json
import network_handler
import global_var

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
        if global_var.debug_mode == True:
            b.setFreq(global_var.user_freq+debug_sine)
            a.mul=0
            time.sleep(5)
            
            #set back to sine
            b.setFreq(global_var.user_freq)
            a.mul=0.3

            #change debug mode to false
            global_var.debug_mode = False

        # Auto mode implemented
        if global_var.auto_mode == True:
            #Automode steps:
            #   1.Accept input from microphone
            #   2.Run through DFT
            #   3.Examine output in table format
            #   4.Take Average
            #   5.Determine best course of action
        else:
            a.setFreq(global_var.user_freq)
            b.setFreq(global_var.user_freq)
            user_phase_float = float(global_var.user_phase)/360

            b.setPhase(1 - user_phase_float)
            #sleep the system for a little bit
        time.sleep(0.05)
except KeyboardInterrupt:
    s.stop()
    
