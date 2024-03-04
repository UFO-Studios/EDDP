def log(logMessage, function="main"):
    """
    Default EDDP logging function
    Inputs: logMessage, function
    logMessage: The message to log
    function: The function that the log message is coming from
    E.G: log("Hallo!", "main").
    Does not return anything
    """
    out = "EDDP." + function + ": " + logMessage
    print(out)
    return