#!/usr/bin/env python3.6

import Bot
import cv2

cam = cv2.VideoCapture(0)

b = Bot.Bot(cam)

while(True):

    b.determineOutput()
    cv2.imshow("frame",b.frame)


    keyPressed  = cv2.waitKey(2) & 0xFF

    if(keyPressed == ord('q')):
        break