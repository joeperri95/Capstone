import gpiozero
import time

class Elevator():
    '''
    Elevator controller class
    As of now this does not need to be multithreaded the main program will cede control
    '''

    def __init__(self, initialState):
        '''
        takes inital state of elevator as argument (UP/DOWN)
        '''        
        self.elevator = gpiozero.PhaseEnableMotor(24, 4)
        
        if(str.upper(initialState) == 'UP' or str.upper == 'DOWN'):
            self.state = initialState
        else:
            raise ValueError("Please enter state UP or DOWN")

    def elevatorUp(self):
        '''
        If elevator is down raise it
        '''

        if self.state == "UP":
            return

        self.elevator.on()

        # ramp up the motor in half a second
        for i in range(9):
            self.elevator.value += 0.1
            time.sleep(0.05)

        time.sleep(4)

        for j in range(9):
            self.elevator.value -= 0.1
            time.sleep(0.05)

        self.elevator.off()
        self.state = 'UP'

    def elevatorDown(self):
        '''
        If elevator is up lower it
        '''

        if(self.state == 'DOWN'):
            return

        self.elevator.on()

        # ramp up the motor in half a second
        for i in range(9):
            self.elevator.value -= 0.1
            time.sleep(0.05)

        time.sleep(4)

        for j in range(9):
            self.elevator.value += 0.1
            time.sleep(0.05)

        self.elevator.off()
        self.state == 'DOWN'
