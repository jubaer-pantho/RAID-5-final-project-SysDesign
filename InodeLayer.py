'''
THIS MODULE IS INODE LAYER OF THE FILE SYSTEM. IT INCLUDES THE INODE DEFINITION DECLARATION AND GLOBAL HANDLE OF BLOCK LAYER OF API.
THIS MODULE IS RESPONSIBLE FOR PROVIDING ACTUAL BLOCK NUMBERS SAVED IN INODE ARRAY OF BLOCK NUMBERS TO FETCH DATA FROM BLOCK LAYER.
'''
import datetime, config, BlockLayer, InodeOps, hashlib, time

#HANDLE OF BLOCK LAYER
interface = BlockLayer.BlockLayer()

class InodeLayer():

    #RETURNS BLOCK NUMBER FROM RESPECTIVE INODE DIRECTORY
    def INDEX_TO_BLOCK_NUMBER(self, inode, index):
        if index == len(inode.blk_numbers): return -1
        return inode.blk_numbers[index]


    #RETURNS BLOCK DATA FROM INODE
    def INODE_TO_BLOCK(self, inode, offset):
        index = offset / config.BLOCK_SIZE
        block_number = self.INDEX_TO_BLOCK_NUMBER(inode, index)
        if block_number == -1: return ''
        else: return interface.BLOCK_NUMBER_TO_DATA_BLOCK(block_number)


    #MAKES NEW INODE OBJECT
    def new_inode(self, type):
        return InodeOps.Table_Inode(type)


    #FLUSHES ALL THE BLOCKS OF INODES FROM GIVEN INDEX OF MAPPING ARRAY
    def free_data_block(self, inode, index):
        for i in range(index, len(inode.blk_numbers)):
            if(inode.blk_numbers[i] != -1):
                interface.free_data_block(inode.blk_numbers[i])
                inode.blk_numbers[i] = -1


