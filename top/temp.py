import threading
import queue
import cv2
import os
import time
import sys

from Navigation import BotStates

class Bot(threading.Thread):
    def __init__(self, serverQueue, serverLock, location):

        #These variables deal with orders being processed from server
        self.serverQueue = serverQueue
        self.serverLock = serverLock
        self.currentOrder = None

        threading.Thread.__init__(self)

        #these variables handle the state of the machine
        self.state = BotStates.IDLE
        self.prevState = BotStates.IDLE

        #these variables determine location of machine
        self.location = location
        self.destinationQueue = queue.Queue()
        self.destination = location
    
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

            if(self.state == BotStates.IDLE):
                
                self.currentOrder = self.serverQueue.get(block=True)
                
                if(self.currentOrder.location != self.location):
                    self.destination = self.currentOrder.location
                    self.graph()
                    self.prevState = self.state
                    self.state = BotStates.MOTION
                

            elif(self.state == BotStates.MOTION):
                pass

            elif(self.state == BotStates.WAITING_FOR_CUP):
                pass

            elif(self.state == BotStates.DISPENSING):
                pass

            elif(self.state == BotStates.WAITING_FOR_RETRIEVAL):
                pass

            elif(self.state == BotStates.ALERT):
                pass
            
            elif(self.state == BotStates.LINE_LOST):
                #perform recovery
                pass