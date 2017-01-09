__author__ = 'Jens'

import logging
from instruction32BitLoad import Instruction32BitLoad

# Class to encapsulate all necessary methods for a 32 bit instruction
class Instruction32Bit:
    def __init__(self, HW1, HW2):
        self.HW1 = HW1
        self.HW2 = HW2
        logging.debug("Instruction to debug: 0x{:X}{:X}".format(self.HW1, self.HW2))

    def getRegister(self):
        """
            Function to return the necessary register
        """
        if not self._isBranch() and not self._isNOP():
            if self._isLoadStore() and self._isStore():
                logging.debug("Store instruction, get Rt at HW2 [15:12]")
                register = self._getRt()
            else:
                logging.debug("Load or other instruction, get Rn at HW1 [3:0]")
                register = self._getRn()
            return register
        else:
            return -1

    def getMemoryAddressValues(self):
        if not self._isBranch() and not self._isNOP():
            if self._isLoadStore() and not self._isStore():
                logging.debug("Load instruction, extracting values")
                instr32Load = Instruction32BitLoad(self.HW1, self.HW2)
                values = instr32Load.getNecessaryValues()
                return values
            else:
                logging.debug("Not a Load instruction")
                return None
        else:
            return None

    def getNecessaryValues(self):
        """
            Function to return all necessary values to
            inject a fault instruction aware
        :return: a register or dictionary containing all values
        """
        if not self._isBranch() and not self._isNOP():
            if self._isLoadStore():
                logging.debug("Load/Store instruction")
                if self._isStore():
                    logging.debug("Store instruction, get Rt at HW2 [15:12]")
                    return self._getRt()
                else:
                    logging.debug("Load instruction, extracting values")
                    instr32Load = Instruction32BitLoad(self.HW1, self.HW2)
                    return instr32Load.getNecessaryValues()
            else:
                logging.debug("Other instruction, get Rn at HW1 [3:0]")
                return self._getRn()
        else:
            return None

    def _isLoadStore(self):
        """
            Function to determine if the instruction
            is a load/store instruction
        """
        # Use a copy to be safe
        hw1 = self.HW1
        # Create mask and determine type
        mask = (hw1 >> 8) & 0b11111111
        # Create conditions
        cond1 = (mask == 0b11111000)
        cond2 = (mask == 0b11111001)
        if cond1 or cond2:
            return True
        else:
            return False

    def _isStore(self):
        """
            Function to determine if the instruction
            is a store instruction
            Determined by bit 4
        """
        # Use a copy to be safe
        hw1 = self.HW1
        # Isolate bit 4
        bit = (hw1 >> 4) & 1
        if bit == 0:
            return True
        else:
            return False

    def _getRn(self):
        """
            Function to isolate and return register Rn
            Rn is located at HW1 [3:0]
        """
        # Use a copy to be safe
        hw1 = self.HW1
        # Isolate and return
        reg = hw1 & 0xF
        return reg

    def _getRt(self):
        """
            Function to isolate and return register Rt
            Rt is locate at HW2 [15:12]
        """
        # Use a copy to be safe
        hw2 = self.HW2
        # Isolate and return
        reg = (hw2 >> 12) & 0xF
        return reg

    def _isBranch(self):
        """
            Function to determine if the instruction is
            a branch instruction
        :return: True is branch, False if not.
        """
        # Use copies to be safe
        hw1 = self.HW1
        hw2 = self.HW2
        # Create conditions
        mask1 = (hw1 >> 11) & 0x1F
        cond1 = (mask1 == 0x1E)
        mask2 = (hw2 >> 14) & 0x3
        cond2 = (mask2 == 0x2)
        if cond1 and cond2:
            logging.log(25, "Instruction is a branch instruction")
            return True
        else:
            logging.debug("Instruction is not a branch instruction")
            return False

    def _isNOP(self):
        """
            Function to determine if the instruction
            is a NOP instruction
        :return: True if NOP, False if not.
        """
        # Create copy to be safe
        hw1 = self.HW1
        mask = (hw1 >> 4 ) & 0xFFF
        if mask == 0xF3A:
            logging.log(25, "Instruction is a NOP")
            return True
        else:
            logging.debug("Instruction is not a NOP")
            return False
