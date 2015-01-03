#INTERFACE PROGRAM V0.03
#Uses phone as interface instead of manual
#Now takes in a special parameter: debug

from pyo import *
import time
import socket
import threading
import SocketServer
import json

#data format:
#{'freq': int, 'phase': int, 'auto': 'True'/'False', 'debug': 'True'/'False'}

#globals
user_phase = 0
user_freq = 200
auto_mode = False
debug_mode = False

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        global user_phase
        global user_freq
        global auto_mode
        global debug_mode

        data = self.rfile.readline().strip()
        cur_thread = threading.current_thread()

        print data

        #response handling
        client_input = json.loads(data)
        user_phase = client_input['phase']
        user_freq = client_input['freq']
        auto_mode = client_input['auto']

        if client_input['auto'] == 'True':
            auto_mode = True
        else:
            auto_mode = False

        if client_input['debug'] == 'True':
            debug_mode = True

        response = "ok\n"
        self.request.sendall(response)

#    def handle(self):
#        #receive the data (socket)
#        self.data = self.rfile.readline().strip()
#        print "{} wrote:".format(self.client_address[0])
#        print self.data

        #send back
#        self.request.sendall(self.data.upper())

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass


#MAIN
s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.5)
b = Sine(freq=261, phase=0, mul=0.5)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#debug mode
debug_sine=Sine(freq=5,mul=20)


#set up server
HOST, PORT = '', 9999
server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
ip, port = server.server_address
server_thread = threading.Thread(target=server.serve_forever)
server_thread.daemon = True
server_thread.start()

#initial setup set frequency:
#user_freq = float(raw_input('Enter desired frequency:'))
#a.setFreq(user_freq)
#b.setFreq(user_freq)

try:
    while True:
        if debug_mode == True:
            b.setFreq(user_freq+debug_sine)
            a.mul=0
            time.sleep(5)
            
            #set back to sine
            b.setFreq(user_freq)
            a.mul=0.3

            #change debug mode to false
            debug_mode = False

        #set user phase etc (for now auto mode does not work)

        a.setFreq(user_freq)
        b.setFreq(user_freq)
        user_phase_float = float(user_phase)/360

        b.setPhase(1 - user_phase_float)
        #sleep the system for a little bit
        time.sleep(0.05)
except KeyboardInterrupt:
    s.stop()
    server.shutdown()
    
