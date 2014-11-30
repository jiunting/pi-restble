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
		# /gap/nodes/<node> GetEnabledNodeWithIdentified
		# /gap/nodes/<node>?name=1    GetNameDiscoveryIdentifiedNode
		self.write(node)
		name = self.get_argument('name', '')
		if name != '':
			self.write('Perform a name discovery of the node identified by handle <node>.')

	def put(self, node):
		#Enable and connect to the node identified by <node>. The gateway will try to use the connection 
		#interval <interval> and the connection latency <latency>. If left out, default values will be used. 
		#The gateway will try to reconnect to the device if the connection is lost or at gateway power-up.
		# /gap/nodes/<node>?connect=1(&interval=<interval>&latency=<latency>&enable=1)  PutConnectingTheIdentifiedNode
		
		# Remove the node <node> from the list of enabled nodes.
		# /gap/nodes/<node>?enable=0   PutDisconnectingTheIdentifiedNode
		connect = self.get_argument('connect', '0')
		interval = self.get_argument('interval', '0')
		latency = self.get_argument('latency', '0')
		enable = self.get_argument('enable', '0')
		if connect == '1':
			if enable == '1':
				self.write( 'Enable and connect to the node identified by <node> <br> ')
				self.write( 'latency ' + latency)
				self.write( 'interval ' + interval)
			else :
				self.write( 'Remove the node <node> from the list of enabled nodes. <br> ')
		
class ListAvailableNodes(tornado.web.RequestHandler):
	def initialize(self):
		# Available nodes
		self.write( 'ListAvailableNodes ')

	def get(self):
		# /gatt/nodes
		self.write( 'Available Nodes ')

class DataReadWithSpecificNode(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'DataReadWithSpecificNode ')

	def get(self, node):
		# Read data for a specific node identified by the handle <node>,
		# /gatt/nodes/<node>
		self.write( node)

class DiscoverServicesWithNode(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'DiscoverServicesWithNode ')

	def get(self, node):
		# TODO:
		# Discover all services in the node identified by <node>.
		#/gatt/nodes/<node>/services"  GetFindIncludedServices

		# Discover all primary services in the node identified by <node>
		# /gatt/nodes/<node>/services?primary=1"  GetDiscoveyAllPrimaryServices
		
		# Discover primary services by UUID in the node identified by <node>
		#/gatt/nodes/<node>/services?primary=1&uuid=<uuid>  GetDiscoveyPrimaryServicesByUUID
		
		self.write(node)
		primary = self.get_argument('primary', '0')
		uuid = self.get_argument('uuid', '0')

class DiscoverServicesWithNodeRead(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'DiscoverServicesWithNodeRead ')

	def get(self, node, service):
		# Read data for a service in the node <node> identified by the handle <service> (discovered by 
		# one of the methods/URIs defined earlier in this section).
		# /gatt/nodes/<node>/services/<service>
		self.write(node)
		self.write(service)

