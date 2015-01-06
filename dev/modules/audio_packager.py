import pyaudio
import wave
import global_var
import StringIO

TASK_AUDIO = "AUDIO_INPUT_INIT"

def initAudioThread():
	# Communicates with main thread using queue


def audioThread():
	while True:
		# Block until you get a job! saves cpu!
		task = global_var.input_queue.get()
		if task == TASK_AUDIO:
			out_file = getAudio(1)
			global_var.input_queue.put(out_file)
			global_var.input_queue.task_done()


def getAudio(RECORD_SECONDS):
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS = 1
	RATE = 44100
	WAVE_OUTPUT_FILENAME = StringIO.StringIO()

	p = pyaudio.PyAudio()

	stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

	for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

    #stop stream after done
    stream.stop_stream()
    stream.close()
    p.terminate()

    #initiate writing to wave file
    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
	wf.setnchannels(CHANNELS)
	wf.setsampwidth(p.get_sample_size(FORMAT))
	wf.setframerate(RATE)
	wf.writeframes(b''.join(frames))
	wf.close()

	return WAVE_OUTPUT_FILENAME



