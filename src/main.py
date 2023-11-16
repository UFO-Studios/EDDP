from discordrp import Presence
import time
import getpass
import os
import threading
import queue
import sys

Queue = queue.Queue()
from iconTray import createIcon
from log import log
from game import getCMDR, load, eventHandler
global username
username = getpass.getuser()
global currently
currently = "nope"


def awaitGame():
    """
    Detects the game launch by checking for new journal files.
    Runs mainGameLoop() when the game is found.
    Checks every 15s.
    Does not return anything.
    """
    log("Awaiting game", "awaitGame")
    while True:
        #list logs dir
        listOne = os.listdir("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        time.sleep(15)
        listTwo = os.listdir("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        if listOne != listTwo:
            log("Game found", "awaitGame")
            mainGameLoop()
        else:
            log("Game not found", "awaitGame")
            pass

def updatePrecense(presence, state, start_time, cmdr):
    """
    Updated the data send to discord
    Inputs:
    presence: the discordrp.Presence object
    state: The main message to be displayed
    start_time: the time the game was started (int)
    cmdr: the cmdr's name
    Does not return anything
    """
    state = str(state) + "  "
    presence.set(
        {
            "state": str(state),
            "details": "Playing Elite: Dangerous as CMDR " + str(cmdr),
            "timestamps": {
                "start": start_time,
            },
            "assets": {
                "large_image": "ed_main",  

            },

            
        }
    )
    log("Presence updated", "updatePrecense")


client_id = "1170388114498392095"  

def mainGameLoop():
    time.sleep(1)
    currently = "Loading EDDP..."
    log("Starting game loop", "mainGameLoop")
    currently = " "
    start_time = int(time.time())
    now = "  "

    with Presence(client_id) as presence:
        logFileLoaded = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
        log("Connected", "mainGameLoop")
        cmdr = getCMDR(logFileLoaded)
        if cmdr == 1:
            log("CMDR not found, trying again in 3s", "mainGameLoop.initBoot")
            time.sleep(3)
            mainGameLoop()
        updatePrecense(presence, "In the main menu", start_time, cmdr)

        while True:
            if Queue.get() == "exit":
                log("Exiting...", "mainGameLoop")
                break
            elif Queue.get() == "ghostModeOn":
                log("Ghost mode enabled", "mainGameLoop")
                
            time.sleep(15)
            logs = load("C:/Users/"+username+"/Saved Games/Frontier Developments/Elite Dangerous")
            j = 0
            while j < len(logs):
                if len(logs) < 2:
                    log("Game not fully loaded, skipping update for now...", "mainGameLoop")
                    break
                logLineNow = logs[j]
                now = eventHandler(logLineNow["event"], j)
                log("Event: " + str(now) + " No: " + str(j), "mainGameLoop")
                j += 1
                if now != 1:
                    currently = now
                    break
                else: 
                    currently = "In the main menu"
                    pass

            if now == 0:
                log("Exiting...", "mainGameLoop")
                
                
            updatePrecense(presence, currently, start_time, cmdr)
            
            
def main():
    if 'debugpy' in sys.modules:
        log("Running in VSC debug mode!", "debug")
        mainGameLoop()
    else:
        awaitGame()

if __name__ == "__main__":
    log("Starting...", "__name__")
    icon_thread = threading.Thread(target=createIcon(Queue))
    game_thread = threading.Thread(target=main)
    icon_thread.start()
    game_thread.start()
    time.sleep(2)
    log("All threads running! ", "__name__")
else:
    log("Uh-Oh you seem to be importing this! Try running the main.py file instead!", "__name__")