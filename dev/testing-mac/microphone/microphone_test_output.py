from pyo import *
pa_list_devices()

s = Server(nchnls=2, duplex=1)
s.setOutputDevice(1)
s.setInputDevice(2)
s.boot()
s.start()

sine_out = Sine(freq=261, mul=1).mix(2).out()
inp = Input(chnl=0, mul=1)
out_rec = Record(sine_out, filename="output/output_sine.wav",fileformat=0, sampletype=0)
audio_rec = Record(inp, filename="output/input_mic_unfiltered.wav", fileformat=0, sampletype=0)

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
	audio_rec.stop()
	out_rec.stop()
	s.stop()