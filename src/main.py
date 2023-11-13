from discordrp import Presence
import time
import getpass
import os
import pystray
from PIL import Image
import threading
import sys

from log import log
from game import getCMDR, load, eventHandler
global username
username = getpass.getuser()
global currently
currently = "nope"
global shutdownBool
shutdownBool = False

#the icon for the tray
def create_icon():
    image = Image.open(str(os.getcwd()) + '\\src\\icon.png')
    icon = pystray.Icon("EDDP", image)
    #action for exit
    def action(icon, item):
        exit(1)
    #action for the status text
    def action_online(icon, item):
        log("Online!", "tray")

    # Add a menu item to the icon
    icon.menu = pystray.Menu(
        pystray.MenuItem('Online!', action_online),
        pystray.MenuItem('Quit', action)
        )

    # Run the icon
    icon.run()


def awaitGame():
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
    state = str(state) + ""
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
            if shutdownBool == True:
                log("Shutdown detected, exiting...", "mainGameLoop.shutdownDetect")
                break
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
                exit()
                
            updatePrecense(presence, currently, start_time, cmdr)
            
            
if __name__ == "__main__":
    icon_thread = threading.Thread(target=create_icon)

    # Start the thread
    icon_thread.start()
    if 'debugpy' in sys.modules:
        log("Running in VSC debug mode!", "debug")
        mainGameLoop()
    else:
        awaitGame()