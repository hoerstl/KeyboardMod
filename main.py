import pythoncom
import pyWinhook
from secondaryActions import performSecondaryAction

in_secondary_keyboard_mode = False
last_key_released = ''


def is_shift_key(key_name):
    shift_names = [
        "shift",
        "Lshift",
        "Rshift"
    ]
    return key_name in shift_names


def on_key_press(event):
    global in_secondary_keyboard_mode
    if not in_secondary_keyboard_mode:
        return True

    # Process keyboard input as you wish
    performSecondaryAction(event)

    return False


def on_key_release(event):
    global in_secondary_keyboard_mode, last_key_released
    # print(event.Key)
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
    # Return True to pass the event to other applications
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
    print(dir(pyWinhook.HookManager))
    start_hook()


