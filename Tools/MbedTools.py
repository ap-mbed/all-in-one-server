#!/usr/bin/env python

import sys, getopt, time, shutil, os
import logging
import serial, serial.tools.list_ports

class ArgumentsException(Exception): pass
class DetectPortException(Exception): pass

class MbedTools:

	# Parameters
	file = None
	target = None
	port = None
	mode = "dist"

	def __init__(self, args):
		# Dont exist arguments
		if len(args) == 0: 
			raise ArgumentsException("Required arguments are 'f', 't'.")

		# Get arguments
		optlist, args = getopt.getopt(args, 'f:t:p', ['test'])

		# Still have arguments
		if len(args) > 0: 
			raise ArgumentsException("Possible arguments are 'f', 't', 'p', 'm'.")

		# Projdeme ziskane argumenty
		for key, val in optlist:
			# Filename
			if key == '-f': 
				self.file = val
			# Target
			if key == '-t': 
				self.target = val
			# Port
			if key == '-p': 
				self.port = val
			# Port
			if key == '--test': 
				self.mode = "test"

		if self.port is None:
			self.port = self.autoDetectPort()


	## Method for restart mbed on serial port
	def restartMbed(self):
		ser = self.getSerial()
		ser.isOpen()
		ser.sendBreak()
		ser.close()


	## Method for open serial port for communication
	def getSerial(self):
		return serial.Serial(
			port = self.getPort(),
			baudrate = 9600,
			#parity = serial.PARITY_NONE,
			#stopbits = serial.STOPBITS_ONE,
			#bytesize = serial.SEVENBITS
		)


	## Get port name (depands on OS)
	def getPort(self):
		return '\\.\\' + self.port if sys.platform.startswith('win') else self.port


	## Copy file to mbed device and call restart
	def copy(self, restart = False):
		output = self.getDestPath()
		shutil.copy(self.file, output)

		if restart:
			time.sleep(2) # Delay for finish copy
			self.restartMbed()

		return output


	## Get filename for target (in test mode is prefixed by 'test.')
	def getDestPath(self):
		if self.mode == 'test':
			filename = os.path.basename(self.file)
			return os.path.join(self.target, "test." + filename)
		else:
			return self.target


	## Mbed port auto detection
	def autoDetectPort(self):
		# Get list of port with keyword "mbed"
		if sys.platform.startswith('win'):
			ports = list(serial.tools.list_ports.grep('mbed'))
		else:
			ports = list(serial.tools.list_ports.grep('/dev/ttyACM'))

		# No port
		if len(ports) == 0:
			raise DetectPortException("Not possible auto-detect mbed port.")

		port = ports[0]
		logging.info('Auto detect port: %s' % str(port))
		sys.stdout.flush()

		# Get the first one
		return port[0]

