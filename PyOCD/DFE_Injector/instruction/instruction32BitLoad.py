__author__ = 'Jens Vankeirsbilck'

import logging


class Instruction32BitLoad:
    def __init__(self, HW1, HW2):
        self.HW1 = HW1
        self.HW2 = HW2

    def getNecessaryValues(self):
        # use copy to be safe
        hw2 = self.HW2
        # Create decision mask
        mask = (hw2 >> 6) & 0x3F
        # Start procedure
        if mask == 0 and self._getU7() == 0:
            logging.debug("Need Rn, Rm and shift")
            Rn = self._getRn()
            Rm = self._getRm()
            shift = self._getShift()
            return {'Rn': Rn, 'Rm': Rm, 'shift': shift}
        else:
            logging.debug("Need base, U and offset")
            base = self._getRn()
            U = self._getU()
            offset = self._getOffset()
            return {'base': base, 'U': U, 'offset': offset}

    def _getU(self):
        # use copies to be safe
        hw1 = self.HW1
        hw2 = self.HW2
        # Isolate U
        U1 = self._getU7()
        U2 = self._getU9()
        # get HW2[11]
        b11 = (hw2 >> 11) & 1
        if U1 == 1:
            return 1
        elif U1 == 0 and self._isRnPC():
            return 0
        elif U1 == 0 and b11 == 1 and not self._isRnPC():
            return U2
        else:
            return 1

    def _getOffset(self):
        # use copy to be safe
        hw2 = self.HW2
        # Get necessary variable
        u7 = self._getU7()
        # start procedure
        if u7 == 1 or self._isRnPC():
            # Isolate Offset
            offset = hw2 & 0xFFF
            return offset
        else:
            # Isolate Offset
            offset = hw2 & 0xFF
            return offset

    def _getShift(self):
        # use copy to be safe
        hw2 = self.HW2
        # Isolate shift
        shift = (hw2 >> 4) & 0b11
        return shift

    def _isRnPC(self):
        Rn = self._getRn()
        if Rn == 0xF:
            return True
        else:
            return False

    def _getRn(self):
        # use copy to be safe
        hw1 = self.HW1
        # Isolate Rn
        Rn = hw1 & 0xF
        return Rn

    def _getRm(self):
        # use copy to be safe
        hw2 = self.HW2
        # Isolate Rm
        Rm = hw2 & 0xF
        return Rm

    def _getU7(self):
        # use copies to be safe
        hw1 = self.HW1
        # Isolate U7
        U7 = (hw1 >> 7) & 1
        return U7

    def _getU9(self):
        # use copy to be safe
        hw2 = self.HW2
        # Isolate U9
        U9 = (hw2 >> 9) & 1
        return U9