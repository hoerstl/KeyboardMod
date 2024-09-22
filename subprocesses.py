import multiprocessing as mp
import globals
from functools import wraps
import sys
import time



def threadedSubprocess(createSubprocessQueue=None):
    """
    NOTE: All functions with this decorator must define **kwargs as function arguments
    
    This decorator does nothing to change the original function, instead creating a new function named
    'async{OriginalFunctionName}' which spawns a new subprocess running the function passed.
    Note, the first letter of the original function name will be capitalized to enforce proper camelCase.

    This functionality is necessary because to spawn a function as a subprocess, it needs to be pickleable 
    but functions defined with decorators are not pickleable so the decorator cannot change the function if 
    it wants to spawn a subprocess with it.

    createSubprocessQueue func() => mp.Queue: This function is used to create a new queue and may be 
    implemented in order to add the same queue to globals.data with a dynamically created name.
    """
    def threadedSubprocessWithParameters(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal func
            ms = 100
            timestamp = round((time.time() * 1000)/ms) * ms / 1000
            spCountOutdated = globals.data['subprocessTimestamp'] != timestamp
            if spCountOutdated:
                globals.data['subprocessTimestamp'] = timestamp
                if mp.current_process().name != "MainProcess":
                    print("Don't call an asynchronous function from a subprocess")
                subProcessQueue = createSubprocessQueue and createSubprocessQueue()
                kwargs.update({'mainQueue': globals.data['mainQueue'], 'subprocessQueue': subProcessQueue})
                globals.data['subprocessPool'].apply_async(func, args, kwargs, error_callback=lambda e:print(f'There was an error in a subprocess: {e}'))
            else:
                pass

        # Name of the wrapped and decorated function
        decorated_name = "async" + func.__name__[0].upper() + func.__name__[1:]
        wrapper.__name__ = decorated_name
        module = sys.modules[func.__module__]
        setattr(module, decorated_name, wrapper)
        return func
    return threadedSubprocessWithParameters









