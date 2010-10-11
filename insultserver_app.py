# 
# Runs the insult server from twistd
# Start the server by entering 
#  twistd -y insultserver_app.py
# Stop the server by entering 
#  kill `cat twistd.pid`
#

from twisted.application import service
import insultserver_twistd

port = 8080
greetings = ['Welcome to the CPOSC Insult Server.  Enter a topic to receive an insult.',
             'Enter "quit" to disconnect.']

# It is important that we name the variable below "application".
# twistd will look for an object with that name.
application = service.Application("InsultServer")
insult_service = insultserver_twistd.InsultService(port, greetings)
insult_service.setServiceParent(application)