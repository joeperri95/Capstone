
import sys 
sys.path.append("/home/pi/Capstone/Bot")

from Bot import Motors

def main():
    m = Motors.Motors()
    m.forwardTimed(0.01, 0.1)