import multiprocessing as mp
data = {}

def init():
    data['remoteClipboardIP'] = '0.0.0.0'
    data['allSubProcesses'] = []
    data['subProcessQueue'] = mp.Queue()

