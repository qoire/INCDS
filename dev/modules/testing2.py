import subprocess
from pyo import *

#MAIN
s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, phase=0, mul=0.5)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

proc = subprocess.Popen(['python', 'audio_main.py'], stdout=subprocess.PIPE)

while True:
	line = proc.stdout.readline()
	if line != '':
		print "test:", line.rstrip()
	else:
		break