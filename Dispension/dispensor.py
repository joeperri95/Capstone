#!/usr/bin/env python3.6

import gpiozero
import threading
import time
import queue

DELAY = 1

class Dispensor(threading.Thread):
        
        def __init__(self, q, qLock):
                '''     
                q is a threadsafe queue that will hold orders
                qLock is a mutex for that queue

                '''
                self.pump1 = gpiozero.DigitalOutputDevice(27)  # Orange Juice
                self.pump2 = gpiozero.DigitalOutputDevice(22)  # Ginger Ale
                self.levelSensor = gpiozero.DigitalInputDevice(pin=17, bounce_time=0.05)
                self.delay = 1
                self.q = q
                self.qLock = qLock
                threading.Thread.__init__(self)

        def orangejuice(self):
                '''
                Dispense orange juice or beverage corresponding to pump 1
                '''
                while(not self.levelSensor.is_active):
                        self.pump1.on()
                        time.sleep(DELAY)
                        self.pump1.off()


        def gingerAle(self):
                '''
                Dispense ginger ale or beverage corresponding to pump 2
                '''
                while(not self.levelSensor.is_active):
                        self.pump2.on()
                        time.sleep(DELAY)
                        self.pump2.off()


        def mimosa(self):
                '''
                Dispense mimosa or beverage corresponding to both pumps
                '''
                while(not self.levelSensor.is_active):
                        self.pump1.on()
                        self.pump2.on()
                        time.sleep(DELAY)
                        self.pump1.off()
                        self.pump2.off()

        def run(self):
                '''
                Thread execution function
                '''
                while(1):
                        #block until lock is acquired
                        self.qLock.acquire()
                        if(not self.q.empty()):
                                order = self.q.get()
                                if(order == 1):
                                        self.orangejuice()
                                elif(order == 2):
                                        self.gingerAle()
                                elif(order == 3):
                                        self.mimosa()
                        time.sleep(0.01)
                        self.qLock.release()