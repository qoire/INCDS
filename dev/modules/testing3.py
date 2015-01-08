import incds_mode
import audio_packager
import time
import numpy
from pyo import *
from scipy.io.wavfile import read

WAVE_LOCATION = "./output/noramlize_wav.wav"

s = Server(audio="offline").boot()
filedur=sndinfo(WAVE_LOCATION)[1]
s.recordOptions(dur=filedur, filename="./output/filtered.wav")
ifile = SfPlayer(WAVE_LOCATION)
f = Biquadx(ifile, freq=261, q=10, type=2, stages=26)
s.start()

time.sleep(3)
s.shutdown()



