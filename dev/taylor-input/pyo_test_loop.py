# INCDS TEST ENVIRONMENT

# FIRST LOOP = REFERENCE SINE WAVE (speaker A)
# SUBSEQUENT LOOPS = ADJUSTED WAVE (speaker B)
from pyo import *

def amplitudeAdjustment(data_tab):
	# your code here!
	# you can add more inputs as necessary
	# just make sure you return a new amplitude value

	amp = 0.1
	return amp

OUTPUT_FILE = "./output/output.wav"

TARGET_MUL = 0.5
d = 0.01

s = Server(audio="offline").boot()
s.recordOptions(dur=0.2, filename=OUTPUT_FILE)
b = Sine(freq=450, mul=TARGET_MUL).out()

#DATA_TABLE
DATA_TABLE = NewTable(length=0.2,chnls=1)
rec = TableRec(b, table=DATA_TABLE, fadetime=0).play()
s.start()
s.stop()

print DATA_TABLE.getTable()

#get your initial amplitude here from speaker A

test_amp = 0.1

try:
	while True:
		#set new amplitude values for b
		b.mul = test_amp
		s.start()
		#record new values!
		rec = TableRec(b, DATA_TABLE)
		print DATA_TABLE.getTable()
		test_amp = amplitudeAdjustment(DATA_TABLE)

		# d is the delta parameter this is how strict the test is
		if (test_amp <= TARGET_MUL + d) or (test_amp >= TARGET_MUL - d):
			break
		
except KeyboardInterrupt:
	s.stop()

