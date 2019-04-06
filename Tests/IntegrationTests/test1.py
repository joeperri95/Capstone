#!/usr/bin/env python3.5

import sys
sys.path.append('/home/pi/Capstone')

import Bot
import directions
import queue
import threading

def main():

    q = queue.Queue()
    ql = threading.Lock()
    loc = (1,1)
    direction = directions.UP

    bot = Bot.Bot(q, ql, loc, direction)
    bot.start()
    bot.join()


if __name__ == '__main__':
    main()