import timeit
import MemoryInterface, AbsolutePathNameLayer

def Initialize_My_FileSystem():
    MemoryInterface.Initialize_My_FileSystem()
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
    def write(self, path, data, offset=0):
        interface.write(path, offset, data)
      

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
        print(MemoryInterface.status())



if __name__ == '__main__':
    #DO NOT MODIFY THIS
    Initialize_My_FileSystem()
    my_object = FileSystemOperations()
    #my_object.status()
    #YOU MAY WRITE YOUR CODE AFTER HERE
    
    my_object.mkdir("/A")
    #my_object.status()
    my_object.mkdir("/B")
    #my_object.status()
    my_object.create("/A/1.txt") #, as A is already there we can crete file in A
    my_object.create("/B/2.txt") #, as A is already there we can crete file in A
    #my_object.status()
    start = timeit.default_timer()
    my_object.write("/A/1.txt", "Pantho", 0)
    stop = timeit.default_timer()
    print('Write Time: ', stop - start)

    start = timeit.default_timer()
    my_object.read("/A/1.txt", 0, 6)
    stop = timeit.default_timer()
    print('Read Time: ', stop - start)
    
    #my_object.status()
    start = timeit.default_timer()
    my_object.mv("/A/1.txt", "/B")
    stop = timeit.default_timer()
    print('Move Time: ', stop - start)

    my_object.read("/B/1.txt", 0, 6)
    my_object.status()
    #my_object.rm("/B/1.txt")
    my_object.mv("/B", "/A")

    start = timeit.default_timer()
    my_object.rm("/A/B/1.txt") 
    stop = timeit.default_timer()
    print('remove Time: ', stop - start)
    #my_object.status()

