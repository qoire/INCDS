import global_var
import audio_packager
import incds_dft
import threading
import subprocess
import time
from pyo import *

class INCDS(threading.Thread):

    def __init__(self, freq, WAVE_LOCATION):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True
        self.freq = frequency
        self.WAVE_LOCATION = WAVE_LOCATION

    def run(self):
        while self.signal:
            cmd = "python audio_main.py"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.communicate()

            #biquad filter
            audio_packager.biquad_filter(self.WAVE_LOCATION, freq)

