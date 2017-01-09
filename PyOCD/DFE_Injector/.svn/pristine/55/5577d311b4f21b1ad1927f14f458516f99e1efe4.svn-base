__author__ = 'Jens Vankeirsbilck'

from Tkinter import *
from faultInjection.mmio.pwmFaultInjector import PWMFaultInjector
import random
import logging


class PWMGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()

    def setup(self):
        pwmLabel = Label(self, text="PWM Fault Injector", fg="blue", font="bold", bg="orange", width=55)
        pwmLabel.grid(row=0, column=0, columnspan=3)

        pwmpinLabel = Label(self, text="PWMpin to affect (PWM1.X)")
        pwmpinLabel.grid(row=1, column=0)
        self.pwmpinEntry = Entry(self)
        self.pwmpinEntry.grid(row=1, column=1)

        pwmPowerButton = Button(self, text="Toggle power all PWM", command= self._toggleFullPWM)
        pwmPowerButton.grid(row=2, column=0)

        pwmEnableButton = Button(self, text="Toggle enable all PWM", command=self._togglePWMEnable)
        pwmEnableButton.grid(row=2, column=1)

        counterEnableButton = Button(self, text="Toggle counter all PWM", command=self._toggleCounterEnable)
        counterEnableButton.grid(row=2, column=2)

        pwmPinEnableButton = Button(self, text="Toggle enable PWMpin", command=self._togglePWMPinEnable)
        pwmPinEnableButton.grid(row=3, column=0)

        pwmPinEdgeModeButton = Button(self, text="Toggle edge mode PWMpin", command=self._toggleEdgeMode)
        pwmPinEdgeModeButton.grid(row=3, column=1)

        injectPWMButton = Button(self, text="Change pulsewidth PWMpin", command=self._injectPWM)
        injectPWMButton.grid(row=3, column=2)

    # Private handlers
    def _toggleFullPWM(self):
        inj = PWMFaultInjector()
        inj.togglePWMPower()
        inj.unInit()

    def _togglePWMEnable(self):
        inj = PWMFaultInjector()
        inj.togglePWMEnable()
        inj.unInit()

    def _toggleCounterEnable(self):
        inj = PWMFaultInjector()
        inj.toggleCounterEnable()
        inj.unInit()

    def _togglePWMPinEnable(self):
        bitPos = self._getBitPos()
        inj = PWMFaultInjector()
        inj.togglePWMPinEnable(bitPos)
        inj.unInit()

    def _toggleEdgeMode(self):
        bitPos = self._getBitPos()
        inj = PWMFaultInjector()
        inj.toggleEdgeMode(bitPos)
        inj.unInit()

    def _injectPWM(self):
        bitPos = self._getBitPos()
        inj = PWMFaultInjector()
        inj.injectPWM(bitPos)
        inj.unInit()

    def _getBitPos(self):
        bitString = self.pwmpinEntry.get()
        if bitString == '':
            logging.log(25, "No PWMpin specified! choosing randomly")
            return random.randint(1, 6)
        else:
            return int(bitString)

if __name__ == "__main__":
    root = Tk()
    root.title("PWM Fault Injector")
    root.geometry("500x200")
    app = PWMGUI(root)
    root.mainloop()