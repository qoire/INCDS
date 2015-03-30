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
        self.speakerB = 0
        self.newavg = 0
        self.d = 0.01

    def setInitial(self, initial_val):
        self.speakerB = initial_val

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