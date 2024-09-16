from DQ.surveyMaster import getFreeIceCreamCode
import QuizTaker.main as quizTaker
import clipboardServer
from subprocesses import threadedSubProcess
from popup import displayToUser, getString
import secondaryActions as secActions

import multiprocessing as mp
import globals
import requests
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
    secActions.pressAndReleaseKey("Left")
    time.sleep(1e-5)
    wordToCapitalize = pyperclip.paste()
    charIndexToCapitalize = -1
    for i, character in enumerate(wordToCapitalize):
        if character.islower():
            charIndexToCapitalize = i
            letterToReplace = character.upper()
            for j in range(charIndexToCapitalize+1):
                secActions.pressAndReleaseKey("Right")
            secActions.pressAndReleaseKey("Back")
            secActions.pressKeyCombo(f"Lshift+{letterToReplace}")
            break
    if homeDirection == "Left":
        for j in range(charIndexToCapitalize+1):
            secActions.pressAndReleaseKey("Left")
    elif homeDirection == "Right":  # Return cursor back to initial position on right
        for j in range(len(wordToCapitalize) - (charIndexToCapitalize+1)):
            secActions.pressAndReleaseKey("Right")

    pyperclip.copy(initialClipboardContent)

@threadedSubProcess
def showIcecreamCode(**kwargs):
    freeIceCreamCode = getFreeIceCreamCode()
    displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)


@threadedSubProcess
def answerVisableQuizQuestion(**kwargs):
    keywordArguments = {key: value for key, value in kwargs.items() if key == 'verbose'}
    displayToUser('Answer', quizTaker.answerVisableQuizQuestion(**keywordArguments), fontSize='small', desiredHeight=200)

@threadedSubProcess
def answerVisableExtendedResponseQuestion(**kwargs):
    isStealthy = kwargs.get('stealthy')
    
    answer = quizTaker.answerVisableExtendedResponseQuestion()
    if isStealthy:
        pyperclip.copy(answer)
    else:
        displayToUser('Answer', answer, fontSize='small', desiredHeight=200)

    print("Recieved an answer to the extended response question.")


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
    displayToUser("IP Address", str(ipAddress))

@threadedSubProcess
def setRemoteClipboardIP(**kwargs):
    _remoteClipboardIP = getString("Clipboard Sync IP", "Please enter the IP of the computer you'd like to read the clipboard of.")
    print(f"Got an ip address of {_remoteClipboardIP}")
    kwargs['mainQueue'].put(('remoteClipboardIP', _remoteClipboardIP))


def showRemoteClipboardIP():
    print(globals.data['remoteClipboardIP'])


@threadedSubProcess
def readRemoteClipboard(remoteClipboardIP, **kwargs):
    try:
        response = requests.get(f"http://{remoteClipboardIP}:8080")
        remoteClipboardData = response.json()
        print(f"Successfully read remote clipboard data: {remoteClipboardData}")
        pyperclip.copy(remoteClipboardData)
    except requests.exceptions.ConnectionError as e:
        print(f"Couldn't read remote clipboard at {remoteClipboardIP}")



def createNotepadQueue():
    mostRecentNotepadID = globals.data['mostRecentNotepadID']
    if not mostRecentNotepadID:
        return None
    # Create a queue and put into the correct spot depending on the 'mostRecentNotepadID'
    notepadQueue = mp.Queue()

    

@threadedSubProcess(createSubprocessQueue=createNotepadQueue)
def openNotepad(**kwargs):
    # This function needs to open the .txt file and handle all the reading and saving
    pass
    #os.makedirs(, exist_ok=True)



def toggleNotepad(notepadID):
    """
    This function saves and exits irrelevant open notepads if one is open and then
    opens a notepad with notepadID [0, 9].
    """
    # We need some logic that checks if a notepad that isn't the desired notepad is open
    # If it is, then we need to save and exit that one before opening the next

    notepadIsOpen = bool(globals.data['notepadQueues'][notepadID])
    if notepadIsOpen: # close the notepad
        toNotepadQueue = globals.data['notepadQueues'][notepadID]
        toNotepadQueue.put('saveAndExit')  # Tell the notepad to save and exit
        globals.data['notepadQueues'][notepadID] = None
        globals.data['mostRecentNotepadID'] = None
    else: # open the notepad
        globals.data['mostRecentNotepadID'] = notepadID
        asyncOpenNotepad()

    











def killAllSubprocesses():
    for process in globals.data['allSubProcesses']:
        print(f"Killed subprocess: {process}")
        process.terminate()
    globals.data['allSubProcesses'] = []



def init():
    """
    This function serves as a place to initialize any submodules that need it
    """
    quizTaker.init()
