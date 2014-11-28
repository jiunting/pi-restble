import tornado.ioloop
import tornado.web
import tornado.template
import tornado.httpserver
import json
import datetime
import sys
import os 

# pyble module 
#import pyble

class MainHandler(tornado.web.RequestHandler):

    def initialize(self):
		print "init"

    def get(self, playlist=None):
		print "get"

application = tornado.web.Application(
[
	# Nodes (discover nodes and list enabled nodes)
	(r"/gap/nodes?passive=1", GetScanPassive),
	(r"/gap/nodes?active=1", GetScanActive),
	(r"/gap/nodes?enable=1", GetEnableAllNodes),
	(r"/gap/nodes/<node>", GetEnabledNodeWithIdentified), 

	# Nodes (enabling or disabling connection of nodes)
	(r"/gap/nodes/<node>?connect=1(&interval=<interval>&latency=<latency>&enable=1)", PutConnectingTheIdentifiedNode),
	(r"/gap/nodes/<node>?enable=0", PutDisconnectingTheIdentifiedNode), 	

	# Perform a name discovery of the node identified by handle <node>.
	(r"/gap/nodes/<node>?name=1", GetNameDiscoveryIdentifiedNode),

	# Server Configuration / Exchange MTU / Not applicable
	#
	# Primary Service Discovery
	(r"/gatt/nodes/<node>/services?primary=1", GetDiscoveyAllPrimaryServices),
	(r"/gatt/nodes/<node>/services?primary=1&uuid=<uuid>", GetDiscoveyPrimaryServicesByUUID),
	
	# Relationship Discovery
	(r"/gatt/nodes/<node>/services", GetFindIncludedServices),
	
	# Characteristic Discovery
	(r"/gatt/nodes/<node>/services/<service>/characteristics", GetDiscoverAllCharacteristicsOfService),
	(r"/gatt/nodes/<node>/characteristics?uuid=<uuid>", GetDiscoverCharacteristicbyUUID),
	
	# Characteristic Descriptor Discovery
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/descriptors", GetDiscoverAllCharacteristicDescriptors),

	# Characteristic Value Read	
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value", GetReadCharacteristicValue),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?uuid=<uuid>&start=<handle>&end=<handle>", GetReadUsingCharacteristicUUID),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?long=1", GetReadLongCharacteristicsValue),
	(r"/gatt/nodes/<node>/characteristics/value?multiple=1", GetReadMultipleCharacteristicsValue),
	
	# Characteristic Value Write
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value/<value>?noresponse=1", PutWriteWithoutResponse),
	(r"/notdefined",SignedWriteWithoutResponse),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value/<value>", PutWriteCharacteristicValue),	
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value/<value>?long=1",PutWriteLongCharacteristicValue),
	(r"/gatt/nodes/<node>/characteristics/value?reliable=1", PutCharacteristicValueReliableWrite),
	
	# Characteristic Value Notification
	(r"/gatt/nodes/<node>>/characteristics?notify=1", PutNotification),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?notify=1",GetNotification),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?notify=1&event=1", EventSourceNotification),
	
	# Characteristic Value Indication
	(r"/gatt/nodes/<node>/characteristics?indicate=1", PutIndication),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?indicate=1",GetIndication),
	(r"/gatt/nodes/<node>/characteristics/<characteristic>/value?indicate=1&event=1", EventSourceIndication),
	
	# Characteristic Descriptor Value Read
	(r"/gatt/nodes/<node>/descriptor/<descriptor>/value", GetReadCharacteristicDescriptor),
	(r"/gatt/nodes/<node>/descriptor/<descriptor>value?long=1", GetReadLongCharacteristicDescriptors),
	
	# Characteristic Descriptor Value Write
	(r"/gatt/nodes/<node>/descriptor/<descriptor>/value/<value>", PutWriteCharacteristicDescriptor),
	(r"/gatt/nodes/<node>/descriptor/<descriptor>/value/<value>?long=1", GetWriteLongCharacteristicDescriptors),
    (r"/(.*)", MainHandler)
])

if __name__ == "__main__":
    port = 8888
    if len(sys.argv) == 2 and sys.argv[1].isdigit():
		port = int(sys.argv[1])
		print port
	http_server = tornado.httpserver.HTTPServer(application)
	http_server.listen(port)
	
	print "Raspberry Pi - Pi-BLEGateway"
	print "Server start .."
	try:
		tornado.ioloop.IOLoop.instance().start()
	except KeyboardInterrupt:
		print('\nExit ..')
    	sys.exit(0)
