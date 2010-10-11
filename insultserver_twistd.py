#
# This is a copy of the basic insult server,except that it provides the 
# InsultService class needed to run from twistd.  
#
from twisted.application import service, internet 
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
    

class InsultService(internet.TCPServer):
	def __init__(self, port, greetings):
		internet.TCPServer.__init__(self, port, InsultServerFactory(greetings))
    