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
        inputs = (raw_input("Type the desidered operation: $ ").split(' '))

        if(inputs[0] == 'mkdir'):
            my_object.mkdir(inputs[1])
        elif (inputs[0] == 'create'):
           my_object.create(inputs[1])
        elif (inputs[0] == 'write'):
           my_object.write(inputs[1], inputs[2], int(float(inputs[3])), int(float(inputs[4])))
        elif (inputs[0] == 'read'):
           my_object.read(inputs[1], int(float(inputs[2])), int(float(inputs[3])))
        elif (inputs[0] == 'status'):
           my_object.status()
        elif (inputs[0] == 'rm'):
           my_object.rm(inputs[1])
        #elif (inputs[0] == 'mv'):
          # my_object.mv(inputs[1], inputs[2])
        else:
           print('Incorrect input')




        #else:




    #Examples:
    '''my_object.mkdir("/A")
    #my_object.mkdir("/A/B")
    #my_object.status()
    $ mkdir("/A")
    $ mkdir("/B")
    $ mkdir("/C")
    $ mkdir("/D")

    #my_object.mkdir("/A/B")

    my_object.create("/A/1.txt")
    my_object.create("/A/2.txt")
    string = 2048*'a'

    my_object.write("/A/1.txt",string,0)
    my_object.read("/A/1.txt",0,2047) #test1
    #my_object.write("/A/1.txt",'bbbbb',0)
    #my_object.status()#test2
    #test2
    #my_object.write("/A/1.txt",' wie gehts',0)
    #my_object.create("/A/asasd.txt")
    #my_object.write("/A/asasd.txt",' hooi',0) #test2
    my_object.status()'''
    #my_object.status()#test2'''

    '''my_object.read("/A/1.txt",0,6) #test1
    my_object.mkdir("/B")
    my_object.write("/A/1.txt",' wie gehts',5) #test2
    my_object.read("/A/1.txt",0,15) #test1
    my_object.mv("/A/1.txt", "/B/")
    my_object.rm("/B/1.txt")
    my_object.status()'''
    '''my_object.create("/A/2.txt")#, as A is already there we can crete file in A
    my_object.status()





    my_object.write("/A/2.txt",'01234567',0) #test3
    #my_object.read("/A/1.txt",2,2) #test3/4

    #my_object.write("/A/2.txt",'reset\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"',0) #test5/6
    #my_object.read("/A/2.txt",0,5) #test5/6


    interface.link("/A/2.txt","/A/B/3.txt")
    my_object.rm("/A/2.txt")
    my_object.read("/A/B/3.txt",0,4) #test3/4

    my_object.status()
    #my_object.write("/A/1.txt",'hallo',0)
    #my_object.read("/B/3.txt",1,4)

    #my_object.rm("/A")
    #my_object.rm("/A/1.txt")'''
    '''my_object.mv("/A/B/1.txt", "/")

    my_object.rm("/A")
    my_object.status()'''
    '''my_object.status()



    my_object.status()
    '''
