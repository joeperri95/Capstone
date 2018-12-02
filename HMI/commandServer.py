#!/usr/bin/env python3.6

import socket
import queue
import threading
import sys
import time
import datetime
import logging

HOST = 'localhost'
PORT = 58000
ADDRESS = (HOST, PORT)
BUFF_SIZE = 4096


class commandServer:
    def __init__(self, filename):
        
        self.HOST, self.PORT, self.BUFF_SIZE = self.readFile(filename)

    def readFile(self, filename):

        




sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

logging.basicConfig(format = "%(asctime)s %(levelname)s %(message)s", filename="server.log", level=logging.DEBUG)

try:
    sock.bind(ADDRESS)

except OSError:
    logging.error("IP address in use try adjusting the port")
    print("IP address in use try adjusting the port")
    sys.exit(-1)

print("waiting for connections")
sock.listen(1)

def getTimeStamp():

    stamp = time.time()
    prettyTimestamp = datetime.datetime.fromtimestamp(stamp).strftime('%Y-%m-%d %H:%M:%S')
    return prettyTimestamp

def doit(sock):
    while True:

        data, _ = sock.recvfrom(BUFF_SIZE)
        addr = sock.getpeername() 
        
        if(data):

            data = data.decode('utf-8')
            
            #Log this
            logging.info("address: {}, message: {}".format(addr, data))
            print("{}: address: {}, message: {}".format(getTimeStamp(), addr, data))

            paramList = data.split(' ')
            cmd = paramList[0].upper()

            if(cmd == "QUIT"):
                sock.send("Bye".encode('utf-8'))
                break

            elif(cmd == "HELP"):

                helpstr = """

                Commands:
                    Quit: exit program
                    Go: go to station
                    Order: fill order
                    Base: ignore orders return to base
                    Help: display this message

                """

                sock.send(helpstr.encode('utf-8'))

            elif(cmd == "GO"):
                if(len(paramList) == 1):
                    sock.send("Please enter stations to go to".encode('utf-8'))
                else:
                    sock.send('this function has not been implemented yet'.encode('utf-8'))

            elif(cmd == "ORDER"):
                sock.send('this function has not been implemented yet'.encode('utf-8'))

            elif(cmd == "BASE"):
                sock.send('this function has not been implemented yet'.encode('utf-8'))

            else:
                sock.send('Command not recognized type "help" for a list of commands'.encode('utf-8'))


            
    print("{}: {} has disconnected".format(getTimeStamp(), addr))
    sock.close()


def main():

    while(1):        

        connection, client_address = sock.accept()  
        logging.info(f": connection from {client_address}")
        print(f'{getTimeStamp()}: connection from {client_address}')

        t = threading.Thread(target=doit,args=(connection,))
        t.start()
    
    t.join()
    sock.close()

    
if __name__ == "__main__":
    
    main()
