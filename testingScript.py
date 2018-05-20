
# Testing script to help figure out the programming flow.

from obd_capture import OBD_Capture

cap = OBD_Capture()
cap.connect()
portState = cap.is_connected()

if portState is None:
    print("Cannot connect to car.  Please check connections and try again.")
