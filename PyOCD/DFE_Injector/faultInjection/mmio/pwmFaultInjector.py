__author__ = 'Jens Vankeirsbilck'

import logging
import random
from pyOCD.board import MbedBoard


class PWMFaultInjector:
    def __init__(self, board=None):
        self.TCR = 0x40018004
        self.PCR = 0x4001804C
        if board is None:
            try:
                self.board = self._initialize()
                self.target = self.board.target
            except Exception as e:
                logging.error("Initialization of PWMFaultInjector failed!\n%s" % e)
        else:
            self.board = board
            self.target = self.board.target

    # Public methods
    def unInit(self):
        if self.board is not None:
            logging.info("Board uninitialised")
            self.board.uninit()

    def togglePWMPower(self):
        """
            Function to inject flip the bit in
            the power register so PWM turns on or off
        """
        # PCPWM1 is located at position 6
        mask = 1 << 6
        self._injectFault("PCONP", 0x400FC0C4, mask)

    def togglePWMEnable(self):
        """
            Function to toggle the enable bit
            that controls the full PWM system
        """
        mask = 1 << 3
        self._injectFault("PWM1TCR", self.TCR, mask)

    def togglePWMPinEnable(self, PWMpin):
        """
            Function to toggle the enable bit that
            controls a specific PWMpin
        :param PWMpin: PWMpin that the injected fault must affect
            1 = p26; 2 = p25; 3 = p24; 4 = p23; 5 = p22; 6 = p21
        """
        bitPos = PWMpin + 8
        mask = 1 << bitPos
        self._injectFault("PWM1PCR",self.PCR,mask)

    def toggleCounterEnable(self):
        """
            Function to toggle the counter enable bit
            of TCR
        """
        mask = 1
        self._injectFault("PWM1TCR", self.TCR, mask)

    def toggleEdgeMode(self, PWMpin):
        """
            Function to toggle between single or double edge
            controlled mode for PWM of the selected pin
        :param PWMpin: PWMpin that the injected fault must affect
            1 = p26; 2 = p25; 3 = p24; 4 = p23; 5 = p22; 6 = p21
        """
        mask = 1 << PWMpin
        self._injectFault("PWM1PCR", self.PCR, mask)

    def injectPWM(self, PWMpin):
        """
            Function to inject a fault in the memory mapped
            PWM location
            ! Only works when 2 bits are flipped !
        :param PWMpin: PWMpin that the injected fault must affect
            1 = p26; 2 = p25; 3 = p24; 4 = p23; 5 = p22; 6 = p21
        """
        try:
            address = self._getPWMRegister(PWMpin)
            self.target.halt()
            # Emulate do-while loop
            bitPos = random.randint(1,32)
            current = self.target.readMemory(address)
            newContent = current ^ (1 << bitPos)
            if newContent > 0xE100 or newContent < 0x3840:
                logging.debug("New content 0x%X not safe!" % newContent)
                safe = False
            else:
                safe = True
            while not safe:
                logging.debug("New try to find a safe value for PWM")
                bitPos = random.randint(1,32)
                current = self.target.readMemory(address)
                newContent = current ^ (1 << bitPos)
                if newContent > 0xE100 or newContent < 0x3840:
                    logging.debug("New content 0x%X not safe!" % newContent)
                    safe = False
                else:
                    safe = True
            logging.log(25,
                "Eventually flipping bit at position {}, generating the new content 0x{:X}".format(bitPos,newContent))
            self.target.writeMemory(address, newContent)
            self.target.writeMemory(0x40018050, (1 << PWMpin))
        except Exception as e:
            logging.error("Could not inject a fault that affects PWM\n%s" % e)
        finally:
            self.target.resume()

    # Private methods
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

    def _getPWMRegister(self, PWMPin):
        """
            Function to get the correct address of the PWMregister
            matching the PWMPin
        :param PWMpin: PWMpin that the injected fault must affect
        :return: the address of the PWMMR register
        """
        if PWMPin == 1:
            logging.debug("PWMPin is 1, returning address 0x4001801C")
            return 0x4001801C
        elif PWMPin == 2:
            logging.debug("PWMPin is 2, returning address 0x40018020")
            return 0x40018020
        elif PWMPin == 3:
            logging.debug("PWMPin is 3, returning address 0x40018024")
            return 0x40018024
        elif PWMPin == 4:
            logging.debug("PWMPin is 4, returning address 0x40018040")
            return 0x40018040
        elif PWMPin == 5:
            logging.debug("PWMPin is 5, returning address 0x40018044")
            return 0x40018044
        elif PWMPin == 6:
            logging.debug("PWMPin is 6, returning address 0x40018048")
            return 0x40018048
        else:
            raise Exception("Only 1 - 6 supported as PWMPin")

    def _injectFault(self, regName, regAddress, mask):
        """
            Function to inject a fault (defined by mask) in the register with
            name regName, address regAddress
        :param regName: Name of the register
        :param regAddress: Address of the register
        :param mask: bit to flip
        """
        try:
            self.target.halt()
            current = self.target.readMemory(regAddress)
            logging.debug("Current {}: 0x{:X}".format(regName,current))
            newContent = current ^ mask
            logging.debug("New content to be written: 0x%X" % newContent)
            self.target.writeMemory(regAddress, newContent)
            logging.log(25, "Successfully injected fault into %s" % regName)
        except Exception as e:
            logging.error("Failed to inject a fault into {}!\n{}".format(regName,e))
        finally:
            self.target.resume()