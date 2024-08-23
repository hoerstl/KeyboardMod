import pythoncom
import pyWinhook
import time
from secondaryActions import *


def is_shift_key(key_name):
    shift_names = [
        "shift",
        "Lshift",
        "Rshift"
    ]
    return key_name in shift_names


def process_mode_shift(event):
    """
    Decides whether or not to switch the keyboard into ShiftLock
    Runs every key release.
    """
    global keyboard_mode, last_key_released, shift_release_time
    if is_shift_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - shift_release_time < .05
        if is_shift_key(last_key_released) and is_different and was_quick_enough:
            if keyboard_mode == 'ShiftLock':
                print("ShiftLock Off")
                keyboard_mode = 'Default'
            else:
                print("ShiftLock On")
                keyboard_mode = 'ShiftLock'

            last_key_released = ''
            return True
        shift_release_time = time.time()


def process_mode_cap(event):
    """
    Decides whether or not to switch the keyboard into CapMode
    Runs every key release.
    """
    global keyboard_mode, cap_press_time, cap_mode_used
    if event.Key == 'Capital':
        if event.MessageName == 'key down' and keyboard_mode != 'CapMode':
            cap_mode_used.value = False
            if keyboard_mode != 'Default':  # We should count disabling another keyboard mode as a valid use case of cap mode.
                cap_mode_used.value = True
            keyboard_mode = 'CapMode'
            # TODO: Fix a bug where someone holds down shift (or another non-letter key) and the release is blocked by capmode
            print('Entering Cap Mode')
            cap_press_time = time.time()
        elif event.MessageName == 'key up' or event.MessageName == 'key sys up':
            cleanupHeldKeys()
            keyboard_mode = 'Default'
            print('Leaving Cap Mode')
            if time.time() - cap_press_time < .3 and not cap_mode_used.value:
                pressKey("Capital")
        return True

    return False



def is_ctrl_key(key_name):
    ctrl_names = [
        "control",
        "Lcontrol",
        "Rcontrol",
    ]
    return key_name in ctrl_names

def process_mode_ctrl(event):
    """
    Decides whether or not to switch the keyboard into CtrlMode
    Runs every key release.
    """
    global keyboard_mode, last_key_released, ctrl_release_time
    if is_ctrl_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - ctrl_release_time < .05
        if is_ctrl_key(last_key_released) and is_different and was_quick_enough:
            'passed all criteria'
            if keyboard_mode == 'CtrlMode':
                print("CtrlMode Off")
                keyboard_mode = 'Default'
            else:
                print("CtrlMode On")
                keyboard_mode = 'CtrlMode'

            last_key_released = ''
            return True
        ctrl_release_time = time.time()


def update():
    """
    Performs logic as frequently as possible (every frame ideally but really every time a button is pressed)
    to make it available to the user
    """
    # Update all information given from subprocesses
    while not globals.data['subProcessQueue'].empty():
        key, value = globals.data['subProcessQueue'].get()
        globals.data.update({key: value})






def on_key_press(event):
    """
    This function is a callback function which is called every time a key is pressed on the system.
    
    Return:
    bool | If the response is True, then the keystroke is passed onto windows. If false, then the 
    default keystroke behavior is blocked
    """
    global keyboard_mode
    update()
    if is_press_bypassed(event):
        return True
    if process_mode_cap(event):
        return False

    # Process keyboard input as you wish
    if keyboard_mode == 'Default':
        return True
    elif keyboard_mode == 'ShiftLock':
        onPress_ShiftLock(event)
    elif keyboard_mode == 'CapMode':
        onPress_CapMode(event)
    elif keyboard_mode == 'CtrlMode':
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
    global keyboard_mode, last_key_released
    if is_release_bypassed(event):
        return True

    # Read these if statements as "if the key falls under entering _____ mode's juristiction. Ex. shift keys fall under shiftmode etc."
    if process_mode_shift(event):
        return True  # We need to allow the shift keys to be released when we swap to and from modes since it involves two keys
    if process_mode_cap(event):
        return False # We can just block both the press and release of a single key since interacting with it at all means that we are certainly changing keyboard modes
    if process_mode_ctrl(event):
        return True # We need to allow the ctrl keys to be released when we swap to and from modes since it involves two keys
    last_key_released = event.Key

    # Default keyboard input
    if keyboard_mode == 'Default':
        return True
    elif keyboard_mode == 'ShiftLock':
        return False
    elif keyboard_mode == 'CapMode':
        onRelease_CapMode(event)
        return False
    elif keyboard_mode == 'CtrlMode':
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
    keyboard_mode = 'Default'  # This can have the value 'Default', 'ShiftLock', 'CapMode', or 'CtrlMode'. Starts as 'Default'
    globals.init() # Perform first time initialization of global data and environment variables
    cap_press_time = 0
    shift_release_time = 0
    ctrl_release_time = 0
    last_key_released = ''
    start_hook()


