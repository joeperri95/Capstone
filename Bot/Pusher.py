import socket
import pickle
import time
import threading
import queue

class Pusher(threading.Thread):
    '''
    pusher class will wait for a user to go to the order tracking tab
    pusher will send flask tcp/ip messages 
    '''

    def __init__(self, PORT, serverQueue, serverLock):
        '''
        takes port number, server queue object and corresponding mutex

        '''
        self.address = ('localhost', PORT)
        self.sock = None 
        threading.Thread.__init__(self)
        self.isActive = False
        self.BUFF_SIZE = 1024
        self.serverQueue = serverQueue
        self.serverLock = serverLock

    def setBuffSize(self, size):
        '''
        set size of receive buffer
        argument must be a power of 2
        '''
        if(size != 0 and ((size & (size - 1)) == 0)):
            self.BUFF_SIZE = size
        else:
            raise ValueError('Size is not a power of two')

    def run(self):
        '''
        Loop will run as long as program is alive
        Send data to flask server and add it to order queue

        '''

        while(True):    
            if(self.isActive == False): 
                try:
                    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sock.connect(self.address)
                    print('connected to guy')
                    self.isActive = True
                except ConnectionRefusedError as e:
                    print(e)
                    time.sleep(0.5)
                except Exception as f:
                    print(f)
                    time.sleep(0.5)
            else:
                try:
                    
                    self.serverLock.acquire()
                    
                    #get the first order
                    getFirst = 0

                    tempQueue = queue.Queue()
                    order = []

                    while(not self.serverQueue.empty()):
                            temp = self.serverQueue.get()
                            order.append(temp)
                            tempQueue.put(temp)

                    while(not tempQueue.empty()):
                        self.serverQueue.put(tempQueue.get())

                    self.serverLock.release()
                    
                    if(not self.serverQueue.empty()):
                        serializedObject = pickle.dumps(order)
                        self.sock.send(serializedObject)
                        self.sock.close()
                        self.isActive = False

                except ConnectionAbortedError as e:
                    #if server connection dies keep running 
                    if(self.sock is not None):
                        self.sock.close()
                    self.isActive = False

                except Exception as f:
                    print(f)
                    if(self.sock is not None):
                        self.sock.close()
                    self.isActive = False