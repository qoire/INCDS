# INCDS TEST ENVIRONMENT

# FIRST LOOP = REFERENCE SINE WAVE (speaker A)
# SUBSEQUENT LOOPS = ADJUSTED WAVE (speaker B)


from pyo import *
import time
from incds_amplitude_module import amplitudeModule
from incds_phase_module import phaseModule
import csv

OUTPUT_FOLDER = './output/3.4.1/'

#setup csv writer
TARGET_MUL = 0.7
TEST_MUL = 0.1

s = Server(nchnls=2, duplex=1)
s.recordOptions(filename=OUTPUT_FOLDER+'output_audio_speaker.wav')
s.setInputDevice(2)
s.setOutputDevice(1)
s.boot()
a = Sine(freq=261, mul=TARGET_MUL) #target amplitude (reference) will not change
b = Sine(freq=261, mul=TEST_MUL)
p = Pan(a, outs=2, pan=1, spread=0).out() #start both speakers
p2 = Pan(b, outs=2, pan=0, spread=0).out()

s.setVerbosity(1)
inp = Input(chnl=1, mul=1)
s.start()

# feed input into a filter
fil_inp = Biquadx(inp, freq=261, q=5, type=2, stages=7)
audio_rec = Record(fil_inp, filename=OUTPUT_FOLDER+"input_mic_filter.wav", fileformat=0, sampletype=0)
mic_rec = Record(inp, filename=OUTPUT_FOLDER+"input_mic_unfilter.wav", fileformat=0, sampletype=0)
s.recstart()

#set start time
start_time = time.time()


phase_mod = phaseModule()

##########get the reference amplitude
b.mul = 0 #turn off this speaker leaving just the reference one on
time.sleep(1)
    
DATA_TABLE = NewTable(length=0.1,chnls=1)
rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
time.sleep(0.15)

# instantiate your amplitudeModule module
amp_mod = amplitudeModule()
amp_mod.setInitial(TEST_MUL)
ref_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())

##########get the starting amplitude of the second speaker
a.mul = 0 #turn the reference speaker off
b.mul = TEST_MUL

time.sleep(1)


#enter loop to equalize the amplitudes
try:
    while True:
        #record new values!
        DATA_TABLE = NewTable(length=0.1,chnls=1)
        rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.15)

        amp_mod.changeFloatList = DATA_TABLE.getTable()
        #change the amplitude to a new one (adjust)
        test_amp_input = amp_mod.averageAmplitude(DATA_TABLE.getTable())
        test_amp = amp_mod.amplitudeEqualizer()

        #exit condition:
        if (float(amp_mod.referenceAmplitude - test_amp_input) < float(0.0010000)):
            print "Amplitude Equalized"
            print "B: Amplitude" + str(test_amp)
            break

        b.mul = test_amp
        time.sleep(0.1) #sleep for 500ms (JAWBONE has more delay than usual)     

    a.mul = TARGET_MUL
    print "Proceeding to Phase test"

    time.sleep(0.5)

    with open(OUTPUT_FOLDER+'results.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['Time', 'Phase', 'Amplitude'])

    while True:
        DATA_TABLE = NewTable(length=0.1, chnls=1)
        rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.15)
        input_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())
        nx_phase = phase_mod.phaseChange(input_amp)
        new_phase = float(nx_phase)/float(360)
        b.setPhase(new_phase)
        print new_phase

        with open(OUTPUT_FOLDER+'results.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([time.time()-start_time, nx_phase, input_amp])


        if (input_amp < 0.01):
            time.sleep(2)
            break
        time.sleep(0.2)

    phase_mod_180 = phaseModule()
    loop_counter1=0;
    print "Initiated 180 Phase Loop"

    with open(OUTPUT_FOLDER+'results.csv', 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        writer.writerow([0, 0, 0])

    out_phase = nx_phase
    while True:
        DATA_TABLE = NewTable(length=0.1, chnls=1)
        rec = TableRec(fil_inp, table=DATA_TABLE, fadetime=0).play()
        time.sleep(0.15)
        test_recieve_amp = amp_mod.averageAmplitude(DATA_TABLE.getTable())

        with open(OUTPUT_FOLDER+'results.csv', 'a') as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([time.time()-start_time, out_phase, test_recieve_amp])

        if loop_counter1==0:
            phase_mod_180 = float(nx_phase) + float(180)
            if phase_mod_180>360:
                phase_mod_180=phase_mod_180%360
            out_phase = float(phase_mod_180)/float(360)
            b.setPhase(out_phase)
            time.sleep(5)
            loop_counter1=1
            print ("new phase is " + str(out_phase))
        else:
            out_phase = float(nx_phase)/float (360)
            b.setPhase(out_phase)
            loop_counter1 = 0
            time.sleep(5)
            print ("new phase is " + str(out_phase))

except KeyboardInterrupt:
    s.recstop()
    audio_rec.stop()
    mic_rec.stop()
    s.stop()