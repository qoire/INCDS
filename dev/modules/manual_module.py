#INTERFACE PROGRAM V0.03
#Uses phone as interface instead of manual
#Now takes in a special parameter: debug

from pyo import *
import time
import socket
import threading
import ServerSocket
import json

#data format:
#{'freq': int, 'phase': int, 'auto': True/False}

#globals
user_phase = 0.0
user_freq = 200
auto_mode = False

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        global user_phase
        global user_freq
        global auto_mode 

        data = self.rfile.readline().strip()
        cur_thread = threading.current_thread()

        #response handling
        client_input = json.loads(data)
        user_phase = client_input['phase']
        user_freq = client_input['freq']
        auto_mode = client_input['auto']

        response = "ok\n"
        self.request.sendall(response)

class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def client(ip, port, message):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    try:
        sock.sendall(message)
        response = sock.recv(1024)
        print "Received: {}".format(response)
    finally:
        sock.close()

#MAIN
s = Server(nchnls=2).boot()
s.start()
a = Sine(freq=261, mul=0.3)
b = Sine(freq=261, phase=0, mul=0.3)
p = Pan(a, outs=2, pan=1, spread=0).out()
p2 = Pan(b, outs=2, pan=0, spread=0).out()

#debug mode
debug_sine=Sine(freq=5,mul=20)


#set up server
HOST, PORT = "localhost", 9999
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

except KeyboardInterrupt:
    s.stop()
    server.shutdown()
    
