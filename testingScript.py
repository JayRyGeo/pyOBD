# Testing script to help figure out the programming flow.

# script dependant includes
import RPi.GPIO as GPIO
from Logger import WriteToLog
import time
import os

# normalCapture() includes
from obd_capture import OBD_Capture
from obd_utils import scanSerial as GetPort

# findBaudRate() includes
from obd_io import OBDPort

# Memory for the buttons
btn1 = 0
btn2 = 0
btn3 = 0
btn4 = 0

# GPIO locations of the buttons in order from top to bottom
# when the buttons are on the right of the screen
btn1Loc = 17
btn2Loc = 22
btn3Loc = 23
btn4Loc = 27
GPIO.setmode(GPIO.BCM)

# Setup the buttons to capture data.
GPIO.setup(btn1Loc, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn2Loc, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn3Loc, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(btn4Loc, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def normalCapture():
    """"Run the OBD_IO script with static values to capture OBD Data"""
    cap = OBD_Capture()
    cap.connect()
    portState = cap.is_connected()

    if portState is None:
        print("Cannot connect to car.  Please check connections and try again.")


def findBaudRate():
    """"Find the Baud Rate by Iterating Through Common Rates"""
    # Standard baud rates come from the pySerial documentation. Alt baud list comes from
    # python-OBD read the docs.
    stdBaudList = [50, 75, 110, 134, 150, 200, 300, 600, 1200, 1800, 2400, 4800, 9600, 19200, 38400, 57600, 115200]
    altBaudList = [9600, 38400, 19200, 57600, 115200]

    # Protocols, this may come in hand later
    # https://python-obd.readthedocs.io/en/latest/Connections/#protocol_id

    successPortBaud = { 'Port' : 'Baud' }
    #time.sleep(5)

    # Get Port
    portlist = []
    portlist = GetPort()

    WriteToLog("Found ports: %s" % portlist)
    time.sleep(5)

    for port in portlist:
        for baud in stdBaudList:
            WriteToLog("Attempting Baud %s on Port %s " % (baud,port))
            time.sleep(5)
            obdConn = OBDPort(port, baud, 2)
            time.sleep(5)

            if ( obdConn == True ):
                WriteToLog("Successfull Connection: Port %s, Baud %s" % (port, baud))
                successPortBaud[str(port)] = str(baud)




def printActivePorts():
    """Log the Active Ports on the System"""
    devList = []

    for entry in os.walk("/dev"):
        # Make a list, for future use as what we are doing can easily be accomplished without
        # the use of a list.
        devList.append(entry)

    WriteToLog(devList)


# Clear the terminal
os.system("clear")

# Print welcome screen and menu
print("Button Actions:")
print("[TOP]\tNormal Capture Mode")
print("[2nd]\tFind Baud Rate")
print("[3rd]\tPrint Active Ports on Device")
print("[Btm]\tEMPTY")

while True:
    # Btn 1
    Btn1_state = GPIO.input(btn1Loc)
    if Btn1_state == False:
        if btn1 == 1:
            btn1 = 0
            #off action
        else:
            btn1 = 1
            normalCapture()
        time.sleep(0.5)

    # Btn 2
    Btn2_state = GPIO.input(btn2Loc)
    if Btn2_state == False:
        if btn2 == 1:
            btn2 = 0
            # off action
        else:
            btn2 = 1
            findBaudRate()
        time.sleep(60)

    # Btn 3
    Btn3_state = GPIO.input(btn3Loc)
    if Btn3_state == False:
        if btn3 == 1:
            btn3 = 0
            # off action
        else:
            btn3 = 1
            printActivePorts()
        time.sleep(0.5)

    # Btn 4


time.sleep(60)