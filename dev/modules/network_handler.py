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

        # response handling
        try:
            client_input = json.loads(data)

            # check that json is correct
            if not (checkJSONFile(client_input)):
                client_input = global_var.old_hash
        except ValueError:
            print 'Decoding JSON has failed'
            client_input = global_var.old_hash


        response = "ok\n"
        self.request.sendall(response)

        # handling each variable individually
        global_var.network_queue.put(client_input)
        global_var.network_queue.join()

        # replace old hash with current hash
        global_var.old_hash = client_input

    def checkJSONFile(json_file):
        check_list = ['freq', 'phase', 'auto', 'debug']

        for item in check_list:
            if item not in json_file:
                return False
        return True


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

def startInterfaceServer(HOST, PORT):
    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    ip, port = server.server_address
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    print "Network thread started"

