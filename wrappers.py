import multiprocessing as mp
from functools import wraps
import sys


if mp.current_process().name == "MainProcess":
    allSubProcesses = []

def threadedSubProcess(func):
    # This decorator does nothing to change the original function but creates a new function named
    # 'async{OriginalFunctionName}' which spawns a new subprocess running the function passed
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal func
        subprocess = mp.Process(target=func, args=args, kwargs=kwargs)
        subprocess.start()
        if mp.current_process().name != "MainProcess":
            print("Don't call an asynchronous function from a subprocess")
        allSubProcesses.append(subprocess)
        return subprocess

    # Name of the wrapped and decorated function
    decorated_name = "async" + func.__name__[0].upper() + func.__name__[1:]
    wrapper.__name__ = decorated_name
    module = sys.modules[func.__module__]
    setattr(module, decorated_name, wrapper)
    return func










