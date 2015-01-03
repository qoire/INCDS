import SocketServer

class ServerHandler(SocketServer.StreamRequestHandler):
	def handle(self):
		#receive the data (socket)
		self.data = self.rfile.readline().strip()
		print "{} wrote:".format(self.client_address[0])
		print self.data

		#send back
		self.wfile.write(self.data.upper())

if __name__ == "__main__":
	HOST, PORT = '', 9999

	server = SocketServer.TCPServer((HOST, PORT), ServerHandler)

	#run untill we interrupt
	server.serve_forever()
	