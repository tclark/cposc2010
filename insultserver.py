#
# A basic twisted TCP server
# It listens for client connections and prints a welcome message when
# a client connects. Then it takes input from the client on a 
# per-line basis.  If the client sends "help", it responds with a help
# message.  If the client sends "quit" it sends a closing messages and
# closes the connection.  If the client sends anything else it tries to 
# send a matching insult.  Insults and insult subjects are read from a 
# text file.
#
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from twisted.protocols.basic import LineReceiver

class Insults:
    def __init__(self):
        self.insults = dict()
        datafile = open("insults.txt", "r")
        lines = datafile.readlines()
        datafile.close()
        for line in lines:
            (k,v) = line.split(":",1)
            self.insults[k] = v.strip()

    def getInsult(self, topic):
        try: 
            return(self.insults[topic])
        except KeyError:
            return("I've got nothing.")
	
    def getTopics(self):
        return self.insults.keys()

class InsultServerProtocol(LineReceiver):
    def __init__(self):
       self.insults = Insults()
    
    def getHelp(self):
	    self.sendLine("I can provide insults about the following items:")
	    for item in self.insults.getTopics():
		    self.sendLine(item)
		   
    def connectionMade(self):
        for line in self.factory.greeting_lines:
	        self.sendLine(line)
    
    def lineReceived(self, line):
        line = line.lower()
        if line == "quit":
            self.sendLine("Goodbye, loser.")
            self.transport.loseConnection()
        elif line == "help":
	        self.getHelp()
        else:
            self.sendLine(self.insults.getInsult(line))
               
class InsultServerFactory(Factory):
    protocol = InsultServerProtocol
    
    def __init__(self,greetings):
	    self.greeting_lines = greetings
    
if __name__ == "__main__":
    port = 8080
    greetings = ['Welcome to the CPOSC Insult Server.  Enter a topic to receive an insult.',
                 'Enter "quit" to disconnect.']
    reactor.listenTCP(port, InsultServerFactory(greetings))
    reactor.run()
    
    