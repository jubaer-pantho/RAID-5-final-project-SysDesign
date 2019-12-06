#This script is written to generate timing data and provided as a sample

import timeit, time
import MemoryInterface, AbsolutePathNameLayer, os, sys



element_size = 512 #data size = element_size * 8 Bytes
large_data = ["Florida "] * element_size
large_string = ''.join(large_data)



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
        #if read_buffer != -1: print(path + " : " + read_buffer)
        return read_buffer


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
        print("Incorrect argument. Initializing with correct input")
        Initialize_My_FileSystem(4)

    my_object = FileSystemOperations()
    #YOU MAY WRITE YOUR CODE AFTER HERE


    my_object.mkdir("/A")
    my_object.create("/A/1.txt") #, as A is already there we can crete file in A
    start = timeit.default_timer()
    my_object.write("/A/1.txt", 0, 1, large_string)
    stop = timeit.default_timer()
    print('Write Time: ', stop - start)

    print("waiting...")
    time.sleep(5)

    start = timeit.default_timer()
    retVal = my_object.read("/A/1.txt", 0, 8 * element_size)
    stop = timeit.default_timer()
    print('Read Time: ', stop - start)


    if (retVal == large_string):
        print("Read data matches the write !!")
    else:
        print("TEST FAILED")


    '''my_object.mkdir("/B")
    #my_object.status()
    #start = timeit.default_timer()
    my_object.mv("/A/1.txt", "/B/")
    stop = timeit.default_timer()
    print('Move Time: ', stop - start)

    retVal = my_object.read("/B/1.txt", 0, 8 * element_size)


    if (retVal == large_string):
        print("Move works. Read data matches the write !!")
    else:
        print("Move failed. TEST FAILED")



    start = timeit.default_timer()
    my_object.rm("/B/1.txt") 
    stop = timeit.default_timer()
    print('remove Time: ', stop - start)'''
