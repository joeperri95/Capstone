#!/usr/bin/env python3.6

import threading
import queue
import cv2
import Motors

class Navigator(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        #motor controller class
        self.motors = Motors.Motors()

        #image related fields
        self.cap = cv2.VideoCapture(0)
        self.frame = None
        self.lastFrame = None

        #center of line contour
        self.center = (0, 0)

    def __del__(self):
        self.cap.release()

    def update(self):
        #update logic run each tick

        self.lastFrame = self.frame
        _ , self.frame = self.cap.read()

        self.processLine()
        self.detect()

    def processLine(self):
        
        try:
            pass
            #red = 
            #green = 
            #yellow =

        except TypeError as e:
            print(e)

        
        pass

    def detect(self):
        pass

    def run(self):

        while(True):
            pass