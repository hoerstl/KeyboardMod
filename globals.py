import multiprocessing as mp
import dotenv
import os
from collections import defaultdict
import settings as sett

data = {}
settings = {}
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
    global data, settings
    ensureENVfile()
    dotenv.load_dotenv()
    # Data
    data['keyboardMode'] = 'Default' # This can have the value 'Default', 'ShiftMode', 'CapMode', or 'CtrlMode'. Starts as 'Default'
    data['atomicSubprocesses'] = set()
    data['subprocessTimestamp'] = 0
    data['subprocessManager'] = mp.Manager()
    data['maxSubprocesses'] = 5
    data['subprocessPool'] = mp.Pool(processes=data['maxSubprocesses'])
    data['mainQueue'] = data['subprocessManager'].Queue()
    data['mostRecentNotepadID'] = None
    data['notepadQueues'] = [None for i in range(10)]

    # Settings
    settings = sett.loadSettings()
