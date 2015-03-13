# INCDS TEST ENVIRONMENT

# FIRST LOOP = REFERENCE SINE WAVE (speaker A)
# SUBSEQUENT LOOPS = ADJUSTED WAVE (speaker B)
import csv

from pyo import *

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
        self.speakerB = 0.2
        self.newavg = 0
        self.d = 0.01

    def averageAmplitude(self, float_list):
    	#this is your amplitude averager function
        #the input is a list of floats (DATA_TABLE.getTable() outputs list of floats)

        ref = 0  	#starting with reference of 0
        inc = 1  	#when inc=1 --> increasing, when inc=0 --> decreasing
        index = 0  	#indexes the peaks array
        peaks = []  #max/min amplitudes

        for i in float_list: 				#cycle through the amplitude values
            if (i>ref): 					#if the value is bigger than the one before it, it's increasing
                if (inc == 0): 				#but if it was previously decreasing, we know there's a minimum
                    peaks.insert(index,ref) #store the peak value
                    index = index+1 		#and increase the index
                inc = 1 					#we know we're increasing now
            elif (i<ref): 					#same idea as before but opposite for maximum values
                if (inc == 1):
                    peaks.insert(index,ref)
                    index = index+1
                inc = 0
            ref = i 		#update the reference to the previous value
    	
    	if (len(peaks)==0):
    	    avg = 0
        else:
            avg = 100*sum(abs(x) for x in peaks)/float(len(peaks)) 	#average the abs() values of the peaks
            
        print "AVERAGE:", avg
        if not self.gotReference:
            self.referenceAmplitude = avg 					#store the reference
            self.gotReference = True
            print "REFERENCE:", self.referenceAmplitude
        return avg

    def amplitudeEqualizer(self):
        self.newavg = self.averageAmplitude(self.changeFloatList)
        if self.newavg < self.referenceAmplitude: 		#if the speaker volume needs to be increased
            self.speakerB = self.speakerB + self.d
            return self.speakerB						#'d' is the delta value threshold define below
        elif self.newavg > self.referenceAmplitude: 	#if the speaker volume needs to be decreased
            self.speakerB = self.speakerB - self.d
            return self.speakerB

    def printReference(self):
        print self.referenceFloatList

    def printChange(self):
        print self.changeFloatList

TARGET_MUL = 0.7
TEST_MUL = 0.2

s = Server(nchnls=2, duplex=1)
s.recordOptions(filename='./output/test_case_3/speaker_audio.wav')
s.setInputDevice(3)
s.setOutputDevice(1)
s.boot()
a = Sine(freq=261, mul=TARGET_MUL) #target amplitude (reference) will not change
b = Sine(freq=261, mul=TEST_MUL)
p = Pan(a, outs=2, pan=1, spread=0).out() #start both speakers
p2 = Pan(b, outs=2, pan=0, spread=0).out()

s.setVerbosity(1)
inp = Input(chnl=0, mul=1)
s.start()
s.recstart()

# feed input into a filter
fil_inp = Biquadx(inp, freq=261, q=10, type=2, stages=5)
audio_rec = Record(fil_inp, filename="./output/test_case_3/filtered_input.wav", fileformat=0, sampletype=0)
mic_rec = Record(inp, filename="./output/test_case_3/microphone_input.wav", fileformat=0, sampletype=0)


##########get the reference amplitude
b.mul = 0 #turn off this speaker leaving just the reference one on
time.sleep(1)
    
DATA_TABLE = NewTable(length=0.1,chnls=1)
rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
time.sleep(0.15)

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()
ref_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())

with open('./output/jawbone_test.txt', 'w') as f:
    f.write(str(ref_amp)+ '\n')

##########get the starting amplitude of the second speaker
a.mul = 0 #turn the reference speaker off
b.mul = TEST_MUL

max_iterations = 60
#enter loop to equalize the amplitudes
try:
    while True:
        #record new values!
        DATA_TABLE = NewTable(length=0.1,chnls=1)
        rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.15)

        amp_mod.changeFloatList = DATA_TABLE.getTable()
        #change the amplitude to a new one (adjust)
        test_amp_input = amp_mod.averageAmplitude(DATA_TABLE.getTable())
        test_amp = amp_mod.amplitudeEqualizer()
        b.mul = test_amp

        with open('./output/jawbone_test.txt', 'a') as f:
            f.write(str(float(test_amp_input)) + '\n')

        time.sleep(0.1) #sleep for 500ms (JAWBONE has more delay than usual)
        max_iterations = max_iterations - 1
        if max_iterations == 0:
            audio_rec.stop()
            mic_rec.stop()
            s.recstop()
            break
        
except KeyboardInterrupt:
    s.recstop()
    audio_rec.stop()
    mic_rec.stop()
    s.stop()