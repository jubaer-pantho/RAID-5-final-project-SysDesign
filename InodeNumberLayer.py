'''
THIS MODULE ACTS AS A INODE NUMBER LAYER. NOT ONLY IT SHARES DATA WITH INODE LAYER, BUT ALSO IT CONNECTS WITH MEMORY INTERFACE FOR INODE TABLE
UPDATES. THE INODE TABLE AND INODE NUMBER IS UPDATED IN THE FILE SYSTEM USING THIS LAYER
'''
import InodeLayer, config, MemoryInterface, datetime, InodeOps, MemoryInterface


#HANDLE OF INODE LAYER
interface = InodeLayer.InodeLayer()

class InodeNumberLayer():

	#PLEASE DO NOT MODIFY
	#ASKS FOR INODE FROM INODE NUMBER FROM MemoryInterface.(BLOCK LAYER HAS NOTHING TO DO WITH INODES SO SEPERTAE HANDLE)
	def INODE_NUMBER_TO_INODE(self, inode_number):#

		array_inode = MemoryInterface.inode_number_to_inode(inode_number)

		inode = InodeOps.InodeOperations().convert_array_to_table(array_inode)
		if inode: inode.time_accessed = datetime.datetime.now()   #TIME OF ACCESS
		return inode


	#PLEASE DO NOT MODIFY
	#RETURNS DATA BLOCK FROM INODE NUMBER
	def INODE_NUMBER_TO_BLOCK(self, inode_number, offset, length):
		inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if not inode:
			print("Error InodeNumberLayer: Wrong Inode Number! \n")
			return -1
		return interface.read(inode, offset, length)


	#PLEASE DO NOT MODIFY
	#UPDATES THE INODE TO THE INODE TABLE
	def update_inode_table(self, table_inode, inode_number):
		if table_inode: table_inode.time_modified = datetime.datetime.now()  #TIME OF MODIFICATION
		array_inode = InodeOps.InodeOperations().convert_table_to_array(table_inode)
		MemoryInterface.update_inode_table(array_inode, inode_number)


	#PLEASE DO NOT MODIFY
	#FINDS NEW INODE INODE NUMBER FROM FILESYSTEM
	def new_inode_number(self, type, parent_inode_number, name):

		if parent_inode_number != -1:

			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size
			if len(parent_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
		for i in range(0, config.MAX_NUM_INODES):
			if self.INODE_NUMBER_TO_INODE(i) == False: #FALSE INDICTES UNOCCUPIED INODE ENTRY HENCE, FREEUMBER
				inode = interface.new_inode(type)
				inode.name = name
				self.update_inode_table(inode, i)

				return i
		print("Error InodeNumberLayer: All inode Numbers are occupied!\n")


	#LINKS THE INODE
	def link(self, file_inode_number, hardlink_name, hardlink_parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		if hardlink_parent_inode_number != -1:
			entry_size = config.MAX_FILE_NAME_SIZE + len(str(config.MAX_NUM_INODES))
			max_entries = (config.INODE_SIZE - 79 ) / entry_size

			hardlink_inode = self.INODE_NUMBER_TO_INODE(hardlink_parent_inode_number)
			file_inode = self.INODE_NUMBER_TO_INODE(file_inode_number)
			if len(hardlink_inode.directory) == max_entries:
				print("Error InodeNumberLayer: Maximum inodes allowed per directory reached!")
				return -1
			hardlink_inode.directory[hardlink_name] = file_inode_number
			file_inode.links += 1
			self.update_inode_table(hardlink_inode, hardlink_parent_inode_number)
			self.update_inode_table(file_inode, file_inode_number)
			return True
		else:
			print("Error InodeNumberLayer: Incorrect Parent Inode")
			return -1

	#REMOVES THE INODE ENTRY FROM INODE TABLE
	def unlink(self, inode_number, parent_inode_number, filename):
		'''WRITE YOUR CODE HERE'''

		parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
		file_inode = self.INODE_NUMBER_TO_INODE(inode_number)
		if(file_inode.type == 0):   ##inode is a file
			if(file_inode.links == 1):
				#parent_inode.directory[filename] = FALSE
				self.update_inode_table(False,inode_number)
				del parent_inode.directory[filename]
				self.update_inode_table(parent_inode,parent_inode_number)
				return True

			else:
				del parent_inode.directory[filename]
				file_inode.links -= 1
				self.update_inode_table(parent_inode,parent_inode_number)
				return True



		elif(file_inode.type == 1):
			if(len(file_inode.directory) > 0):
				print("Error InodeNumberLayer: Directory not empty")
				return -1
			else:
				self.update_inode_table(False,inode_number)
				del parent_inode.directory[filename]
				self.update_inode_table(parent_inode,parent_inode_number)
				return True
		else:
			print("Error InodeNumberLayer: Inode type is not correct")
			return -1


	#IMPLEMENTS WRITE FUNCTIONALITY
	def write(self, inode_number, offset, data, parent_inode_number, delay):
		'''WRITE YOUR CODE HERE'''
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1

		child_inode = self.INODE_NUMBER_TO_INODE(inode_number)
		inode = interface.write(child_inode,offset,data, delay)
		if(inode == -1):
			print("Error InodeNumberLayer: Inode not a file")
			return -1
		if(inode == -2):
			print("Error InodeNumberLayer: Offset wrong")
			return -1
		self.update_inode_table(inode, inode_number)
		return True
	#IMPLEMENTS READ FUNCTIONALITY
	def read(self, inode_number, offset, length, parent_inode_number):
		'''WRITE YOUR CODE HERE'''
		if parent_inode_number != -1:
			parent_inode = self.INODE_NUMBER_TO_INODE(parent_inode_number)
			if not parent_inode:
				print("Error InodeNumberLayer: Incorrect Parent Inode")
				return -1

		child_inode = self.INODE_NUMBER_TO_INODE(inode_number)
		data = self.INODE_NUMBER_TO_BLOCK(inode_number, offset, length)
		return data[1]
