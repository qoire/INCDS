from pyo import *
# Setup this script to output to headphones

s = Server(nchnls=2, duplex=1)
s.setInputDevice(5)
s.setOutputDevice(4)
s.boot()
s.start()

mic_input = Input(chnl=0, mul=1)
#recording
biquad_fil = Biquadx(mic_input, freq=261, q=10, type=2, stages=10)
rec = Record(biquad_fil, filename="./output/filtered_output.wav", fileformat=0, sampletype=0)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    s.stop()


