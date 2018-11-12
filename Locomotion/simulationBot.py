import cv2
import math
import time
import random
import sys
from utils import *

#Used in simulation

class Slice:

    def __init__(self, img, x, y, w, h):
        self.w = w
        self.h = h
        self.img = img
        self.update(x, y)
        
       
    def update(self, x, y):
        self.x = x
        self.y = y
        
        self.crop = self.img[y:y+self.h, x:x+self.w]
        
        try:
            gray = cv2.cvtColor(self.crop, cv2.COLOR_BGR2GRAY)
            self.gray = 255 - gray
            
            self.blur = cv2.GaussianBlur(self.gray,(5,5),0)
            _, thresh = cv2.threshold(self.blur, 127, 255, 0)
            _ ,self.contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        except TypeError:
            print("Bot is offscreen")
            sys.exit(-1)

    def isEmpty(self):
        if(len(self.contours) == 0):
            return True
        else:
            return False

    def getLocalCenter(self):
        if(not self.isEmpty()):
            c = max(self.contours, key = cv2.contourArea)
            M = cv2.moments(c)

            if(M["m00"] == 0):
                cx = int(self.w / 2)
                cy = int(self.h / 2)
            else:    
                cx = int(M["m10"]/M["m00"])
                cy = int(M["m01"]/M["m00"])
            
            return  (cx, cy)
    
    def getGlobalCenter(self):
        cx, cy = self.getLocalCenter()
        
        cx += self.x
        cy += self.y

        return (cx, cy)

    def getDeflection(self):
        if(not self.isEmpty):
            cx, cy = self.getLocalCenter()
            
            #for cartesian coordinates with the center as the origin
            dy = int(self.h / 2) - cy
            dx = cx - int(self.w / 2)

            return (dx, dy)
    
    def __repr__(self):
        res = "X: {}, Y: {}, width: {}, height: {}, empty?: {}".format(self.x, self.y, self.w, self.h, self.isEmpty())
        return res


class Camera:

    def __init__(self, img, x, y, w, h):
        
        self.img = img
        
        if(w < 30):
            print("width must be at least 30 pixels")
            self.w = 30
        else:
            self.w = w
        if(h < 30):
            print("height must be at least 30 pixel")
            self.h = 30
        else:
            self.h = h
        
        self.update(x,y)
        

    def update(self, x, y):
        self.x = x
        self.y = y
        self.center = (int(self.x + self.w/2) , int(self.y + self.h/2))
        self.getSlices()
        
    def getSlices(self):    
        self.slices = []    
        for i in range(3):
            self.slices.append([])
            for j in range(3):
                self.slices[i].append(Slice(self.img, self.x + i*int(self.w/3), self.y + j*int(self.y/3), int(self.w/3), int(self.h/3)))

    def getPoints(self):
        res = []
        for row in self.slices:
            for col in row:
                if(not col.isEmpty()):
                    res.append(col.getGlobalCenter())
                    
        return res

    def fit(self):
         
        pts = self.getPoints()
        if(len(pts) == 0):
            print("Line lost")
            return None
         
        else:
            mat = []
            for row in self.slices:
                i = 0
                for col in row:
                    if(not col.isEmpty()):
                        mat.append(col.getGlobalCenter())
        
        xav = 0
        yav = 0

        for pt in mat:
            xav += pt[0]
            yav += pt[1]

        xav = int(xav / len(mat))
        yav = int(yav / len(mat))

        return(xav, yav)





