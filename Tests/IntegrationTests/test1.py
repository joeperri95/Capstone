#!/usr/bin/env python3.5

import sys
sys.path.append('/home/pi/Capstone')

from Bot import Robot
#import directions
import queue
import threading

def main():

    q = queue.Queue()
    ql = threading.Lock()
    loc = (1,1)
    direction = 1
    bot = Robot.Bot(q, ql, loc, direction)
    bot.start()
    bot.join()


if __name__ == '__main__':
    main()
