from pyo import *

INPUT_FILE = "./output/microphone_test_2_cropped.wav"
OUTPUT_FILE = "./output/biquad_output.wav"

s = Server(audio="offline").boot()
filedur = sndinfo(INPUT_FILE)[1]
s.recordOptions(dur=filedur, filename=OUTPUT_FILE)
ifile = SfPlayer(INPUT_FILE)
f = Biquadx(ifile, freq=450, q=4, type=2, stages=6).out()
s.start()