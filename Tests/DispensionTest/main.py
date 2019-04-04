import sys
sys.path.append('/home/pi/Capstone')

from Bot import Dispensor

def main():

    disp = Dispensor.Dispensor()

    while(True):
        order = input("enter order")
        
        if(order.upper() == 'ORANGE JUICE'):
            
            if(disp.orangejuice()):
                print("good oj")

        elif(order.upper() == 'GINGER ALE'):
            if(disp.gingerAle()):
                print("good ginger ale")
        elif(order.upper() == 'MIMOSA'):
            if(disp.mimosa()):
                print("good mimosa")
        else:
            print("invalid order")
        