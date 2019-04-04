#!/usr/bin/env python3.5

'''
TODO

implement directions

take contour and get output

only do one calculation per direction


do yellow detection


station IDS

'''



import threading
import queue
import cv2
import numpy as np
import Motors
import directions

#tunable parameters
RED_LOW = 150
RED_HIGH = 200

GREEN_LOW = 60
GREEN_HIGH = 100

YELLOW_LOW = 0
YELLOW_HIGH = 40

class Navigator(threading.Thread):
    def __init__(self, opt=directions.UP):
        threading.Thread.__init__(self)

        #motor controller class
        self.motors = Motors.Motors()

        #image related fields
        self.cap = cv2.VideoCapture(0)
        _, self.frame = self.cap.read()
        self.lastFrame = None
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)
        
        self.h, self.w = self.frame.shape[:2]
        self.direction = directions.getDir(opt)

        self.red = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self.green = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        self.yellow = np.zeros((self.h, self.w, 3), dtype=np.uint8)
        #self.draw = np.zeros((self.h, self.w, 3), dtype=np.uint8)

        #center of line contour
        self.center = (0, 0)

    def __del__(self):
        try:
            self.cap.release()
        except NameError as e:
            #if class is never initialized cap will not be created
            pass

    def update(self):
        #update logic run each tick

        self.lastFrame = self.frame
        _ , self.frame = self.cap.read()
        self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

        self.processLine()
        self.detect()
        self.setMotors()

    def setOpt(self, newopt):
        res = directions.getDir(newopt)
        if(res):
            self.opt = newopt

    def processLine(self):
        
        try:
            
            #threshold by hsv value
            r = cv2.inRange(self.hsv, (RED_LOW, 10, 15), (RED_HIGH ,255, 200))
            g = cv2.inRange(self.hsv, (GREEN_LOW, 10, 15), (GREEN_HIGH, 255, 200))
            y = cv2.inRange(self.hsv, (YELLOW_LOW,10, 15), (YELLOW_HIGH, 255, 200))

            #perform open morphological operation to fill region
            r = cv2.morphologyEx(r, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
            g = cv2.morphologyEx(g, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
            y = cv2.morphologyEx(y, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
        
            #median blur to fill region
            self.red = cv2.medianBlur(r, 3)
            self.green = cv2.medianBlur(g, 3)
            self.yellow = cv2.medianBlur(y, 3)

            #get contours
            self.yc, _ = cv2.findContours(self.yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            self.rc, _ = cv2.findContours(self.red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            self.gc, _ = cv2.findContours(self.green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


            if(self.direction == directions.UP):
                if(self.rc):
                    rcmax = max(self.rc, key=cv2.contourArea)
                    M = cv2.moments(rcmax)

                    #if no contour put center in center of screen
                    if(M["m00"] == 0):
                        cx = int(self.w / 2)
                        cy = int(self.h / 2)
                    else:    
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        self.center = (cx, cy)
            
            elif(self.direction == directions.LEFT):
                if(self.gc):
                    gcmax = max(self.gc, key=cv2.contourArea)
                    M = cv2.moments(gcmax)

                    #if no contour put center in center of screen
                    if(M["m00"] == 0):
                        cx = int(self.w / 2)
                        cy = int(self.h / 2)
                    else:    
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        self.center = (cx, cy)
                    
                    
                

        except TypeError as e:
            print(e)

        
    def detect(self):
        if(self.yc.contourArea > 10):
            print('detected')
        pass

    def setMotors(self):

        if(self.direction == directions.UP):
            if(self.center[0] > int(self.w * 0.75)):
                self.motors.leftTimed(0.1, 0.01)

            elif(self.center[0] < int(self.w * 0.25)):
                self.motors.rightTimed(0.1, 0.01)
            
            else:
                self.motors.forwardTimed(0.1, 0.01)
        
        elif(self.direction == directions.LEFT):
            if(self.center[1] > int(self.h * 0.75)):
                self.motors.leftTimed(0.1, 0.01)

            elif(self.center[1] < int(self.h * 0.25)):
                self.motors.rightTimed(0.1, 0.01)
            
            else:
                self.motors.forwardTimed(0.1, 0.01)
            

    def run(self):
        while(True):
            self.update()
 
