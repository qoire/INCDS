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
		self.counter = 0
		self.increment=30*3.1415/180
		self.prev_phase=None
		self.prev_mag=None
		self.is_phase_going_negative=None
		self.abs_min_mag = 0
		

    def setPhase(self, phase):
        self.current_phase = phase

    def phaseChange(self, cur_mag):
		if self.counter == 0:
			self.abs_min_mag = cur_mag
			self.abs_min_phase = 0
			self.counter = self.counter + 1
			next_phase = self.counter  * 3.1415/180
			
		else:
			if cur_mag < self.abs_min_mag:
				self.abs_min_mag = cur_mag
				self.abs_min_phase = self.counter
			self.counter = self.counter + 1
			next_phase = self.counter  * 3.1415/180
			
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
i=0
nx_phase = 0 #initially set to 0
while True:
	mag = var_a*(math.cos(var_b*(-var_d+nx_phase))) + var_c 
	nx_phase = ph.phaseChange(mag)
	print "Magnitude:" + str(mag) + " Next Phase:" + str(nx_phase) + " Target mag:" + str(min_val)
	time.sleep(0.01)
	if i>360:
		print "The absolute minimum phase:" + str(ph.abs_min_phase)
		print "The absolute minimum magnitude:" + str(ph.abs_min_mag)
		break
	else:
		i=i+1