import global_var
import audio_packager
import threading
import subprocess
import time
from pyo import *

class INCDS(threading.Thread):

    def __init__(self, WAVE_LOCATION, freq):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True
        self.freq = freq
        self.WAVE_LOCATION = WAVE_LOCATION

    def run(self):
        while self.signal:
            pass

