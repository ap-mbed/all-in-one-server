__author__ = 'Jens'

import logging
from instruction16BitLoad import Instruction16BitLoad

# Class to encapsulate all necessary methods for a 16 bit instruction
class Instruction16Bit:
    def __init__(self, instruction):
        self.instruction = instruction
        logging.debug("16 bit instruction to decode: 0x%X" % self.instruction)

    def getRegister(self):
        """
            Function to return the register that
            must be bit-flipped
        """
        if not self._isBranch() and not self._mustSkip():
            if self._isNormalLoadStore() and self._isStore():
                logging.debug("Normal Store instruction, get Rt at [2:0]")
                register = self._getReg(0)
            elif self._isExceptionLoadStore() and self._isStore():
                logging.debug("Exceptional Store instruction, get Rt at [10:8]")
                register = self._getReg(8)
            else:
                logging.debug("Load or other instruction, get Rn at [5:3]")
                register = self._getReg(3)
            return register
        else:
            return -1

    def getMemoryAddressValues(self):
        """
            Function to return the necessary
            values to be able to calculate the
            memory address
        :return: dictionary containing the two necessary values
        """
        if not self._isBranch() and not self._mustSkip():
            if (self._isNormalLoadStore() or self._isExceptionLoadStore()) and not self._isStore():
                logging.debug("Load instruction, fetching values")
                load = Instruction16BitLoad(self.instruction)
                values = load.getNecessaryValues()
                return values
            else:
                logging.debug("Not a Load instruction")
                return None
        else:
            return None

    def getNecessaryValues(self):
        """
            Function to return the necessary memory location(s)
            to inject a fault instruction aware
        :return: either a register or a dictionary containing all values
        """
        if not self._isBranch() and not self._mustSkip():
            if self._isNormalLoadStore():
                logging.debug("Normal Load/Store instruction")
                if self._isStore():
                    logging.debug("Normal Store instruction, get Rt at [2:0]")
                    return self._getReg(0)
                else:
                    logging.debug("Normal Load instruction, fetching values")
                    load = Instruction16BitLoad(self.instruction)
                    return load.getNecessaryValues()
            elif self._isExceptionLoadStore():
                logging.debug("Exceptional Load/Store instruction")
                if self._isStore():
                    logging.debug("Exceptional Store instruction, get Rt at [10:8]")
                    return self._getReg(8)
                else:
                    logging.debug("Exceptional Load instruction, fetching values")
                    load = Instruction16BitLoad(self.instruction)
                    return load.getNecessaryValues()
            else:
                logging.debug("Other type of instruction, get Rn at [5:3]")
                return self._getReg(3)
        else:
            return None

    # Private methods
    def _isNormalLoadStore(self):
        """
            Function to determine if opcode matches
            the regular cases for load/store
            Opcode are bits [15:12]
        """
        # Use copy of instruction to be safe
        instr = self.instruction
        mask = (instr >> 12) & 0xF
        # Prepare conditions
        cond1 = (mask == 0b0110)
        cond2 = (mask == 0b0101)
        cond3 = (mask == 0b0111)
        cond4 = (mask == 0b1000)
        # If one of them holds, load/store instruction
        if cond1 or cond2 or cond3 or cond4:
            return True
        else:
            return False

    def _isExceptionLoadStore(self):
        """
            Function to determine if opcode matches
            the exception for load/store
            Opcode are bits [15:12]
        """
        # Use copy of instruction to be safe
        instr = self.instruction
        mask = (instr >> 12) & 0xF
        mask2 = (instr >>11) & 0x1F
        # Prepare conditions
        cond1 = (mask == 0b1001)
        cond2 = (mask == 0b1100)
        cond3 = (mask2 == 0b01001)
        # If match, load/store instruction
        if cond1 or cond2 or cond3:
            return True
        else:
            return False

    def _isStore(self):
        """
            Function to determine if instruction
            is a store instruction
            Determined by bit 11
        """
        # Use copy of instruction to be safe
        instr = self.instruction
        bit = (instr >> 11) & 1
        # If bit is 0, store instruction
        if bit == 0:
            return True
        else:
            return False

    def _getReg(self, bitPos):
        """
            Function to isolate and return the
            necessary register (3 bits wide)
            Start at bitPos
        """
        # Use copy of instruction to be safe
        instr = self.instruction
        register = (instr >> bitPos) & 0b111
        return register

    def _isBranch(self):
        """
            Function to determine if the instruction
            is a branch instruction
        :return: True if branch, False if not.
        """
        # Use copy of instruction to be safe
        instr = self.instruction
        mask1 = (instr >> 11) & 0x1F
        cond1 = (mask1 == 0x1C)
        mask2 = (mask1 >> 1) & 0xF
        cond2 = (mask2 == 0xD)
        if cond1 or cond2:
            logging.log(25, "Instruction is a branch instruction")
            return True
        else:
            logging.debug("Instruction is not a branch instruction")
            return False

    def _mustSkip(self):
        """
            Function to determine if the instruction
            starts with 0xBF..
        :return: True or False
        """
        # Use copy to be safe
        instr = self.instruction
        # Isolate opcode
        mask1 = (instr >> 8) & 0xFF
        cond1 = (mask1 == 0xBF)
        mask2 = (instr >> 9) & 0x7F
        cond2 = (mask2 == 0b1011110)
        cond3 = (mask2 == 0b1011010)
        if cond1 or cond2 or cond3:
            logging.log(25,"Instruction does not contain injection information (0xBF.., POP, PUSH...")
            return True
        else:
            logging.debug("Instruction contains injection information")
            return False

