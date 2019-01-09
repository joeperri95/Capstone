import gpiozero

# setup of inputs and outputs
levelSensor = gpiozero.DigitalInputDevice(pin=11, bounce_time=0.05)
pump1 = gpiozero.DigitalOutputDevice(13)  # Oramge Juice
pump2 = gpiozero.DigitalOutputDevice(15)  # Ginger Ale


def orangejuice:
    while(!levelSensor.is_active()):
        pump1.on()
        sleep(1)
        pump1.off()


def gingerAle:
    while(!levelSensor.is_active()):
        pump2.on()
        sleep(1)
        pump2.off()


def mimosa:
    while(!levelSensor.is_active()):
        pump1.on()
        pump2.on()
        sleep(1)
        pump1.off()
        pump2.off()
