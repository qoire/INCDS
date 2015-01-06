import global_var
import audio_packager
import incds_dft
import threading
import subprocess
import time

class INCDS(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True

    def run(self):
        while self.signal:
            cmd = "python audio_main.py"
            p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
            p.communicate()
            print p.returncode
            time.sleep(1)