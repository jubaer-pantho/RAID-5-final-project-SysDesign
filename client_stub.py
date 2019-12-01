import xmlrpclib, config, pickle
#10.0.2.15

# pass all parameters using pickle.dumps(parameter)
# get all return values using pickle.loads(return value)

#raid_server[0] = xmlrpclib.Serverraid_server[0]("http://localhost:8000/")

portNumber = 8000
server_number = 4


class client_stub():
    raid_server = []
    next_server = 0
    virt_block_list = [0] * 1000 #config.TOTAL_NO_OF_BLOCKS
    virt_index = 0
    virtual_array = dict()


    def __init__(self):

        for i in range(server_number):
            tmp =  xmlrpclib.ServerProxy("http://localhost:"+ str(portNumber + i) +"/")
            self.raid_server.append(tmp)
        print('---------------------------------------')
        print('attempting to connect to server')
        print('---------------------------------------')


    def Initialize(self):
        try :
            for i in range(server_number):
                self.raid_server[i].Initialize()
        except Exception as err :
            print('connection error, failed to initialize file system, exiting')
            quit()

    def addr_inode_table(self): 
        try :
            return self.raid_server[0].addr_inode_table()
        except Exception as err :
            print('connection error')
            return -1

    def get_data_block(self, block_number):
        svnumber, localBlockNum =  self.__block_number_translate(block_number)
        try :
            retVal =  self.raid_server[svnumber].get_data_block(pickle.dumps(localBlockNum))
        except Exception as err :
            print('connection error')
            return -1

        retVal, state =  pickle.loads(retVal)
        return retVal


    def __get_parity_block_number(self, virtual_block_number):
        
        self.virt_block_list[self.next_server] = virtual_block_number       

        parity_server = 3 - (int(self.next_server / 4) % 4)


        flag = 0
        if (self.next_server != 0):
            prev_virt_block_num = self.virt_block_list[self.next_server -1]
            if (prev_virt_block_num == 0):
                prev_virt_block_num = self.virt_block_list[self.next_server -2]

            prev_parity_server = self.virtual_array[prev_virt_block_num] % 100

            if (prev_parity_server == parity_server):
                self.virtual_array[virtual_block_number] = self.virtual_array[prev_virt_block_num]
                flag = 1

        if (flag == 0):
            try :
                retVal = self.raid_server[parity_server].get_valid_data_block()
                print("Received new parity block from server : ", parity_server)
            except Exception as err :
                print('parity data block error')
                return -1
            retVal, state = pickle.loads(retVal)
            par_virt_block = retVal * 100 + parity_server
            self.virtual_array[virtual_block_number] = par_virt_block

            #testData= self.get_data_block(par_virt_block)
            #if (testData[0] == '\x00'):
            #    print("first element of new data block", testData[0])
        return 1
        




    def __block_number_translate(self, virtual_block_number) :
        '''WRITE CODE HERE'''
        serverNum = int(virtual_block_number % 100)
        localBlockNum = int(virtual_block_number / 100)
        return serverNum, localBlockNum

    def __get_virtual_data_block(self, block_number, server_id) :
        virtual_block_number = block_number * 100 + server_id
        retVal = self.__get_parity_block_number(virtual_block_number)
        
        return virtual_block_number

    def get_valid_data_block(self):
        if (self.next_server % 3 == 0 and self.next_server > 0):
            self.next_server = self.next_server + 1
        try :
            retVal = self.raid_server[(self.next_server % server_number)].get_valid_data_block()
            print("Received block from server : ", (self.next_server % server_number))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        retVal = self.__get_virtual_data_block(retVal, (self.next_server % server_number))

        self.next_server = self.next_server + 1
        return retVal

    def free_data_block(self, block_number):
        try :
            svnumber, localBlockNum =  self.__block_number_translate(block_number)
            retVal =  self.raid_server[svnumber].free_data_block(pickle.dumps(localBlockNum))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def __calculate_parity_block(self, new_data, old_data, parity_data):
        '''Write your code to calculate parity'''
        new_parity = parity_data
        return new_parity

    def __update_parity_block(self, blocknumber, parity_server , block_data):
        '''Write your code here'''
        try :
            retVal =  self.raid_server[parity_server].update_data_block(pickle.dumps(blocknumber), pickle.dumps(block_data))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)

    def update_data_block(self, block_number, block_data):
        svnumber, localBlockNum =  self.__block_number_translate(block_number)
        parityBlockNum = self.virtual_array[block_number] / 100
        parityServer = self.virtual_array[block_number] % 100

        # fetching parity block
        try :
            parityBlockData =  self.raid_server[parityServer].get_data_block(pickle.dumps(parityBlockNum))
            print("Update : Received parity block from server : ", parityServer)
        except Exception as err :
            print('connection error')
            return -1

        parityBlockData, stateParity =  pickle.loads(parityBlockData)

        # fetching old data block
        try :
            oldBlockData =  self.raid_server[svnumber].get_data_block(pickle.dumps(localBlockNum))
            print("Received old block from server : ", svnumber)
        except Exception as err :
            print('connection error')
            return -1

        oldBlockData, stateOld =  pickle.loads(oldBlockData)

        new_parity_data = self.__calculate_parity_block(block_data, oldBlockData, parityBlockData)
        self.__update_parity_block(parityBlockNum, parityServer, new_parity_data)

        try :
            retVal =  self.raid_server[svnumber].update_data_block(pickle.dumps(localBlockNum), pickle.dumps(block_data))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def update_inode_table(self, inode, inode_number):
        try :
            for i in range(server_number):
                retVal =  self.raid_server[i].update_inode_table(pickle.dumps(inode), pickle.dumps(inode_number))
        except Exception as err :
            print('connection error')
            return -1
        retVal, state =  pickle.loads(retVal)
        return retVal

    def inode_number_to_inode(self, inode_number):

        for i in range(server_number):
            try :
                retVal = self.raid_server[i].inode_number_to_inode(pickle.dumps(inode_number))
                break
            except Exception as err :
                print('server down')
                return -1
        retVal, state = pickle.loads(retVal)
        return retVal

    def status(self):
        try :
            retVal = self.raid_server[0].status()
        except Exception as err :
            print('connection error')
            return -1
        retVal, state = pickle.loads(retVal)
        return retVal



#print "3 is even: %s" % str(raid_server[0].is_even(3))
#print "100 is even: %s" % str(raid_server[0].is_even(100))
