__author__ = 'Jens Vankeirsbilck'

import logging


class Instruction16BitLoad():
    def __init__(self, instruction):
        self.instruction = instruction

    # Public methods
    def getNecessaryValues(self):
        values = None
        if self._isRnRmLoad():
            Rn = self._getRegister(3)
            Rm = self._getRegister(6)
            values = {'Rn': Rn, 'Rm': Rm}
        elif self._isRnOffsetLoad():
            base = self._getRegister(3)
            offset = self._getOffset(6)
            values = {'base': base, 'offset': offset}
        elif self._isSPoffsetLoad():
            offset = self._getOffset(0)
            values = {'base': 13, 'offset': offset}
        elif self._isPCoffsetLoad():
            offset = self._getOffset(0)
            values = {'base': 15, 'offset': offset}
        elif self._isRnLoad():
            base = self._getRegister(8)
            values = {'base': base, 'offset' : 0}
        return values

    # Private methods
    def _isRnRmLoad(self):
        # use copy to be safe
        instr = self.instruction
        # Isolate opcode
        opcode = (instr >> 9) & 0x7F
        # determine conditions
        cond1 = (opcode == 0b0101100)
        cond2 = (opcode == 0b0101110)
        cond3 = (opcode == 0b0101101)
        cond4 = (opcode == 0b0101011)
        cond5 = (opcode == 0b0101111)
        # If a condition holds, return true else false
        if cond1 or cond2 or cond3 or cond4 or cond5:
            logging.debug("Instruction is a RnRmLoad")
            return True
        else:
            logging.debug("Instruction is not a RnRmLoad")
            return False

    def _isRnOffsetLoad(self):
        # use copy to be safe
        instr = self.instruction
        # Isolate opcode
        opcode = (instr >> 11) & 0x1F
        # determine conditions
        cond1 = (opcode == 0b01101)
        cond2 = (opcode == 0b01111)
        cond3 = (opcode == 0b10001)
        # If a condition holds, return true else false
        if cond1 or cond2 or cond3:
            logging.debug("Instruction is a RnOffsetLoad")
            return True
        else:
            logging.debug("Instruction is not a RnOffsetLoad")
            return False

    def _isSPoffsetLoad(self):
        # use copy to be safe
        instr = self.instruction
        # Isolate opcode
        opcode = (instr >> 11) & 0x1F
        # If condition holds, return true else false
        if opcode == 0b10011:
            logging.debug("Instruction is a SPoffsetLoad")
            return True
        else:
            logging.debug("Instruction is not a SPoffsetLoad")
            return False

    def _isPCoffsetLoad(self):
        # use copy to be safe
        instr = self.instruction
        # Isolate opcode
        opcode = (instr >> 11) & 0x1F
        # If condition holds, return true else false
        if opcode == 0b01001:
            logging.debug("Instruction is a PCoffsetLoad")
            return True
        else:
            logging.debug("Instruction is not a PCoffsetLoad")
            return False

    def _isRnLoad(self):
        # use copy to be safe
        instr = self.instruction
        # Isolate opcode
        opcode = (instr >> 11) & 0x1F
        # If condition holds, return true else false
        if opcode == 0b11001:
            logging.debug("Instruction is a RnLoad")
            return True
        else:
            logging.debug("Instruction is not a RnLoad")
            return False

    def _getRegister(self, pos):
        # use copy to be safe
        instr = self.instruction
        # Isolate register
        reg = (instr >> pos) & 0x7
        return reg

    def _getOffset(self, pos):
        # use copy to be safe
        instr = self.instruction
        # Isolate offset
        if pos == 0:
            offset = instr & 0xFF
            return offset
        elif pos == 6:
            offset = (instr >> 6) & 0x1F
            return offset
        else:
            return 0