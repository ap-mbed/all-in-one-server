__author__ = 'Jens Vankeirsbilck'

from pyOCD.board import MbedBoard
import logging


class SpecialRegisterFaultInjector:
    def __init__(self):
        try:
            self.board = self._initialize()
            self.target = self.board.target
        except Exception as e:
            logging.error("Failed to initialize PCFaultInjector!\n%s" % e)

    def __init__(self,board):
        self.board = board
        self.target = self.board.target

    # public functions
    def unInit(self):
        if self.board != None:
            logging.info("Board uninitialised")
            self.board.uninit()

    def flipPC(self, bitToFlip, address=None):
        self._injectFault('pc', bitToFlip, address)

    def flipSP(self, bitToFlip, address=None):
        self._injectFault('sp', bitToFlip, address)

    def flipLR(self, bitToFlip, address=None):
        self._injectFault('lr',  bitToFlip, address)

    def flipXPSR(self, bitToFlip, address=None):
        self._injectFault('xPSR', bitToFlip, address)

    # private functions
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

    def _injectFault(self, reg, bitToFlip, address=None):
        inject = 1
        mask = 1 << bitToFlip
        try:
            self.target.halt()
            if address is not None:
                flag = self.target.readMemory(address)
                inject = flag & 1
            if inject == 1:
                value = self.target.readCoreRegister(reg)
                newValue = value ^ mask
                self.target.writeCoreRegister(reg, newValue)
                logging.log(25, "{} was injected, value was 0x{:X} and is changed to 0x{:X}".format(reg,value, newValue))
            else:
                logging.log(25, "Flag at address 0x%X was 0, No fault injected!" % address)
        except Exception as e:
            logging.error("Failed to inject a fault into {}\n{}".format(reg, e))
        finally:
            self.target.resume()