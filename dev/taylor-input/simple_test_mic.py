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
            print "AMPLITUDE:", self.referenceAmplitude
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

s = Server(nchnls=2, duplex=1).boot()
s.setVerbosity(1)

#setup input
inp = Input(chnl=0, mul=1)
s.start()
#DATA_TABLE

try:
    while True:
        DATA_TABLE = NewTable(length=0.1,chnls=1)
        rec = TableRec(inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.11) #sleep for a little bit to wait for table
        # instantiate your amplitudeModule module
        amp_mod = amplitudeModule()

        amp_mod.referenceFloatList = DATA_TABLE.getTable()
        amp_mod.averageAmplitude(DATA_TABLE.getTable())
        
        time.sleep(2)
        
except KeyboardInterrupt:
    s.stop()


