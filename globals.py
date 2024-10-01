import multiprocessing as mp
import dotenv
import os
from collections import defaultdict

data = {}
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
    ensureENVfile()
    dotenv.load_dotenv()
    data['keyboardMode'] = 'Default' # This can have the value 'Default', 'ShiftMode', 'CapMode', or 'CtrlMode'. Starts as 'Default'
    data['remoteServerIP'] = '127.0.0.1'
    data['atomicSubprocesses'] = set()
    data['timesToClick'] = 1
    data['subprocessTimestamp'] = 0
    data['subprocessManager'] = mp.Manager()
    data['maxSubprocesses'] = 5
    data['subprocessPool'] = mp.Pool(processes=data['maxSubprocesses'])
    data['mainQueue'] = data['subprocessManager'].Queue()
    data['mostRecentNotepadID'] = None
    data['notepadQueues'] = [None for i in range(10)]
