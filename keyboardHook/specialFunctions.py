from DQ.surveyMaster import getFreeIceCreamCode
import QuizTaker.main as quizTaker
import localServer
from subprocesses import threadedSubprocess
from popup import displayToUser, getString, OverlayEditModal
from settings import PaginatedSettingsWindow
import convenienceFunctions as kbd

from PIL import Image
from io import BytesIO
import ctypes
import multiprocessing as mp
import globals
import requests
import pyperclip
import socket
import time
import os
import runpy

def typeTemplate(template):
    template += '|' if '|' not in template else ''
    first, second = template.split('|')
    for char in first:
        kbd.typeCharacter(char)
    for char in second:
        kbd.typeCharacter(char)
    lines_in_second = second.split('\n')
    if len(lines_in_second) > 1:  # Move to the right spot
        for character in lines_in_second[-1]:  # Move to the start of the line you're on
            kbd.pressAndReleaseKey('Left')
        for line in range(len(lines_in_second) - 1):  # Move up a number of lines equal to the number of lines since the cursor position
            kbd.pressAndReleaseKey('Up')
        for character in first.split('\n')[-1]:  # Move right the correct number of times
            kbd.pressAndReleaseKey('Right')
    else:
        for character in second:
            kbd.pressAndReleaseKey('Left')


@threadedSubprocess()
def showIcecreamCode(**kwargs):
    freeIceCreamCode = getFreeIceCreamCode()
    displayToUser('DQ', f"Your icecream my leige: {freeIceCreamCode}", 800)


@threadedSubprocess()
def answerVisableQuizQuestion(**kwargs):
    keywordArguments = {key: value for key, value in kwargs.items() if key == 'verbose'}
    quizTaker.init(kwargs['GOOGLE_API_KEY'])
    displayToUser('Answer', quizTaker.answerVisableQuizQuestion(**keywordArguments), fontSize='small', desiredHeight=200)

@threadedSubprocess()
def answerVisableExtendedResponseQuestion(**kwargs):
    isStealthy = kwargs.get('stealthy')
    quizTaker.init(kwargs['GOOGLE_API_KEY'])
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
def clickMouseXTimes(timesToClick, **kwargs):
    MOUSEEVENTF_MOVE = 0x0001
    MOUSEEVENTF_ABSOLUTE = 0x8000
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

    for _ in range(timesToClick):
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        time.sleep(0.05)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)


@threadedSubprocess(atomic=True)
def hostServer(**kwargs):
    localServer.startApplication(kwargs['mainQueue'])
    kwargs['mainQueue'].put(('command', ('terminateAtomicSubprocess', hostServer.__name__)))

@threadedSubprocess(atomic=True)
def showIPAddress(**kwargs):
    hostname = socket.gethostname()
    ipAddress = socket.gethostbyname(hostname)
    displayToUser("IP Address", str(ipAddress))
    kwargs['mainQueue'].put(('command', ('terminateAtomicSubprocess', showIPAddress.__name__)))


def showRemoteServerIP():
    print(globals.settings['remoteServerIP'])


@threadedSubprocess()
def readRemoteClipboard(remoteServerIP, **kwargs):
    url = f"http://{remoteServerIP}:8080/getClipboard"
    try:
        response = requests.get(f"http://{remoteServerIP}:8080/getClipboard")
        remoteClipboardData = response.json()
        print(f"Successfully read remote clipboard data: {remoteClipboardData}")
        kwargs['mainQueue'].put(('remoteServerClipboard', remoteClipboardData))
    except requests.exceptions.ConnectionError as e:
        print(f"Couldn't read remote clipboard at {remoteServerIP}")
        kwargs['mainQueue'].put(('command', ('remoteClipboardReadFailed', None)))

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

@threadedSubprocess()
def sendNotify(remoteServerIP, **kwargs):
    requests.get(f"http://{remoteServerIP}:8080/notify")

@threadedSubprocess()
def notify(**kwargs):
    for _ in range(8):
        print("pressing capital")
        kbd.pressAndReleaseKey('Capital')
        time.sleep(.5)


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
    kwargs['mainQueue'].put(('command', ('closeNotepad', notepadID)))


def toggleNotepad(notepadID):
    """
    This function saves and exits irrelevant open notepads if one is open and then
    opens a notepad with notepadID [0, 9].
    """
    mostRecentNotepadID = globals.data['mostRecentNotepadID']

    if mostRecentNotepadID is not None: # If a notepad is open, close it
        toNotepadQueue = globals.data['notepadQueues'][mostRecentNotepadID]
        if toNotepadQueue:
            toNotepadQueue.put('forcedSaveAndExit')  # Tell the notepad to save and exit
    elif notepadID != mostRecentNotepadID: # If the selected notepad is different from the one that was open, open the selected notepad
        globals.data['mostRecentNotepadID'] = notepadID
        asyncOpenNotepad(notepadID)

######################################################################################

@threadedSubprocess(atomic=True)
def openSettingsMenu(settings, **kwargs):
    root = PaginatedSettingsWindow(lambda key, value: kwargs['mainQueue'].put((key, value)), default_values=settings)
    root.mainloop()
    kwargs['mainQueue'].put(('command', ('terminateAtomicSubprocess', openSettingsMenu.__name__)))



def killAllSubprocesses():
    globals.data['subprocessPool'].terminate()
    globals.data['subprocessPool'] = mp.Pool(processes=globals.data['maxSubprocesses'])
    globals.data['atomicSubprocesses'] = set()
    globals.data['mostRecentNotepadID'] = None
    globals.data['notepadQueues'] = [None for _ in globals.data['notepadQueues']]
    print("All subprocesses killed")



def init():
    """
    This function serves as a place to initialize any submodules that need it
    """
    pass





@threadedSubprocess()
def runPythonFile(filepath, **kwargs):
    runpy.run_path(filepath)