class CharacteristicDescriptorDiscoveryWithNode(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicDescriptorDiscoveryWithNode ')

	def get(self, node, service):
		# TODO:
		# Discover all characteristics of the service <service> in the node identified by <node>
		# /gatt/nodes/<node>/services/<service>/characteristics  GetDiscoverAllCharacteristicsOfService
		self.write(node)
		self.write(service)

class DiscoverCharacteristicbyUUID(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'DiscoverCharacteristicbyUUID ')

	def get(self, node):
		# Discover characteristics by UUID in the node identified by <node>.
		# /gatt/nodes/<node>/characteristics?uuid=<uuid>"   GetDiscoverCharacteristicbyUUID
		self.write(node)
		uuid = self.get_argument('uuid', '0')

class DiscoverAllCharacteristicDescriptors(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'DiscoverAllCharacteristicDescriptors ')

	def get(self, node, characteristic):
		# Get data for the characteristic identified by <characteristics> in the node identified <node> 
		# (discovered by one of the methods/URIs defined earlier in this section). 
		# /gatt/nodes/<node>/characteristics/<characteristic>/descriptors  GetDiscoverAllCharacteristicDescriptors
		self.write(node)
		self.write(characteristic)

class ReadCharacteristicValue(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'ReadCharacteristicValue ')

	def get(self, node, characteristic):
		# Characteristic Value Read	
		#/gatt/nodes/<node>/characteristics/<characteristic>/value    GetReadCharacteristicValue),
		#/gatt/nodes/<node>/characteristics/<characteristic>/value?uuid=<uuid>&start=<handle>&end=<handle>   GetReadUsingCharacteristicUUID
		#/gatt/nodes/<node>/characteristics/<characteristic>/value?long=1   GetReadLongCharacteristicsValue
		self.write(node)
		self.write(characteristic)
		uuid = self.get_argument('uuid', '0')
		start_handle =  self.get_argument('start', '0')
		end_handle =  self.get_argument('end', '0')
		long_id = self.get_argument('long', '0')

class ReadMultipleCharacteristicsValue(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'ReadMultipleCharacteristicsValue ')

	def get(self, node):
		# Characteristic Value Read	
		# /gatt/nodes/<node>/characteristics/value?multiple=1 GetReadMultipleCharacteristicsValue
		multiple =  self.get_argument('multiple', '0')

class CharacteristicValueWrite(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicValueWrite ')

	def put(self, node, characteristic, value):
		# Characteristic Value Read	
		# /gatt/nodes/<node>/characteristics/<characteristic>/value/<value>?noresponse=1 	PutWriteWithoutResponse
		# /gatt/nodes/<node>/characteristics/<characteristic>/value/<value> 				PutWriteCharacteristicValue
		# /gatt/nodes/<node>/characteristics/<characteristic>/value/<value>?long=1       PutWriteLongCharacteristicValue
		noresponse =  self.get_argument('noresponse', '0')
		long_id = self.get_argument('long', '0')

class CharacteristicValueReliableWrite(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicValueReliableWrite ')

	def put(self, node):
		# /gatt/nodes/<node>/characteristics/value?reliable=1 PutCharacteristicValueReliableWrite
		reliable = self.get_argument('reliable', '0')

class CharacteristicEnablingNotification(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicEnablingNotification ')

	def put(self, node):
		# /gatt/nodes/<node>/characteristics?notify=1", PutNotification
		notify = self.get_argument('notify', '0')

class CharacteristicValueNotification(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicValueNotification ')

	def get(self, node, characteristic):
		# /gatt/nodes/<node>/characteristics/<characteristic>/value?notify=1    CharacteristicValueNotification
		# /gatt/nodes/<node>/characteristics/<characteristic>/value?notify=1&event=1  CharacteristicValueNotification
		notify = self.get_argument('notify', '0')
		event = self.get_argument('event', '0')

class CharacteristicEnablingIndication(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicEnablingIndication ')

	def put(self, node):
		# /gatt/nodes/<node>/characteristics?indicate=1  PutIndication
		indicate = self.get_argument('indicate', '0')

class CharacteristicValueIndication(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicValueIndication ')

	def get(self, node, characteristic):
		# /gatt/nodes/<node>/characteristics/<characteristic>/value?indicate=1  	GetIndication
		# /gatt/nodes/<node>/characteristics/<characteristic>/value?indicate=1&event=1 EventSourceIndication
		indicate = self.get_argument('indicate', '0')
		event = self.get_argument('event', '0')

class CharacteristicDescriptorValueRead(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicDescriptorValueRead ')

	def get(self, node, descriptor):
		# /gatt/nodes/<node>/descriptor/<descriptor>/value  CharacteristicDescriptorValueRead
		# /gatt/nodes/<node>/descriptor/<descriptor>value?long=1  GetReadLongCharacteristicDescriptors
		long_id = self.get_argument('long', '0')

class CharacteristicDescriptorValueWrite(tornado.web.RequestHandler):
	def initialize(self):
		self.write( 'CharacteristicDescriptorValueWrite ')

	def get(self, node, descriptor, value):
		# /gatt/nodes/<node>/descriptor/<descriptor>value?long=1  GetWriteLongCharacteristicDescriptors
		long_id = self.get_argument('long', '0') 
	def put(self, node, descriptor, value):
		# /gatt/nodes/<node>/descriptor/<descriptor>/value  PutWriteCharacteristicDescriptor
		self.write( descriptor)


'''
	TODO:
	(r"/notdefined",SignedWriteWithoutResponse),
'''
application = tornado.web.Application(
[
	# Nodes (discover nodes and list enabled nodes)
	(r"/gap/nodes", StartScanAndListEnablingDiscover),
	(r"/gap/nodes/(.*)", DataWithEnabledNode),
	(r"/gatt/nodes", ListAvailableNodes),
	(r"/gatt/nodes/(.*)", DataReadWithSpecificNode),
	(r"/gatt/nodes/(.*)/services", DiscoverServicesWithNode),
	(r"/gatt/nodes/(.*)/services/(.*)", DiscoverServicesWithNodeRead),
	(r"/gatt/nodes/(.*)/services/(.*)/characteristics", CharacteristicDescriptorDiscoveryWithNode),
	(r"/gatt/nodes/(.*)/characteristics", DiscoverCharacteristicbyUUID),
	(r"/gatt/nodes/(.*)/characteristics/(.*)/descriptors", DiscoverAllCharacteristicDescriptors),
	(r"/gatt/nodes/(.*)/characteristics/(.*)/value", ReadCharacteristicValue),
	(r"/gatt/nodes/(.*)/characteristics/value", ReadMultipleCharacteristicsValue),
	(r"/gatt/nodes/(.*)/characteristics/(.*)/value/(.*)", CharacteristicValueWrite),
	(r"/gatt/nodes/(.*)/characteristics/value", CharacteristicValueReliableWrite),
	(r"/gatt/nodes/(.*)/characteristics", CharacteristicEnablingNotification),
	(r"/gatt/nodes/(.*)/characteristics/(.*)/value",CharacteristicValueNotification),
	(r"/gatt/nodes/(.*)/characteristics", CharacteristicEnablingIndication),
	(r"/gatt/nodes/(.*)/characteristics/(.*)/value",CharacteristicValueIndication),
	(r"/gatt/nodes/(.*)/descriptor/(.*)/value", CharacteristicDescriptorValueRead),
	(r"/gatt/nodes/(.*)/descriptor/(.*)/value/(.*)", CharacteristicDescriptorValueWrite),
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
