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
old_hash = {'freq': 261, 'phase': 0, 'auto': 'False', 'debug': 'False', 'stop': 'False'}

# Queue for communication between audio/DFT threads
input_queue = Queue.PriorityQueue(maxsize=1)
network_queue = Queue.PriorityQueue(maxsize=1)