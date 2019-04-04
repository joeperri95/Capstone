#!/usr/bin/env python3.5

import time
import gpiozero

class Motors():

	def __init__(self):
		self.M1 = gpiozero.PhaseEnableMotor(17, 18)
		self.M2 = gpiozero.PhaseEnableMotor(6, 13)

	# forwards longitudinal 
	# pwm = 0 to 1
	def forwardTimed(self, pwm, seconds): 
		startTime = time.time()
		elapsedTime = 0

		while elapsedTime < seconds:
			elapsedTime = time.time() - startTime
			self.M1.forwards(pwm) 
			self.M2.forwards(pwm)

	# backwards longitudinal 
	# pwm = 0 to 1
	def backwardTimed(self, pwm, seconds): 
		startTime = time.time()
		elapsedTime = 0

		while elapsedTime < seconds:
			elapsedTime = time.time() - startTime
			self.M1.backward(pwm) 
			self.M2.backward(pwm)

	# rotate left 
	def leftTimed(self, pwm, seconds):
		startTime = time.time()
		elapsedTime = 0
		
		while elapsedTime < seconds:
			elapsedTime = time.time() - startTime
			self.M1.forward(pwm)
			self.M2.backward(pwm)

	# rotate right
	def rightTimed(self, pwm, seconds):
		
		startTime = time.time()
		elapsedTime = 0
		
		while elapsedTime < seconds:
			elapsedTime = time.time() - startTime
			self.M1.backward(pwm)
			self.M2.forward(pwm)

	# directly give motors value
	def setMotors(self, m1, m2):

		if(m1 > 0):
			self.M1.forward(m1)
		elif(m1 < 0):
			self.M1.backward(m1)
		elif(m1 == 0):
			self.M1.stop()

		if(m2 > 0):
			self.M2.forward(m2)
		elif(m2 < 0):
			self.M2.backward(m2)
		elif(m2 == 0):
			self.M2.stop()

		
	def stop(self):
		self.M1.stop()
		self.M2.stop()
