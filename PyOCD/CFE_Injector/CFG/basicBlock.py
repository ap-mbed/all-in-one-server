__author__ = 'Jens Vankeirsbilck'

import logging

class BasicBlock:
    def __init__(self, startAddress, endAddress, falseJump, trueJump, listOfBlock):
        self.startAddress = startAddress
        self.endAddress = endAddress
        self.falseJumpAddress = falseJump
        self.trueJumpAddress = trueJump
        self.listOfBlock = listOfBlock

    def isEndAddress(self, givenAddress):
        if(givenAddress == self.endAddress):
            return True
        else:
            return False

    def isFalseJumpAddress(self, givenAddress):
        if(givenAddress == self.falseJumpAddress):
            return True
        else:
            return False

    def isTrueJumpAddress(self, givenAddress):
        if(givenAddress == self.trueJumpAddress):
            return True
        else:
            return False

    def isValidAddressForBasicBlock(self, givenAddress):
        if((self.startAddress<=givenAddress) and (self.endAddress>=givenAddress)):
            if (givenAddress in self.listOfBlock):
                return True
        else:
            return False

    def getStartAddress(self):
        return self.startAddress

    def getEndAddress(self):
        return self.endAddress
