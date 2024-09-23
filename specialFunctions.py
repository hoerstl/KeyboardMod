from DQ.surveyMaster import getFreeIceCreamCode
import QuizTaker.main as quizTaker
import localServer
from subprocesses import threadedSubprocess
from popup import displayToUser, getString, OverlayEditModal
import secondaryActions as secActions

from PIL import Image
from io import BytesIO
import multiprocessing as mp
import globals
import requests
import pyperclip
import socket
import time
import os


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

@threadedSubprocess()
def showIcecreamCode(**kwargs):
    freeIceCreamCode = getFreeIceCreamCode()
    displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)


@threadedSubprocess()
def answerVisableQuizQuestion(**kwargs):
    keywordArguments = {key: value for key, value in kwargs.items() if key == 'verbose'}
    displayToUser('Answer', quizTaker.answerVisableQuizQuestion(**keywordArguments), fontSize='small', desiredHeight=200)

@threadedSubprocess()
def answerVisableExtendedResponseQuestion(**kwargs):
    isStealthy = kwargs.get('stealthy')
    
    answer = quizTaker.answerVisableExtendedResponseQuestion()
    if isStealthy:
        pyperclip.copy(answer)
    else:
        displayToUser('Answer', answer, fontSize='small', desiredHeight=200)

    print("Recieved an answer to the extended response question.")


@threadedSubprocess()
def countToTheMoon(**kwargs):
    for i in range(10):
        time.sleep(1)
    print("slept 10 seconds")


@threadedSubprocess()
def hostServer(**kwargs):
    localServer.app.run(host='0.0.0.0', port=8080)

@threadedSubprocess()
def showIPAddress(**kwargs):
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    displayToUser("IP Address", str(ipAddress))

@threadedSubprocess()
def setRemoteServerIP(**kwargs):
    _remoteServerIP = getString("Clipboard Sync IP", "Please enter the IP of the P2P computer you'd like to read the information of.")
    print(f"Got an ip address of {_remoteServerIP}")
    kwargs['mainQueue'].put(('remoteServerIP', _remoteServerIP))


def showRemoteServerIP():
    print(globals.data['remoteServerIP'])


@threadedSubprocess()
def readRemoteClipboard(remoteServerIP, **kwargs):
    url = f"http://{remoteServerIP}:8080/getClipboard"
    try:
        response = requests.get(f"http://{remoteServerIP}:8080/getClipboard")
        remoteClipboardData = response.json()
        print(f"Successfully read remote clipboard data: {remoteClipboardData}")
        pyperclip.copy(remoteClipboardData)
    except requests.exceptions.ConnectionError as e:
        print(f"Couldn't read remote clipboard at {remoteServerIP}")

@threadedSubprocess()
def displayRemoteScreenshot(remoteServerIP, **kwargs):
    try:
        response = requests.get(f"http://{remoteServerIP}:8080/getScreenshot")
        img_data = BytesIO(response.content)
        screenshot = Image.open(img_data) # Read in the image
        print(f"Successfully read remote screenshot displaying...")
        screenshot.show()
    except requests.exceptions.ConnectionError as e:
        print(f"Couldn't read remote screenshot at {remoteServerIP}")



####################################### NOTEPAD LOGIC ##################################
def createNotepadQueue():
    mostRecentNotepadID = globals.data['mostRecentNotepadID']
    if mostRecentNotepadID is None or (not 0 <= mostRecentNotepadID <= 9):
        return None
    # Create a queue and put into the correct spot depending on the 'mostRecentNotepadID'
    newNotepadQueue = globals.data['subprocessManager'].Queue()
    globals.data['notepadQueues'][mostRecentNotepadID] = newNotepadQueue
    return newNotepadQueue



@threadedSubprocess(createSubprocessQueue=createNotepadQueue)
def openNotepad(notepadID, **kwargs):
    """
    This function opens the .txt file and handle all the reading and saving
    """
    if notepadID is None or (not 0 <= notepadID <= 9):
        return None
    notepadPath = f'./notepads/{notepadID}.txt'
    # If the folder doesn't exist, create it
    os.makedirs('./notepads', exist_ok=True)
    textContent = ""
    # If the file doesn't exist, create it
    if not os.path.exists(notepadPath):
        with open(notepadPath, 'x') as file:
            pass
    # Read from the file
    with open(notepadPath, "r") as notepad:
        textContent = ''.join(notepad.readlines())
    
    def saveFunction(textToSave):
        with open(notepadPath, "w") as notepad:
            notepad.write(textToSave)

    def checkActionQueue():
        queue = kwargs['subprocessQueue']
        if queue.empty():
            return None
        return queue.get()
    
    modal = OverlayEditModal(f"Notepad #{notepadID}", textContent, 'small', saveCallback=saveFunction, checkActionQueue=checkActionQueue)
    modal.startMainLoop()


def toggleNotepad(notepadID):
    """
    This function saves and exits irrelevant open notepads if one is open and then
    opens a notepad with notepadID [0, 9].
    """
    mostRecentNotepadID = globals.data['mostRecentNotepadID']

    if mostRecentNotepadID is not None: # If a notepad is open, close it
        globals.data['mostRecentNotepadID'] = None
        toNotepadQueue = globals.data['notepadQueues'][mostRecentNotepadID]
        if toNotepadQueue:
            globals.data['notepadQueues'][mostRecentNotepadID] = None
            toNotepadQueue.put('forcedSaveAndExit')  # Tell the notepad to save and exit

    if notepadID != mostRecentNotepadID: # If the selected notepad is different from the one that was open, open the selected notepad
        globals.data['mostRecentNotepadID'] = notepadID
        asyncOpenNotepad(notepadID)

######################################################################################



def killAllSubprocesses():
    globals.data['subprocessPool'].terminate()
    globals.data['subprocessPool'] = mp.Pool(processes=globals.data['maxSubprocesses'])
    print("All subprocesses killed")



def init():
    """
    This function serves as a place to initialize any submodules that need it
    """
    quizTaker.init()
