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

        ref = 0
        inc = 1
        index = 0
        peaks = []

        for i in float_list:
            if (i>ref):
                if (inc == 0):
                    peaks.insert(index,ref)
                    index = index+1
                inc = 1
            elif (i<ref):
                if (inc == 1):
                    peaks.insert(index,ref)
                    index = index+1
                inc = 0
            ref = i
    	
        avg = sum(abs(x) for x in peaks)/float(len(peaks))
        print "AVERAGE:", avg
        self.referenceAmplitude = avg
        self.gotReference = True
        return avg

    def amplitudeEqualizer(self):
        return self.averageAmplitude(self.changeFloatList) + 0.1

    def printReference(self):
        print self.referenceFloatList

    def printChange(self):
        print self.changeFloatList

OUTPUT_FILE = "./output/output.wav"
##fake_file = StringIO.StringIO()

TARGET_MUL = 0.5
d = 0.01

s = Server(audio="offline").boot()
s.recordOptions(dur=0.2, filename=OUTPUT_FILE)
s.setVerbosity(1)
b = Sine(freq=450, mul=TARGET_MUL).out()

#DATA_TABLE
DATA_TABLE = NewTable(length=0.2,chnls=1)
rec = TableRec(b, table=DATA_TABLE, fadetime=0).play()
s.start()
s.stop()

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()

amp_mod.referenceFloatList = DATA_TABLE.getTable()
amp_mod.averageAmplitude(DATA_TABLE.getTable())
# amp_mod.referenceAmplitude = averageAmplitude(DATA_TABLE.getTable())
# amp_mod.printReference()

#get your initial amplitude here from speaker A

test_amp = 0.1

try:
    while True:
        #set new amplitude values for b
        b.mul = test_amp
        #record new values!
        DATA_TABLE = NewTable(length=0.2,chnls=1)
        rec = TableRec(b, table=DATA_TABLE, fadetime=0).play()
        s.start()
        #say we wanted to print the new values!
        amp_mod.changeFloatList = DATA_TABLE.getTable() #store the list!
        # print our stored list!
        # amp_mod.printChange()
        #change the amplitude to a new one (adjust)
        test_amp = amp_mod.amplitudeEqualizer()

        # d is the delta parameter this is how strict the test is
        if (test_amp <= TARGET_MUL + d) and (test_amp >= TARGET_MUL - d):
            print "TEST AMPLITUDE:", test_amp
            print "TARGET AMPLITUDE:", TARGET_MUL
            break
        
except KeyboardInterrupt:
    s.stop()

