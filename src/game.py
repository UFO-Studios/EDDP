import json
import os
import glob
import getpass
from log import log

global username
username = getpass.getuser()

global journalPath
journalPath = (
    "C:/Users/" + username + "/Saved Games/Frontier Developments/Elite Dangerous"
)

cmdr_name = "CMDR"

global eventAssociationsMain
global eventAssociationsDocked
global eventAssociationsCombat
global eventAssociationsPlanetside
eventAssociationsMain = {
    "SupercruiseEntry": "Supercrusing in ", 
    "SupercruiseExit": "Flying around ",
    "FSDJump": "Supercrusing in ",
    "Undocked": "Flying in ",
    "LeaveBody": "Flying in ",
    }
eventAssociationsDocked = {
    "Touchdown": "Landed on ",
    "Docked": "Docked at ",
    "DockingGranted": "Docked at ",
    "DockingRequested": "Docked at ",
}
eventAssociationsCombat = {"UnderAttack": "In a fight!"}
eventAssociationsPlanetside = {"LaunchSRV": "Driving on ", "ApproachBody": "Flying to ", }


def load(logDir):
    """
    Loads the log file and returns it as a list.
    Accepts logDir as string.
    """
    log("Parsing log file", "load")
    log_files = glob.glob(os.path.join(logDir, "*.log"))
    latest_file = max(log_files, key=os.path.getmtime)
    log("Opening log file " + str(latest_file), "load")
    res = []
    i = 0
    with open(latest_file) as f:
        for line in f:
            line = line.strip()  # Remove leading/trailing whitespace
            if line:  # Skip empty lines
                try:
                    data = json.loads(line)
                    res.append(data)
                    i = i +1
                except json.JSONDecodeError:
                    log(f"Skipping line: {line}", "load")
    log("Log file parsed, "  + str(i) + " lines found", "load")
    res.reverse()  # so that it will stop when at the latest event it recognizes
    return res


def getCMDR(logs):
    """
    Returns the commander name as a string.
    Accepts logs as a list. (array)
    """
    log("Parsing log data", "getCMDR")
    logs.reverse()  # becuase we want the first one. Undoes line 34
    cmdr_name = " "
    if len(logs) < 2:
        log("Game not fully loaded, skipping update for now...", "getCMDR")
        return 1
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Commander":
                    cmdr_name = logLine.get("Name", "")
                    log(f"Found commander: {cmdr_name}", "getCMDR")
                    return cmdr_name
            except Exception:
                log("No commander found", "getCMDR")
                return "Unknown"


def getSystem(logs, gm=False):
    """
    Returns the system name as a string.
    Accepts logs as a list. (array)
    """
    if gm == True:
        log("Ghost mode active. Skipping...", "getSystem")
        return
    log("Parsing log data - looking for system name", "getSystem")
    system_name = " "
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Location":
                    system_name = logLine.get("StarSystem", "")
                    log(f"Found system: {system_name}", "getSystem")
                    return system_name  # because we start with the latest one, we can just return it straight away
                if logLine["event"] == "FSDJump":
                    system_name = logLine.get("StarSystem", "")
                    log(f"Found system: {system_name}", "getSystem")
                    return system_name
            except Exception:
                log("No system found", "getSystem")
                return "Unknown system"


def getStation(logs, ghostMode=False):
    """
    Returns the station name as a string.
    Accepts logs as a list. (array)
    """
    if ghostMode == True:
        log("Ghost mode active. Skipping...", "getStation")
    log("Parsing log data - looking for station", "getStation")
    for logLine in logs:
        if "event" in logLine:
            try:
                if logLine["event"] == "Location":
                    log("Location entry detected!", "getStation")
                    station_name = logLine.get("StationName", "")
                    log(f"Found station: {station_name}", "getStation")
                if "Docked" in logLine:
                    station_name = logLine.get("StationName", "")
                    log(f"Found station: {station_name}", "getStation")
                else:
                    log("No station found", "getStation")
                    station_name = "Unknown station"
                    return station_name
            except Exception:  # If it gets muddled, it will return "Unknown station"
                log("No station found", "getStation")
                station_name = "Unknown station"
            return station_name



def eventHandler(event, logLineNum=0, ghostMode=False):
    """
    Event handler for journal events.
    Run once per line.
    Accepts event as string.
    If the event is not recognized, it will return 1.
    If the event is recognized, it will return the event type as a string.
    If it detects a shutdown, it will return 0.
    """
    log(f"Parsing log data - looking for events in {event}...", "eventHandler")

    if ghostMode == True:
        log("Ghost mode on!", "eventHandler")
        match event:
            case "Shutdown":
                return 0
            case "Location":
                log("Location entry detected!", "eventHandler")
                fullLogLine = load(journalPath)[logLineNum]
                if fullLogLine["Docked"] == True:
                    log("Docked", "eventHandler")
                    return "Docked"
                else:
                    log("Not docked", "eventHandler")
                    return "Flying around"
            case _ if event in eventAssociationsMain:
                return "Flying around"
            case _ if event in eventAssociationsDocked:
                return "Docked"
            case _ if event in eventAssociationsCombat:
                return eventAssociationsCombat[event]
            case _ if event in eventAssociationsPlanetside:
                return "Exploring a planet"
            case _:
                return 1
    
        

    match event:
        case "Shutdown":
            return 0
        case "Location":
            log("Location entry detected!", "eventHandler")
            fullLogLine = load(journalPath)[logLineNum]
            if fullLogLine["Docked"] == True:
                log("Docked", "eventHandler")
                return "Docked at " + getStation(load(journalPath), ghostMode)
            else:
                log("Not docked", "eventHandler")
                return "Flying around " + getSystem(load(journalPath), ghostMode)
        case _ if event in eventAssociationsMain:
            return eventAssociationsMain[event] + getSystem(load(journalPath), ghostMode)
        case _ if event in eventAssociationsDocked:
            return eventAssociationsDocked[event] + getStation(load(journalPath), ghostMode)
        case _ if event in eventAssociationsCombat:
            return eventAssociationsCombat[event]
        case _ if event in eventAssociationsPlanetside:
            return eventAssociationsPlanetside[event] + getSystem(load(journalPath), ghostMode)
        case _:
            return 1
        
