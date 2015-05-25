import sys
import subprocess
import atexit
import os
import signal

#Global the pid
global gui_pid, server_pid

#Get current directory
gui_dir = os.path.join(os.getcwd(), "GUI")
audio_dir = os.path.join(os.getcwd(), "audio")
#Get basedir
base_dir = os.getcwd()

print "Running msgserver"
#Server proc
serverproc = subprocess.Popen([sys.executable, os.path.join(base_dir, "msgserver.py")])
server_pid = serverproc.pid

print "Running audioserver"
#Audio proc
audioproc = subprocess.Popen([sys.executable, os.path.join(audio_dir, "microphone_output.py")], cwd=audio_dir)
audio_pid = audioproc.pid

print "Running GUI"
#GUI proc
guiproc = subprocess.Popen([sys.executable, os.path.join(gui_dir, "main.py")], cwd=gui_dir)
gui_pid = guiproc.pid

pid_list = [gui_pid, audio_pid, server_pid]

def kill_child():
	guiproc.kill()
	audioproc.kill()
	serverproc.kill()

atexit.register(kill_child)

#Exit on GUI Exit
guiproc.communicate()