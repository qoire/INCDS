# INCDS TEST ENVIRONMENT

# FIRST LOOP = REFERENCE SINE WAVE (speaker A)
# SUBSEQUENT LOOPS = ADJUSTED WAVE (speaker B)

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
        self.speakerB = TEST_MUL
        self.newavg = 0

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
            avg = 10*sum(abs(x) for x in peaks)/float(len(peaks)) 	#average the abs() values of the peaks
            
        print "AVERAGE:", avg
        if not self.gotReference:
            self.referenceAmplitude = avg 					#store the reference
            self.gotReference = True
            print "REFERENCE:", self.referenceAmplitude
        return avg

    def amplitudeEqualizer(self):
        self.newavg = self.averageAmplitude(self.changeFloatList)
        if self.newavg < self.referenceAmplitude: 		#if the speaker volume needs to be increased
            self.speakerB = self.speakerB + d
            return self.speakerB						#'d' is the delta value threshold define below
        elif self.newavg > self.referenceAmplitude: 	#if the speaker volume needs to be decreased
            self.speakerB = self.speakerB - d
            return self.speakerB

    def printReference(self):
        print self.referenceFloatList

    def printChange(self):
        print self.changeFloatList

TARGET_MUL = 0.5
TEST_MUL = 0.3

d = 0.01 	#program doesn't seem to work if this delta is <0.01

s = Server(nchnls=2, duplex=1)
s.setInputDevice(3)
s.setOutputDevice(1)
s.boot()
a = Sine(freq=450, mul=TARGET_MUL) #target amplitude (reference) will not change
b = Sine(freq=450, mul=TEST_MUL)
p = Pan(a, outs=2, pan=1, spread=0).out() #start both speakers
p2 = Pan(b, outs=2, pan=0, spread=0).out()

s.setVerbosity(1)
inp = Input(chnl=0, mul=1)
s.start()

##########get the reference amplitude
b.mul = 0 #turn off this speaker leaving just the reference one on
time.sleep(1)

##TRY SETTING FOR() LOOP HERE TO GET REFERENCE AMPLITUDE
prntfile = open('equalize.txt', 'w')

time.sleep(5)
    
DATA_TABLE = NewTable(length=0.1,chnls=1)
rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
time.sleep(0.11)
#for i in DATA_TABLE.getTable():
#     prntfile.write(str(i)+'\n')

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()
amp_mod.averageAmplitude(DATA_TABLE.getTable())
prntfile.write(str(amp_mod.referenceAmplitude)+'\n')

#reference amplitude is now stored

##########get the starting amplitude of the second speaker
a.mul = 0 #turn the reference speaker off
b.mul = TEST_MUL

#enter loop to equalize the amplitudes
try:
    while True:
        #set new amplitude values for b
        time.sleep(0.3)
        #record new values!
        DATA_TABLE = NewTable(length=0.1,chnls=1)
        rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.11)
        
        for i in DATA_TABLE.getTable():
             prntfile.write(str(10*i)+'\n')

        #say we wanted to print the new values!
        amp_mod.changeFloatList = DATA_TABLE.getTable() #store the list!
        # print our stored list!
        # amp_mod.printChange()
        #change the amplitude to a new one (adjust)
        test_amp = amp_mod.amplitudeEqualizer()

        # d is the delta parameter this is how strict the test is
        if (amp_mod.newavg <= amp_mod.referenceAmplitude + d) and (amp_mod.newavg >= amp_mod.referenceAmplitude - d):
            print "FINAL ACHIEVED AMPLITUDE:", amp_mod.newavg
            print "TARGET AMPLITUDE:", amp_mod.referenceAmplitude
            break       
        b.mul = test_amp
        
except KeyboardInterrupt:
    prntfile.close()
    s.stop()