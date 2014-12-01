from pyo import *

SND_PATH = '../input/'

s = Server().boot()
s.start()

sf = SfPlayer(SND_PATH + "input1.wav")
info = sndinfo(SND_PATH + "input1.wav")
print info
t = DataTable(info[0])
f = Biquadx(sf, freq=261, q=10, type=2, stages=26).out()

#recording
rec = Record(f, filename=SND_PATH+"out1.wav", fileformat=0, sampletype=0)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()