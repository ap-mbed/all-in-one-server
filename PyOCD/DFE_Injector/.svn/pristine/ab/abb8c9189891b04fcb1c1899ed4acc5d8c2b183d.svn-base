__author__ = 'Jens Vankeirsbilck'

from Tkinter import *
from faultInjection.mmio.gpioFaultInjector import GPIOFaultInjector
import logging

class GPIOGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()

    def setup(self):
        gpioLabel = Label(self, text="GPIO Fault Injector", fg="blue", font="bold", bg="yellow", width=50)
        gpioLabel.grid(row=0, column=0, columnspan=4)

        portLabel = Label(self, text="Port of pin")
        portLabel.grid(row=1, column=0)
        self.portEntry = Entry(self)
        self.portEntry.grid(row=1, column=1)

        bitLabel = Label(self, text="Bit of port for pin")
        bitLabel.grid(row=1, column=2)
        self.bitEntry = Entry(self)
        self.bitEntry.grid(row=1, column=3)

        changeInputButton = Button(self, text="Change Input", command=self._changeInput)
        changeInputButton.grid(row=2, column=0, columnspan=2)

        toggleInputButton = Button(self, text="Toggle Input", command=self._toggleInput)
        toggleInputButton.grid(row=2, column=2, columnspan=2)

        outputHighButton = Button(self, text="Ouput High", command=self._setOutputHigh)
        outputHighButton.grid(row=3, column=0, columnspan=2)

        outputLowButton = Button(self, text="Output Low", command=self._setOutputLow)
        outputLowButton.grid(row=3, column=2, columnspan=2)

    # Private methods and handlers
    def _changeInput(self):
        port = self._getPort()
        bit = self._getBit()
        inj = GPIOFaultInjector()
        inj.changeInput(port, bit)
        inj.unInit()

    def _toggleInput(self):
        port = self._getPort()
        bit = self._getBit()
        inj = GPIOFaultInjector()
        inj.toggleInput(port, bit)
        inj.unInit()

    def _setOutputHigh(self):
        port = self._getPort()
        bit = self._getBit()
        inj = GPIOFaultInjector()
        inj.setOutputHigh(port, bit)
        inj.unInit()

    def _setOutputLow(self):
        port = self._getPort()
        bit = self._getBit()
        inj = GPIOFaultInjector()
        inj.setOutputLow(port, bit)
        inj.unInit()

    def _getPort(self):
        portString = self.portEntry.get()
        if portString == '':
            logging.error("No port given!!!")
            top = Toplevel()
            top.title("! ERROR !")
            msg = Message(top, text="No port given! Please provide one!")
            msg.pack()
            okButton = Button(top, text="OK", command=top.destroy)
            okButton.pack()
            raise Exception("No port given! Please provide one!")
        else:
            return int(portString)

    def _getBit(self):
        bitString = self.bitEntry.get()
        if bitString == '':
            logging.error( "No bit given!!!")
            top = Toplevel()
            top.title("! ERROR !")
            msg = Message(top, text="No bit given! Please provide one!")
            msg.pack()
            okButton = Button(top, text="OK", command=top.destroy)
            okButton.pack()
            raise Exception("No bit given! Please provide one!")
        else:
            return int(bitString)

if __name__ == "__main__":
    root = Tk()
    root.title("GPIO Fault Injector")
    root.geometry("460x100")
    app = GPIOGUI(root)
    root.mainloop()