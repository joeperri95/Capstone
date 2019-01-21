#!/usr/bin/env python3.6

import socket
import threading
import queue
import sys

HOST = 'localhost'
PORT = 58000
ADDRESS = (HOST, PORT)
BUFF_SIZE = 4096

def main():

    #TODO read params from file        

    sock = socket.socket(socket.AF_INET, type=socket.SOCK_STREAM)
    
    try:
        sock.connect(ADDRESS)
        print("connection from {}".format(ADDRESS))

    except OSError:
        print('IP address in use try adjusting the port')
        sys.exit(-1)

    sys.stdout.write('>>')

    while(1):
        
        cmd = input()
        
        sock.send(cmd.encode('utf-8'))
        
        resp = sock.recv(BUFF_SIZE).decode('utf-8')
        print(resp)

        if(cmd.upper() == "QUIT"):
            break

        sys.stdout.write('>>')
    
    sock.close()
    
main()