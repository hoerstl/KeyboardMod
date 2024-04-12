from DQ.surveyMaster import getFreeIceCreamCode
import wrappers
from wrappers import threadedSubProcess
from popup import displayToUser
import secondaryActions as secActions
import pyperclip
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

@threadedSubProcess
def showIcecreamCode():
    freeIceCreamCode = getFreeIceCreamCode()
    displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

@threadedSubProcess
def countToTheMoon():
    for i in range(10):
        time.sleep(1)
    print("slept 10 seconds")

def killAllSubprocesses():
    for process in wrappers.allSubProcesses:
        process.terminate()
    wrappers.allSubProcesses = []


