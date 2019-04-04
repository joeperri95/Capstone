#!/usr/bin/env python3.5

import sys 
sys.path.append("/home/pi/Capstone/Bot")

from Bot import Navigator

def main():
    nav = Navigator.Navigator()
    nav.start()

if __name__ == '__main__':
    main()