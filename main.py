import pythoncom
import pyWinhook
import time
from keyboardModes import *
import convenienceFunctions as kbd

# TODO: When two keys are released at the same time, only one of those key releases triggers the keyboard hook. This means that we sometimes
# don't get signals when we release keys. This might be the case for pressing keys too. This issue requires further research.

def process_mode_shift(event):
    """
    Decides whether or not to switch the keyboard into ShiftMode
    Runs every key release.
    """
    global last_key_released, shift_release_time
    if is_shift_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - shift_release_time < .05
        if is_shift_key(last_key_released) and is_different and was_quick_enough:
            if globals.data['keyboardMode'] == 'ShiftMode':
                print("ShiftMode Off")
                globals.data['keyboardMode'] = 'Default'
            else:
                print("ShiftMode On")
                globals.data['keyboardMode'] = 'ShiftMode'

            last_key_released = ''
            return True
        shift_release_time = time.time()


def process_mode_cap(event):
    """
    Decides whether or not to switch the keyboard into CapMode
    Runs every key release.
    """
    global cap_press_time
    if event.Key == 'Capital':
        if event.MessageName == 'key down' and globals.data['keyboardMode'] != 'CapMode':
            globals.data['cap_mode_used'] = False
            if globals.data['keyboardMode'] != 'Default':  # We should count disabling another keyboard mode as a valid use case of cap mode.
                globals.data['cap_mode_used'] = True
            globals.data['keyboardMode'] = 'CapMode'
            print('Entering Cap Mode')
            cap_press_time = time.time()
        elif event.MessageName == 'key up' or event.MessageName == 'key sys up':
            kbd.cleanupHeldKeys()
            globals.data['keyboardMode'] = 'Default'
            print('Leaving Cap Mode')
            if time.time() - cap_press_time < .3 and not globals.data.get('cap_mode_used'):
                kbd.pressAndReleaseKey("Capital")
        return True

    return False


def process_mode_ctrl(event):
    """
    Decides whether or not to switch the keyboard into CtrlMode
    Runs every key release.
    """
    global last_key_released, ctrl_release_time
    if is_ctrl_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - ctrl_release_time < .05
        if is_ctrl_key(last_key_released) and is_different and was_quick_enough:
            'passed all criteria'
            if globals.data['keyboardMode'] == 'CtrlMode':
                print("CtrlMode Off")
                globals.data['keyboardMode'] = 'Default'
            else:
                print("CtrlMode On")
                globals.data['entering_ctrl_mode'] = True
                globals.data['keyboardMode'] = 'CtrlMode'

            last_key_released = ''
            return True
        ctrl_release_time = time.time()


def update():
    """
    Performs logic as frequently as possible (every frame ideally but really every time a button is pressed)
    to make it available to the user
    """
    # Update all information given from subprocesses and put them into the globally accessable data dict from globals.py
    while not globals.data['mainQueue'].empty():
        key, payload = globals.data['mainQueue'].get()
        if key == "command":
            command, value = payload
            if command == "terminateAtomicSubprocess":
                globals.data['atomicSubprocesses'].remove(value)
                
            elif command == "closeNotepad":
                globals.data['mostRecentNotepadID'] = None
                globals.data['notepadQueues'][value] = None
        else:
            globals.data.update({key: payload})


def is_press_bypassed(event):
    if globals.keypress_bypass[event.Key] > 0:
        globals.keypress_bypass[event.Key] -= 1
        return True
    return False


def is_release_bypassed(event):
    if globals.keyrelease_bypass[event.Key] > 0:
        globals.keyrelease_bypass[event.Key] -= 1
        return True
    return False


def is_default_bypassed(event):
    """
    This function is used to bypass keys pressed during the default keyboard mode so they can be released in other modes.
    Unlike release_bypass, these key releases can still trigger logic meant to switch between modes.
    """
    if globals.default_bypass[event.Key] > 0:
        globals.default_bypass[event.Key] -= 1
        return True
    return False


def on_key_press(event):
    """
    This function is a callback function which is called every time a key is pressed on the system.
    
    Return:
        bool | If the response is True, then the keystroke is passed onto windows. If false, then the 
        default keystroke behavior is blocked
    """
    update()
    if is_press_bypassed(event):
        return True
    if process_mode_cap(event):
        return False

    # Process keyboard input as you wish
    if globals.data['keyboardMode'] == 'Default':
        globals.default_bypass[event.Key] = 1
        return True
    elif globals.data['keyboardMode'] == 'ShiftMode':
        onPress_ShiftMode(event)
    elif globals.data['keyboardMode'] == 'CapMode':
        onPress_CapMode(event)
    elif globals.data['keyboardMode'] == 'CtrlMode':
        onPress_CtrlMode(event)

    return False


def on_key_release(event):
    """
    This function contains logic for swapping between modes as well as for describing the behavior 
    of blocking key releases.

    Return:
        bool | If the response is True, then the keystroke is passed onto windows. If false, then the 
        default key release behavior is blocked
    """
    global last_key_released
    if is_release_bypassed(event):
        return True

    # Read these if statements as "if the key falls under entering _____ mode's juristiction. Ex. shift keys fall under shiftmode etc."
    if process_mode_shift(event):
        pass  # We need to allow the shift keys to be released via a default bypass when we swap to and from modes since it involves two keys
    if process_mode_cap(event):
        return False # We can just block both the press and release of a single key since interacting with it at all means that we are certainly changing keyboard modes
    if process_mode_ctrl(event):
        pass # We need to allow the ctrl keys to be released via a default bypass when we swap to and from modes since it involves two keys
    last_key_released = event.Key

    if is_default_bypassed(event):
        return True

    # Default keyboard input
    if globals.data['keyboardMode'] == 'Default':
        return True
    elif globals.data['keyboardMode'] == 'ShiftMode':
        return False
    elif globals.data['keyboardMode'] == 'CapMode':
        onRelease_CapMode(event)
        return False
    elif globals.data['keyboardMode'] == 'CtrlMode':
        return False
    return True




def start_hook():
    # Create an instance of the hook manager
    hook_manager = pyWinhook.HookManager()

    # Register the callback function for keyboard events
    hook_manager.KeyDown = on_key_press
    hook_manager.KeyUp = on_key_release

    # Set the hook and start the event loop
    hook_manager.HookKeyboard()
    pythoncom.PumpMessages()


if __name__ == '__main__':
    globals.init() # Perform first time initialization of global data and environment variables
    cap_press_time = 0
    shift_release_time = 0
    ctrl_release_time = 0
    last_key_released = ''
    start_hook()


