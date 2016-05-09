# Contains all global variables necessary
# Acts like a singleton
# Changing could lead to unintended consequences
# Yao Jan 3rd, 2015
import Queue

# DEFINE GLOBALS
user_phase = 0
user_freq = 200
auto_mode = False
debug_mode = False

#store old hash
old_hash = {'freq': 261, 'phase': 0, 'auto': 0, 'debug': 0, 'stop': 0, 'mag1': 300, 'mag2': 300, 'mute1': 0, 'mute1': 0, 'shutdown': 0}

# Queue for communication between audio/DFT threads
input_queue = Queue.PriorityQueue(maxsize=1) # Communication between networkhandler and main
switch_queue = Queue.PriorityQueue(maxsize=1) # Communication between main and automode
network_queue = Queue.Queue()