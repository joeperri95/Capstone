import gpiozero

# setup of inputs and outputs
levelSensor = gpiozero.DigitalInputDevice(pin=17, bounce_time=0.05)
pump1 = gpiozero.DigitalOutputDevice(27)  # Oramge Juice
pump2 = gpiozero.DigitalOutputDevice(22)  # Ginger Ale


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
