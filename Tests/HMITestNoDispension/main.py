#!/usr/bin/env python3.5

import sys
sys.path.append('/home/pi/Capstone')

from Bot import Listener
from Bot import Pusher

import queue
import threading
import socket
import time


def main():
    q = queue.Queue()
    ql = threading.Lock()

    listenerThread = Listener.Listener(12345, q, ql)
    pusherThread = Pusher.Pusher(12346, q, ql)

    listenerThread.start()
    pusherThread.start()

    currTime = time.time()

    while(True):
        if(currTime + 10 < time.time()):    
            ql.acquire()
            if(not q.empty()):
                q.get()
            ql.release()

    listenerThread.join()
    pusherThread.join()

if __name__ == '__main__':
    main()