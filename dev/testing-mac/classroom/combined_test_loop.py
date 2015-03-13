#phase test loop

import math #math module for sine function
import random
import time
from pyo import *

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
        

    def setPhase(self, phase):
        self.current_phase = phase

    def phaseChange(self, cur_mag):
        if self.counter==0:
            next_phase=5*3.1415/180
            self.ini_mag=cur_mag
            self.counter=self.counter+1
        elif self.counter==1:
            if cur_mag > self.ini_mag:
                next_phase=-10*3.1415/180
                self.prev_phase=0
                self.prev_mag=cur_mag
                self.is_phase_going_negative=True
                self.counter=self.counter+1
            else:
                next_phase=10*3.1415/180
                self.prev_phase=0
                self.prev_mag=cur_mag
                self.is_phase_going_negative=False
                self.counter=self.counter+1
        else:
            if cur_mag <= self.prev_mag:
                if self.is_phase_going_negative==True:
                    next_phase=self.prev_phase-self.increment
                    self.prev_mag=cur_mag
                else:
                    next_phase=self.prev_phase+self.increment
                    self.prev_mag=cur_mag
                self.prev_phase=next_phase
            else:
                self.increment=self.increment/2
                self.prev_mag=cur_mag
                if self.is_phase_going_negative==True:
                    next_phase=self.prev_phase+self.increment
                else:
                    next_phase=self.prev_phase-self.increment
                self.is_phase_going_negative=not(self.is_phase_going_negative)
                self.prev_phase=next_phase
                
        #main function that will contain the phase change algorithm
        print " self.increment=%s " %self.increment
        return next_phase


#instantiate class
ph = phaseModule()
ph.setPhase(0)
OUTPUT_FILE = './out/output.wav'

#instantiate server
s = Server(audio="offline").boot()
s.recordOptions(dur=0.2, filename=OUTPUT_FILE)
s.setVerbosity(1)
ref_signal = Sine(freq=450, mul=0.5).out()
change_signal = Sine(freq=450, mul=0.5).out()

#DATA_TABLE
DATA_TABLE = NewTable(length=0.2,chnls=1)
rec = TableRec(ref_signal, table=DATA_TABLE, fadetime=0).play()
s.start()
s.stop()

ref_dat = DATA_TABLE.getTable()

# instantiate your amplitudeModule module & phase changer module
amp_mod = amplitudeModule()
phase_mod = phaseModule()


#create new text file
#with open('./out/phase_change.txt', 'w') as f:
#    f.write('OUTPUT\n')

iterations = 0
next_phase = 0 #initially set to 0
try:
    while True:
        #setup phase change for each loop
        change_signal.setPhase(float(next_phase))
        VAR_TABLE = NewTable(length=0.2, chnls=1)
        rec = TableRec(change_signal, table=VAR_TABLE, fadetime=0).play()
        s.start()
        s.stop()

        t = SndTable(OUTPUT_FILE)
        #print VAR_TABLE.getTable()

        mag = amp_mod.averageAmplitude(t.getTable())
        print "magnitude: " + str(mag) + " next_phase:" + str(next_phase)

        #feed magnitude into phase
        next_phase = phase_mod.phaseChange(mag)

        with open('./out/phase_change.txt', 'ab') as f:
            f.write(str(mag) + '\n')


        if iterations > 20: #set iteration cap
            break

        #print "Magnitude:" + str(mag) + " Next Phase:" + str(next_phase)
        time.sleep(0.2)
except KeyboardInterrupt:
    s.stop()