__author__ = 'Jens Vankeirsbilck'

from pyOCD.board import MbedBoard
import logging


class PCinjector:
    def __init__(self, board=None):
        if board is None:
            try:
                self.board = self._initialize()
                self.target = self.board.target
            except Exception as e:
                logging.error("Failed to initialize PCinjector!\n%s" % e)
        else:
            self.board = board
            self.target = self.board.target

    def readPC(self):
        PC = None
        try:
            self.target.halt()
            PC = self.target.readCoreRegister('pc')
            logging.debug("PC = 0x%X" % PC)
        except Exception as e:
            logging.error("Failed to read PC!\n%s" % e)
            raise Exception("Could not read PC!")
        finally:
            if PC is not None:
                return PC

    def writeNewPC(self, newPC):
        try:
            self.target.halt()
            self.target.writeCoreRegister('pc', newPC)
            logging.debug("Written 0x%X to PC" % newPC)
        except Exception as e:
            logging.error("Failed to write to PC!\n%s" % e)
            raise Exception("Could not write to PC!")
        finally:
            self.target.resume()

    def reset(self):
        try:
            self.target.reset()
        except Exception as e:
            logging.error("Error while resetting device\n%s" % e)
            start = input("Disconnect device, reconnect, press reset. Then hit SPACE and ENTER\n")
            self.__init__()
            logging.debug("can continue % start\n")


    # Private Methods
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
