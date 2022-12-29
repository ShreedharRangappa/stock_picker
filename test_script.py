from threading import Thread, Event
from queue import Queue
from time import sleep, time
import copy
import ctypes



class Test():
    def __init__(self, event) -> None:
        self.event =event
        self.template = {'id':-1,'valid':0}
        self.addressListCount=10
        self.list_ = [ copy.copy(self.template) for i in range(self.addressListCount)]
        # self.list_=[{}]*self.listCount
        self.addressList=[]
        self.writeCount=0
        self.readCount=0
        self.freeCount=-1
        self.upadteAddressList()

        self.t1 = Thread(target=self.writeList, args=())
        self.t2 = Thread(target=self.readList)#, args=(self.list_, self.readCount))

        self.t1.start()
        self.t2.start()



    def upadteAddressList(self):
        for i in self.list_:
            # print(id(i))
            self.addressList.append(id(i))
        print("Updated address list \n")
    
    def getWriteCount(self,verbose=0):
        if verbose:
            print('Write count is %d',self.writeCount)
        return self.writeCount
    
    def getReadCount(self, verbose = 0):
        if verbose:
            print('Read count is %d',self.readCount)
        return self.readCount
    
    def setReadCount(self):
        if (self.readCount+1 >= self.addressListCount):
            self.readCount=0
        else:
            self.readCount+=1
    
    def setWriteCount(self):
        if (self.writeCount+1 >= self.addressListCount):
            self.writeCount=0
        else:
            self.writeCount+=1

    def getAddress(self,cond):
        # cond is the switch case for read/write
        if cond == 'read':
            addr = self.addressList[self.readCount]
        elif cond == "write":
            addr = self.addressList[self.writeCount]
        else:
            return []
        return addr

    def addValues2List(self,id_, verbose=0):
        val = self.getWriteCount(verbose)
        if verbose:
            print({"id":id_, "valid":1})
        self.list_[val]={"id":id_, "valid":1}
    
    def getValue4List(self, verbose=0):
        addr = self.getAddress('read')

        # get the value through memory address
        if verbose:
            
            print("Reading")
        ctypes.cast(addr, ctypes.py_object).value

        
    def getListSize(self,verbose = 0):
        if verbose:
            print("Length of list %d",len(self.list_))
        return len(self.list_)

    def writeList(self):
        while (True):
            if (self.event.is_set()):
                self.addValues2List(1, 1)
                self.setWriteCount()
            else:
                print('not set')
            
            self.event.clear()
            sleep(.1)
    
    def readList(self):
        while(True):
            self.getValue4List(verbose=1)
            self.setReadCount()
            sleep(.5)



    
    



if __name__ == '__main__':
    test=Test()
    test.t1.join()
    test.t2.join()
    # test.upadteAddList()
    # test.getValue()

