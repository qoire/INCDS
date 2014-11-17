from pyo import *
import csv
import argparse

#MATLAB Testing Script
#Script is designed to accept inputs in a .txt file (just specify)
#Script will run that input file once in its entirety, then quit
#Please input a script of the format:

#Ex. Test1.txt:
#<MAG_VALUE_1>,<MAG_VALUE_2>,<PHASE_VALUE>,<FREQ_VALUE>,<TIME>
#Rows are newline seperate, please don't add unecessary spaces after commas
#This is standard .csv format (used by excel)

HASH_MAG_1='mul1'
HASH_MAG_2='mul2'
HASH_PHASE='phase'
HASH_FREQ='freq'
HASH_TIME='time'
HASH_DONE='done'

def gen_action_list(n):
    action_list = ''
    for row in n:
        action_hash[HASH_MAG_1] = float(row[1])
        action_hash[HASH_MAG_2] = float(row[2])
        action_hash[HASH_PHASE] = 1 - float(row[3])/360
        action_hash[HASH_FREQ] = float(row[4])
        action_hash[HASH_TIME] = int(row[5])
        action_hash[HASH_DONE] = False
        action_list.append(action_hash)

    return action_list

#CSV Processing section
parser = argparse.ArgumentParser(description='please enter .csv file')
parser.add_argument("csv_file")
args = parser.parse_args()

with open(args.csv_file, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')

# Generate action list that will run
action_list = gen_action_list(n)

#Audio Portion
s = Server(nchnls=2).boot()
s.start()
s.recstart()

# Takes first element of the list as initial settings
magnitude = {'ch1': action_list[0][HASH_MAG_1], 'ch2': action_list[0][HASH_MAG_2]}
phase = {'ch1': action_list[0][HASH_PHASE], 'ch2': 0.0}
freqency = {'ch1': action_list[0][HASH_FREQ], 'ch2': action_list[0][HASH_FREQ]}

a = Sine(freq=frequency['ch1'], phase=phase['ch1'], mul=magnitude['ch1'])
b = Sine(freq=frequency['ch2'], phase=phase['ch2'], mul=magnitude['ch2'])

# Spread controls, by default two channels have no interference with eachother
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

try:
    
except KeyboardInterrupt:
    s.stop()
    s.recstop()
    
