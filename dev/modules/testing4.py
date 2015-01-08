# simulate subprocess audio collection

import audio_packager
import subprocess
from pyo import *

WAVE_LOCATION = "./output/temp.wav"

s = Server(audio="offline").boot()

try:
	while True:
		# wave audio collection
		cmd = "python audio_main.py"
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		p.communicate()

		tab = SndTable(WAVE_LOCATION)
		s.start()
		print tab.getTable()
except KeyboardInterrupt:
	s.stop()