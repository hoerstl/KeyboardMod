from DQ.surveyMaster import getFreeIceCreamCode
from popup import displayToUser
import secondaryActions as secActions
import pyperclip
import importlib
import threading
import sys
import os
import time


def capitalizeWord(direction):
    assert direction == "Left" or direction == "Right"
    initialClipboardContent = pyperclip.paste()
    homeDirection = "Left" if direction == "Right" else "Right"
    secActions.pressKeyCombo(f"Lcontrol+Lshift+{direction}")
    secActions.pressKeyCombo("Lcontrol+C")
    time.sleep(1e-5)
    secActions.pressKey("Left")
    time.sleep(1e-5)
    wordToCapitalize = pyperclip.paste()
    charIndexToCapitalize = -1
    for i, character in enumerate(wordToCapitalize):
        if character.islower():
            charIndexToCapitalize = i
            letterToReplace = character.upper()
            for j in range(charIndexToCapitalize+1):
                secActions.pressKey("Right")
            secActions.pressKey("Back")
            secActions.pressKeyCombo(f"Lshift+{letterToReplace}")
            break
    if homeDirection == "Left":
        for j in range(charIndexToCapitalize+1):
            secActions.pressKey("Left")
    elif homeDirection == "Right":  # Return cursor back to initial position on right
        for j in range(len(wordToCapitalize) - (charIndexToCapitalize+1)):
            secActions.pressKey("Right")

    pyperclip.copy(initialClipboardContent)


# def showTaskScheduler():
#     def target():
#         global taskSchedulerPath, taskSchedulerModule
#         print("Ran the target")
#         os.chdir(taskSchedulerPath)
#         taskSchedulerModule.main()
#
#     thread = threading.Thread(target=target)
#     thread.start()


def showIcecreamCode():
    def target():
        freeIceCreamCode = getFreeIceCreamCode()
        displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

    thread = threading.Thread(target=target)
    thread.start()


def init():
    # global taskSchedulerPath, taskSchedulerModule
    # #  For the task scheduler
    # taskSchedulerPath = "\\".join(os.getcwd().split("\\") + ["ADHDassist"])
    # sys.path.append(taskSchedulerPath)
    # taskSchedulerModule = importlib.import_module("ADHDassist.main", "ADHDassist")
    pass


# taskSchedulerModule = None
# taskSchedulerPath = None
init()
