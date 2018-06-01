# Logger takes string input and prints to the console
# while also making a log file.

def WriteToLog(logText):
    """Allows for printing to the console and logging at the same time"""
    print(logText)
    with open('./OBD.log', 'a') as logFile:
        logFile.write(logText + "\n")