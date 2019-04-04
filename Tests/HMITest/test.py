#!/usr/bin/env python3.5

import sys
sys.path.append('/home/pi/Capstone')

from Bot import Listener
from Bot import Pusher
from Bot import Dispensor

import queue
import threading
import socket

def main():
    q = queue.Queue()
    ql = threading.Lock()

    disp = Dispensor.Dispensor()
    listenerThread = Listener.Listener(12345, q, ql)
    pusherThread = Pusher.Pusher(12346, q, ql)

    listenerThread.start()
    pusherThread.start()

    while(True):
        ql.acquire()
        if(not q.empty()):
            currentOrder = q.get()
            ql.release()
            if(currentOrder['drink'] == '1'):
                        resp =  disp.orangejuice()
                        if(resp):
                            print('oj')
                        else:
                            print('error')

            elif( currentOrder['drink'] == '2'):
                resp =  disp.gingerAle()
                if(resp):
                        print('ginger ale')
                else:
                        print('error')

            elif( currentOrder['drink'] == '3'):
                resp =  disp.mimosa()
                if(resp):
                        print('good mimosa')
                else:
                        print('error')
        else:
            ql.release()

    listenerThread.join()
    pusherThread.join()

if __name__ == '__main__':
    main()