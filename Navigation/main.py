#!/usr/bin/env python3.6

import Bot
import cv2
import queue
import threading

cam = cv2.VideoCapture(0)

a = queue.Queue()

b = Bot.Bot(cam, a)

while(True):
    
    b.determineOutput()
    cv2.imshow("frame",b.frame)


    keyPressed  = cv2.waitKey(2) & 0xFF

    if(keyPressed == ord('q')):
        break