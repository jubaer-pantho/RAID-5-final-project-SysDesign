import MemoryInterface, AbsolutePathNameLayer, os, sys

def Initialize_My_FileSystem(no_of_servers):
    MemoryInterface.Initialize_My_FileSystem(no_of_servers)
    AbsolutePathNameLayer.AbsolutePathNameLayer().new_entry('/', 1)


#HANDLE TO ABSOLUTE PATH NAME LAYER
interface = AbsolutePathNameLayer.AbsolutePathNameLayer()

class FileSystemOperations():

    #MAKES NEW DIRECTORY
    def mkdir(self, path):
        interface.new_entry(path, 1)

    #CREATE FILE
    def create(self, path):
        interface.new_entry(path, 0)


    #WRITE TO FILE
    def write(self, path, data, offset=0, delay = 1):
        interface.write(path, offset, data, delay)


    #READ
    def read(self, path, offset=0, size=-1):
        read_buffer = interface.read(path, offset, size)
        if read_buffer != -1: print(path + " : " + read_buffer)


    #DELETE
    def rm(self, path):
        interface.unlink(path)


    #MOVING FILE
    def mv(self, old_path, new_path):
        interface.mv(old_path, new_path)


    #CHECK STATUS
    def status(self):
        statuse = MemoryInterface.status()
        print(statuse)

            #print str([0])



if __name__ == '__main__':



    try:
        #temporary fix
        if (int(sys.argv[1]) == 4):
            Initialize_My_FileSystem(int(sys.argv[1]))
        else:
            print("The current design only support 4 servers.")
            quit()
    except:
        print("Incorrect argument to intilialize the file server")
        quit()

    my_object = FileSystemOperations()
    #YOU MAY WRITE YOUR CODE AFTER HERE

    while True:
        inputs = (raw_input("Type the desired operation: $ ").split(' '))

        if(inputs[0] == 'mkdir'):
            try:
                my_object.mkdir(inputs[1])
            except:
                print("Incorrect input, Input format to create folder is <mkdir yourFolderName>")
        elif (inputs[0] == 'create'):
            try:
                my_object.create(inputs[1])
            except:
                 print("Incorrect input, Input format to create file is <create yourFileName>")
        elif (inputs[0] == 'write'):
            try:
                my_object.write(inputs[1], inputs[2], int(float(inputs[3])), int(float(inputs[4])))
            except:
                print("Incorrect input, Input format to write to a file is <write AbsoluteFilePath data offset delay>")
        elif (inputs[0] == 'read'):
            try:
                my_object.read(inputs[1], int(float(inputs[2])), int(float(inputs[3])))
            except:
                print("Incorrect input, Input format to read from a file is <read AbsoluteFilePath offset readSize>")
        elif (inputs[0] == 'status'):
           my_object.status()
        elif (inputs[0] == 'rm'):
            try:
                my_object.rm(inputs[1])
            except:
                print("Incorrect input, Input format to remove a file/folder is <rm AbsoluteFilePath>")
        #elif (inputs[0] == 'mv'):
          # my_object.mv(inputs[1], inputs[2])
        else:
           print('Incorrect input')



