import win32api
import win32con

from keyMap import key_map, combo_key_map, common_character_map


mainQueue = None
processQueue = None
processId = None
def __init__(_mainQueue, _processQueue, _processId):
    global mainQueue, processQueue, processId
    mainQueue = _mainQueue
    processQueue = _processQueue
    processId = _processId


def _sendCommandAndWait(command, *args):
    """
    Sends a command to the main thread to be processed in the main thread's update function.

    command str: the name of the command to be run by the main thread. Acceptable commands are limited and predefined in main's update function.
    *args list: 0 or more positional arguments to be used in completing the command.
    """
    global mainQueue, processQueue, processId

    mainQueue.put(("__action__", (processId, command, *args)))
    confirmationOfCompletion = processQueue.get()
    return confirmationOfCompletion


def _globalGet(getRequest):
    """
    Requests a piece of global data from the main server

    getRequest str(): The attribute you'd like to request from globals. Acceptable values are limited and predefined in main's update function.
    """
    global mainQueue, processQueue, processId

    mainQueue.put(("__globalGet__", (processId, getRequest)))
    requestedData = processQueue.get()
    return requestedData



########################### Convenience functions for common keyboard manipulation ##########################################
def cleanUpHeldKeys():
    global key_map
    for key_name in _globalGet("held_keys"):
        key = key_map.get(key_name)
        if not key:
            raise ValueError(f"Somehow '{key_name}' was added to the held keys yet we have no mapping for it in keyMap.py")
        _sendCommandAndWait(("keyReleaseBypass", key_name))
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
    _sendCommandAndWait("cleanUpHeldKeys")


def holdKey(key_name):
    global key_map
    key = key_map.get(key_name)
    if key:
        _sendCommandAndWait("keyPressBypass", key_name)
        win32api.keybd_event(key, 0, 0, 0)
        _sendCommandAndWait("markKeyAsHeld", key_name)
        return

    raise ValueError(f"Keybinding for '{key_name}' not given in keyMap.py")


def releaseKey(key_name):
    global key_map
    key = key_map.get(key_name)
    if key:
        _sendCommandAndWait("keyReleaseBypass", key_name)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        _sendCommandAndWait("markKeyAsReleased", key_name)
        return

    raise ValueError(f"Keybinding for '{key_name}' not given in keyMap.py")


def pressAndReleaseKey(key_name):
    global key_map
    key = key_map.get(key_name)
    if key:
        # Key presses are activated via their ascii code while in this system but are converted to a human-readable names in pythoncom when we process them as input.
        # Therefore, to press and release a key, we must bypass a key's NAME and press its ASCII code. 
        _sendCommandAndWait("keyPressBypass", key_name)
        win32api.keybd_event(key, 0, 0, 0)
        _sendCommandAndWait("keyReleaseBypass", key_name)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        return

    raise ValueError(f"Keybinding for '{key_name}' not given in keyMap.py")


def pressAndReleaseKeys(keys):
    """
    Takes in a string of keys separated by underscores. Presses and releases each of them in order.
    :param keys:
    :return:
    """
    keyList = keys.split('_')
    for key in keyList:
        pressAndReleaseKey(key)


def pressKeyCombo(keycombo):
    """
    Presses more complex keyboard input. Splits the keycombo on the +'s and then presses them down in order before
    releasing them in reverse order.
    :param keycombo: str. E.X. Ctrl+Left runs press Ctrl -> Left -> release Ctrl -> release Left
    :return: None
    """
    global key_map
    key_names = keycombo.split("+")
    keys = [key_map.get(key) for key in key_names]
    if None in keys:
        raise ValueError(f"Keybinding for key '{key_names[keys.index(None)]}' not specified in keyMap.py")

    for key, key_name in zip(keys, key_names):
        _sendCommandAndWait("keyPressBypass", key_name)
        win32api.keybd_event(key, 0, 0, 0)
    key_names.reverse()
    keys.reverse()
    for key, key_name in zip(keys, key_names):
        _sendCommandAndWait("keyReleaseBypass", key_name)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def typeCharacter(character):
    global key_map, combo_key_map, common_character_map
    # If the character is one pressed with a key combination like capital 'A', do so.
    keycombo = combo_key_map.get(character)
    if keycombo:
        pressKeyCombo(keycombo)
        return

    # Otherwise, convert the character to the pywincom name and type it
    character = common_character_map.get(character, character)
    if key_map.get(character):
        pressAndReleaseKey(character)
        return
    
    raise ValueError(f"Found no way to type the character '{character}' ord:'{ord(character)}'.")


