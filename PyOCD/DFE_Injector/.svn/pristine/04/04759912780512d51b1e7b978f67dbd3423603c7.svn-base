__author__ = 'Jens Vankeirsbilck'

import os
from Tkinter import *
from faultInjection.mmio.pwmFaultInjector import PWMFaultInjector
from faultInjection.specialRegisterFaultInjector import SpecialRegisterFaultInjector
from faultInjection.registerFaultInjector import RegisterFaultInjector
from faultInjection.WetenschapsDag import RobotFI
import logging
logging.basicConfig(level=logging.DEBUG)

class WDGUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.seaGreen = "#158CAF"
        self.ostendBlue = "#52BDEC"
        self.grid(sticky=N+E+S+W)
        self.setup()

    def setup(self):
        self._makeScalable(6,3)
        self.config(bg=self.seaGreen)

        # Size variables for the buttons
        buttonWidth = 20
        buttonHeight = 5

        title = Label(self, text="Probeer de robot te laten crashen", font=("bold", 20), fg="white", bg=self.seaGreen,
                      height=2)
        title.grid(row=0, column=0, columnspan=3, sticky=E+W)

        pwmPowerButton = Button(self, text="Fout 5", command=self._toggleFullPWM, height=buttonHeight,
                                width=buttonWidth)
        pwmPowerButton.grid(row=2, column=1, sticky=E+W)

        pcRegisterButton = Button(self, text="Fout 1", command=self._jumpPC, height=buttonHeight, width=buttonWidth)
        pcRegisterButton.grid(row=1, column=0)

        pwmPinEnableButton = Button(self, text="Fout 2", command=self._togglePWMPinEnable, height=buttonHeight,
                                    width=buttonWidth)
        pwmPinEnableButton.grid(row=1, column=1, sticky=E+W)

        changePrevPosButton = Button(self, text="Fout 4", command=self._changePrevPos, height=buttonHeight,
                                     width=buttonWidth)
        changePrevPosButton.grid(row=2, column=0, sticky=E+W)

        changeWaitTimeButton = Button(self, text="Fout 3", command=self._changeWaitTime, height=buttonHeight,
                                      width=buttonWidth)
        changeWaitTimeButton.grid(row=1, column=2, sticky=E+W)

        toggleEdgeModeButton = Button(self, text="Fout 6", command=self._toggleEdgeMode, height=buttonHeight,
                                      width=buttonWidth)
        toggleEdgeModeButton.grid(row=2, column=2, sticky=E+W)

        changeSPButton = Button(self, text="Fout 7", command=self._changeSP, height=buttonHeight,
                                width=buttonWidth)
        changeSPButton.grid(row=3, column=1, sticky=E+W)

        #resetButton = Button(self, text="Reset", command=self._reset)
        #resetButton.grid(row=4, column=1, sticky=E+W)

        photo = PhotoImage(file='{}/{}'.format(os.path.dirname(os.path.dirname(__file__)), "KULEUVEN_LOGO 300_110.gif"))
        logo = Label(self, image=photo, bg=self.ostendBlue)
        logo.image = photo
        logo.grid(row=5, column=0, columnspan=2, sticky=E+W+N+S)

        TCOlabel = Label(self, text="Technologie\nCampus\nOostende", fg="white", bg=self.ostendBlue, font=("bold", 16))
        TCOlabel.grid(row=5, column=2, sticky=E+W+N+S)

    # Private handlers
    def _toggleFullPWM(self):
        inj = PWMFaultInjector()
        inj.togglePWMPower()
        inj.unInit()

    def _togglePWMPinEnable(self):
        inj = PWMFaultInjector()
        inj.togglePWMPinEnable(3)
        inj.unInit()

    def _jumpPC(self):
        inj = SpecialRegisterFaultInjector()
        inj.flipPC(20, None)
        inj.unInit()

    def _changePrevPos(self):
        inj = RobotFI()
        inj.changePrevPos()
        inj.unInit()

    def _changeWaitTime(self):
        inj = RobotFI()
        inj.changeWaitTime()
        inj.unInit()

    def _toggleEdgeMode(self):
        inj = PWMFaultInjector()
        inj.toggleEdgeMode(5)
        inj.unInit()

    def _changeSP(self):
        inj = SpecialRegisterFaultInjector()
        inj.flipSP(12, None)
        inj.unInit()

    def _reset(self):
        inj = RegisterFaultInjector()
        inj.resetDevice()
        inj.unInit()

    # Other Private Methods
    def _makeScalable(self, nrOfRow=3, nrOfCol=3):
        top = self.winfo_toplevel()
        for x in range(nrOfRow):
            top.rowconfigure(x, weight=1)
            self.rowconfigure(x, weight=1)
        for i in range(nrOfCol):
            top.columnconfigure(i, weight=1)
            self.columnconfigure(i, weight=1)

if __name__ == "__main__":
    root = Tk()
    root.title("Crasher")
    #root.geometry("400x200")
    app = WDGUI(root)
    root.mainloop()