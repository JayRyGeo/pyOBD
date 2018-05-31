# Logger takes string input and prints to the console
# while also making a log file.

def WriteToLog(logText):
    logFile = open("./OBD.log", "w+")

    writeThis = str(logText) + "\n"

    logFile.writelines(writeThis)
    print(logText)
    logFile.close()