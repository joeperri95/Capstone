#!/usr/bin/env python3.5

import socket
import pickle
import threading
import queue

class Listener(threading.Thread):
    '''
    listener class will wait for orders to be processed in the flask process
    flask will send listener tcp/ip messages 
    listener will push messages to order queue
    '''
    def __init__(self, PORT, serverQueue, serverLock):
        '''
        takes port number, server queue object and corresponding mutex

        '''
        self.address = ('localhost', PORT)
        self.sock = socket.socket()
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
        Receive data from flask server and add it to order queue

        '''

        try:
            self.sock.bind(self.address)

        except ConnectionRefusedError as e:
            print(e)
            return 


        while(True):    
            if(self.isActive == False): 
                self.sock.listen(1)
                self.conn, addr = self.sock.accept()
                print("connection from " + addr[0] + ":" + addr[1])
                self.isActive = True
            
            data = self.conn.recv(self.BUFF_SIZE)
            
            if(data):
                #if message received put it on queue

                #deserialize data
                order = pickle.loads(data)
                
                #trim excess data that was passed from flask
                finalOrder = {'firstname' : order['firstname'], \
                    'lastname' : order['lastname'],\
                    'station' : order['station'],\
                    'drink' : order['drink']}

                #push it to queue
                self.serverLock.acquire()
                self.serverQueue.push(finalOrder)
                self.serverLock.release()
                
            else:
                #if server connection dies keep running 
                self.conn.close()
                self.isActive = False
