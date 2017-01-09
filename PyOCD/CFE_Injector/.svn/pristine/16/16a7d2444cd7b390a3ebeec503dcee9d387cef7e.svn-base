__author__ = 'Jens Vankeirsbilck'

from Tkinter import *
from pyOCD.board import MbedBoard
from time import sleep
import random
from faultInjection.cfeInjector import CFEInjector
import logging
logging.basicConfig(level=logging.DEBUG)

class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()
        self.board = self._initialize()

    def setup(self):
        titleLabel = Label(self, text="CFE Injector", fg="white", font="bold", bg="blue", width=50)
        titleLabel.grid(row=0, column=0, columnspan=4)

        PCtextLabel = Label(self, text="PC:")
        PCtextLabel.grid(row=1, column=0)
        self.PClabelText = StringVar()
        self.PClabelText.set("")
        PClabel = Label(self, textvariable=self.PClabelText)
        PClabel.grid(row=1, column=1)

        newPCLabel = Label(self, text="new PC:")
        newPCLabel.grid(row=1, column=2)
        self.newPCValue = StringVar(self)
        self.newPcChoices = OptionMenu(self, self.newPCValue, '')
        self.newPcChoices.grid(row=1, column=3)

        readPCbutton = Button(self, text="read PC", command=self._fillInPC)
        readPCbutton.grid(row=2, column=0, columnspan=2)

        injectNewPCbutton = Button(self, text="Inject new PC", command=self._injectPC)
        injectNewPCbutton.grid(row=2, column=2, columnspan=2)

    # Private Methods
    def _fillInPC(self):
        inj = CFEInjector(self.board)
        ok = False
        while not ok:
            try:
                PC = inj.pcInjector.readPC()
                self.PClabelText.set("0x%X" % PC)
                PCOptions = inj._possibleNewPCList(PC,True,False)
                # http://stackoverflow.com/questions/17252096/change-optionmenu-based-on-what-is-selected-in-another-optionmenu
                menu = self.newPcChoices['menu']
                menu.delete(0, 'end')
                for pc in PCOptions:
                    menu.add_command(label="0x%X"%pc, command= lambda newPC = pc: self.newPCValue.set("0x%X"%newPC))
                self.newPCValue.set("0x%X"%PCOptions[0])
                ok = True
            except Exception as e:
                    logging.error("Failed to create new PC list\n%s"%e)
            finally:
                inj.pcInjector.reset()
                sleep(random.randint(0,5))

    def _injectPC(self):
        newPCString = self.newPCValue.get()
        PC = int(newPCString, 16)
        inj = CFEInjector(self.board)
        inj.pcInjector.writeNewPC(PC)

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

if __name__ == "__main__":
    root = Tk()
    root.title("CFE Injector")
    root.geometry("525x100")
    app = GUI(root)
    root.mainloop()
