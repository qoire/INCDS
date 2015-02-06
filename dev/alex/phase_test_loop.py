#phase test loop

import math #math module for sine function
import random
import time

#hello

class phaseModule():
    # Alex keep your code here
    def __init__(self):
        # initiate self variables here
        self.phase_list = []
        self.current_phase = 0

    def setPhase(self, phase):
        self.current_phase = phase

    def phaseChange(self, cur_mag):

        #main function that will contain the phase change algorithm

        min=sinfunc(0)#call taylor's function
        cursor=sinfunc(15)
        increment=30

        if cursor>min:
            buff=-10
            cursor=sinfunc(buff)
            isdecre=true

            while increment > 0.1:
                while cursor<=min:
                    min=cursor
                    if isdecre==1:
                        buff=buff-increment
                    else:
                        buff=buff+increment

                    cursor=sinfunc(buff)#call taylor's function

            min=cursor
            increment=increment/2
            isdecre=not(isdecre)
        else:
            buff=10
            cursor=sinfunc(buff)
            isdecre=false
            while increment > 0.1:
                while cursor<=min:
                    min=cursor
                    if isdecre==1:
                        buff=buff-increment
                    else:
                        buff=buff+increment
                    
                    cursor=sinfunc(buff)#call taylor's function

                min=cursor
                increment=increment/2
                isdecre=not(isdecre)

        next_phase = 0
        return next_phase

# MAIN START
MIN_RAND = 1
MAX_RAND = 8


#equation a*cos(b*(x-d)) + c
var_a = random.randint(MIN_RAND, MAX_RAND)
var_b = random.randint(MIN_RAND, MAX_RAND)
var_c = random.randint(MIN_RAND, MAX_RAND)
var_d = random.randint(MIN_RAND, MAX_RAND)

print str(var_a) + str(var_b) + str(var_c) + str(var_d)

min_val = var_c - var_a

#instantiate class
ph = phaseModule()
ph.setPhase(0)

nx_phase = 0 #initially set to 0
while True:
    mag = var_a*(math.cos(var_b*(-var_d+nx_phase))) + var_c 
    nx_phase = ph.phaseChange(mag)
    print "Magnitude:" + str(mag) + " Next Phase:" + str(nx_phase) + "Target mag:" + str(min_val)
    time.sleep(0.2)