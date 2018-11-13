import math
import cv2
import subprocess
import os
import pathlib

def nothing():
    '''
    Incase a callback is a mandatory argument
    '''
    pass

def getBarcodeResults(filepath):
    
    filepath = pathlib.Path(filepath)

    try:
        filepath = filepath.resolve()
    except FileNotFoundError:
        print("No such file: {}".format(filepath))

    procPath = "Dynamsoft/BarcodeReader6.4/samples/c++/ReadBarcode/"
    os.chdir(procPath)

    proc = subprocess.Popen(["./ReadBarcode", filepath], stdout=subprocess.PIPE)
    out, _ = proc.communicate()
    
    return str(out) 



def getBoundingBoxFromPoints(p1, p2, p3, p4):
    xmin = min(p1[0], p2[0], p3[0], p4[0])
    xmax = max(p1[0], p2[0], p3[0], p4[0])
    ymin = min(p1[1], p2[1], p3[1], p4[1])
    ymax = max(p1[1], p2[1], p3[1], p4[1])

    p1 = (xmin, ymax)
    p2 = (xmax, ymax)
    p3 = (xmax, ymin)
    p4 = (xmin, ymin)

    return p1, p2, p3, p4

def getRectanglePointsFromAngle(h, w, cx, cy, angle):
    
    #aog = angle
    angle = angle / 180 * math.pi
    
    y1 = -w / 2 * math.sin(angle) + h / 2 * math.cos(angle) + cy
    y2 =  w / 2 * math.sin(angle) + h / 2 * math.cos(angle) + cy
    y3 =  w / 2 * math.sin(angle) - h / 2 * math.cos(angle) + cy
    y4 = -w / 2 * math.sin(angle) - h / 2 * math.cos(angle) + cy 

    x1 = -w / 2 * math.cos(angle) - h / 2 * math.sin(angle) + cx
    x2 =  w / 2 * math.cos(angle) - h / 2 * math.sin(angle) + cx
    x3 =  w / 2 * math.cos(angle) + h / 2 * math.sin(angle) + cx
    x4 = -w / 2 * math.cos(angle) + h / 2 * math.sin(angle) + cx

    p1 = (int(x1), int(y1))
    p2 = (int(x2), int(y2))
    p3 = (int(x3), int(y3))
    p4 = (int(x4), int(y4))

    return(p1,p2,p3,p4)

def drawRectangleFromPoints(img, p1, p2, p3, p4, color):
    """
    draw rectangle with possibility of angle from 4 points
    """

    res = cv2.line(img, p1, p2, color)
    res = cv2.line(res, p2, p3, color)
    res = cv2.line(res, p3, p4, color)
    res = cv2.line(res, p4, p1, color)    
    
    return res

def drawRectangleFromAngle(img, h, w, cx, cy, angle, color):
    
    #aog = angle
    angle = angle / 180 * math.pi

    y1 = -w / 2 * math.sin(angle) + h / 2 * math.cos(angle) + cy
    y2 =  w / 2 * math.sin(angle) + h / 2 * math.cos(angle) + cy
    y3 =  w / 2 * math.sin(angle) - h / 2 * math.cos(angle) + cy
    y4 = -w / 2 * math.sin(angle) - h / 2 * math.cos(angle) + cy 

    x1 = -w / 2 * math.cos(angle) - h / 2 * math.sin(angle) + cx
    x2 =  w / 2 * math.cos(angle) - h / 2 * math.sin(angle) + cx
    x3 =  w / 2 * math.cos(angle) + h / 2 * math.sin(angle) + cx
    x4 = -w / 2 * math.cos(angle) + h / 2 * math.sin(angle) + cx

    p1 = (int(x1), int(y1))
    p2 = (int(x2), int(y2))
    p3 = (int(x3), int(y3))
    p4 = (int(x4), int(y4))

    res = cv2.line(img, p1, p2, color)
    res = cv2.line(img, p2, p3, color)
    res = cv2.line(img, p3, p4, color)
    res = cv2.line(img, p4, p1, color)    

    return res
