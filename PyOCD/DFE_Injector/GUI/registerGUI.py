__author__ = 'Jens Vankeirsbilck'

from faultInjection.registerFaultInjector import RegisterFaultInjector
from faultInjection.specialRegisterFaultInjector import SpecialRegisterFaultInjector
from Tkinter import *
import logging
import random


class RegisterGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self,master)
        self.grid()
        self.setup()
        self.faultMask = 0

    def setup(self):
        registerLabel = Label(self, text="Register Fault Injector", fg="white", font="bold", bg="blue", width=50)
        registerLabel.grid(row=0, column=0, columnspan=4)

        bitPosLabel = Label(self, text="Position of bit to flip (0-31)")
        bitPosLabel.grid(row=1, column=0)
        self.bitPosEntry = Entry(self)
        self.bitPosEntry.grid(row=1, column=1)

        addressLabel = Label(self, text="Address of flag")
        addressLabel.grid(row=1, column=2)
        self.addressEntry = Entry(self)
        self.addressEntry.grid(row=1, column=3)

        fiRegisterButton = Button(self, text=" FI register", command=self._injectRegister)
        fiRegisterButton.grid(row=2, column=0)

        pcRegisterButton = Button(self, text="FI PC", command=self._jumpPC)
        pcRegisterButton.grid(row=2, column=1)

        spRegisterButton = Button(self, text="FI SP", command=self._jumpSP)
        spRegisterButton.grid(row=2, column=2)

        lrRegisterButton = Button(self, text="FI LR", command=self._jumpLR)
        lrRegisterButton.grid(row=3, column=0)

        xpsrRegisterButton = Button(self, text="FI XPSR", command=self._jumpXPSR)
        xpsrRegisterButton.grid(row=3, column=1)

        resetButton = Button(self, text="Reset", command=self._reset)
        resetButton.grid(row=3, column=2)

        faultMaskButton = Button(self, text="Toggle FAULTMASK", command=self._changeFaultMask)
        faultMaskButton.grid(row=4, column=0, columnspan=3)

    def _injectRegister(self):
        address = self._getAddress()
        mask = 1 << self._getBitPos()
        inj = RegisterFaultInjector()
        inj.injectFaultRegisterInstructionAware(mask, address)
        inj.unInit()

    def _jumpPC(self):
        address = self._getAddress()
        pos = self._getBitPos()
        inj = SpecialRegisterFaultInjector()
        inj.flipPC(pos, address)
        inj.unInit()

    def _jumpSP(self):
        address = self._getAddress()
        pos = self._getBitPos()
        inj = SpecialRegisterFaultInjector()
        inj.flipSP(pos, address)
        inj.unInit()

    def _jumpLR(self):
        address = self._getAddress()
        pos = self._getBitPos()
        inj = SpecialRegisterFaultInjector()
        inj.flipLR(pos, address)
        inj.unInit()

    def _jumpXPSR(self):
        address = self._getAddress()
        pos = self._getBitPos()
        inj = SpecialRegisterFaultInjector()
        inj.flipXPSR(pos)
        inj.unInit()

    def _reset(self):
        self.faultMask = 0;
        inj = RegisterFaultInjector()
        inj.resetDevice()
        inj.unInit()

    def _getBitPos(self):
        bitPosString = self.bitPosEntry.get()
        if bitPosString == "":
            logging.log(25, "No bit position supplied! Chosen randomly!")
            return random.randint(0, 31)
        else:
            bitPos = int(bitPosString)
            if bitPos >= 0 and bitPos <= 31:
                return bitPos
            else:
                logging.log(25,"Wrong bit supplied, chosen randomly")
                return random.randint(0,31)


    def _changeFaultMask(self):
        self.faultMask += 1
        self.faultMask %= 2
        inj = RegisterFaultInjector()
        inj.setFAULTMASK(self.faultMask)
        inj.unInit()

    def _getAddress(self):
        addressString = self.addressEntry.get()
        if addressString == "":
            return None
        else:
            return int(addressString,16)

if __name__ == "__main__":
    root = Tk()
    root.title("Register Fault Injector")
    root.geometry("310x100")
    app = RegisterGUI(root)
    root.mainloop()