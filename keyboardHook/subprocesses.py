import multiprocessing as mp
import globals
from functools import wraps
import sys
import traceback
import time



def threadedSubprocess(atomic=False, createSubprocessQueue=None):
    """
    NOTE: All functions with this decorator must define **kwargs as function arguments
    
    This decorator does nothing to change the original function, instead creating a new function named
    'async{OriginalFunctionName}' which spawns a new subprocess running the function passed.
    Note, the first letter of the original function name will be capitalized to enforce proper camelCase.

    This functionality is necessary because to spawn a function as a subprocess, it needs to be pickleable 
    but functions defined with decorators are not pickleable so the decorator cannot change the function if 
    it wants to spawn a subprocess with it.

    Params:
    createSubprocessQueue func() => mp.Queue: This function is used to create a new queue and may be 
    implemented in order to add the same queue to globals.data with a dynamically created name.
    
    atomic bool: Allows only a single subprocess of this function to be run at a time
    """
    def threadedSubprocessWithParameters(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal func
            if atomic and func.__name__ in globals.data['atomicSubprocesses']:
                print(f"Subprocess {func.__name__} already running.")
                return
            elif atomic:
                globals.data['atomicSubprocesses'].add(func.__name__)

            ms = 100
            currentTimestamp = round((time.time() * 1000)/ms) * ms / 1000
            if globals.data['subprocessTimestamp'] != currentTimestamp:
                globals.data['subprocessTimestamp'] = currentTimestamp
                if mp.current_process().name != "MainProcess":
                    print("Don't call an asynchronous function from a subprocess")
                subprocessQueue = globals.data['subprocessManager'].Queue()
                subprocessId = globals.data["unusedSubprocessId"]
                globals.data["unusedSubprocessId"] += 1
                globals.data["subprocessQueues"][subprocessId] = subprocessQueue
                kwargs.update({'mainQueue': globals.data['mainQueue'], 'processQueue': subprocessQueue, 'processId': subprocessId})
                def error_callback(e):
                    print("There was an error in a subprocess:")
                    traceback.print_exception(type(e), e, e.__traceback__)
                globals.data['subprocessPool'].apply_async(func, args, kwargs, callback=lambda _: globals.data["subprocessQueues"].pop(subprocessId), error_callback=error_callback)
            else:
                pass

        # Name of the wrapped and decorated function
        decorated_name = "async" + func.__name__[0].upper() + func.__name__[1:]
        wrapper.__name__ = decorated_name
        module = sys.modules[func.__module__]
        setattr(module, decorated_name, wrapper)
        return func
    return threadedSubprocessWithParameters









