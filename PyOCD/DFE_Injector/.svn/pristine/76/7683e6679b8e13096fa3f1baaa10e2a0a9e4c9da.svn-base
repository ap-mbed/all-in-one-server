__author__ = 'Jens Vankeirsbilck'

import logging
import random
from pyOCD.board import MbedBoard


class I2CFaultInjector:
    def __init__(self, sda,  scl):
        try:
            self.board = self._initialize()
            self.target = self.board.target
            if sda == 9 or sda == 28:
                self.sda = sda
                if sda == 9:
                    self.powerBit = 19
                    self.I2CONSET = 0x4005C000
                    self.I2STAT = 0x4005C004
                    self.I2DAT = 0x4005C008
                    self.I2SCLH = 0x4005C010
                    self.I2SCLL = 0x4005C014
                    self.I2CONCLR = 0x4005C018
                    self.I2DataBuffer = 0x4005C02C
                else:
                    self.powerBit = 26
                    self.I2CONSET = 0x400A0000
                    self.I2STAT = 0x400A0004
                    self.I2DAT = 0x400A0008
                    self.I2SCLH = 0x400A0010
                    self.I2SCLL = 0x400A0014
                    self.I2CONCLR = 0x400A0018
                    self.I2DataBuffer = 0x400A002C
            else:
                raise Exception("sda must be pin 9 or pin 28")
            if scl == 10 or scl == 27:
                self.scl = scl
            else:
                raise Exception("scl must be pin 10 or pin 27")
        except Exception as e:
            logging.error("Could not initialize I2CFaultInjector\n%s" % e)

    # Public methods
    def unInit(self):
        if self.board is not None:
            logging.info("Board uninitialised")
            self.board.uninit()

    def toggleI2CPower(self):
        """
            Function to turn I2C communication
            on or off
        """
        mask = 1 << self.powerBit
        try:
            self.target.halt()
            # Read PCONP
            current = self.target.readMemory(0x400FC0C4)
            newContent = current ^ mask
            self.target.writeMemory(0x400FC0C4, newContent)
            powerBit = current >> self.powerBit
            if powerBit == 0:
                logging.log(25, "powerBit was 0, turned I2C on")
            else:
                logging.log(25, "powerBit was 1, turned I2C off")
        except Exception as e:
            logging.error("Failed to turn on/off I2C\n%s" % e)
        finally:
            self.target.resume()

    def injectFaultI2CONSET(self,bitPos=None):
        """
            Function to inject a fault in the I2CxCONSET register
        """
        self._injectFault("I2CONSET", self.I2CONSET,bitPos)

    def injectFaultI2DAT(self, bitPos=None):
        """
            Function to inject a fault in the I2DAT register
        """
        self._injectFault("I2DAT", self.I2DAT, bitPos)

    def injectFaultI2SCLH(self, bitPos=None):
        """
            Function to inject a fault in the I2SCLH register
        """
        self._injectFault("I2SLH", self.I2SCLH, bitPos)

    def injectFaultI2SCLL(self, bitPos=None):
        """
            Function to inject a fault in the I2SCLH register
        """
        self._injectFault("I2SCLL", self.I2SCLL, bitPos)

    def injectFaultI2CONCLR(self, bitPos=None):
        """
            Function to inject a fault in the I2CxCONCLR register
        """
        self._injectFault("I2CONCLR", self.I2CONCLR, bitPos)

    def injectFaultI2DataBuffer(self, bitPos=None):
        """
            Function to inject a fault in the I2DATA_BUFFER register
        """
        self._injectFault("I2DATABUFFER", self.I2DataBuffer, bitPos)

    # Private methods
    def _initialize(self):
        """
            Initialize mbed
        :return: board encapsulating the mbed
        """
        board = None
        try:
            # Search and initialize mbed
            board = MbedBoard.chooseBoard()

            # Confirm LPC1768
            if board.getTargetType() == "lpc1768":
                logging.debug("Target type mbed lpc1768 found")
            else:
                raise Exception("Only NXP LPC1768 supported")
        finally:
            if board is not None:
                return board

    def _injectFault(self, regName, registerAddress, bitPos = None):
        """
            Function to inject a fault at the given address
        :param registerAddress: address of the register that must be bit-flipped
        """
        if bitPos is None:
            bitPos = random.randint(0, 7)
        mask = 1 << bitPos
        try:
            self.target.halt()
            # Read I2STAT
            current = self.target.readMemory(registerAddress)
            logging.debug("Current content: 0x%X" % current)
            # Flip content
            newContent = current ^ mask
            logging.debug("New content: 0x%X" % newContent)
            # Write new content
            self.target.writeMemory(registerAddress, newContent)
            logging.log(25, "Succesfully injected fault into %s" % regName)
        except Exception as e:
            logging.error("Could not inject fault into 0x{%X}\n{}".format(registerAddress, e))
        finally:
            self.target.resume()
