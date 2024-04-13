from DQ.surveyMaster import getFreeIceCreamCode
import clipboardServer
import subprocesses
from subprocesses import threadedSubProcess
from popup import displayToUser, getString
import secondaryActions as secActions

import globals
import pyperclip
import socket
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
def showIcecreamCode(**kwargs):
    freeIceCreamCode = getFreeIceCreamCode()
    displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)

@threadedSubProcess
def countToTheMoon(**kwargs):
    for i in range(10):
        time.sleep(1)
    print("slept 10 seconds")


@threadedSubProcess
def hostClipboard(**kwargs):
    clipboardServer.app.run(host='0.0.0.0', port=8080)

@threadedSubProcess
def showIPAddress(**kwargs):
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    displayToUser("IP Address", str(ip_address))

@threadedSubProcess
def setRemoteClipboardIP(**kwargs):
    _remoteClipboardIP = getString("Clipboard Sync IP", "Please enter the IP of the computer you'd like to read the clipboard of.")
    print(f"Got an ip address of {_remoteClipboardIP}")
    kwargs['queue'].put(('remoteClipboardIP', _remoteClipboardIP))


def showRemoteClipboardIP():
    print(globals.data['remoteClipboardIP'])


def killAllSubprocesses():
    for process in globals.data['allSubProcesses']:
        print(f"Killed subprocess: {process}")
        process.terminate()
    globals.data['allSubProcesses'] = []



