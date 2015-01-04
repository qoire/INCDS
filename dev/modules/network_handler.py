# Network Handler Module
# Responsible for handling communication with client interface
# Yao Sun Jan 3rd, 2015

# Notes:
#data format:
#{'freq': int, 'phase': int, 'auto': 'True'/'False', 'debug': 'True'/'False'}

import time
import socket
import SocketServer
import json
import threading
import global_var

class ThreadedTCPRequestHandler(SocketServer.StreamRequestHandler):

    def handle(self):
        data = self.rfile.readline().strip()
        cur_thread = threading.current_thread()

        print data

        #response handling
        client_input = json.loads(data)

        #handling each variable individually
        global_var.user_phase = client_input['phase']
        global_var.user_freq = client_input['freq']
        global_var.auto_mode = client_input['auto']

        if client_input['auto'] == 'True':
            global_var.auto_mode = True
        else:
            global_var.auto_mode = False

        if client_input['debug'] == 'True':
            global_var.debug_mode = True

        response = "ok\n"
        self.request.sendall(response)


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def startInterfaceServer(HOST, PORT):
	server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
	ip, port = server.server_address
	server_thread = threading.Thread(target=server.serve_forever)
	server_thread.daemon = True
	server_thread.start()

