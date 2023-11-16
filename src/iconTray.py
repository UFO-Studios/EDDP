import pystray
from PIL import Image
import os
from log import log

#the icon for the tray
def createIcon(Queue):
    image = Image.open(str(os.getcwd()) + '\\src\\icon.png')
    icon = pystray.Icon("EDDP", image)
    global gm #gm = ghost mode. this is used for the tray menu
    #action for ghost mode
    def ghostMode(icon, item):
        Queue.put("ghostMode")
        log("Ghost mode enabled", "createIcon")
        Queue.put("GMon") # ghost mode on
        gm = 'off' if gm == 'on' else 'on'
        #gm = False
        icon.menu = pystray.Menu(
        pystray.MenuItem('Ghost mode ' + gm, ghostMode),
        pystray.MenuItem('Online!', action_online),
        pystray.MenuItem('Quit', action)
        )
        icon.update_menu()
    
        
    #action for exit
    def action(icon, item):
        Queue.put("exit")
        print("Exiting...")
    #action for the status text
    def action_online(icon, item):
        log("Online!", "tray")

    # Add a menu item to the icon
    icon.menu = pystray.Menu(
        pystray.MenuItem('Ghost mode ' + gm, ghostMode),
        pystray.MenuItem('Online!', action_online),
        pystray.MenuItem('Quit', action)
        )

    # Run the icon
    icon.run()