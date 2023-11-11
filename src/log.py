import datetime
import getpass

username = getpass.getuser()
global logDir 
logDir =  "C:/Users/"+username+"/.AW2C/EDDP/logs"
global logFile
logFile = "LOG - " + str(datetime.datetime.now().strftime("%Y-%m-%d")) + ".log"


def logToConsole(logMessage, function="main"):
    out = "EDDP." + function + ": " + logMessage
    print(out)

# def logToFile(logMessage, function):
#     out = "eddp." + function + ": " + logMessage
#     with open(logDir + "/" + logFile, "a") as f:
#         f.write(out + "\n")
#     f.close()

def log(logMessage, function):
    logToConsole(logMessage, function)
    #logToFile(logMessage, function)
    return True