import global_var
import threading
import subprocess
import time
from pyo import *

class INCDS(threading.Thread):

    def __init__(self, freq, fil_inp, speaker_A, speaker_B):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True
        self.freq = freq
        self.fil_inp = fil_inp
        self.speaker_A = speaker_A
        self.speaker_B = speaker_B

    def run(self):
        while self.signal:
        	print "FROM THREAD!" + str(self.freq)
        	self.speaker_A.setFreq(850)
        	time.sleep(1)
