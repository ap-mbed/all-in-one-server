#!/usr/bin/env python

from pyOCD.board import MbedBoard
import time
import logging
import sys

class TestCore:

	# Debug mode
	PRINT_INFO = False

	# Board
	board = None
	initSleepTime = 0

	def __init__(self, board = None):
		if board is None:
			self.chooseBoard()

	def chooseBoard(self):
		self.board = MbedBoard.chooseBoard()

	def getTarget(self):
		return self.board.target

	def getFlash(self):
		return self.board.flash

	def runTests(self):
		raise NotImplementedError("Method 'runTests' must be implemented!")

	def clean(self):
		self.board.uninit()

	def initSleep(self):
		time.sleep(self.initSleepTime)


	## Print to stdout
	#  @param  self  Object
	#  @param  value Messages
	def printInfo(self, *msgs):
		if self.PRINT_INFO and msgs is not None:
			for msg in msgs:
				sys.stdout.write(msg)
			sys.stdout.flush()	