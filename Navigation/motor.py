import gpiozero
import time

# motor pin setup
outM1Dir = gpiozero.DigitalOutputDevice(pin=17)
outM1Pwm = gpiozero.PWMOutputDevice(pin=18)
outM2Dir = gpiozero.DigitalOutputDevice(pin=6)
outM2Pwm = gpiozero.PWMOutputDevice(pin=13)

# longitudinal 
# direction = 0 or 1, pwm = 0 to 1
def longitudinal(direction, pwm, seconds): 
	startTime = time.time()
	elapsedTime = 0

	outM1Dir.value = direction
	outM2Dir.value = direction

	while elapsedTime < seconds:
		elapsedTime = time.time() - startTime
		outM1Pwm.value = pwm
		outM2Pwm.value = pwm

# lateral
# direction = 0 or 1
def lateral(direction, seconds):
	startTime = time.time()
	elapsedTime = 0

	outM1Dir.value = direction
	outM2Dir.value = ~direction

	while elapsedTime < seconds:
		elapsedTime = time.time() - startTime
		outM1Pwm.value = 0.25 % To be tune on final chassis
		outM2Pwm.value = 0.25 % To be tune on final chassis

