#!/usr/bin/env python3.6

import BotStates
import locations
import cv2
import sys
import os
import utils
import time
import numpy as np
import queue

class Bot:
    def __init__(self, cam, queue):
        '''
        cam = cv2 capture object
        '''
        
        self.state = BotStates.IDLE
        self.prevState = BotStates.IDLE
        
        self.cam = cam
        
        #doesn't know where it is on bootup assume base
        self.location = locations.BASE
        self.destinations = []

        #for use in time critical situations
        self.currentTime = 0
        self.MessageQueue = queue

        _, frame = cam.read()
        self.h, self.w = frame.shape[:2]
        
        #call this as a thread
        #self.determineOutput()
        
    
    def isEmpty(self):
        if(len(self.contours) == 0):
            return True
        else:
            return False

    def update(self):
        
        _, self.frame = self.cam.read()

        try:
            #Don't need gray elsewhere I don't think
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            
            #So openCV doesn't take the image border as the maximum contour
            self.gray = 255 - gray
            
            self.blur = cv2.GaussianBlur(self.gray,(5,5),0)
            _, thresh = cv2.threshold(self.blur, 127, 255, 0)
            _ ,self.contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            c = self.frame.__copy__()
            cv2.drawContours(c, self.contours, -1, (255,255,0))
            cv2.imshow('frame1', c)

            self.updateCenter()

        except TypeError as e:
            print(e)
            print("frame is empty")
            sys.exit(-1)
        
    def updateCenter(self): 
        if(not self.isEmpty()):
            c = max(self.contours, key = cv2.contourArea)
            M = cv2.moments(c)

            if(M["m00"] == 0):
                cx = int(self.w / 2)
                cy = int(self.h / 2)
            else:    
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
            
        else:
            print("Line lost")
            self.state = BotStates.LINE_LOST
        
        self.center = (cx, cy)

    def scanBarcode(self):
        '''
        Look for barcode return boolean
        '''

        gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)

        # Sobel gradients for x an y direction of the image
        X2 = cv2.Sobel(gray, ddepth = cv2.CV_64F, dx = 1, dy = 0, ksize = -1)
        Y2 = cv2.Sobel(gray, ddepth = cv2.CV_64F, dx = 0, dy = 1, ksize = -1)
        grad_sobel=np.sqrt(X2*X2+Y2*Y2)
        cv2.normalize(grad_sobel, grad_sobel, 0, 3, cv2.NORM_MINMAX)
        
        # Blur and threshold the gradient magnitude
        blurred = cv2.blur(grad_sobel, (12, 12))
        
        # Extract minimum and maximum values of the pixels from 'Blurred Sobel Gradient Magnitude'
        (minVal, maxVal, _, _) = cv2.minMaxLoc(blurred)
        
        # Extract mean and standard deviation values of the pixels from 'Blurred Sobel Gradient Magnitude'
        (mean, stddev) = cv2.meanStdDev(blurred)
        
        # Apply different threshold:
        (_, thresh1) = cv2.threshold(blurred, mean, maxVal, cv2.THRESH_BINARY)
        (_, thresh2) = cv2.threshold(blurred, mean+stddev, maxVal, cv2.THRESH_BINARY)
        
        #create and apply kernel
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
        closed = cv2.morphologyEx(thresh2, cv2.MORPH_CLOSE, kernel)
        mod1 = cv2.morphologyEx(closed, cv2.MORPH_OPEN, kernel)
        opened = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)
        mod2 = cv2.morphologyEx(thresh1, cv2.MORPH_CLOSE, kernel)

        # Convert the float image to 8-bit image
        opened = cv2.convertScaleAbs(opened)
        
        _, contours, _ = cv2.findContours(opened, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        
        # Sort all contours by area (descending order)
        contours = sorted(contours, key=cv2.contourArea, reverse=True)
        
        #something else may be recognized as a barcode ensure
        #barcode is correct by validating area
        minArea = 100
        maxArea = 200

        area = cv2.contourArea(contours[0])

        if (area >= minArea and area <= maxArea):
            return True
        else:
            return False  

    
    def pollMessageQueue(self):
        if(self.MessageQueue.empty()):
            return
        else:
            location, order = self.MessageQueue.get()
            

    def determineOutput(self):
        '''
        Main logic where actions are performed and state is determined
        '''
        while(True):
            
            self.pollMessageQueue()
            self.update()

            if(self.state == BotStates.IDLE):
                if(self.destinations == None):
                    pass
                else:
                    self.prevState = self.state
                    self.state = BotStates.MOTION
            

            elif(self.state == BotStates.MOTION):
                
                #TODO store the limits as variables
                #TODO implement some kind of PID or PI control

                #if moment is at an extreme turn the robot
                if(self.center[0] > int(self.w * 0.75)):
                    #motor1 = fullspeed
                    #motor2 = off
                    print("turn left")
                    pass
                elif(self.center[0] < int(self.w * 0.25)):
                    #motor1 = off
                    #motor2 = fullspeed
                    print("turn right")
                    pass
                else:
                    print("straight ahead")
                    #motor1 = fullspeed
                    #motor2 = fullspeed
                    pass
                pass

                if(self.scanBarcode()):
                    #if robot was just at a station ignore the barcode
                    
                    #this might be expensive look for workaround
                    cv2.imshow("frame2", self.frame)
                    cv2.imwrite("temp.png",self.frame)
                    code = utils.getBarcodeResults("temp.png")
                    os.remove("temp.png")

                    if(code == self.location):
                        pass
                    else:
                        self.prevState = self.state
                        self.state = BotStates.BARCODE_DETECTED

            elif(self.state == BotStates.BARCODE_DETECTED):
                
                cv2.imwrite("temp.png",self.frame)
                
                code = utils.getBarcodeResults("temp.png")
                os.remove("temp.png")

                #TODO error handling on the barcode
                self.location = code


                if(self.location == self.destinations[0]):
                    self.prevState = self.state
                    self.destinations.remove(self.destinations[0])
                    self.state = BotStates.WAITING_FOR_CUP
                else:
                    self.prevState = self.state
                    self.state = BotStates.MOTION

                pass

            elif(self.state == BotStates.WAITING_FOR_CUP):
                
                TIMEOUT = 3000
                
                if(self.currentTime == 0):
                    self.startTime = time.time()
                    self.currentTime = time.time()
                    diff = self.currentTime - self.startTime
                else:
                    self.currentTime = time.time()
                    diff = self.currentTime - self.startTime

                #If some sensor detects cup is taken
                #TODO make sensor manager class

                #if( CUP IS GIVEN ):
                #    self.currentTime = 0
                #    self.startTime = 0
                #    self.prevState = self.state
                #    self.state = BotStates.DISPENSING

                if(diff > TIMEOUT):
                    self.currentTime = 0
                    self.startTime = 0
                    self.prevState = self.state
                    #Later sucker
                    self.state = BotStates.MOTION
            
            elif(self.state == BotStates.DISPENSING):
                
                #dispense the liquid with GPIO
                #wait or make blocking call

                self.prevState = self.state
                self.state = BotStates.WAITING_FOR_RETRIEVAL
                

            elif(self.state == BotStates.WAITING_FOR_RETRIEVAL):
                
                TIMEOUT = 3000
                
                if(self.currentTime == 0):
                    self.startTime = time.time()
                    self.currentTime = time.time()
                    diff = self.currentTime - self.startTime
                else:
                    self.currentTime = time.time()
                    diff = self.currentTime - self.startTime

                #If some sensor detects cup is taken
                
                #if( CUP IS TAKEN )
                #    self.currentTime = 0
                #    self.startTime = 0
                #    self.prevState = self.state
                #    if(self.destinations == None):
                #        self.state == BotStates.IDLE
                #    else:
                #       self.state = BotStates.MOTION

                if(diff > TIMEOUT):
                    self.currentTime = 0
                    self.startTime = 0
                    self.prevState = self.state
                    self.state = BotStates.ALERT

            
            elif(self.state == BotStates.ALERT):
                
                #play tone or flash LEDs somehow
                #need to look into pi compatible media
                
                self.prevState = self.state 
                self.state = BotStates.WAITING_FOR_RETRIEVAL

            elif(self.state == BotStates.LINE_LOST):
                
                #What do we do in this situation?
                print("line lost")

                sys.exit(-1)
                



        
