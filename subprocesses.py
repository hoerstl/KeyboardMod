import multiprocessing as mp
import globals
from functools import wraps
import sys



def threadedSubProcess(func):
    """
    NOTE: All functions with this decorator must define **kwargs as function arguments
    
    This decorator does nothing to change the original function, instead creating a new function named
    'async{OriginalFunctionName}' which spawns a new subprocess running the function passed.
    Note, the first letter of the original function name will be capitalized to enforce proper camelCase.

    This functionality is necessary because to spawn a function as a subprocess, it needs to be pickleable 
    but functions defined with decorators are not pickleable so the decorator cannot change the function if 
    it wants to spawn a subprocess with it.
    """
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal func
        if mp.current_process().name != "MainProcess":
            print("Don't call an asynchronous function from a subprocess")
        kwargs.update({'queue': globals.data['subProcessQueue']})
        subprocess = mp.Process(target=func, args=args, kwargs=kwargs)
        subprocess.start()
        globals.data['allSubProcesses'].append(subprocess)
        return subprocess

    # Name of the wrapped and decorated function
    decorated_name = "async" + func.__name__[0].upper() + func.__name__[1:]
    wrapper.__name__ = decorated_name
    module = sys.modules[func.__module__]
    setattr(module, decorated_name, wrapper)
    return func










