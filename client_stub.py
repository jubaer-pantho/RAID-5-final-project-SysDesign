# SKELETON CODE FOR CLIENT STUB HW4
import xmlrpclib, config, pickle, time, hashlib

portNumber = 8000

class client_stub():
    server_number = 0
    def __init__(self):
	self.virtual_block_numbers = [False]*config.TOTAL_NO_OF_BLOCKS
	self.physical_block_numbers = [-1]*config.TOTAL_NO_OF_BLOCKS
	self.physical_parity_block_numbers = [-1]*config.TOTAL_NO_OF_BLOCKS
	self.faulty_server = -1
	self.servers = []

    # example provided for initialize
    def Initialize(self, no_of_servers):
        self.server_number = no_of_servers

        for i in range(self.server_number):
            self.servers.append(xmlrpclib.ServerProxy("http://localhost:"+ str(portNumber + i) +"/"))


        for (index,server) in enumerate(self.servers):
    		try :
    			server.Initialize()
    			print('Server initialized' ,server)
    		except Exception as err :
    			print('Error Initializing ' ,server)

    			if(self.faulty_server == -1):
    				self.faulty_server = index
    			else:
    				print('More then one server down!!')
    				quit()



    def inode_number_to_inode(self, inode_number):

    	inode_number = pickle.dumps(inode_number)

    	for (index,server) in enumerate(self.servers):
    		try:
    			retVal =  server.inode_number_to_inode(inode_number)
    			retVal = pickle.loads(retVal)
    			return retVal[0]

    		except Exception as err :
    			self.faulty_server = index



    def get_data_block(self, block_number, parity_server = 0):

    	server, parityserver = self.block_number_translate(block_number)

    	if(parity_server == 0):
    		phy_blocknumer = self.physical_block_numbers[block_number]

    	else:
    		phy_blocknumer = self.physical_parity_block_numbers[block_number/3]
    		server = parityserver

    	if(server != self.faulty_server):

    		try:

    			phy_blocknumer = pickle.dumps(phy_blocknumer)
    			retVal =  self.servers[server].get_data_block(phy_blocknumer)

    			retVal = pickle.loads(retVal)[0]
    			read_hash = retVal[-16::]

    			read_hash = ''.join(read_hash)
    			hash = hashlib.md5()
    			retVal = retVal[0:config.BLOCK_SIZE]
    			retVal = ''.join(retVal)
    			hash.update(retVal) #compute hash with extracted data

    			if(read_hash  == hash.digest()):
    				print('CHECKSUM OK')
    				return retVal
    			else:

    				time.sleep(5)
    				self.faulty_server = server
    				return self.get_data_block(block_number, parity_server)

    		except Exception as err :

    			if(self.faulty_server == -1):
    				self.faulty_server = server
    				return self.get_data_block(block_number, parity_server)
    			else:
    				print('more then one server down or corrupted')
    				quit()

    	else: # if server from whom we want to read is down or data is currupted
            print('Server '+ str(self.faulty_server) + ' is down or corrupted, data is reconstructed by reading from other servers')
            datareconstructed = (config.BLOCK_SIZE+16)*'\0'
            old_parity =  (config.BLOCK_SIZE+16)*'\0'
            blocklist = range(3)

            for i in blocklist:
                blocklist[i] += (block_number/3)*3

            blocklist = [x for i, x in enumerate(blocklist) if x != block_number]

            dataotherservers = []

            for blocknum in blocklist:
                if(self.physical_block_numbers[blocknum] != -1): #check if exits
                    dataotherservers.append(self.get_data_block(blocknum,0))
            if(len(dataotherservers) == 2):
                datareconstructed = ''.join(chr(ord(a)^ord(b)) for a, b in zip(dataotherservers[0],dataotherservers[1]))
            elif(len(dataotherservers) == 1):
                datareconstructed = dataotherservers[0]


            if(self.physical_parity_block_numbers[block_number/3] == -1): #check if exits
                phy_paritynumer = self.get_valid_data_block(parityserver)
                phy_paritynumer = phy_paritynumer[0]
                self.physical_parity_block_numbers[block_number/3] = phy_paritynumer

            else:
                phy_paritynumer = self.physical_parity_block_numbers[block_number/3]
                old_parity = self.get_data_block(block_number,1)

            datareconstructed = ''.join(chr(ord(a)^ord(b)) for a, b in zip(datareconstructed,old_parity))


            return datareconstructed

    def get_valid_data_block(self,server):
    	try:
    		retVal =  self.servers[server].get_valid_data_block()
    		return pickle.loads(retVal)

    	except Exception as err :
    		print('Error get_valid_data_block')
    		quit()

    def free_data_block(self, block_number):

    	server = self.block_number_translate(block_number)[0]

    	phy_blocknumer = self.physical_block_numbers[block_number]
    	phy_blocknumer = pickle.dumps(phy_blocknumer)
        self.update_parity(block_number)
        try:
        	if(server != self.faulty_server):
        		self.servers[server].free_data_block(phy_blocknumer)
        	self.physical_block_numbers[block_number] = -1
        	self.virtual_block_numbers[block_number] = False
        except Exception as err:
        	print('Error free_data_block')
        	quit()


    def __calculate_block_hash(self, block_data):

        hash = hashlib.md5()
        hash.update(block_data)
        block_data += hash.digest()

        return block_data



    def update_data_block(self, block_number, block_data, delay):

        server, parityserver = self.block_number_translate(block_number)
        old_data = (config.BLOCK_SIZE+16)*'\0'
        datareconstructed = (config.BLOCK_SIZE+16)*'\0'
        old_parity =  (config.BLOCK_SIZE+16)*'\0'

        if(self.faulty_server == -1 or (self.faulty_server != server and self.faulty_server != parityserver)): #doesnt affect our write


            if(self.physical_block_numbers[block_number] == -1): #check if exits

                phy_blocknumer = self.get_valid_data_block(server)
                phy_blocknumer = phy_blocknumer[0]
                self.physical_block_numbers[block_number] = phy_blocknumer

            else:
                phy_blocknumer = self.physical_block_numbers[block_number]
                old_data = self.get_data_block(block_number,0)



            if(self.physical_parity_block_numbers[block_number/3] == -1): #check if exits
                phy_paritynumer = self.get_valid_data_block(parityserver)
                phy_paritynumer = phy_paritynumer[0]
                self.physical_parity_block_numbers[block_number/3] = phy_paritynumer
            else:
                phy_paritynumer = self.physical_parity_block_numbers[block_number/3]
                old_parity = self.get_data_block(block_number,1)


            #calculate_parity_block((old_data xor block_data) xor old_parity)
            parity_data = ''.join(chr(ord(a)^ord(b)) for a, b in zip(old_data, block_data))
            parity_data = ''.join(chr(ord(a)^ord(b)) for a, b in zip(old_parity,parity_data))

            try:
                block_data = self.__calculate_block_hash(block_data)
                parity_data = self.__calculate_block_hash(parity_data)


                phy_blocknumer = pickle.dumps(phy_blocknumer)
                block_data = pickle.dumps(block_data)
                parity_data = pickle.dumps(parity_data)
                phy_paritynumer = pickle.dumps(phy_paritynumer)

                self.servers[server].update_data_block(phy_blocknumer, block_data)
                print('Waiting to write parity on server ' + str(parityserver))
                time.sleep(delay)

                self.servers[parityserver].update_data_block(phy_paritynumer, parity_data )

            except Exception as err:
                print('Error update_data_block')
                print(err)

        elif(self.faulty_server == parityserver): #parity server down

            if(self.physical_block_numbers[block_number] == -1): #check if exits

                phy_blocknumer = self.get_valid_data_block(server)
                phy_blocknumer = phy_blocknumer[0]
                self.physical_block_numbers[block_number] = phy_blocknumer

            else:
                phy_blocknumer = self.physical_block_numbers[block_number]


            try:
                block_data = self.__calculate_block_hash(block_data)

                phy_blocknumer = pickle.dumps(phy_blocknumer)
                block_data = pickle.dumps(block_data)


                self.servers[server].update_data_block(phy_blocknumer, block_data)
                print('No parity is written since parityserver ' + str(parityserver) + ' is down')
                time.sleep(delay)

            except Exception as err:
                print('Error update_data_block')
                print(err)
        else: #if the server who we want to write is down

            print('Server '+ str(self.faulty_server) + ' is down, parity is updated reading from the other servers')

            blocklist = range(3)
            for i in blocklist:
                blocklist[i] += (block_number/3)*3

            blocklist = [x for i, x in enumerate(blocklist) if x != block_number]

            dataotherservers = []

            for blocknum in blocklist:
                if(self.physical_block_numbers[blocknum] != -1): #check if exits
                    dataotherservers.append(self.get_data_block(blocknum,0))

            if(len(dataotherservers) == 2):
                datareconstructed = ''.join(chr(ord(a)^ord(b)) for a, b in zip(dataotherservers[0],dataotherservers[1]))
            elif(len(dataotherservers) == 1):
                datareconstructed = dataotherservers[0]


            if(self.physical_parity_block_numbers[block_number/3] == -1): #check if exits
                phy_paritynumer = self.get_valid_data_block(parityserver)
                phy_paritynumer = phy_paritynumer[0]
                self.physical_parity_block_numbers[block_number/3] = phy_paritynumer
            else:
                phy_paritynumer = self.physical_parity_block_numbers[block_number/3]
                old_parity = self.get_data_block(block_number,1)

            datareconstructed = ''.join(chr(ord(a)^ord(b)) for a, b in zip(datareconstructed,old_parity))

            parity_data = ''.join(chr(ord(a)^ord(b)) for a, b in zip(datareconstructed,block_data))
            parity_data = ''.join(chr(ord(a)^ord(b)) for a, b in zip(old_parity,parity_data))

            try:
                parity_data = self.__calculate_block_hash(parity_data)

                parity_data = pickle.dumps(parity_data)
                phy_paritynumer = pickle.dumps(phy_paritynumer)

                print('Waiting to write parity on server ' + str(parityserver))
                time.sleep(delay)
                self.servers[parityserver].update_data_block(phy_paritynumer, parity_data)

            except Exception as err:
                print('Error update_data_block')
                print(err)

    def update_inode_table(self, inode, inode_number):
    	inode = pickle.dumps(inode)
    	inode_number = pickle.dumps(inode_number)

    	for (index,server) in enumerate(self.servers):
    		try:

    			server.update_inode_table(inode, inode_number)

    		except Exception as err:
    			self.faulty_server = index
    def status(self):
    	retvalarr = ""
    	for i in range(0, self.server_number):

    		try:
    			retVal =  self.servers[i].status()
    			retVal = pickle.loads(retVal)
    			retvalarr += '\n\n-----  Server%d  ---------\n\n'%i + retVal[0]

    		except Exception as err :
    			continue

    	return retvalarr
    ''' WRITE CODE HERE '''

    def get_new_virtual_block(self):

    	for i in range(0,config.TOTAL_NO_OF_BLOCKS):
    		if(self.virtual_block_numbers[i] == False):
    			self.virtual_block_numbers[i] = True
    			return i
    	print("Memory: No valid virtual blocks available")
    	return -1

    def block_number_translate(self, virtual_block_number):

    	packof3index = virtual_block_number/3
    	vnumbers = virtual_block_number%3
    	parity_server = 3 - (packof3index%4)

    	if(packof3index % 4 == 0):
    		server = vnumbers
    	elif(packof3index % 4 == 1):
    		server = vnumbers + vnumbers/2
    	elif(packof3index % 4 == 2):
    		server = 2*vnumbers - vnumbers/2
    	else:
    		server = vnumbers + 1
    	return server,parity_server

    def update_parity(self, block_number):

    	server, parityserver = self.block_number_translate(block_number)
    	old_data =  (config.BLOCK_SIZE+16)*'\0'
    	old_parity =  (config.BLOCK_SIZE+16)*'\0'

    	old_data = self.get_data_block(block_number, 0)
    	old_parity = self.get_data_block(block_number, 1)
    	parity_data = ''.join(chr(ord(a)^ord(b)) for a, b in zip(old_data,old_parity))


    	try:

    		hash = hashlib.md5()
    		hash.update(parity_data)
    		phy_paritynumer = self.physical_parity_block_numbers[block_number/3]

    		if(parity_data.count('\0') != config.BLOCK_SIZE):
    			parity_data += hash.digest()
    			parity_data = pickle.dumps(parity_data)
    			phy_paritynumer = pickle.dumps(phy_paritynumer)
    			self.servers[parityserver].update_data_block(phy_paritynumer, parity_data )
    		else:
    			phy_paritynumer = pickle.dumps(phy_paritynumer)
    			self.servers[parityserver].free_data_block(phy_paritynumer)


    	except Exception as err:
    		print('Error update_data_block')
    		print(err)
