#!/usr/bin/env python3.5

import sys

sys.path.append('/home/pi/Capstone/Bot')
import Bot
import directions
import queue
import threading

def main():
    ql = threading.Lock()
    q = queue.Queue()
    b = Bot.Bot.Bot(q, ql, (1,1), directions.UP)
    b.start()


if __name__ == '__main__':
    main()
