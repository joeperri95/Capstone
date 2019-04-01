import sys
sys.path.append('/home/pi/Capstone/Bot')

from Bot import Dispensor

def main():

    disp = Dispensor.Dispensor()

    while(True):
        order = input("enter order")
        
        if(order.upper() == 'ORANGE JUICE'):
            disp.orangejuice()
        elif(order.upper() == 'GINGER ALE'):
            disp.gingerAle()
        elif(order.upper() == 'MIMOSA'):
            disp.mimosa()
        else:
            print("invalid order")
        