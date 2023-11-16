from log import log
from main import updatePrecense


def ActivateGhostMode():
    log("Ghost mode activating...", "ghost")
    updatePrecense("In the main menu", 0, "Ghost mode enabled")
    