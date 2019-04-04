
UP = 1
DOWN = 2
LEFT = 3
RIGHT = 4

def getDir(inputStr):
    
    inputStr = str(inputStr)

    if(inputStr.upper() == "UP" or inputStr == str(UP)):
        return UP

    elif(inputStr.upper() == "DOWN" or inputStr == str(DOWN)):
        return DOWN
    
    elif(inputStr.upper() == "LEFT" or inputStr == str(LEFT)):
        return LEFT

    elif(inputStr.upper() == "RIGHT" or inputStr == str(RIGHT)):
        return RIGHT

    else:
        return None


def getStr(inputNum):

    if(inputNum == UP):
        return "UP"

    elif(inputNum == DOWN):
        return "DOWN"

    elif(inputNum == LEFT):
        return "LEFT"

    elif(inputNum == RIGHT):
        return "RIGHT"