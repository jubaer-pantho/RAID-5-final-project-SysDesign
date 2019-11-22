import xmlrpclib, config, pickle
#10.0.2.15

# pass all parameters using pickle.dumps(parameter)
# get all return values using pickle.loads(return value)

#proxy = xmlrpclib.ServerProxy("http://localhost:8000/")

class client_stub():

	def __init__(self):

		
		self.proxy = xmlrpclib.ServerProxy("http://localhost:8000/")
		print('---------------------------------------')
		print('attempting to connect to server')
		print('---------------------------------------')


	def Initialize(self):
		try :
			self.proxy.Initialize()
		except Exception as err :
			print('connection error, failed to initialize file system, exiting')
			quit()

	def addr_inode_table(self):
		try :
			return self.proxy.addr_inode_table()
		except Exception as err :
			print('connection error')
			return -1

	def get_data_block(self, block_number):
		try :
			retVal =  self.proxy.get_data_block(pickle.dumps(block_number))
		except Exception as err :
			print('connection error')
			return -1
			
		retVal, state =  pickle.loads(retVal)
		return retVal

	def get_valid_data_block(self):
		try :
			retVal = self.proxy.get_valid_data_block()
		except Exception as err :
			print('connection error')
			return -1
		retVal, state = pickle.loads(retVal)
		return retVal

	def free_data_block(self, block_number):
		try :
			retVal =  self.proxy.free_data_block(pickle.dumps(block_number))
		except Exception as err :
			print('connection error')
			return -1
		retVal, state =  pickle.loads(retVal)
		return retVal

	def update_data_block(self, block_number, block_data):
		try :
			retVal =  self.proxy.update_data_block(pickle.dumps(block_number), pickle.dumps(block_data))
		except Exception as err :
			print('connection error')
			return -1
		retVal, state =  pickle.loads(retVal)
		return retVal

	def update_inode_table(self, inode, inode_number):
		try :
			retVal =  self.proxy.update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number))
		except Exception as err :
			print('connection error')
			return -1
		retVal, state =  pickle.loads(retVal)
		return retVal

	def inode_number_to_inode(self, inode_number):
		try :
			retVal = self.proxy.inode_number_to_inode(pickle.dumps(inode_number))
		except Exception as err :
			print('connection error')
			return -1
		retVal, state = pickle.loads(retVal)
		return retVal

	def status(self):
		try :
			retVal = self.proxy.status()
		except Exception as err :
			print('connection error')
			return -1
		retVal, state = pickle.loads(retVal)
		return retVal



#print "3 is even: %s" % str(proxy.is_even(3))
#print "100 is even: %s" % str(proxy.is_even(100))
