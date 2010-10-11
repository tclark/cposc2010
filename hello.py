#
# This is the simplest twisted appication I could write that does anything
# It prints "Hello, world!" after about one second and then loops until
# you hit ctrl-c to kill it.
#
from twisted.internet import reactor

def hello():
	print "Hello, world!"

reactor.callLater(1, hello)
reactor.run()
