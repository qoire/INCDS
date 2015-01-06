from pyo import *
import global_var

def biquad_filter(sound_file, point_freq):
    sf = SfPlayer(sound_file)
    info = sndinfo(sound_file)

    print info

    f = Biquadx(sf, freq=point_freq, q=10, type=2, stages=26)
    print "Successfully filtered"