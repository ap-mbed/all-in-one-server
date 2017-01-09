__author__ = 'Jens Vankeirsbilck'

from Tkinter import *
from faultInjection.mmio.i2cFaultInjector import I2CFaultInjector
import logging


class I2CGUI(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()

    def setup(self):
        i2cLabel = Label(self, text="I2C Fault Injector", fg="blue", font="bold", bg="green", width=50)
        i2cLabel.grid(row=0, column=0, columnspan=4)

        sdaLabel = Label(self, text="sda (pinNumber)")
        sdaLabel.grid(row=1, column=0)
        self.sdaEntry = Entry(self)
        self.sdaEntry.grid(row=1, column=1)

        sclLabel = Label(self, text="scl (pinNumber)")
        sclLabel.grid(row=1, column=2)
        self.sclEntry = Entry(self)
        self.sclEntry.grid(row=1, column=3)

        toggleButton = Button(self, text="Toggle I2C Power", command=self._toggleI2CPower)
        toggleButton.grid(row=2, column=0, columnspan=4)

        bitPosLabel = Label(self, text="bit to flip (0-7)")
        bitPosLabel.grid(row=3, column=0)
        self.bitPosEntry = Entry(self)
        self.bitPosEntry.grid(row=3, column=1)

        consetButton = Button(self, text="FI CONSET", command=self._fiI2CONSET)
        consetButton.grid(row=4, column=0)

        conclrButton = Button(self, text="FI CONCLR", command=self._fiI2CONCLR)
        conclrButton.grid(row=4, column=1)

        datButton = Button(self, text="FI DAT", command=self._fiI2DAT)
        datButton.grid(row=4, column=2)

        sclhButton = Button(self, text="FI SCLH", command=self._fiI2SCLH)
        sclhButton.grid(row=5, column=0)

        scllButton = Button(self, text="FI SCLL", command=self._fiI2SCLL)
        scllButton.grid(row=5, column=1)

        dataBufferButton = Button(self, text="FI DataBuffer", command=self._fiI2DataBuffer)
        dataBufferButton.grid(row=5, column=2)

    # Private Handlers
    def _toggleI2CPower(self):
        sda = self._getSDA()
        scl = self._getSCL()
        inj = I2CFaultInjector(sda, scl)
        inj.toggleI2CPower()
        inj.unInit()

    def _fiI2CONSET(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2CONSET(bitPos)
        inj.unInit()

    def _fiI2CONCLR(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2CONCLR(bitPos)
        inj.unInit()

    def _fiI2DAT(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2DAT(bitPos)
        inj.unInit()

    def _fiI2SCLH(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2SCLH(bitPos)
        inj.unInit()

    def _fiI2SCLL(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2SCLL(bitPos)
        inj.unInit()

    def _fiI2DataBuffer(self):
        sda = self._getSDA()
        scl = self._getSCL()
        bitPos = self._getBitPos()
        inj = I2CFaultInjector(sda, scl)
        inj.injectFaultI2DataBuffer(bitPos)
        inj.unInit()

    def _getSDA(self):
        sdaString = self.sdaEntry.get()
        if sdaString == '':
            logging.error("No SDA given!")
            top = Toplevel()
            top.title("! ERROR !")
            msg = Message(top, text="No SDApin given! Please provide one!")
            msg.pack()
            okButton = Button(top, text="OK", command=top.destroy)
            okButton.pack()
            raise Exception("No SDApin given!")
        else:
            return int(sdaString)

    def _getSCL(self):
        sclString = self.sclEntry.get()
        if sclString == '':
            logging.error("No SCL given!")
            top = Toplevel()
            top.title("! ERROR !")
            msg = Message(top, text="No SCLpin given! Please provide one!")
            msg.pack()
            okButton = Button(top, text="OK", command=top.destroy)
            okButton.pack()
            raise Exception("No SCLpin given!")
        else:
            return int(sclString)

    def _getBitPos(self):
        bitString = self.bitPosEntry.get()
        if bitString == '':
            logging.log(25, "No position specified, translated to None")
            return None
        else:
            bit = int(bitString)
            if 0 <= bit <= 7:
                return bit
            else:
                logging.log(25, "Wrong value submitted, changed to None")
                return None

if __name__ == "__main__":
    root = Tk()
    root.title("I2C Fault Injector")
    root.geometry("460x200")
    app = I2CGUI(root)
    root.mainloop()