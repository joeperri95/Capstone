
#utility functions

import os

def espeak(string):
    os.popen('espeak "' + string + '"')
