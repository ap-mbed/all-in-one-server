__author__ = 'Jens Vankeirsbilck'


import os
from Tkinter import *
from pyOCD.board import MbedBoard
from faultInjection.mmio.pwmFaultInjector import PWMFaultInjector
from faultInjection.specialRegisterFaultInjector import SpecialRegisterFaultInjector
from faultInjection.registerFaultInjector import RegisterFaultInjector
from faultInjection.WetenschapsDag import RobotFI
import logging
logging.basicConfig(level=logging.DEBUG)

class Drads2016(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.seaGreen = "#158CAF"
        self.ostendBlue = "#52BDEC"
        self.KULblue = "#00407A"
        self.grid(sticky=N+E+S+W)
        self.setup()
        self.board = self._initialize()

    def setup(self):
        self._makeScalable(6,3)
        self.config(bg=self.seaGreen)

        # Size variables for the buttons
        buttonWidth = 20
        buttonHeight = 5

        title = Label(self, text="Inject Faults into the robot", font=("bold", 20), fg="white", bg=self.seaGreen,
                      height=2)
        title.grid(row=0, column=0, columnspan=3, sticky=E+W)

        pwmLabel = Label(self, text="PWM-Signal (motor control)", fg="white", bg=self.KULblue, font=("bold", 12))
        pwmLabel.grid(row=1, column=0, columnspan=3, sticky=E+W)

        pwmPowerButton = Button(self, text="Turn On/Off\nPWM", command=self._toggleFullPWM, height=buttonHeight,
                                width=buttonWidth)
        pwmPowerButton.grid(row=2, column=0, sticky=E+W)

        pwmPinEnableButton = Button(self, text="Disable/Enable\nShoulder", command=self._togglePWMPinEnable, height=buttonHeight,
                                    width=buttonWidth)
        pwmPinEnableButton.grid(row=2, column=1, sticky=E+W)

        toggleEdgeModeButton = Button(self, text="Toggle Edge Mode\nWrist", command=self._toggleEdgeMode, height=buttonHeight,
                                      width=buttonWidth)
        toggleEdgeModeButton.grid(row=2, column=2, sticky=E+W)

        memoryLabel = Label(self, text="Memory", fg="white", bg=self.KULblue, font=("bold", 12))
        memoryLabel.grid(row=3,column=0, columnspan=3, stick=E+W)

        changePrevPosButton = Button(self, text="Change Previous\nPosition", command=self._changePrevPos, height=buttonHeight,
                                     width=buttonWidth)
        changePrevPosButton.grid(row=4, column=0, sticky=E+W)

        changeWaitTimeButton = Button(self, text="Change Motor\nSpeed", command=self._changeWaitTime, height=buttonHeight,
                                      width=buttonWidth)
        changeWaitTimeButton.grid(row=4, column=1, sticky=E+W)

        registerLabel = Label(self, text="Registers", fg="white", bg=self.KULblue, font=("bold", 12))
        registerLabel.grid(row=5, column=0, columnspan=3, sticky=E+W)

        pcRegisterButton = Button(self, text="Change Program\nCounter", command=self._jumpPC, height=buttonHeight, width=buttonWidth)
        pcRegisterButton.grid(row=6, column=0, sticky=E+W)

        changeSPButton = Button(self, text="Change Stack\nPointer", command=self._changeSP, height=buttonHeight,
                                width=buttonWidth)
        changeSPButton.grid(row=6, column=1, sticky=E+W)

        resetButton = Button(self, text="Reset", command=self._reset)
        resetButton.grid(row=7, column=1, sticky=E+W)

        photo = PhotoImage(file='{}/{}'.format(os.path.dirname(os.path.dirname(__file__)), "KULEUVEN_LOGO 300_110.gif"))
        logo = Label(self, image=photo, bg=self.ostendBlue)
        logo.image = photo
        logo.grid(row=8, column=0, columnspan=2, sticky=E+W+N+S)

        TCOlabel = Label(self, text="Technology\nCampus\nOostende", fg="white", bg=self.ostendBlue, font=("bold", 16))
        TCOlabel.grid(row=8, column=2, sticky=E+W+N+S)

    # Private handlers
    def _toggleFullPWM(self):
        inj = PWMFaultInjector(self.board)
        inj.togglePWMPower()


    def _togglePWMPinEnable(self):
        inj = PWMFaultInjector(self.board)
        inj.togglePWMPinEnable(3)

    def _jumpPC(self):
        inj = SpecialRegisterFaultInjector(self.board)
        inj.flipPC(20, None)

    def _changePrevPos(self):
        inj = RobotFI(self.board)
        inj.changePrevPos()

    def _changeWaitTime(self):
        inj = RobotFI(self.board)
        inj.changeWaitTime()

    def _toggleEdgeMode(self):
        inj = PWMFaultInjector(self.board)
        inj.toggleEdgeMode(5)

    def _changeSP(self):
        inj = SpecialRegisterFaultInjector(self.board)
        inj.flipSP(12, None)

    def _reset(self):
        inj = RegisterFaultInjector(self.board)
        inj.resetDevice()
        #self.board = self._initialize()

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
    root.title("DRADS 2016")
    #root.geometry("400x200")
    app = Drads2016(root)
    root.mainloop()