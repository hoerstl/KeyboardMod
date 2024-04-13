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
    last_key_released = event.Key


def process_mode_cap(event):
    global keyboard_mode, cap_press_time, cap_mode_used
    if event.Key == 'Capital':
        if event.MessageName == 'key down' and keyboard_mode != 'CapMode':
            cap_mode_used.value = False
            if keyboard_mode == 'ShiftLock':  # We should count disabling the shiftlock as a valid use case of cap mode.
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
        return False

    return True


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
    global keyboard_mode
    update()
    if is_press_bypassed(event):
        return True
    if not process_mode_cap(event):
        return False

    # Process keyboard input as you wish
    if keyboard_mode == 'Default':
        return True
    elif keyboard_mode == 'ShiftLock':
        onPress_ShiftLock(event)
    elif keyboard_mode == 'CapMode':
        onPress_CapMode(event)

    return False


def on_key_release(event):
    global keyboard_mode
    if is_release_bypassed(event):
        return True

    if process_mode_shift(event):
        return True  # We need to allow the shift keys to be released when we swap to and from modes
    if not process_mode_cap(event):
        return False
    # Default keyboard input
    if keyboard_mode == 'Default':
        return True
    elif keyboard_mode == 'ShiftLock':
        return False
    elif keyboard_mode == 'CapMode':
        onRelease_CapMode(event)
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
    keyboard_mode = 'Default'  # This can have the value 'Default', 'ShiftLock', or 'CapMode'. Starts as 'Default'
    globals.init()
    cap_press_time = 0
    shift_release_time = 0
    last_key_released = ''
    start_hook()


