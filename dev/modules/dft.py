from pyo import *
import os

SND_PATH = '../input/input.wav'

s = Server().boot()
s.start()


#recording
#rec = Record(f, filename=SND_PATH+"out1.wav", fileformat=0, sampletype=0)

try:
    while True:
        time.sleep(0.1)
        if os.path.isfile(SND_PATH):
            sf = SfPlayer(SND_PATH)
            info = sndinfo(SND_PATH)
            f = Biquadx(sf, freq=261, q=10, type=2, stages=26)
            t = DataTable(info[0])

            print info
            print "DFS_Module: Information Read Successful"
            os.remove(SND_PATH)
except KeyboardInterrupt:
    s.stop()