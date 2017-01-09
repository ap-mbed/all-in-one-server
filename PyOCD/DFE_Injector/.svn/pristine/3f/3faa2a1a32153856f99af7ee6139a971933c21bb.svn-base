__author__ = 'Jens'

import logging
from instruction16Bit import Instruction16Bit
from instruction32Bit import Instruction32Bit


# Class to encapsulate the instruction with some methods
class Instruction:
    def __init__(self, target):
        self.instruction1 = []
        self.instruction2 = []
        try:
            instr1 = self._getInstruction(target)
            self.instruction1.append(self._getHW1(instr1))
            self.instruction1.append(self._getHW2(instr1))
            target.step()
            instr2 = self._getInstruction(target)
            self.instruction2.append(self._getHW1(instr2))
            self.instruction2.append(self._getHW2(instr2))
        except Exception as e:
            logging.error("!--! Exception: %s" %e)

    # Public methods
    def getNecessaryRegister(self):
        """
            Function that returns the register
            that is used in the instruction (Rt, Rn or Rd)
        """
        index = self._searchIndexHalfWord()
        halfword = self.instruction2[index]
        register = 0
        if self._is16bit(halfword):
            instruction16 = Instruction16Bit(halfword)
            register = instruction16.getRegister()
        elif self._is32bit(halfword):
            if index == 0:
                HW1 = self.instruction2[0]
                HW2 = self.instruction2[1]
            else:
                HW1 = self.instruction2[1]
                HW2 = self.instruction2[0]
            instruction32 = Instruction32Bit(HW1, HW2)
            register = instruction32.getRegister()
        return self._getRegisterType(register)

    def getMemoryAddressValues(self):
        """
            Function that returns the two necessary values to calculate the
            memory address
        :return: dictionary containing the 2 necessary values
        """
        index = self._searchIndexHalfWord()
        halfword = self.instruction2[index]
        if self._is16bit(halfword):
            instr16 = Instruction16Bit(halfword)
            values = instr16.getMemoryAddressValues()
            if values is not None:
                if 'Rn' in values:
                    Rn = self._getRegisterType(values['Rn'])
                    Rm = self._getRegisterType(values['Rm'])
                    return {'Rn': Rn, 'Rm': Rm}
                else:
                    base = self._getRegisterType(values['base'])
                    return {'base': base, 'offset': values['offset']}
            else:
                return None
        elif self._is32bit(halfword):
            if index == 0:
                HW1 = self.instruction2[0]
                HW2 = self.instruction2[1]
            else:
                HW1 = self.instruction2[1]
                HW2 = self.instruction2[0]
            instruction32 = Instruction32Bit(HW1, HW2)
            values = instruction32.getMemoryAddressValues()
            if values is not None:
                if 'U' in values:
                    base = self._getRegisterType(values['base'])
                    return {"base": base, 'U': values['U'], 'offset': values['offset']}
                else:
                    Rn = self._getRegisterType(values['Rn'])
                    Rm = self._getRegisterType(values['Rm'])
                    return {'Rn': Rn, 'Rm': Rm, 'shift': values['shift']}
            else:
                return None

    def getNecessaryValues(self):
        """
            Function to return the necessary value(s) to
            inject a fault instruction aware
        :return: a register or dictionary containing the values
        """
        index = self._searchIndexHalfWord()
        halfword = self.instruction2[index]
        if self._is16bit(halfword):
            instr16 = Instruction16Bit(halfword)
            necessary = instr16.getNecessaryValues()
            if necessary is not None:
                if isinstance(necessary, dict):
                    logging.debug("Dictionary returned, extracting values")
                    if 'Rn' in necessary:
                        Rn = self._getRegisterType(necessary['Rn'])
                        Rm = self._getRegisterType(necessary['Rm'])
                        return {'Rn': Rn, 'Rm': Rm}
                    else:
                        base = self._getRegisterType(necessary['base'])
                        return {'base': base, 'offset': necessary['offset']}
                else:
                    logging.debug("Value for a register returned")
                    return self._getRegisterType(necessary)
            else:
                return None
        elif self._is32bit(halfword):
            if index == 0:
                HW1 = self.instruction2[0]
                HW2 = self.instruction2[1]
            else:
                HW1 = self.instruction2[1]
                HW2 = self.instruction2[0]
            instruction32 = Instruction32Bit(HW1, HW2)
            necessary = instruction32.getNecessaryValues()
            if necessary is not None:
                if isinstance(necessary, dict):
                    logging.debug("Dictionary returned, extracting values")
                    if 'U' in necessary:
                        base = self._getRegisterType(necessary['base'])
                        return {"base": base, 'U': necessary['U'], 'offset': necessary['offset']}
                    else:
                        Rn = self._getRegisterType(necessary['Rn'])
                        Rm = self._getRegisterType(necessary['Rm'])
                        return {'Rn': Rn, 'Rm': Rm, 'shift': necessary['shift']}
                else:
                    logging.debug("Value for a register returned")
                    return self._getRegisterType(necessary)
            else:
                return None

    # Private methods
    def _getInstruction(self, target):
        # Get content of Program Counter
        pc = target.readCoreRegister('pc')
        logging.debug("Program Counter: 0x%X" % pc)
        # Get instruction
        instruction = target.readMemory(pc)
        logging.debug("Instruction: 0x%X" % instruction)
        return instruction

    def _is16bit(self, halfword):
        mask = (halfword >> 11) & 0b11111
        if mask == 0b11101:
            logging.debug("32 bit instruction")
            return False
        elif mask == 0b11110:
            logging.debug("32 bit instruction")
            return False
        elif mask == 0b11111:
            logging.debug("32 bit instruction")
            return False
        else:
            logging.debug("16 bit instruction")
            return True

    def _is32bit(self, halfword):
        mask = (halfword >> 11) & 0b11111
        if mask == 0b11101:
            logging.debug("32 bit instruction")
            return True
        elif mask == 0b11110:
            logging.debug("32 bit instruction")
            return True
        elif mask == 0b11111:
            logging.debug("32 bit instruction")
            return True
        else:
            logging.debug("16 bit instruction")
            return False

    def _getHW1(self, instruction):
        logging.debug("Isolating HalfWord 1")
        halfword = (instruction >> 16) & 0xFFFF
        logging.debug("HW1: 0x%X" % halfword)
        return halfword

    def _getHW2(self, instruction):
        logging.debug("Isolating HalfWord 2")
        halfword = instruction & 0x0000FFFF
        logging.debug("HW2: 0x%X" % halfword)
        return halfword

    def _searchIndexHalfWord(self):
        index = self._getIndexHalfWord(self.instruction1[0])
        if index == -1:
            index = self._getIndexHalfWord(self.instruction1[1])
            if index == -1:
                return 0
            else:
                return index
        else:
            return index

    def _getIndexHalfWord(self, halfword):
        index = -1
        try:
            index = self.instruction2.index(halfword)
        except Exception as e:
            logging.debug("Halfword not found in second instruction")
        finally:
            return index

    def _getRegisterType(self, register):
        if register >= 0:
            if register < 13:
                # Create reg variable
                reg = "r%s" % register
            elif register == 13:
                # Create reg variable
                reg = 'sp'
            elif register == 14:
                # Create reg variable
                reg = 'lr'
            elif register == 15:
                # Create reg variable
                reg = 'pc'
            logging.debug("Created reg: %s" % reg)
            return reg
        else:
            logging.debug("Instruction does not use a register")
            return None
