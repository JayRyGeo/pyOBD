# This is my own adaptation of the pyOBD application
from GetPorts import scanSerial as GetPorts
from dualIO import WriteToLog
import OBDConn
import serial
import time

def Testing():
    baudList = [9600, 38400, 19200, 57600, 115200]

    portList = []
    portList = GetPorts()

    WriteToLog("Found ports: %s" % portList)
    time.sleep(1)

    if portList != None:
        for port in portList:
            for baud in baudList:
                WriteToLog("Attemping %s with baud %s" % (port, baud))
                time.sleep(1)
                conn = OBDConn.OBDConn(port, baud)
                time.sleep(1)


Testing()