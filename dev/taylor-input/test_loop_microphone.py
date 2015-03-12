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
    	
        if ((len(peaks)) != 0):
            avg = sum(abs(x) for x in peaks)/float(len(peaks)) 	#average the abs() values of the peaks
        else:
            avg = 0
        #print "AVERAGE:", avg
        if not self.gotReference:
            self.referenceAmplitude = avg 					#store the reference
            self.gotReference = True
            print "REFERENCE:", self.referenceAmplitude
        return avg

    def amplitudeEqualizer(self):
        newavg = self.averageAmplitude(self.changeFloatList)
        if (newavg < 1):
            if newavg < self.referenceAmplitude: 	#if the speaker volume needs to be increased
            	return (newavg + d)					#'d' is the delta value threshold define below
            elif newavg > self.referenceAmplitude: 	#if the speaker volume needs to be decreased
                return (newavg - d)
        else:
            return 1 #added in a hard limiter, dont want to blow up speakers

    def printReference(self):
        print self.referenceFloatList

    def printChange(self):
        print self.changeFloatList

TARGET_MUL = 0.6
d = 0.01 	#program doesn't seem to work if this delta is <0.01

s = Server(nchnls=2, duplex=1)
s.setInputDevice(3)
s.setOutputDevice(1)
s.boot()
s.setVerbosity(1)
a = Sine(freq=450, mul=TARGET_MUL)
b = Sine(freq=450, mul=0)

p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#setup input
inp = Input(chnl=0, mul=1)
s.start()
#DATA_TABLE
DATA_TABLE = NewTable(length=0.1,chnls=1)
rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()

time.sleep(0.15) #sleep for a little bit to wait for table

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()

amp_mod.referenceFloatList = DATA_TABLE.getTable()
amp_mod.averageAmplitude(DATA_TABLE.getTable())
print 

#open up speaker B close speaker A
########a.mul = 0

test_amp = 1

try:
    while True:
        #set new amplitude values for b
        ########b.mul = test_amp
        #record new values!
        DATA_TABLE = NewTable(length=0.1,chnls=1)
        rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.11)
        #say we wanted to print the new values!
        amp_mod.changeFloatList = DATA_TABLE.getTable() #store the list!
        # print our stored list!
        # amp_mod.printChange()
        #change the amplitude to a new one (adjust)
        test_amp = amp_mod.amplitudeEqualizer()

        # d is the delta parameter this is how strict the test is
        #if (test_amp <= amp_mod.referenceAmplitude + d) and (test_amp >= amp_mod.referenceAmplitude - d):
        if (test_amp <= amp_mod.referenceAmplitude + d) and (test_amp >= amp_mod.referenceAmplitude - d):
            print "FINAL ACHIEVED AMPLITUDE:", amp_mod.changeAmplitude
            print "TARGET AMPLITUDE:", amp_mod.referenceAmplitude
            break
except KeyboardInterrupt:
    s.stop()

