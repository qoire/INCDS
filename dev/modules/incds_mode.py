import global_var
import threading
import subprocess
import time
from incds_amplitude_module import amplitudeModule
from incds_phase_module import phaseModule
from pyo import *

class INCDS(threading.Thread):
    def __init__(self, input_freq, input_mag, filtered_inp, inp_A, inp_B):
        threading.Thread.__init__(self)
        self.started = False
        self.signal = True
        self.freq = input_freq
        self.fil_inp = filtered_inp
        self.a = inp_A
        self.b = inp_B
        self.input_mag = input_mag

    def list_shifting(self, a_list, new_amplitude):
        # only works for lists with 3 indices
        a_list[0] = a_list[1]
        a_list[1] = a_list[2]
        a_list[2] = new_amplitude
        return a_list

    def run(self):
        TARGET_MUL = self.input_mag/float(1000)
        TEST_MUL = self.input_mag/float(1000)
        DIVIDE_MAGNITUDE = 30

        start_time = time.time()

        # change phase
        self.a.setFreq(650)
        self.b.setFreq(650)

        # instantiate modules
        phase_mod = phaseModule()
        amp_mod = amplitudeModule()
        self.a.mul = TARGET_MUL
        self.b.mul = 0
        time.sleep(0.5)

        # setup data table
        DATA_TABLE = NewTable(length=0.1, chnls=1)
        rec = TableRec(self.fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.45)

        amp_mod.setInitial(TEST_MUL)
        ref_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())
        dynamic_ref = ref_amp/float(20)

        self.a.mul = 0 
        self.b.mul = TEST_MUL
        time.sleep(0.5)

        avg_amp_list = [0, 0, 0]

        print "Amplitude Equalizer: Started"
        while self.signal:
            # Check for pause
            if not global_var.switch_queue.empty():
                temp_dict = global_var.switch_queue.get()
                print "INCDS_MODE: Retrieved Queue Data"
                if (temp_dict['auto'] == 2):
                    print "Automode: Paused"
                    while True:
                        new_temp_dict = global_var.switch_queue.get(True)
                        if (new_temp_dict['auto'] == 0):
                            break

            # Normal operation
            DATA_TABLE = NewTable(length=0.1, chnls=1)
            rec = TableRec(self.fil_inp, table=DATA_TABLE, fadetime=0).play()
            time.sleep(0.15)

            amp_mod.changeFloatList = DATA_TABLE.getTable()
            test_amp_input = amp_mod.averageAmplitude(DATA_TABLE.getTable())
            test_amp = amp_mod.amplitudeEqualizer()
            avg_amp_list = self.list_shifting(avg_amp_list, test_amp_input)

            if (abs(float(amp_mod.referenceAmplitude - test_amp_input)) < dynamic_ref):
                print "Reference Amplitude: " + str(amp_mod.referenceAmplitude)
                print "Test Amplitude: " + str(test_amp_input)
                print "Amplitude Equalizer: Finished"
                break

            self.b.mul = test_amp
            time.sleep(0.1)

        # Turn speaker A back on
        self.a.mul = TARGET_MUL

        time.sleep(0.4)
        
        nx_phase = 0
        avg_lt= (float(avg_amp_list[0])+float(avg_amp_list[1])+float(avg_amp_list[2]))/float(DIVIDE_MAGNITUDE)
        print "Phase Module: Started"
        while self.signal:
            if not global_var.switch_queue.empty():
                temp_dict = global_var.switch_queue.get()
                print "INCDS_MODE: Retrieved Queue Data"
                if (temp_dict['auto'] == 2):
                    print "Automode: Paused"
                    while True:
                        new_temp_dict = global_var.switch_queue.get(True)
                        if (new_temp_dict['auto'] == 0):
                            break

            # Normal operation
            DATA_TABLE = NewTable(length=0.1, chnls=1)
            rec = TableRec(self.fil_inp, table=DATA_TABLE, fadetime=0).play()
            time.sleep(0.35)

            input_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())
            if (input_amp < avg_lt):
                time.sleep(2)
                print "Phase Module: Finished"
                break

            nx_phase = phase_mod.phaseChange(input_amp)
            new_phase = float(nx_phase)/float(360)
            self.b.setPhase(new_phase)
 
            print "Phase Module: Desired Amplitude: " + str(avg_lt)
        
            time.sleep(0.4)  #change sleep time

        out_phase = nx_phase
        phase_mod_180 = None
        loop_set = 0
        while self.signal:
            # Get data from queue
            in_dict = global_var.switch_queue.get(block=True)
            DATA_TABLE = NewTable(length=0.1, chnls=1)
            rec = TableRec(self.fil_inp, table=DATA_TABLE, fadetime=0).play()
            test_recieve_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())

            if not in_dict['switch']:
                phase_mod_180 = float(nx_phase) + float(180)
                if phase_mod_180>360:
                    phase_mod_180=phase_mod_180%360
                out_phase = float(phase_mod_180)/float(360)
                self.b.setPhase(out_phase)

                print ("Phase Change: " + str(out_phase))
            else:
                out_phase = float(nx_phase)/float (360)
                self.b.setPhase(out_phase)
                print ("Phase Change: " + str(out_phase))
            



