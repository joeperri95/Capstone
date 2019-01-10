import gpiozero

# drill motor pin setup
elevator = gpiozero.PWMOutputDevice(pin=16)
direction = gpiozero.DigitalOutputDevice(pin=18)


def elevatorUp:
    direction.on()  # dturn moter CW
    elevator.on()

    # ramp up the motor in half a second
    for i in range(9):
        elevator.value += 0.1
        sleep(0.05)

    # hold motor at constant full power
    sleep(4)

    # ramp motor down in half a second
    for j in range(9):
        elevator.value -= 0.1
        sleep(0.05)

    elevator.off()


def elevatorDown:
    direction.off()  # dturn moter CCW
    elevator.on()

    # ramp up the motor in half a second
    for i in range(9):
        elevator.value += 0.1
        sleep(0.05)

    # hold motor at constant full power
    sleep(4)

    # ramp motor down in half a second
    for j in range(9):
        elevator.value -= 0.1
        sleep(0.05)

    elevator.off()
