#!/usr/bin/env python3.5

import sys 
sys.path.append("/home/pi/Capstone/Bot")

from Bot import Navigator
from Bot import directions

def main():
    nav = Navigator.Navigator((3,3), direction=1,location=(3,2))
    nav.start()

if __name__ == '__main__':
    main()