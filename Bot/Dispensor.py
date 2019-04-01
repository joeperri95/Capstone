#!/usr/bin/env python3.5

import gpiozero
import serial
import threading
import time
import queue

DELAY = 1

class Dispensor():
        
        def __init__(self):
                '''     
                Initialize serial module and send commands

                '''

                self.conn = serial.Serial()
                self.conn.baudrate = 9600
                self.conn.port = '/dev/ttyACM0'
                #wait 5 seconds at most to write
                #otherwise assume arduino is closed
                self.conn.write_timeout = 5.0
                
                #wait 90 seconds for dispension to run
                self.conn.timeout = 90.0
                self.conn.open()

        def orangejuice(self):
                '''
                Dispense orange juice or beverage corresponding to pump 1
                '''
        
                try:        
                        self.conn.write('oj')
                        response = self.conn.read()

                        if(response == 'done'):
                                pass

                except serial.SerialException as e:
                        print(e)
                


        def gingerAle(self):
                '''
                Dispense ginger ale or beverage corresponding to pump 2
                '''
                try:
                        self.conn.write('ga')
                        response = self.conn.read()

                        if(response == 'done'):
                                pass

                except serial.SerialException as e:
                        print(e)
                

        def mimosa(self):
                '''
                Dispense mimosa or beverage corresponding to both pumps
                '''
                try:
                        self.conn.write('mimosa')
                        response = self.conn.read()

                        if(response == 'done'):
                                pass

                except serial.SerialException as e:
                        print(e)
                