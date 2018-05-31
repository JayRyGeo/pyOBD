import serial
from Logger import WriteToLog
import platform


def scanSerial():
    """scan for available ports. return a list of serial names"""
    available = []

    # Check for Bluetooth in Pi
    for i in range(10):
        # debug : WriteToLog("Trying /dev/rfcomm%s" % i)
        try:
            s = serial.Serial("/dev/rfcomm" + str(i))
            available.append((str(s.port)))
            s.close()  # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass

    # Check for USB in Pi
    for i in range(256):
        # debug : WriteToLog("Trying /dev/ttyUSB%s" % i)
        try:
            s = serial.Serial("/dev/ttyUSB" + str(i))
            available.append(s.portstr)
            s.close()  # explicit close 'cause of delayed GC in java
        except serial.SerialException:
            pass

    # Check in windows
    # The windows module exists for testing against an OBD Simulator
    for i in range(4, 6):
        try:
            s = serial.Serial(
                port='COM' + str(i))
            available.append(s.portstr)
            s.close()
        except serial.SerialException:
            pass

    return available