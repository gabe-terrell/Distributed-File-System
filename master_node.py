import sys, setup, json
from threading import Thread
from threaded_server import ThreadedServer
from file_structure import Directory, File, Node
from client_server_protocol import RequestType, ClientResponse
from viewer import Viewer

_, CLIENT_PORT = setup.SERVER_ADDR
_, NODE_PORT = setup.NODE_ADDR

BUFFER_SIZE = 1024

class MasterNode():

	def __init__(self):

		self.root = Directory('')
		self.nodes = []
		self.clientServer = ThreadedServer(CLIENT_PORT)
		self.nodeServer = ThreadedServer(NODE_PORT)

	def start(self):

		target = self.__startServer

		self.clientServer.handler = self.handleClientRequest
		clientThread = Thread(target=target, args=[self.clientServer])
		clientThread.start()

		self.nodeServer.handler = self.handleNodeConnection
		nodeThread = Thread(target=target, args=[self.nodeServer])
		nodeThread.start()


	def __startServer(self, server):
		server.listen()

	def handleClientRequest(self, socket, address):
		viewer = Viewer(self.root)

		# TODO: This is disgusting to look at right now
		while True:
			try:
				data = socket.recv(BUFFER_SIZE)

				if data:
					request = json.loads(data)

					if 'type' in request:
						type = request['type']

						if type == RequestType.viewer:
							if 'command' in request:
								command = request['command']
								self.handleViewerRequest(socket, viewer, command)
							else:
								raise error("Invalid Command Request")
						elif type == RequestType.download:
							pass
						elif type == RequestType.upload:
							pass
						else:
							raise error("Invalid Type Request")
					else:
						raise error("Invalid Client Request")
				else:
					raise error("Client disconnected")
			except:
				socket.close()
				return

	def handleViewerRequest(self, socket, viewer, command):
		if command == 'init':
			output = 'OK'
		else:
			argv = command.split()
			output = viewer.process(len(argv), argv)
		response = ClientResponse(RequestType.viewer, output)
		socket.send(response.toJson())
	

	def handleDownloadRequest(self, socket, path):
		pass

	def handleUploadRequest(self, socket, path, file):
		pass

	def handleNodeConnection(self, socket, address):
		# TODO: Handle request to create new file node
		pass






def main(argc, argv):
	# TODO
	mnode = MasterNode()
	mnode.start()


if __name__ == '__main__':
	main(len(sys.argv), sys.argv)
