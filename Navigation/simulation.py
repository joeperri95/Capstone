#!/usr/bin/env python3.6

import cv2
import numpy as np
import sys
import utils
import time
import math
from simulationBot import Camera

def setup():
    FILENAME = sys.argv[1]
    print(FILENAME)
    img = cv2.imread(FILENAME, cv2.IMREAD_COLOR)
    
    #Place the robot at the start of the path
    if(FILENAME == "Simulation_Images/test2.png"):
        c = Camera(img, 75, 100, 90, 90)
    elif(FILENAME == "Simulation_Images/test3.png"):
        c = Camera(img, 50, 50, 90, 90)
    elif(FILENAME == "Simulation_Images/test4.png"):
        c = Camera(img, 350, 370, 90, 90)
    else:
        c = Camera(img, 0, 0, 90, 90)
    
    cv2.imshow("frame", img)
    overlay = img.__copy__()
    loop(c, img, overlay)



def loop(c, img, overlay):

    cv2.namedWindow("frame")
    cv2.createTrackbar("speed", "frame", 1, 50, utils.nothing)
    pause = True
    speed = cv2.getTrackbarPos("speed", "frame")
    angle = 270

    while(True):
        
        text_overlay = overlay.__copy__()

        if(not pause):
            
            b = c.getPoints()
            
            speed = cv2.getTrackbarPos("speed", "frame")
            #overlay = img.__copy__()

            for pt in b:
                cv2.circle(overlay, pt , 3, (255, 0, 0), -1)

            for row in c.slices:
                for col in row:
                    cv2.rectangle(overlay, (col.x, col.y) , (col.x + col.w, col.y + col.h), (0,0,255) )

            mid = c.fit()
            
            if(mid is not None):
                cv2.circle(overlay, mid, 3, (127,0,127), -1)

                cv2.line(overlay, c.center , mid, (0,0,30))

                angle = math.atan2(mid[0] - c.center[0], c.center[1] - mid[1])
                print(angle * 180 / math.pi)
                
                
                c = Camera(img, int(c.x + speed * math.cos(angle)), int(c.y + speed * math.sin(angle)), 90, 90)

                time.sleep(0.3)
                cv2.putText(text_overlay, "Simulation running", (300,50), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 255,0))
            
            else:
                c = Camera(img, int(c.x + speed * math.cos(angle)), int(c.y + speed * math.sin(angle)), 90, 90)
                cv2.putText(text_overlay, "LINE LOST", (300,25), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))
                time.sleep(0.3)
        else:

            cv2.putText(text_overlay, "Simulation paused", (300, 100), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255))

        cv2.imshow("frame", text_overlay)

        k = cv2.waitKey(1)
        
        if k == ord('q'):
            break
        elif k == ord(' '):
            pause = not pause


setup()