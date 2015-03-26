import global_var
import threading
import subprocess
import time
from pyo import *

class INCDS(threading.Thread):
    def __init__(self, freq, fil_inp, A, B):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True
        self.freq = 850
        self.fil_inp = fil_inp
        self.a = speaker_A
        self.b = speaker_B

    def list_shifting(self, a_list, new_amplitude):
        # only works for lists with 3 indices
        a_list[0] = a_list[1]
        a_list[1] = a_list[2]
        a_list[2] = a_list[3]
        a_list[3] = new_amplitude
        return a_list

    def run(self):
        TARGET_MUL = 0.7
        TEST_MUL = 0.7
        DIVIDE_MAGNITUDE = 60

        start_time = time.time()

        # instantiate modules
        phase_mod = phaseModule()
        amp_mod = amplitudeModule()
        self.b.mul = 0
        time.sleep(0.5)

        # setup data table
        DATA_TABLE = NewTable(length=0.1, chnls=1)
        rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.45)

        amp_mod.setInitial(TEST_MUL)
        ref_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())

        self.a.mul = 0 
        self.b.mul = TEST_MUL
        time.sleep(0.5)

        avg_amp_list = [0, 0, 0]

        print "Amplitude Equalizer: Started"
        while self.signal:
            DATA_TABLE = NewTable(length=0.1, chnls=1)
            rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
            time.sleep(0.15)

            amp_mod.changeFloatList = DATA_TABLE.getTable()
            test_amp_input = amp_mod.averageAmplitude(DATA_TABLE.getTable())
            test_amp = amp_mod.amplitudeEqualizer()
            avg_amp_list = list_shifting(avg_amp_list, test_amp_input)

            if (float(amp_mod.referenceAmplitude - test_amp_input) < float(0.0010000)):
                print "Amplitude Equalizer: Finished"
                break

            self.b.mul = test_amp
            time.sleep(0.1)

        time.sleep(0.5)
        avg_lt= (float(avg_amp_list[0])+float(avg_amp_list[1])+float(avg_amp_list[2]))/float(DIVIDE_MAGNITUDE)

        while self.signal:
            DATA_TABLE = NewTable(length=0.1, chnls=1)
            rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
            time.sleep(0.15)

            



