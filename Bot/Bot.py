#!/usr/bin/env python3.5

import threading
import queue
import cv2
import os
import time
import sys

from . import Navigator
from . import botstates
from . import Dispensor
from . import Listener
from . import Pusher
from . import directions
from . import LEDManager
#import Motors

listenerPort = 12345
pusherPort = 12346

class Bot(threading.Thread):
    def __init__(self, serverQueue, serverLock, location, direction):

        #These variables deal with orders being processed from server
        self.serverQueue = serverQueue
        self.serverLock = serverLock
        self.currentOrder = None

        threading.Thread.__init__(self)

        #these variables handle the state of the machine
        self.state = botstates.IDLE
        self.prevState = botstates.IDLE

        self.leds = LEDManager.BotLEDManager()
        self.navigator = Navigator.Navigator(directions.getDir(direction), location)
        self.dispensor = Dispensor.Dispensor()
        self.listener = Listener.Listener(listenerPort, self.serverQueue, self.serverLock)
        self.pusher = Pusher.Pusher(pusherPort, self.serverQueue, self.serverLock)

        self.listener.start()
        self.pusher.start()

    def run(self):
        #do initialization

        while(True):

            if(self.state == botstates.IDLE):
                
                self.currentOrder = self.serverQueue.get(block=True)
                
                if(self.currentOrder.location != self.navigator.getDestination()):
                    self.destination = self.currentOrder.location    
                    self.prevState = self.state
                    self.state = botstates.MOTION

                elif(self.currentOrder.location == self.navigator.getDestination()):
                    self.prevState = self.state
                    self.state = botstates.DISPENSING
            

            elif(self.state == botstates.MOTION):                
                self.navigator = Navigator.Navigator(directions.getDir(self.navigator.direction), self.navigator.location)
                self.navigator.start()
                try:
                    self.navigator.join()
                except Exception as e:
                    self.prevState = self.state
                    self.state = botstates.LINE_LOST

                self.prevState = self.state
                self.state = botstates.DISPENSING

            elif(self.state == botstates.DISPENSING):
                
                if(self.currentOrder['drink'] == '1'):
                    resp = self.dispensor.orangejuice()
                    if(resp):
                        self.leds.done()
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR

                elif(self.currentOrder['drink'] == '2'):
                    self.leds.done()
                    resp = self.dispensor.gingerAle()
                    if(resp):
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR

                elif(self.currentOrder['drink'] == '3'):
                    self.leds.done()
                    resp = self.dispensor.mimosa()
                    if(resp):
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR

            elif(self.state == botstates.LINE_LOST):
                #perform recovery
                #utils.espeak('"line has been lost"')
                self.leds.blinkAll()

            elif(self.state == botstates.ERROR):
                #utils.espeak('"error dispensing drink"')
                self.leds.blinkAll()