#IMPLEMENTS WRITE FUNCTIONALITY
    def write(self, inode, offset, data, delay):


        inode.time_accessed = str(datetime.datetime.now())     #update access time
        lenght_hash = 16
        dataarray = []
        start_block = offset/config.BLOCK_SIZE	 #block where to start
        len_old_data = offset % config.BLOCK_SIZE  #determin where in a block the data is going to start
        len_new_data = config.BLOCK_SIZE - len_old_data   #length of old data in block
        data_old = ""
        file_size = 0
        #------------ERROR management------------------------------------------------

        if(inode.type != 0):   #check if Inode is of type file
          return -1



        max_file_size = len(inode.blk_numbers)*config.BLOCK_SIZE	#calculate maximum size file


        if(offset + len(data) > file_size):     #calculate new file size based on data to be written and previous content of the file
          new_file_size =  len(data) + offset
        else: new_file_size =  file_size

        if(new_file_size > max_file_size):   #truncate data if it is bigger than the avaiable space in file
          data = data[:-(new_file_size-max_file_size)]


    	#------------------------------------------------------------------------------
         #provisorisch
            #-------------------------------------create dataarray -----------

    	if(len_old_data != 0):	  #if offset is in the middle of block..

    	  data_old = self.INODE_TO_BLOCK(inode,offset)  #read block to update
          file_size = len(data_old) + start_block*config.BLOCK_SIZE - data_old.count('\0') #sustract ammount of \0
          if((offset > file_size) or (offset < 0)):  #return error if offset ist bigger then text file
            return -2
          dataremain = '\0'*(config.BLOCK_SIZE-len(data)-len_old_data)
          stringtowrite = data_old[0:len_old_data] + data[0:len_new_data] + dataremain

    	  dataarray.append(stringtowrite) #update read block
          #self.free_data_block(inode,start_block)
          #inode.size = 0
    	  for i in range(len_new_data, len(data), config.BLOCK_SIZE):  #create remaining bloxks if there are some

            zeropadding = config.BLOCK_SIZE - len(data[i : i + config.BLOCK_SIZE])
            stringtowrite = data[i : i + config.BLOCK_SIZE] + zeropadding*'\0'

            dataarray.append(stringtowrite)


    	else:

    	 for i in range(0, len(data), config.BLOCK_SIZE):

            zeropadding = config.BLOCK_SIZE - len(data[i : i + config.BLOCK_SIZE])
            stringtowrite = data[i : i + config.BLOCK_SIZE] + zeropadding*'\0'

    	    dataarray.append(stringtowrite)

    	#-----------------------------------write data-------------------------

    	num_block_required = len(dataarray)
        serverprint = 'Data is written on '
    	for i in range(0, num_block_required):
    	  if(inode.size < len(dataarray)):
    	    inode.blk_numbers[start_block + i] = interface.get_new_virtual_block()  #allocate new blocks in inode if needed
    	    inode.size += 1    #update file size
    	    inode.time_modified = str(datetime.datetime.now())   #update modified time when new reference block is created in the inode
          ser = interface.block_number_translate(inode.blk_numbers[start_block + i])

          serverprint = serverprint + 'server ' + str(ser[0])+ ' '
        print(serverprint)
        time.sleep(delay)
        for i in range(0, num_block_required):
          interface.update_data_block(inode.blk_numbers[start_block + i], dataarray[i], delay)   #write blocks

        if (inode.size > num_block_required):
            dif = inode.size - num_block_required

            self.free_data_block(inode, inode.blk_numbers[start_block + num_block_required] )
            inode.size -= dif

        return inode

    #IMPLEMENTS THE READ FUNCTION
    def read(self, inode, offset, length):
    	inode.time_accessed = str(datetime.datetime.now())    #update accessed time
    	start_block_read = offset/config.BLOCK_SIZE      #in which block the reading starts
    	numb_blocks = 1
    	leng_blocks = []
        serverprint = 'Data is read from '

    	#------------ERROR management------------------------------------------------
    	if(inode.type != 0):   #check if Inode is of type file
    	  print('ERROR: Inode is not a file')
    	  return inode, -1

            #------------ determine the length of the read string per block depending on offset and length and for each block involve din read operation
        if(config.BLOCK_SIZE - offset%config.BLOCK_SIZE >= length):
    	  leng_blocks.append(length)
    	  length = 0
    	else:
    	  leng_blocks.append(config.BLOCK_SIZE - offset)
    	  length -= config.BLOCK_SIZE - offset

    	while(length>0):
    	  if(length < config.BLOCK_SIZE):
    	    leng_blocks.append(length)
    	    numb_blocks +=1
            break;
    	  else:
    	    leng_blocks.append(config.BLOCK_SIZE)
    	    length -= config.BLOCK_SIZE
    	    numb_blocks +=1

    	#-------------------------------------------------------------------------------------------
    	dataarray = []
    	read_data = ''
        length_hash = 16
    	offsetcopy = offset

        for i in range(0,numb_blocks):
            index = offset / config.BLOCK_SIZE
            ser = interface.block_number_translate(self.INDEX_TO_BLOCK_NUMBER(inode,index + i))
            serverprint = serverprint + 'server ' + str(ser[0]) + ' '
        print(serverprint)
        time.sleep(5)

        for i in range(0,numb_blocks):
    	  dataarray.append(self.INODE_TO_BLOCK(inode,offset + (i*config.BLOCK_SIZE))) #read all blocks where the desired data is distribuited
          file_size = len(dataarray[i]) -  dataarray[i].count('\0')

          if(offsetcopy%config.BLOCK_SIZE >= file_size):
      	       print('Reading ERROR: Offset too big')
      	       return inode, -1

          read_data += dataarray[i][(offsetcopy%config.BLOCK_SIZE):(offsetcopy%config.BLOCK_SIZE)+leng_blocks[i]]    #read out the right data starting from offset
    	  offsetcopy = 0

        return inode, read_data
