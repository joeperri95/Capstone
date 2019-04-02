#!/usr/bin/env python3.6

import sys
sys.path.append('/home/joe/Capstone')

from Bot import Dispensor

import queue
import threading
import socket

def main():
    q = queue.Queue()
    ql = threading.Lock()

    disp = Dispensor.Dispensor()
    
    currentOrder = {'drink': '1'}

    while(True):
            if(currentOrder['drink'] == '1'):
                resp =  disp.orangejuice()
                if(resp):
                    print('oj')
                else:
                    print('error')

            elif( currentOrder['drink'] == '2'):
                resp =  disp.gingerAle()
                if(resp):
                        print('ginger ale')
                else:
                        print('error')

            elif( currentOrder['drink'] == '3'):
                resp =  disp.mimosa()
                if(resp):
                        print('good mimosa')
                else:
                        print('error')
       
          
if __name__ == '__main__':
    main()