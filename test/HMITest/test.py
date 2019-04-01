from listener import Listener
from pusher import Pusher
import queue
import threading
import socket

q = queue.Queue()
ql = threading.Lock()

l = Listener(12345, q, ql)
p = Pusher(12346, q, ql)

l.start()
p.start()


l.join()
p.join()