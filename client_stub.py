import xmlrpclib, config, pickle
#10.0.2.15

# pass all parameters using pickle.dumps(parameter)
# get all return values using pickle.loads(return value)

#proxy[0] = xmlrpclib.Serverproxy[0]("http://localhost:8000/")

portNumber = 8000
server_number = 2


class client_stub():
    proxy = []
    next_server = 0


    def __init__(self):

        for i in range(server_number):
            tmp =  xmlrpclib.ServerProxy("http://localhost:"+ str(portNumber + i) +"/")
            self.proxy.append(tmp)
        print('---------------------------------------')
        print('attempting to connect to server')
        print('---------------------------------------')


    def Initialize(self):
        try :
            for i in range(server_number):
                self.proxy[i].Initialize()
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
        svnumber, localBlockNum =  self.__block_number_translate(block_number)
        try :
            retVal =  self.proxy[svnumber].get_data_block(pickle.dumps(localBlockNum))
        except Exception as err :
            print('connection error')
            return -1

        retVal, state =  pickle.loads(retVal)
        return retVal

    def __block_number_translate(self, virtual_block_number) :
        '''WRITE CODE HERE'''
        serverNum = 0
        localBlockNum = virtual_block_number
        return serverNum, localBlockNum

    def __get_virtual_data_block(self, block_number, server_id) :
        virtual_block_number = block_number
        return virtual_block_number

    def get_valid_data_block(self):
        try :
            retVal = self.proxy[self.next_server].get_valid_data_block()
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        retVal = self.__get_virtual_data_block(retVal, self.next_server)

        self.next_server = (self.next_server + 1) % server_number
        return retVal

    def free_data_block(self, block_number):
        try :
            svnumber, localBlockNum =  self.__block_number_translate(block_number)
            retVal =  self.proxy[svnumber].free_data_block(pickle.dumps(localBlockNum))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def update_data_block(self, block_number, block_data):
        svnumber, localBlockNum =  self.__block_number_translate(block_number)
        try :
            retVal =  self.proxy[svnumber].update_data_block(pickle.dumps(localBlockNum), pickle.dumps(block_data))
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
