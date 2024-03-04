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
    initialClipboardContent = pyperclip.paste()
    if direction == "Right":
        secActions.pressKeyCombo(f"Lcontrol+Lshift+{direction}")
        secActions.pressKeyCombo("Lcontrol+C")
        secActions.pressKey("Left")
        wordToCapitalize = pyperclip.paste()
        print(wordToCapitalize)
        for i, character in enumerate(wordToCapitalize):
            if character.islower():
                letterToReplace = character.upper()
                for j in range(i+1):
                    secActions.pressKey("Right")
                secActions.pressKey("Back")
                secActions.pressKeyCombo(f"Lshift+{letterToReplace}")
                secActions.pressKey("Left")
                break
        pyperclip.copy(initialClipboardContent)




def showTaskScheduler():
    def target():
        global taskSchedulerPath, taskSchedulerModule
        print("Ran the target")
        os.chdir(taskSchedulerPath)
        taskSchedulerModule.main()

    thread = threading.Thread(target=target)
    thread.start()


def showIcecreamCode():
    def target():
        freeIceCreamCode = getFreeIceCreamCode()
        displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

    thread = threading.Thread(target=target)
    thread.start()


def init():
    global taskSchedulerPath, taskSchedulerModule
    #  For the task scheduler
    taskSchedulerPath = "\\".join(os.getcwd().split("\\") + ["ADHDassist"])
    sys.path.append(taskSchedulerPath)
    taskSchedulerModule = importlib.import_module("ADHDassist.main", "ADHDassist")


taskSchedulerModule = None
taskSchedulerPath = None
init()
