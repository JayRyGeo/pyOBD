import serial
import time
from dualIO import WriteToLog

class OBDConn:
    """The Serial Port that will be created to interact with the OBD Device"""
    def __init__(self, portnum, baudRate):
        # Attempt to connect to the device with the passed parameters
        try:
            WriteToLog("Attempting to connect to port %s with baud rate of %s" %(portnum,baudRate))
            self.activePort = serial.Serial(port=portnum, baudrate=baudRate, bytesize=serial.EIGHTBITS,
                                            parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=2)
        except serial.SerialException:
            WriteToLog("Connecting to port %s was unsuccessful..." % portnum)
            time.sleep(2)
            return None

        # If we get this far, we have a successful connection to the device. We need to test the connection to the
        # car next.
        WriteToLog("Successfully connected on %s" % self.activePort.name)
        WriteToLog("Attempting to connect to the ECU...")
        time.sleep(2)

        # Check the ELM Version first by resetting the device and forcing identification
        self.ELM = self.CmdControl("ATZ")
        WriteToLog(self.ELM)

        # Check the status of the device to see if we are okay to send requests
        WriteToLog("Checking status...")
        time.sleep(1)
        self.at0Status = self.CmdControl("AT0")
        if self.at0Status == "OK" or self.at0Status == "Ok":
            WriteToLog(self.at0Status)
        else:
            WriteToLog("AT0 says not ready: %s" % self.at0Status)
            time.sleep(2)

        # Close the port when we are all done because it won't self destruct and the values will carry over
        WriteToLog("All actions performed, closing port...\n")
        self.activePort.close()
        time.sleep(2)


    def CmdControl(self, cmd):
        """Handles the input and output to the car, returns a sting of the response"""
        self.activePort.flushInput()
        self.activePort.flushOutput()

        # The return signals the end of a command for the device
        cmd = cmd + "\r"

        self.activePort.write(cmd.encode())
        response = self.activePort.read(64)

        # Strip out the extras from the response, this will leave us with a Hex value
        response.replace("\r\n>", "")
        response.replace(" ", "")

        return response