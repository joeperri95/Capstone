
import gpiozero as gp
import time

class NavLEDmanager():

    def __init__(self):
        self.leftLED = gp.LED(24) # green
        self.rightLED = gp.LED(12) # green
        self.stopLED = gp.LED(13)

    def right(self):
        self.rightLED.on()
        self.leftLED.off()
        self.stopLED.off()
        
    def left(self):
        self.rightLED.off()
        self.leftLED.on()
        self.stopLED.off()
        
    def blinkLeft(self):
        self.rightLED.off()
        self.leftLED.blink(0.2, 0.2, 0, 0, 4)
        self.stopLED.off()
    
    def blinkRight(self):
        self.rightLED.blink(0.2, 0.2, 0, 0, 4)
        self.leftLED.off()
        self.stopLED.off()

    def stop(self):
        self.rightLED.off()
        self.leftLED.off()
        self.stopLED.blink(0.3, 0.3, 0.1, 0.1, 5)
            
    def straight(self):
        self.rightLED.on()
        self.leftLED.on()
        self.stopLED.off()

    def reset(self):
        self.rightLED.off()
        self.leftLED.off()
        self.stopLED.off()
    
    def blinkAll(self):
        self.rightLED.blink(0.2, 0.2, 0, 0, 10)
        self.leftLED.blink(0.2, 0.2, 0, 0, 10)
        self.stopLED.blink(0.2, 0.2, 0, 0, 10)
        

class BotLEDmanager():

    def __init__(self):
        self.cupLED = gp.LED(17) #
        self.doneLED = gp.LED(6) # 

    def done(self):
        self.cupLED.off()
        self.doneLED.blink(0.2, 0.2, 0, 0, 4)
        
    def cup(self):
        self.cupLED.blink(0.2, 0.2, 0, 0, 4)
        self.doneLED.off()

    def reset(self):
        self.cupLED.off()
        self.doneLED.off()

    def blinkAll(self):
        self.cupLED.blink(0.2, 0.2, 0, 0, 10)
        self.doneLED.blink(0.2, 0.2, 0, 0, 10)