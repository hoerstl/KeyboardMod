import multiprocessing as mp
import dotenv
import os
data = {}

def ensureENVfile():
    if not os.path.exists('.env'): 
        with open('.env', 'x') as file: 
            pass


def init():
    ensureENVfile()
    dotenv.load_dotenv()
    data['remoteClipboardIP'] = '0.0.0.0'
    data['allSubProcesses'] = []
    data['mainQueue'] = mp.Queue()
    data['mostRecentNotepadID'] = None
    data['notepadQueues'] = [None for i in range(10)]
