import sys, time, logging

from SendEmail import SendEmail
from MbedTools import MbedTools

class UnityTestHandle(MbedTools):

    receiver = "honzikpoul@gmail.com"

    ## Method for restart mbed on serial port
    def restartMbed(self):
        ser = self.getSerial()
        ser.isOpen()

        # capture output and send mail
        output = self.captureOutput(ser)
        print output
        self.sendMail(output)

        # Close serial
        ser.close()

    def captureOutput(self, ser):
        ser.sendBreak()
        time.sleep(2)
        out = ''
        while ser.inWaiting() > 0:
            out += ser.read(1)
        return out

    def sendMail(self, testOutput):
        logging.info("Prepare email report")
        mail = SendEmail("Just a message", testOutput)
        mail.send(self.receiver)
        logging.info("Report sent to email: %s" % self.receiver)


if __name__ == "__main__":
    test = UnityTestHandle(sys.argv[1:])
    test.copy(True)
