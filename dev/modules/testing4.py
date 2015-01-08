# import

from pyo import *

WAVE_LOCATION = "./output/temp.wav"

s = Server(nchnls=2).boot()
tab = SndTable(WAVE_LOCATION)
s.start()

print tab.getTable()

time.sleep(1)