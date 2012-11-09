
""" NameSpaceTV for Slime
Detects and stores unique OSC namespaces being used

@scotthewit
scotthewitt.co.uk
helopg.co.uk

requires
https://trac.v2.nl/wiki/pyOSC
"""


import OSC
import time, threading



# tupple with ip, port.
receive_address = 'shrpi', 10000

# OSC Server. 
s = OSC.OSCServer(receive_address) # basic

# this registers a 'default' handler (for unmatched messages), 
# an /'error' handler, an '/info' handler.
# And, if the client supports it, a '/subscribe' & '/unsubscribe' handler
s.addDefaultHandlers()

# list of used OSC namespaces
nsUsed = []
    
# define a message-handler function for the server to call.
def activens_handler(addr, tags, stuff, source):
    global nsUsed
    startingUniqueCount = len(nsUsed)
   # print "received new osc msg from %s" % OSC.getUrlStr(source)
   # print "with addr : %s" % addr
   # print "data %s" % stuff
   # print "---"
    nsUsed.append(addr)
    nsUnique = list(set(nsUsed))
    currentUniqueCount = len(nsUnique)
    if startingUniqueCount != currentUniqueCount:
        print "!"
        print "New Unique : %s" % addr
        print nsUnique
        print "end of Unique"
        f = open('/var/www/nstv/nsfound.txt', 'w')
        s = str(nsUnique)
        f.write(s)
    del nsUsed
    nsUsed = nsUnique[:]
    print "~",

# Msg Handler over writing default to detect blank namespaces
s.addMsgHandler('default', activens_handler) 

# just checking which handlers we have added
print "Registered Callback-functions are :"
for addr in s.getOSCAddressSpace():
    print addr

# Start OSCServer
print "\nStarting OSCServer. Use ctrl-C to quit."
st = threading.Thread( target = s.serve_forever )
st.start()


try :
    while 1 :
        time.sleep(5)

except KeyboardInterrupt :
    print "\nClosing OSCServer."
    s.close()
    print "Waiting for Server-thread to finish"
    st.join() ##!!!
    print "Done"
        

