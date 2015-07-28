import math
import random
import time
import numpy as np
from pyo import *

# Script begin
# Script purpose: to change the phase from 0 - 90, 0 - 180, 0 - 270, 0 - 360

OUTPUT_FILE = './out/output.wav'

# setup interpolations
list_one = np.linspace(0, 0.3, 100).tolist()
list_two = np.linspace(0, 0.5, 100).tolist()
list_three = np.linspace(0, 1, 100).tolist()

#instantiate offline server
s = Server(nchnls=2, duplex=1).boot()
s.recordOptions(dur=100, filename=OUTPUT_FILE)


r_signal = Sine(freq=450, mul=0.5)
c_signal = Sine(freq=450, mul=0.5)

pan1 = Pan(r_signal, outs=2, pan=1, spread=0).out()
pan2 = Pan(c_signal, outs=2, pan=0, spread=0).out()

s.recstart()
s.start()

list_one_len = len(list_one)
list_two_len = len(list_two)
list_three_len = len(list_three)
print list_one_len
print list_two_len
print list_three_len

def test_one():
    pos = 0
    time.sleep(0.1)
    while True:
        if (pos < list_one_len):
            c_signal.setPhase(float(list_one[pos]))
            pos = pos + 1
            time.sleep(0.005)
        else:
            time.sleep(0.1)
            break

def test_two():
    pos = 0
    c_signal.setPhase(0)
    time.sleep(0.1)
    while True:
        if (pos < list_two_len):
            c_signal.setPhase(float(list_two[pos]))
            pos = pos + 1
            time.sleep(0.005)
        else:
            time.sleep(0.1)
            break

def test_three():
    pos = 0
    c_signal.setPhase(0)
    time.sleep(0.1)
    while True:
        if (pos < list_two_len):
            c_signal.setPhase(float(list_two[pos]))
            pos = pos + 1
            time.sleep(0.005)
        else:
            time.sleep(0.1)
            break

#begin test loop
try:
    test_one()
    test_two()
    test_three()
    s.recstop()
    s.stop()
except KeyboardInterrupt:
    s.recstop()
    s.stop()