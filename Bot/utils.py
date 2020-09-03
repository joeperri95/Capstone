
#utility functions

import os


def espeak(string):
    os.popen('espeak "' + string + '"')

def kindReminder():
    os.popen('espeak "hey buddy I dont have all day"')
    
def func(x):
    return x + 1

def test_answer():
    assert func(3) == 5
