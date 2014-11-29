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

	def get(self):
		print "get"


class StartScanAndListEnablingDiscover(tornado.web.RequestHandler):
	def initialize(self):
		# Requests (discover nodes and list enabled nodes):
		self.write( 'GetStartScanAndListEnablingDiscover ')

	def get(self):
		# /gap/nodes?passive=1
		# /gap/nodes?active=1
		# /gap/nodes?enable=1
		passive = self.get_argument('passive', '0')
		active = self.get_argument('active', '0')
		enable = self.get_argument('enable', '0')
		if passive == '1':
			'''
			The gateway will perform passive scan for nodes. 
			Used scan parameters are decided by the gateway.
			Note: Just perform, and response somethings(state?).
			'''
			self.write( 'passive scan')

		elif active == '1':
			'''
			The gateway will perform active scan for nodes. 
			Used scan parameters are decided by the gateway.
			Note: Just perform, and response somethings(state?).
			'''
			self.write( 'active scan')
		elif enable == '1':
			'''
			The gateway will return a list of enabled devices 
			(devices that are either connected or will be connected when available and at gateway power-up)
			'''
			self.write( 'make connection')
		else :
			self.write( 'Bad Request')

class DataWithEnabledNode(tornado.web.RequestHandler):
	def initialize(self):
		# The gateway will return data for an enabled node identified by the handle <node>.
		self.write( 'GetDataWithEnableNode ')

	def get(self, node):
		self.write(node)

	def put(self, node):
		#Enable and connect to the node identified by <node>. The gateway will try to use the connection 
		#interval <interval> and the connection latency <latency>. If left out, default values will be used. 
		#The gateway will try to reconnect to the device if the connection is lost or at gateway power-up.

		#Remove the node <node> from the list of enabled nodes.
		connect = self.get_argument('connect', '0')
		interval = self.get_argument('interval', '0')
		latency = self.get_argument('latency', '0')
		enable = self.get_argument('enable', '0')
		name = self.get_argument('enable', '')


		if connect == '1':
			if enable == '1':
				self.write( 'Enable and connect to the node identified by <node> <br> ')
				self.write( 'latency ' + latency)
				self.write( 'interval ' + interval)
			else :
				self.write( 'Remove the node <node> from the list of enabled nodes. <br> ')
		elif name != '':
			self.write('Perform a name discovery of the node identified by handle <node>.')

class DiscoverServicesWithNode(tornado.web.RequestHandler):
	def initialize(self):
		# The gateway will return data for an enabled node identified by the handle <node>.
		self.write( 'DiscoverServicesWithNode ')

	def get(self, node):
		self.write(node)
		primary = self.get_argument('primary', '0')

'''
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
'''

application = tornado.web.Application(
[
	# Nodes (discover nodes and list enabled nodes)
	(r"/gap/nodes", StartScanAndListEnablingDiscover),
	(r"/gap/nodes/(.*)", DataWithEnabledNode),
	(r"/gatt/nodes/(.*)/services?primary=1", DiscoverServicesWithNode),
	(r"/gatt/nodes/<node>/services?primary=1&uuid=<uuid>", GetDiscoveyPrimaryServicesByUUID),
	(r"/gatt/nodes/<node>/services", GetFindIncludedServices),
	(r"/gatt/nodes/<node>/services/<service>/characterist,ics", GetDiscoverAllCharacteristicsOfService),

	(r"/", MainHandler)
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
