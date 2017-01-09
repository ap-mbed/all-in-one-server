__author__ = 'Jens Vankeirsbilck'

import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from Tkinter import *
from GPIOGUI import GPIOGUI
from I2CGUI import I2CGUI
from PWMGUI import PWMGUI
from registerGUI import RegisterGUI
from memoryGUI import MemoryGUI
import logging
logging.basicConfig(level=logging.DEBUG)


class GUI(Frame):
    def __init__(self, master):
        Frame.__init__(self, master)
        self.grid()
        self.setup()

    def setup(self):
        masterPane = PanedWindow(self, orient=VERTICAL)
        masterPane.pack(fill=BOTH, expand=1)

        gpioFrame = GPIOGUI(masterPane)
        masterPane.add(gpioFrame)

        childPane = PanedWindow(masterPane, orient=VERTICAL)
        masterPane.add(childPane)

        i2cFrame = I2CGUI(childPane)
        childPane.add(i2cFrame)

        sChildPane = PanedWindow(childPane, orient=VERTICAL)
        childPane.add(sChildPane)

        pwmFrame = PWMGUI(sChildPane)
        sChildPane.add(pwmFrame)

        ssChildPane = PanedWindow(sChildPane, orient=VERTICAL)
        sChildPane.add(ssChildPane)

        registerFrame = RegisterGUI(ssChildPane)
        ssChildPane.add(registerFrame)

        memoryFrame = MemoryGUI(ssChildPane)
        ssChildPane.add(memoryFrame)

if __name__ == "__main__":
    root = Tk()
    root.title("Fault Injector")
    root.geometry("600x600")
    app = GUI(root)
    root.mainloop()

