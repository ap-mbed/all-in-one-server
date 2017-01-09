__author__ = 'Jens Vankeirsbilck'

from Tkinter import *
import logging
import random
from faultInjection.memoryFaultInjector import MemoryFaultInjector


class MemoryGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()

    def setup(self):
        titleLabel = Label(self, text="Memory Fault Injector", fg="white", font="bold", bg="red", width=35)
        titleLabel.grid(row=0, column=0, columnspan=2)

        bitPosLabel = Label(self, text="Position of bit to flip (0-31)")
        bitPosLabel.grid(row=1, column=0)
        self.bitPosEntry = Entry(self)
        self.bitPosEntry.grid(row=1, column=1)

        atSPButton = Button(self, text="FI at SP", command=self._injectAtSP)
        atSPButton.grid(row=2, column=0)

        memLocButton = Button(self, text="FI at memLoc", command=self._injectAtMemLoc)
        memLocButton.grid(row=2, column=1)

    def _injectAtSP(self):
        bitPos = self._getBitPos()
        inj = MemoryFaultInjector()
        inj.injectAtSP(bitPos)
        inj.unInit()

    def _injectAtMemLoc(self):
        bitPos = self._getBitPos()
        inj = MemoryFaultInjector()
        inj.injectMemoryLocationInstructionAware(bitPos)
        inj.unInit()

    def _getBitPos(self):
        posString = self.bitPosEntry.get()
        if posString == '':
            logging.log(25, "No bitPos given, chosen randomly")
            return random.randint(0, 31)
        else:
            pos = int(posString)
            if pos >= 0 and pos <= 31:
                return pos
            else:
                logging.log(25, "Wrong bitPos given, chosen randomly")
                return random.randint(0,31)

if __name__ == "__main__":
    root = Tk()
    root.title("Memory Fault Injector")
    root.geometry("310x100")
    app = MemoryGUI(root)
    root.mainloop()