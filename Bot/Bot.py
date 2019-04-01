#!/usr/bin/env python3.5

import threading
import queue
import cv2
import os
import time
import sys

import Navigator
import botstates
import Dispensor
import Listener
import Pusher

listenerPort = 12345
pusherPort = 12346

class Bot(threading.Thread):
    def __init__(self, serverQueue, serverLock, location):

        #These variables deal with orders being processed from server
        self.serverQueue = serverQueue
        self.serverLock = serverLock
        self.currentOrder = None

        threading.Thread.__init__(self)

        #these variables handle the state of the machine
        self.state = botstates.IDLE
        self.prevState = botstates.IDLE

        #these variables determine location of machine
        self.location = location
        self.destinationQueue = queue.Queue()
        self.destination = location

        self.navigator = Navigator.Navigator("")
        self.dispensor = Dispensor.Dispensor()
        self.listener = Listener.Listener(listenerPort, self.serverQueue, self.serverLock)
        self.pusher = Pusher.Pusher(pusherPort, self.serverQueue, self.serverLock)

        self.listener.start()
        self.pusher.start()
    
    def update(self):
        
        pass

    def determineState(self):
        """
        determine state based on current state

        """
        
        pass

    def graph(self):
        #calculate route to destination
        


        pass

    def run(self):
        #do initialization

        while(True):

            self.update()

            if(self.state == botstates.IDLE):
                
                self.currentOrder = self.serverQueue.get(block=True)
                
                if(self.currentOrder.location != self.location):
                    self.destination = self.currentOrder.location
                    self.graph()
                    self.prevState = self.state
                    self.state = botstates.MOTION

                elif(self.currentOrder.location == self.location):
                    self.prevState = self.state
                    self.state = botstates.DISPENSING
                

            elif(self.state == botstates.MOTION):
                print('motion state')
                
                #self.navigator.start()

                #TODO delete this and add proper navigation 
                self.prevState = self.state
                self.state = botstates.DISPENSING

            elif(self.state == botstates.DISPENSING):
                
                if(self.currentOrder['drink'] == '1'):
                    resp = self.dispensor.orangejuice()
                    if(resp):
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR

                elif(self.currentOrder['drink'] == '2'):
                    resp = self.dispensor.gingerAle()
                    if(resp):
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR

                elif(self.currentOrder['drink'] == '3'):
                    resp = self.dispensor.mimosa()
                    if(resp):
                        self.prevState = self.state
                        self.state = botstates.IDLE
                    else:
                        self.prevState = self.state
                        self.state = botstates.ERROR


            elif(self.state == botstates.ALERT):
                pass
            
            elif(self.state == botstates.LINE_LOST):
                #perform recovery
                pass

            elif(self.state == botstates.ERROR):
                pass