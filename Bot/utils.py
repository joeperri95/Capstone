
#utility functions

import os

def espeak(string):
    os.popen('espeak "' + string + '"')

def kindReminder():
    os.popen('espeak "hey buddy I dont have all day"')