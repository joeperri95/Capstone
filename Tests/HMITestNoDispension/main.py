#!/usr/bin/env python3.5

import sys
sys.path.append('/home/joe/Capstone')

from Bot import Listener
from Bot import Pusher
from Bot import Dispensor

import queue
import threading
import socket

def main():
    q = queue.Queue()
    ql = threading.Lock()

    
    listenerThread = Listener.Listener(12345, q, ql)
    pusherThread = Pusher.Pusher(12346, q, ql)

    listenerThread.start()
    pusherThread.start()

    while(True):
        pass

    listenerThread.join()
    pusherThread.join()

if __name__ == '__main__':
    main()