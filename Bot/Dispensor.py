#!/usr/bin/env python3.5

import gpiozero
import serial
import threading
import time
import queue
import utils

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
                #self.conn.write_timeout = 5.0

                #wait 90 seconds for dispension to run
                self.conn.timeout = 90.0
                self.conn.open()

        def orangejuice(self):
                '''
                Dispense orange juice or beverage corresponding to pump 1 and pump 2
                '''

                try:
                        #print('writing 1 to arduino')
                        self.conn.write(b'1')
                        echo = self.conn.read(1)
                        #print("got " + str(echo) + " from arduino")

                        if(ord(echo) == 255):
                                return False

                        while(True):
                                response = self.conn.read()
                                print(ord(response))
                                if(ord(response) == 5):
                                        print('done')
                                        return True

                                elif(ord(response) == 254):
                                        utils.kindReminder()

                                elif(ord(echo) == 255):
                                        return False

                except serial.SerialException as e:
                        print(e)
                        return False

                return False


        def gingerAle(self):
                '''
                Dispense ginger ale or beverage corresponding to pump 3
                '''

                try:
                        self.conn.write(b'2')
                        echo = self.conn.read()

                        if(ord(echo) == 255):
                                return False

                        while(True):
                                response = self.conn.read()
                                print(ord(response))
                                if(ord(response) == 5):
                                        print('done')
                                        return True

                                elif(ord(response) == 254):
                                        utils.kindReminder()

                                elif(ord(echo) == 255):
                                        return False


                except serial.SerialException as e:
                        print(e)
                        return False

                return False

        def mimosa(self):
                '''
                Dispense mimosa or beverage corresponding to both pumps
                '''

                try:
                        self.conn.write(b'3')
                        echo = self.conn.read()

                        if(ord(echo) == 255):
                                return False

                        while(True):
                                response = self.conn.read()
                                print(ord(response))
                                if(ord(response) == 5):
                                        print('done')
                                        return True

                                elif(ord(response) == 254):
                                        utils.kindReminder()

                                elif(ord(echo) == 255):
                                        return False

                except serial.SerialException as e:
                        print(e)
                        return False

                return False
