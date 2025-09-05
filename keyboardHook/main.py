import pythoncom
import pyWinhook
import time
import keyboardModes
import specialFunctions
import convenienceFunctions as kbd
import settings
import globals
import pyperclip
import threading

# TODO: When two keys are released at the same time, only one of those key releases triggers the keyboard hook. This means that we sometimes
# don't get signals when we release keys. This might be the case for pressing keys too. This issue requires further research.


def updateFromMainQueue():
    """
    This function runs threaded and is blocked, listening for values sent to mainQueue.
    
    Responsible for updating any global keyboard information at the request of any subprocess with access to the mainQueue object, running user-defined 
    functions in response to arbitrary commands passed through.
    """
    global updateHooks # TODO: implement updateHooks and abstract functionality of user defined functions.
    # Rework the way we interact with setting custom globals/settings here. If statements won't scale well.

    while True:
        item = globals.data['mainQueue'].get()
        
        action, data = item
        
        if action == "__action__":
            subprocessId, *values = data
            action, *parameters = values
            if action == "keyPressBypass":
                globals.keypress_bypass[parameters[0]] += 1
            elif action == "keyReleaseBypass":
                globals.keyrelease_bypass[parameters[0]] += 1
            elif action == "markKeyAsHeld":
                globals.held_keys.append(parameters[0])
            elif action == "markKeyAsReleased":
                globals.held_keys.remove(parameters[0])
            elif action == "cleanUpHeldKeys":
                globals.held_keys = []
                globals.active_mimics = []
            else:
                raise ValueError(f"Invalid internal action requested: \"{action}\"")

            globals.data["subprocessQueues"][subprocessId].put("Internal Action Complete")

        if action == "__globalGet__":
            subprocessId, requestedData = data
            data = f"No data spec found for '{requestedData}'"
            if requestedData == "held_keys":
                data = globals.held_keys


            globals.data["subprocessQueues"][subprocessId].put(data)


        settingsChanged = False
        if action == "command":
            command, data = data
            if command == "terminateAtomicSubprocess":
                globals.data['atomicSubprocesses'].remove(data)
                
            elif command == "closeNotepad":
                globals.data['mostRecentNotepadID'] = None
                globals.data['notepadQueues'][data] = None

            elif command == "notify":
                specialFunctions.asyncNotify()

            elif command == "remoteClipboardReadFailed":
                if globals.flags['asyncCtrlModePayloadStatus'] == "Requested":
                    globals.flags['asyncCtrlModePayloadStatus'] = "Failed"

            elif command == "print":
                print(f"Value recieved! {data}")

        else:
            if action in globals.settings and globals.settings[action] != data:
                settingsChanged = True
                globals.settings.update({action: data})
            elif action in globals.data:
                if action == "remoteServerClipboard":
                    globals.data["remoteServerClipboard"] = data
                    if globals.flags['asyncCtrlModePayloadStatus'] == "Requested":
                        globals.flags['asyncCtrlModePayloadStatus'] = "Recieved"
                    else:
                        pyperclip.copy(globals.data["remoteServerClipboard"])


        if settingsChanged: settings.saveSettings(globals.settings)


def process_mode_shift(event):
    """
    Decides whether or not to switch the keyboard into Shift Mode
    Runs every key release.
    """
    global last_key_released, shift_release_time
    if keyboardModes.is_shift_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - shift_release_time < .05
        if keyboardModes.is_shift_key(last_key_released) and is_different and was_quick_enough:
            if globals.data['keyboardMode'] == 'Shift':
                print("Shift Mode Off")
                globals.data['keyboardMode'] = 'Default'
            else:
                print("Shift Mode On")
                globals.data['keyboardMode'] = 'Shift'

            last_key_released = ''
            return True
        shift_release_time = time.time()


