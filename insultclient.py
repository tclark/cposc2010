#
# A simple twisted client corresponding to the insult server examples.
# It connects to a server on a given port (both hardcoded below).
# Basically it just passes anything the client enters to the server
# and outputs anything the server sends.  When the server sends its
# closing message it stops the reactor and the program exits.
#

from twisted.internet import reactor
from twisted.internet.protocol import Protocol, ClientFactory

class InsultClientProtocol(Protocol):
	def dataReceived(self, data):
		data = data.strip()
		print data
		if data == "Goodbye, loser." :
			return
		else:
		    input = raw_input(">").strip()
		    self.transport.write(input)
		    self.transport.write("\r\n")
		

class InsultClientFactory(ClientFactory):
	protocol = InsultClientProtocol
	
	def clientConnectionLost(self, transport, reason):
		reactor.stop()
		
	def clientConnectionFailed(self, transport, reason):
		print reason.getErrorMessage()
		reactor.stop()
	
	
if __name__ == "__main__":
    host = "127.0.0.1"
    port = 8080
    reactor.connectTCP(host, port, InsultClientFactory())
    reactor.run()	

	