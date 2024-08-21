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
    data['subProcessQueue'] = mp.Queue()

