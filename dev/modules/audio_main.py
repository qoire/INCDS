import os
import audio_packager

# Audio Subprocess
# Only purpose is to record audio on a different process
# Assume will always work (this might be bad)

WAVE_LOCATION = "./output/temp.wav"

audio_packager.getAudio(WAVE_LOCATION)

