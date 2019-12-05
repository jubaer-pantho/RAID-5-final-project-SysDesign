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
    def write(self, path, offset=0, delay = 1, data = " "):
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
            print("The current design only supports 4 servers. Initializing for 4 servers")
            Initialize_My_FileSystem(4)
    except:
        print("Error: Might be incorrect argument to intilialize the file server.\n Correct Argument <python FileSystem.py 4>")
        quit()

    my_object = FileSystemOperations()
    #YOU MAY WRITE YOUR CODE AFTER HERE

    while True:
        inputs = (raw_input("Type the desired operation: $ ").split(' '))

        if(inputs[0] == 'mkdir'):
            try:
                my_object.mkdir(inputs[1])
            except:
                print("Error: Revise your input, to create folder : <mkdir yourFolderName>")
        elif (inputs[0] == 'create'):
            try:
                my_object.create(inputs[1])
            except:
                print("Error: Revise your input, to create file : <create yourFileName>")
        elif (inputs[0] == 'write'):
            try:
                string_to_write = []
                for i in range(4,len(inputs)):
                    string_to_write.append(inputs[i])

                sentence_to_write = " ".join(string_to_write)
                sentence_to_write = sentence_to_write.replace("\"", "")

                my_object.write(inputs[1], int(float(inputs[2])), int(float(inputs[3])), sentence_to_write)
            except:
                print("Error: Revise your input, to write to a file : <write AbsoluteFilePath offset delay dataToWrite>")
        elif (inputs[0] == 'read'):
            try:
                my_object.read(inputs[1], int(float(inputs[2])), int(float(inputs[3])))
            except:
                print("Error: Revise your input, to read from a file : <read AbsoluteFilePath offset readSize>")
        elif (inputs[0] == 'status'):
           my_object.status()
        elif (inputs[0] == 'rm'):
            try:
                my_object.rm(inputs[1])
            except:
                print("Error: Revise your input, to remove a file/folder : <rm AbsoluteFilePath>")
        elif (inputs[0] == 'mv'):
            try:
                my_object.mv(inputs[1], inputs[2])
            except:
                print("Error: Revise your input, to move a file : <mv oldPath newPath>")
        elif(inputs[0] == 'exit'):
            break;
        else:
           print('Incorrect input')
