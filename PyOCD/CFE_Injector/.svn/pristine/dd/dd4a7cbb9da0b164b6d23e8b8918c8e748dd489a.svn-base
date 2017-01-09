__author__ = 'Jens Vankeirsbilck'


from Tkinter import *
from pyOCD.board import MbedBoard
from faultInjection.PC_injector import PCinjector
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
        self.newPCEntry = Entry(self)
        self.newPCEntry.grid(row=1, column=3)

        readPCbutton = Button(self, text="read PC", command=self._fillInPC)
        readPCbutton.grid(row=2, column=0, columnspan=2)

        injectNewPCbutton = Button(self, text="Inject new PC", command=self._injectPC)
        injectNewPCbutton.grid(row=2, column=2, columnspan=2)

    # Private Methods
    def _fillInPC(self):
        inj = PCinjector(self.board)
        PC = inj.readPC()
        self.PClabelText.set("0x%X" % PC)

    def _injectPC(self):
        newPCString = self.newPCEntry.get()
        PC = int(newPCString, 16)
        inj = PCinjector(self.board)
        inj.writeNewPC(PC)

    # Private Methods
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
    root.geometry("475x100")
    app = GUI(root)
    root.mainloop()


