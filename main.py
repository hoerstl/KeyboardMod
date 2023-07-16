import pythoncom
import pyWinhook
from secondaryActions import performSecondaryAction_mousetype, performSecondaryAction_keytype, is_press_bypassed, is_release_bypassed

in_secondary_keyboard_mode = False
last_key_released = ''


def is_shift_key(key_name):
    shift_names = [
        "shift",
        "Lshift",
        "Rshift"
    ]
    return key_name in shift_names


def process_mode_shift(event):
    global in_secondary_keyboard_mode, last_key_released
    if is_shift_key(event.Key):
        if is_shift_key(last_key_released):
            if in_secondary_keyboard_mode:
                print("Returning to normal keyboard function")
            else:
                print("Switching to Secondary mode")
            in_secondary_keyboard_mode = not in_secondary_keyboard_mode
            last_key_released = ''
            return True
    last_key_released = event.Key

def on_key_press(event):
    global in_secondary_keyboard_mode
    if not in_secondary_keyboard_mode:
        return True

    # Process keyboard input as you wish
    if is_press_bypassed(event):
        return True
    performSecondaryAction_keytype(event)

    return False


def on_key_release(event):
    global in_secondary_keyboard_mode
    if process_mode_shift(event):
        return True  # We need to allow the shift keys to be released when we swap to and from modes

    # Default keyboard input
    if not in_secondary_keyboard_mode:
        return True

    # Process keyboard releases as you wish
    if is_release_bypassed(event):
        return True
    return False


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
    start_hook()


