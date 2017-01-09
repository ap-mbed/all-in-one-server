__author__ = 'Jens Vankeirsbilck'

from instruction.instruction import Instruction
from pyOCD.board import MbedBoard
import logging


# Class to encapsulate all methods to inject faults into memory
class MemoryFaultInjector:
    def __init__(self):
        try:
            self.board = self._initialize()
            self.target = self.board.target
        except Exception as e:
            logging.error("Initialization of MemoryFaultInjector failed!\n %s" % e)

    # public functions
    def unInit(self):
        if self.board != None:
            logging.info("Board uninitialised")
            self.board.uninit()

    def injectAtSP(self, bitToFlip):
        try:
            self.target.halt()
            logging.debug("Reading SP")
            address = self.target.readCoreRegister('sp')
            logging.debug("Injecting fault into location SP points to")
            self._injectFaultMemoryLocation(address, bitToFlip)
        except Exception as e:
            logging.error("Could not inject fault at location SP points to\n%s" % e)
        finally:
            self.target.resume()

    def injectMemoryLocationInstructionAware(self, bitPos):
        success = False
        tries = 5
        try:
            self.target.halt()
            while not success and tries > 0:
                instr = Instruction(self.target)
                values = instr.getMemoryAddressValues()
                if values is not None:
                    success = True
                    if 'Rn' in values:
                        base = self._readReg(values['Rn'])
                        offset = self._readReg(values['Rm'])
                        if 'shift' in values:
                            offset = offset << values['shift']
                        memAddress = base + offset
                    else:
                        base = self._readReg(values['base'])
                        if 'U' in values:
                            if values['U'] == 1:
                                memAddress = base + values['offset']
                            else:
                                memAddress = base - values['offset']
                        else:
                            memAddress = base + values['offset']
                    self._injectFaultMemoryLocation(memAddress, bitPos)
                else:
                    logging.log(25, "Values was None, instruction does not need memory --> No fault injected")
                    tries -= 1
                    self.target.step()
        except Exception as e:
            logging.error("Could not calculate address or inject at address\n%s" % e)

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

    def _injectFaultMemoryLocation(self, memAddress, bitToFlip):
        try:
            mask = 1 << bitToFlip
            logging.debug("Reading memory location")
            current = self.target.readMemory(memAddress)
            newCurrent = current ^ mask
            logging.debug("Writing new content to memory location")
            self.target.writeMemory(memAddress, newCurrent)
            logging.log(25, "successfully injected fault into 0x%X" % memAddress)
            logging.debug("Value was 0x{:X}, changed to 0x{:X}".format(current, newCurrent))
        except Exception as e:
            logging.error("Could not inject fault into 0x{:X}\n{}".format(memAddress, e))
        finally:
            self.target.resume()

    def _readReg(self, register):
        try:
            value = self.target.readCoreRegister(register)
            return value
        except Exception as e:
            logging.error("Could not read register {}\n{}".format(register, e))


    def _readMemLoc(self, address):
        self.target.halt()
        time = self.target.readMemory(address)
        self.target.resume()
        print (time)