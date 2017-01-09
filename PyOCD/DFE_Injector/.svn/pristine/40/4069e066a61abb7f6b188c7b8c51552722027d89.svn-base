__author__ = 'Jens Vankeirsbilck'

import logging
from pyOCD.board import MbedBoard
from time import sleep

class GPIOFaultInjector:
    def __init__(self):
        try:
            self.board = self._initialize()
            self.target = self.board.target
        except Exception as e:
            logging.error("Initialization of GPIOFaultInjector Failed!\n%s" % e)

    def unInit(self):
        if self.board is not None:
            logging.info("Board uninitialised")
            self.board.uninit()

    def changeInput(self, port, bit):
        """
            Function fake a toggle on a pin set as input and
            keeps it toggled (1->0, remains 0; 0->1, remains 1)
        :param port: GPIO port the pin is located at
        :param bit:  Bit that represents the pin at the port
        """
        addressFIOPIN = self._getFIOPINAddress(port)
        addressFIODIR = self._getFIODIRAddress(port)
        logging.debug("FIOPIN address: 0x%X" % addressFIOPIN)
        logging.debug("FIODIR address: 0x%X" % addressFIODIR)
        mask = 1 << bit
        try:
            self.target.halt()
            FIOPIN = self.target.readMemory(addressFIOPIN)
            FIODIR = self.target.readMemory(addressFIODIR)
            logging.debug("Current FIOPIN: 0x%X" % FIOPIN)
            logging.debug("Current FIODIR: 0x%X" % FIODIR)
            FIOPIN ^= mask
            FIODIR ^= mask
            logging.debug("New FIODIR: 0x%X" % FIODIR)
            logging.debug("New FIOPIN: 0x%X" % FIOPIN)
            self.target.writeMemory(addressFIODIR, FIODIR)
            self.target.writeMemory(addressFIOPIN, FIOPIN)
            self.target.resume()
            logging.log(25, "Input from {}.{} changed".format(port, bit))
        except Exception as e:
            logging.error("Something went wrong, could not toggle the input pin!\n%s" % e)

    def toggleInput(self, port, bit):
        """
            Function that fakes a toggle on a pin set as input
            and sets it to its start value (1->0->1; 0->1->0)
        :param port: GPIO port the pin is located at
        :param bit: Bit that represents the pin at the port
        """
        self.changeInput(port, bit)
        sleep(0.05)
        self.changeInput(port, bit)

    def setOutputHigh(self, port, bit):
        """
            Function to set an output pin High
        :param port: GPIO port the pin is located at
        :param bit: Bit that represents the pin at the port
        """
        addressFIOSET = self._getFIOSETAddress(port)
        logging.debug("FIOSET address: 0x%X" % addressFIOSET)
        mask = 1 << bit
        try:
            self.target.halt()
            FIOSET = self.target.readMemory(addressFIOSET)
            logging.debug("Current FIOSET: 0x%X" % FIOSET)
            FIOSET |= mask
            logging.debug("New FIOSET: 0x%X" % FIOSET)
            self.target.writeMemory(addressFIOSET, FIOSET)
            self.target.resume()
            logging.log(25, "Output {}.{} set High".format(port, bit))
        except Exception as e:
            logging.error("Could not set output pin High!\n%s" % e)

    def setOutputLow(self, port, bit):
        """
            Function to set an output pin Low
        :param port: GPIO port the pin is located at
        :param bit: Bit that represents the pin at the port
        """
        addressFIOCLR = self._getFIOCLRAddress(port)
        logging.debug("FIOCLR address: 0x%X" % addressFIOCLR)
        mask = 1 << bit
        try:
            self.target.halt()
            FIOCLR = self.target.readMemory(addressFIOCLR)
            logging.debug("Current FIOCLR: 0x%X" % FIOCLR)
            FIOCLR |= mask
            logging.debug("New FIOCLR: 0x%X" % FIOCLR)
            self.target.writeMemory(addressFIOCLR, FIOCLR)
            self.target.resume()
            logging.log(25, "Output {}.{} set Low".format(port, bit))
        except Exception as e:
            logging.error("Could not set output pin Low!\n%s" % e)

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

    def _getFIOPINAddress(self, port):
        base = 0x2009C014
        offset = port * 0x20
        return (base + offset)

    def _getFIODIRAddress(self, port):
        base = 0x2009C000
        offset = port * 0x20
        return (base + offset)

    def _getFIOSETAddress(self,port):
        base = 0x2009C018
        offset = port * 0x20
        return (base + offset)

    def _getFIOCLRAddress(self, port):
        base = 0x2009C01C
        offset = port * 0x20
        return (base + offset)