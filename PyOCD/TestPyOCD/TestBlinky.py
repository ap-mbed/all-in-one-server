#!/usr/bin/env python

import time, sys, inspect, os
import logging

path = os.path.dirname(inspect.getfile(inspect.currentframe()))
sys.path.insert(1, os.path.join(path, '..', 'Tools'))

from Core.TestCore import TestCore
from Core.TestException import TestException
from Lib.termcolor import colored
from CopyToMbed import CopyToMbed

logging.basicConfig(level=logging.ERROR)

class BlinkyTest(TestCore):

	# Debug mode
	PRINT_INFO = True

	initSleepTime = 2

	# Adress to memory of each led
	addresses = {
		1: 0x2009C034,
		2: 0x2009C034,
		3: 0x2009C034,
		4: 0x2009C034,
	}

	# Mask for detecting if led is ON
	masks = {
		1: 0x00040000, # 18-bit
		2: 0x00100000, # 20-bit
		3: 0x00200000, # 21-bit
		4: 0x00800000, # 23-bit
	}

	def isLedOn(self, target, led):
		address = self.addresses[led]
		mask = self.masks[led]
		num = target.readMemory(address);
		return num & mask > 0

	def runTests(self, cleanAfter = True):
		self.runTest_1()

		# Clean
		if cleanAfter:
			self.clean()

	def runTest_1(self):

		# Test info
		self.printInfo(
			colored("--- TestBlinky - Test no. 1 (start) ---\n", "yellow"),
			"Assumption:\n",
			"\t - Start up takes max 2s.\n",
			"\t - Led are regularly illuminated.\n",
			"\t - Led is 'ON' for 2s and after switch 'OFF' is 1s delay.\n",
			colored("---\n\r", "yellow")
		)

		# Get target
		target = self.getTarget()

		# Reset
		target.reset()

		# Wait for setup
		self.initSleep()

		# Find start of the cycle
		found = False
		maxAttempts = 60
		period = 0.1
		while found is False:
			# Test if the first led is ON
			target.halt()
			if self.isLedOn(target, 1):
				found = True
				self.printInfo("Finding the start of the cycle: ", colored('PASS', 'green'), "\n")
				#target.resume()
				break
			target.resume()

			# Checkf number of attempts
			maxAttempts = maxAttempts - 1
			if maxAttempts is 0:
				self.printInfo("Finding the start of the cycle: ", colored('FAIL', 'red'), "\n")
				raise TestException("Finding the start of the cycle failed!")

			# Delay for other attempt
			time.sleep(period)
			
		# Start test the cycle
		cycleAttempts = 3
		try:
			for i in range(1, cycleAttempts + 1):
				self.printInfo('Cycle no. ' + str(i) + ': ')
				
				for led in range(1, 5):

					# Check leds
					target.halt()
					for y in range(1, 5):
						if y == led:
							assert self.isLedOn(target, y) is True, "[%d on] The led %d should be %s" % (led, y, 'on')
						else:
							assert self.isLedOn(target, y) is False, "[%d on] The led %d should be %s" % (led, y, 'off')
					target.resume()

					# Wait for off
					time.sleep(1.99)
					target.halt()
					for y in range(1, 5):
						assert self.isLedOn(target, y) is False, "[%d off] The led %d should be %s" % (led, y, 'off')
					target.resume()

					# Delay
					time.sleep(0.98)
				
				self.printInfo(colored("PASS", "green"), "\n")

		except (AssertionError) as e:
			self.printInfo(colored("FAIL", "red"), "\n")
			self.printInfo("AssertionError: ", str(e), "\n")
			raise TestException()

		finally:
			# Test info
			self.printInfo(
				colored("\n--- TestBlinky - Test no. 1 (end) ---", "yellow"),
				"\n\n"
			)

if __name__ == '__main__':
	# Copy file to target adn restart
	inst = CopyToMbed(sys.argv[1:])
	testFilename = inst.copy(True)
	time.sleep(1)

	try:
		test = BlinkyTest()
		test.runTests()
	except Exception as e:
		raise # re-raise the error
	finally:
		try:
		    os.remove(testFilename)
		    inst.restartMbed()
		except OSError:
			pass
