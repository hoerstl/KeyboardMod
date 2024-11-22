import multiprocessing as mp
import dotenv
import os
from collections import defaultdict
import settings as sett
data = {}
settings = {}
flags = {}
keypress_bypass = defaultdict(int)
keyrelease_bypass = defaultdict(int)
default_bypass = defaultdict(int)
active_mimics = []
held_keys = []

def ensureENVfile():
    if not os.path.exists('.env'): 
        with open('.env', 'x') as file: 
            pass


def init():
    global data, settings, flags
    ensureENVfile()
    dotenv.load_dotenv()
    ## Data

    # Semi-Static
    data['subprocessManager'] = mp.Manager()
    data['mainQueue'] = data['subprocessManager'].Queue()
    data['maxSubprocesses'] = 5
    data['subprocessPool'] = mp.Pool(processes=data['maxSubprocesses'])
    data['atomicSubprocesses'] = set()

    # Dynamic
    data['keyboardMode'] = 'Default' # This can have the value 'Default', 'ShiftMode', 'CapMode', or 'CtrlMode'. Starts as 'Default'
    data['subprocessTimestamp'] = 0
    data['remoteServerClipboard'] = ""
    data['mostRecentNotepadID'] = None
    data['notepadQueues'] = [None for i in range(10)]

    

    ## Settings
    settings = sett.loadSettings()
    
    ## Flags
    flags['asyncCtrlModePayloadStatus'] = "Recieved" # Can be 'Requested', 'Recieved', "In Use", or "Failed"

