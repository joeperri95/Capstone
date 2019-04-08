#!/usr/bin/env python3.5

'''
TODO

take contour and get output

station IDS
'''

'''
red = up/down
green = left/right

'''



import threading
import queue
import cv2
import numpy as np
import os
#import Motors
import directions
import LEDmanager

#tunable parameters
RED_H_LOW = 120
RED_H_HIGH = 200
RED_S_LOW = 105
RED_S_HIGH = 255
RED_V_LOW = 150
RED_V_HIGH = 255

GREEN_H_LOW = 70
GREEN_H_HIGH = 110
GREEN_S_LOW = 150
GREEN_S_HIGH = 255
GREEN_V_LOW = 115
GREEN_V_HIGH = 255

YELLOW_H_LOW = 0
YELLOW_H_HIGH = 40
YELLOW_S_LOW = 150
YELLOW_S_HIGH = 255
YELLOW_V_LOW = 200
YELLOW_V_HIGH = 255    

class Navigator(threading.Thread):
    def __init__(self, destination,opt=directions.UP, location=(1,1), debug=False):
        threading.Thread.__init__(self)

        #motor controller class
        #rip
        #self.motors = Motors.Motors()

        self.leds = LEDmanager.NavLEDmanager()

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

        #these variables determine location of machine
        self.location = location
        self.globalDestination = destination
        self.destinationQueue = queue.Quexue()
        self.graph()

    def __del__(self):
        try:
            self.cap.release()
        except NameError as e:
            #if class is never initialized cap will not be created
            pass

    def setDirection(self, newopt):
        res = directions.getDir(newopt)
        if(res):
            self.opt = newopt

    def graph(self):
        #calculate route to destination
        self.destinationQueue = queue.Queue()
        
        xdiff = self.globalDestination[0] - self.location[0]
        ydiff = self.globalDestination[1] - self.location[1]
        
        x = self.location[0]
        y = self.location[1]

        if(xdiff < 0):
            while(x != self.globalDestination[0]):
                x -= 1
                self.destinationQueue.put((x, y))
            
        elif(xdiff > 0):
            while(x != self.globalDestination[0]):
                x += 1
                self.destinationQueue.put((x, y))
            

        if(ydiff < 0):
            while(y != self.globalDestination[1]):
                y -= 1
                self.destinationQueue.put((x, y))
            

        elif(ydiff > 0):
            while(y != self.globalDestination[1]):
                y += 1
                self.destinationQueue.put((x, y))

    def setDestination(self, dest):
        self.globalDestination = dest
        self.graph()

    def getLocation(self):
        return self.location

    def getDestination(self):
        return self.globalDestination


    def processLine(self):
        
        try: 
            #threshold by hsv value
            r = cv2.inRange(self.hsv, (RED_H_LOW, RED_S_LOW, RED_V_LOW), (RED_H_HIGH ,RED_S_HIGH, RED_V_HIGH))
            g = cv2.inRange(self.hsv, (GREEN_H_LOW, GREEN_S_LOW, GREEN_V_LOW), (GREEN_H_HIGH, GREEN_S_HIGH, GREEN_V_HIGH))
            y = cv2.inRange(self.hsv, (YELLOW_H_LOW,YELLOW_S_LOW, YELLOW_V_LOW), (YELLOW_H_HIGH, YELLOW_S_HIGH, YELLOW_V_HIGH))

            #perform open morphological operation to fill region
            r = cv2.morphologyEx(r, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
            g = cv2.morphologyEx(g, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
            y = cv2.morphologyEx(y, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_RECT, (3,3)))
        
            #median blur to fill region
            self.red = cv2.medianBlur(r, 3)
            self.green = cv2.medianBlur(g, 3)
            self.yellow = cv2.medianBlur(y, 3)

            #get contours
            _, self.yc, _ = cv2.findContours(self.yellow, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            _, self.rc, _ = cv2.findContours(self.red, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
            _, self.gc, _ = cv2.findContours(self.green, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)


            if(self.direction == directions.UP or self.direction == direction.DOWN):
                if(self.rc):
                    rcmax = max(self.rc, key=cv2.contourArea)
                    M = cv2.moments(rcmax)

                    #if no contour put center in center of screen
                    if(M["m00"] == 0):
                        raise Exception("line lost")
                        cx = int(self.w / 2)
                        cy = int(self.h / 2)
                    else:    
                        cx = int(M["m10"]/M["m00"])
                        cy = int(M["m01"]/M["m00"])

                        self.center = (cx, cy)
            
            elif(self.direction == directions.LEFT or self.direction == directions.RIGHT):
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
        #detect yellow square
        minArea = 50
        
        if(not self.yc):
            return False

        if(cv2.contourArea(max(self.yc,key=cv2.contourArea)) > minArea):
            self.leds.stop()
            return True
        
        return False
    
    def turnLeft(self):
        #espeak('turn left')
        self.leds.blinkLeft()
        if(self.direction == directions.UP):
            
            self.direction = directions.LEFT
            pass
        elif(self.direction == directions.LEFT):
        
            self.directions = directions.DOWN
            pass
        elif(self.direction == directions.RIGHT):
            
            self.direction = directions.UP
            pass
        elif(self.direction == directions.DOWN):
            
            self.direction = directions.RIGHT
            pass
        

    def turnRight(self):
        #espeak("turn right")
        self.leds.blinkRight()
        if(self.direction == directions.UP):
            
            self.direction = directions.RIGHT
            pass
        elif(self.direction == directions.LEFT):

            self.direction = directions.UP
            pass
        elif(self.direction == directions.RIGHT):

            self.direction = directions.DOWN
            pass
        elif(self.direction == directions.DOWN):
            
            self.direction = directions.LEFT
            pass
        

    def setMotors(self):

        if(self.direction == directions.UP):
            if(self.center[0] > int(self.w * 0.75)):
                #espeak('slight left')
                #self.motors.leftTimed(1, 0.1)
                self.leds.left()
            elif(self.center[0] < int(self.w * 0.25)):
                #espeak('slight right')
                #self.motors.rightTimed(1, 0.1)
                self.leds.right()
            else:
                #self.motors.forwardTimed(1, 0.1)
                self.leds.straight()

        elif(self.direction == directions.DOWN):
            if(self.center[0] > int(self.w * 0.75)):
                #espeak('slight right')
                #self.motors.leftTimed(1, 0.1)
                self.leds.left()
            elif(self.center[0] < int(self.w * 0.25)):
                #espeak('slight left')
                #self.motors.rightTimed(1, 0.1)
                self.leds.right()
            else:
                #self.motors.forwardTimed(1, 0.1)
                self.leds.straight()

        elif(self.direction == directions.LEFT):
            if(self.center[1] > int(self.h * 0.75)):
                #espeak('slight left')
                #self.motors.leftTimed(1, 0.1)
                self.leds.left()
            elif(self.center[1] < int(self.h * 0.25)):
                #espeak('slight right')
                #self.motors.rightTimed(1, 0.1)
                self.leds.right()
            else:
                self.leds.straight()
                #self.motors.forwardTimed(1, 0.1)

        elif(self.direction == directions.RIGHT):
            if(self.center[1] > int(self.h * 0.75)):
                #espeak('slight right')
                #self.motors.leftTimed(1, 0.1)
                self.leds.left()
            elif(self.center[1] < int(self.h * 0.25)):
                #espeak('slight left')
                #self.motors.rightTimed(1, 0.1)
                self.leds.right()
            else:
                self.leds.straight()
                #self.motors.forwardTimed(1, 0.1)
            
    def turningLogic(self):
        '''
        determine if the robot needs to turn based on destination 
        '''

        if(self.location[0] == self.localDestination[0]):
            if((self.localDestination[1] - 1) == self.location[1]):
                if(self.direction == directions.LEFT):
                    return

                elif(self.direction == directions.RIGHT):
                    self.turnRight()
                    self.turnRight()
                elif(self.direction == directions.UP):
                    self.turnLeft()

                elif(self.direction == directions.DOWN):
                    self.turnRight()

            elif((self.localDestination[1] + 1) == self.location[1]):
                if(self.direction == directions.LEFT):
                    self.turnRight()
                    self.turnRight()
                elif(self.direction == directions.RIGHT):
                    return
                elif(self.direction == directions.UP):
                    self.turnRight()
                elif(self.direction == directions.DOWN):
                    self.turnLeft()

        if(self.location[1] == self.localDestination[1]):
            if((self.localDestination[0] + 1) == self.location[0]):
                if(self.direction == directions.LEFT):
                    self.turnRight()
                elif(self.direction == directions.RIGHT):
                    self.turnLeft()
                elif(self.direction == directions.UP):
                    return
                elif(self.direction == directions.DOWN):
                    self.turnRight()
                    self.turnRight()

            elif((self.localDestination[0] - 1) == self.location[0]):
                if(self.direction == directions.LEFT):
                    self.turnLeft()
                elif(self.direction == directions.RIGHT):
                    self.turnRight()
                elif(self.direction == directions.UP):
                    self.turnRight()
                    self.turnRight()
                elif(self.direction == directions.DOWN):
                    return
        
        else:
            self.graph()



    def run(self):
        '''
        main logic loop
        '''
        while(True):
            self.lastFrame = self.frame
            _ , self.frame = self.cap.read()
            self.hsv = cv2.cvtColor(self.frame, cv2.COLOR_BGR2HSV)

            self.processLine()
            stop = self.detect()

            if(stop):
                self.motors.stop()
                if(self.destinationQueue.empty()):
                    #if no more destinations terminate thread
                    break
                else:
                    self.location = self.localDestination
                    self.localDestination = self.destinationQueue.get()
                    self.turningLogic()



            else:
                self.setMotors()

        