def process_mode_cap(event):
    """
    Decides whether or not to switch the keyboard into Caps Lock Mode
    Runs every key release.
    """
    global cap_press_time
    if event.Key == 'Capital':
        if event.MessageName == 'key down' and globals.data['keyboardMode'] != 'Caps Lock':
            globals.data['cap_mode_used'] = False
            if globals.data['keyboardMode'] != 'Default':  # We should count disabling another keyboard mode as a valid use case of cap mode.
                globals.data['cap_mode_used'] = True
            globals.data['keyboardMode'] = 'Caps Lock'
            print('Entering Caps Lock Mode')
            cap_press_time = time.time()
        elif event.MessageName == 'key up' or event.MessageName == 'key sys up':
            kbd.cleanupHeldKeys()
            globals.data['keyboardMode'] = 'Default'
            print('Leaving Caps Lock Mode')
            if time.time() - cap_press_time < .3 and not globals.data.get('cap_mode_used'):
                kbd.pressAndReleaseKey("Capital")
        return True

    return False


def process_mode_ctrl(event):
    """
    Decides whether or not to switch the keyboard into Ctrl Mode
    Runs every key release.
    """
    global last_key_released, ctrl_release_time
    if keyboardModes.is_ctrl_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - ctrl_release_time < .05
        if keyboardModes.is_ctrl_key(last_key_released) and is_different and was_quick_enough:
            'passed all criteria'
            if globals.data['keyboardMode'] == 'Ctrl':
                print("Ctrl Mode Off")
                globals.data['keyboardMode'] = 'Default'
            else:
                print("Ctrl Mode On")
                globals.data['entering_ctrl_mode'] = True
                globals.data['keyboardMode'] = 'Ctrl'

            last_key_released = ''
            return True
        ctrl_release_time = time.time()
        

def process_mode_alt(event):
    """
    Decides whether or not to switch the keyboard into Alt Mode
    Runs every key release.
    """
    global last_key_released, alt_release_time
    if keyboardModes.is_alt_key(event.Key):
        is_different = event.Key != last_key_released
        was_quick_enough = time.time() - alt_release_time < .05
        if keyboardModes.is_alt_key(last_key_released) and is_different and was_quick_enough:
            'passed all criteria'
            if globals.data['keyboardMode'] == 'Alt':
                print("Alt Mode Off")
                globals.data['keyboardMode'] = 'Default'
            else:
                print("Alt Mode On")
                globals.data['entering_alt_mode'] = True
                globals.data['keyboardMode'] = 'Alt'

            last_key_released = ''
            return True
        alt_release_time = time.time()


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
    if is_press_bypassed(event):
        return True
    if process_mode_cap(event):
        return False

    # Process keyboard input as you wish
    if globals.data['keyboardMode'] == 'Default':
        return keyboardModes.onPress_Default(event)
    elif globals.data['keyboardMode'] == 'Shift':
        keyboardModes.onPress_ShiftMode(event)
    elif globals.data['keyboardMode'] == 'Caps Lock':
        keyboardModes.onPress_CapMode(event)
    elif globals.data['keyboardMode'] == 'Ctrl':
        keyboardModes.onPress_CtrlMode(event)
    elif globals.data['keyboardMode'] == 'Alt':
        keyboardModes.onPress_AltMode(event)

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

    # Read these if statements as "if the key falls under entering _____ mode's juristiction. Ex. shift keys fall under shift mode etc."
    if process_mode_shift(event):
        pass  # We need to allow the shift keys to be released via a default bypass when we swap to and from modes since it involves two keys
    if process_mode_cap(event):
        return False # We can just block both the press and release of a single key since interacting with it at all means that we are certainly changing keyboard modes
    if process_mode_ctrl(event):
        pass # We need to allow the ctrl keys to be released via a default bypass when we swap to and from modes since it involves two keys
    if process_mode_alt(event):
        pass # We need to allow the alt keys to be released via a default bypass when we swap to and from modes since it involves two keys
    last_key_released = event.Key

    if is_default_bypassed(event):
        return True

    # Default keyboard input
    if globals.data['keyboardMode'] == 'Default':
        return True
    elif globals.data['keyboardMode'] == 'Shift':
        return False
    elif globals.data['keyboardMode'] == 'Caps Lock':
        keyboardModes.onRelease_CapMode(event)
        return False
    elif globals.data['keyboardMode'] == 'Ctrl':
        return False
    elif globals.data['keyboardMode'] == 'Alt':
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
    specialFunctions.init()
    cap_press_time = 0
    shift_release_time = 0
    ctrl_release_time = 0
    alt_release_time = 0
    last_key_released = ''

    threading.Thread(target=updateFromMainQueue, daemon=True).start()

    start_hook()


