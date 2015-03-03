#phase test loop

import math #math module for sine function
import random
import time
from pyo import *

# Hi Taylor, this is the class you will be using
# Put everything in here! dont leave variables lying around! (its dangerous)
class amplitudeModule():

    # see that self? all functions inside classes must pass that self as 
    # its first parameter.

    def __init__(self):
        #when you want to add variables that you can use
        #in all functions in a class
        #use self.__your_var___ as the definition.
        #same for functions
        self.referenceAmplitude = 0
        self.changeAmplitude = 0
        self.gotReference = False
        self.referenceFloatList = 0
        self.changeFloatList = 0
        self.d = 0.01

    def averageAmplitude(self, float_list):
        #this is your amplitude averager function
        #the input is a list of floats (DATA_TABLE.getTable() outputs list of floats)

        ref = 0     #starting with reference of 0
        inc = 1     #when inc=1 --> increasing, when inc=0 --> decreasing
        index = 0   #indexes the peaks array
        peaks = []  #max/min amplitudes

        for i in float_list:                #cycle through the amplitude values
            if (i>ref):                     #if the value is bigger than the one before it, it's increasing
                if (inc == 0):              #but if it was previously decreasing, we know there's a minimum
                    peaks.insert(index,ref) #store the peak value
                    index = index+1         #and increase the index
                inc = 1                     #we know we're increasing now
            elif (i<ref):                   #same idea as before but opposite for maximum values
                if (inc == 1):
                    peaks.insert(index,ref)
                    index = index+1
                inc = 0
            ref = i         #update the reference to the previous value
        
        avg = sum(abs(x) for x in peaks)/float(len(peaks))  #average the abs() values of the peaks
        #print "AVERAGE:", avg
        if not self.gotReference:
            self.referenceAmplitude = avg                   #store the reference
            self.gotReference = True
            print "REFERENCE:", self.referenceAmplitude
        return avg

    def amplitudeEqualizer(self):
        newavg = self.averageAmplitude(self.changeFloatList)
        if newavg < self.referenceAmplitude:    #if the speaker volume needs to be increased
            return (newavg + self.d)                 #'d' is the delta value threshold define below
        elif newavg > self.referenceAmplitude:  #if the speaker volume needs to be decreased
            return (newavg - self.d)

    def printReference(self):
        print self.referenceFloatList

    def printChange(self):
        print self.changeFloatList

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


#[sum(x) for x in zip(DATA_TABLE.getTable(), VAR_TABLE.getTable())]

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()

#create new text file
with open('./out/phase_change.txt', 'w') as f:
    f.write('OUTPUT\n')

next_phase = 0 #initially set to 0
try:
    while True:
        #setup phase change for each loop
        change_signal.setPhase(float(next_phase)/float(360))
        VAR_TABLE = NewTable(length=0.2, chnls=1)
        rec = TableRec(change_signal, table=VAR_TABLE, fadetime=0).play()
        s.start()
        s.stop()

        t = SndTable(OUTPUT_FILE)
        #print VAR_TABLE.getTable()

        mag = amp_mod.averageAmplitude(t.getTable())
        print mag

        with open('./out/phase_change.txt', 'ab') as f:
            f.write(str(mag) + '\n')

        if next_phase == 360:
            #exit loop we are done
            break

        #hardlimit the phase
        if next_phase < 360:
            next_phase = next_phase+1
        else:
            next_phase = 0
        #print "Magnitude:" + str(mag) + " Next Phase:" + str(next_phase)
        time.sleep(0.2)
except KeyboardInterrupt:
    s.stop()