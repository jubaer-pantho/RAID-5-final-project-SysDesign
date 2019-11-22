import xmlrpclib, config, pickle
#10.0.2.15

# pass all parameters using pickle.dumps(parameter)
# get all return values using pickle.loads(return value)

#proxy[0] = xmlrpclib.Serverproxy[0]("http://localhost:8000/")

portNumber = 8000
serverNumber = 2


class client_stub():
    proxy = []

    def __init__(self):

        for i in range(serverNumber):
            tmp =  xmlrpclib.ServerProxy("http://localhost:"+ str(portNumber + i) +"/")
            self.proxy.append(tmp)
        print('---------------------------------------')
        print('attempting to connect to server')
        print('---------------------------------------')


    def Initialize(self):
        try :
            self.proxy[0].Initialize()
        except Exception as err :
            print('connection error, failed to initialize file system, exiting')
            quit()

    def addr_inode_table(self):
        try :
            return self.proxy[0].addr_inode_table()
        except Exception as err :
            print('connection error')
            return -1

    def get_data_block(self, block_number):
        try :
            retVal =  self.proxy[0].get_data_block(pickle.dumps(block_number))
        except Exception as err :
            print('connection error')
            return -1
            
        retVal, state =  pickle.loads(retVal)
        return retVal

    def get_valid_data_block(self):
        try :
            retVal = self.proxy[0].get_valid_data_block()
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        return retVal

    def free_data_block(self, block_number):
        try :
            retVal =  self.proxy[0].free_data_block(pickle.dumps(block_number))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def update_data_block(self, block_number, block_data):
        try :
            retVal =  self.proxy[0].update_data_block(pickle.dumps(block_number), pickle.dumps(block_data))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def update_inode_table(self, inode, inode_number):
        try :
            retVal =  self.proxy[0].update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def inode_number_to_inode(self, inode_number):
        try :
            retVal = self.proxy[0].inode_number_to_inode(pickle.dumps(inode_number))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        return retVal

    def status(self):
        try :
            retVal = self.proxy[0].status()
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        return retVal



#print "3 is even: %s" % str(proxy[0].is_even(3))
#print "100 is even: %s" % str(proxy[0].is_even(100))
