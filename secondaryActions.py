import ctypes
import win32api
import win32con
import pyperclip
import globals
from myQueue import Queue, Node
from keyMap import key_map, combo_key_map, common_character_map
import specialFunctions
specialFunctions.init()

keypress_bypass = Queue()
keyrelease_bypass = Queue()
active_mimics = []
held_keys = []
cap_mode_used = Node(False)
entering_ctrl_mode = Node(False)





########################## Currently inactive code for moving the mouse with the keyboard ##########################################
# class POINT(ctypes.Structure):
#     _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]



# class Point:

#     def __init__(self, x=0, y=0):
#         self.x = round(x)
#         self.y = round(y)

#     def set(self, x, y):
#         self.x = round(x)
#         self.y = round(y)



# screen_width = ctypes.windll.user32.GetSystemMetrics(0)
# screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# major_tile_pos = Point()


# def performSecondaryAction_mousetype(event):
#     global screen_width, screen_height, major_tile_pos

#     left_hand = [*"QWERTASDFGZXCVB"]
#     major_cols = 5
#     major_rows = 3
#     if len(left_hand) / major_cols != major_rows:
#         raise Exception('The left hand grid is not defined as a proper rectangle.')
#     major_column_width = screen_width // major_cols
#     major_row_height = screen_height // major_rows
#     if event.Key in left_hand:
#         major_grid_index = left_hand.index(event.Key)
#         row_index = major_grid_index // major_cols
#         column_index = major_grid_index % major_cols

#         major_tile_pos.set(column_index * major_column_width, row_index * major_row_height)

#         ctypes.windll.user32.SetCursorPos(major_tile_pos.x, major_tile_pos.y)

#     right_hand = [*'YUIOPHJKL', 'Oem_1', *'NM', 'Oem_Comma', 'Oem_Period', 'Oem_2']
#     minor_cols = 5
#     minor_rows = 3
#     if len(right_hand) / minor_cols != minor_rows:
#         raise Exception('The right hand grid is not defined as a proper rectangle.')
#     minor_column_width = major_column_width // minor_cols
#     minor_row_height = major_row_height // minor_rows
#     if event.Key in right_hand:
#         minor_grid_index = right_hand.index(event.Key)
#         row_index = minor_grid_index // minor_cols
#         column_index = minor_grid_index % minor_cols  # May need to stretch out these columns to fit all the way to the right

#         ctypes.windll.user32.SetCursorPos(major_tile_pos.x + (column_index * minor_column_width), major_tile_pos.y + (row_index * minor_row_height))


#     if event.Key == "Space":
#         MOUSEEVENTF_LEFTDOWN = 0x0002
#         MOUSEEVENTF_LEFTUP = 0x0004

#         # Call the mouse_event function from the Windows API
#         ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
#         ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

#     if event.Key in ["Rcontrol", "Lcontrol"]:
#         exit(0)
############################################ End Mouse Control Code #########################################################


########################### Convenience functions for common keyboard manipulation ##########################################
def is_press_bypassed(event):
    global keypress_bypass
    if event.Key == keypress_bypass.peek():
        keypress_bypass.drop()
        return True
    return False


def is_release_bypassed(event):
    global keyrelease_bypass
    if event.Key == keyrelease_bypass.peek():
        keyrelease_bypass.drop()
        return True
    return False


def cleanupHeldKeys():
    global key_map, held_keys, active_mimics
    for key_name in held_keys:
        key = key_map.get(key_name)
        if not key:
            raise ValueError(f"Somehow '{key_name}' was added to the held keys yet we have no mapping for it in keyMap.py")
        keyrelease_bypass.push(key_name)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
    held_keys = []
    active_mimics = []


def holdKey(key_name):
    global key_map, keypress_bypass, held_keys
    key = key_map.get(key_name)
    if key:
        keypress_bypass.push(key_name)
        win32api.keybd_event(key, 0, 0, 0)
        held_keys.append(key_name)
        return

    raise ValueError(f"Keybinding for '{key_name}' not given in keyMap.py")


def releaseKey(key_name):
    global key_map, keyrelease_bypass, held_keys
    key = key_map.get(key_name)
    if key:
        keyrelease_bypass.push(key_name)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)
        held_keys.remove(key_name)
        return

    raise ValueError(f"Keybinding for '{key_name}' not given in keyMap.py")


def pressAndReleaseKey(key_name):
    global key_map, keypress_bypass, keyrelease_bypass
    key = key_map.get(key_name)
    if key:
        # Key presses are activated via their ascii code while in this system but are converted to a human-readable names in pythoncom when we see them again.
        # Therefore, to press and release a key, we must bypass a key's NAME and press its ASCII code. 
        keypress_bypass.push(key_name)
        win32api.keybd_event(key, 0, 0, 0)
        keyrelease_bypass.push(key_name)
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
    global key_map, keypress_bypass, keyrelease_bypass
    key_names = keycombo.split("+")
    keys = [key_map.get(key) for key in key_names]
    if None in keys:
        raise ValueError(f"Keybinding for key '{key_names[keys.index(None)]}' not specified in keyMap.py")

    for key, keyname in zip(keys, key_names):
        keypress_bypass.push(keyname)
        win32api.keybd_event(key, 0, 0, 0)
    key_names.reverse()
    keys.reverse()
    for key, keyname in zip(keys, key_names):
        keyrelease_bypass.push(keyname)
        win32api.keybd_event(key, 0, win32con.KEYEVENTF_KEYUP, 0)


def typeCharacter(character):
    global key_map, combo_key_map, common_character_map

    # If the character is one pressed with a key combination like capital 'A', do so.
    keycombo = combo_key_map.get(character)
    if keycombo:
        pressKeyCombo(keycombo)
        return

    # Otherwise, convert the character to the pywincom name 
    character = common_character_map.get(character, character)
    if key_map.get(character):
        pressAndReleaseKey(character)
        return
    

    raise ValueError(f"Found no way to type the character '{character}'.")


def typeTemplate(template):
    template += '|' if '|' not in template else ''
    first, second = template.split('|')
    for char in first:
        typeCharacter(char)
    for char in second:
        typeCharacter(char)
    lines_in_second = second.split('\n')
    if len(lines_in_second) > 1:  # Move to the right spot
        for character in lines_in_second[-1]:  # Move to the start of the line you're on
            pressAndReleaseKey('Left')
        for line in range(len(lines_in_second) - 1):  # Move up a number of lines equal to the number of lines since the cursor position
            pressAndReleaseKey('Up')
        for character in first.split('\n')[-1]:  # Move right the correct number of times
            pressAndReleaseKey('Right')
    else:
        for character in second:
            pressAndReleaseKey('Left')




###################### START OF THE SHIFTLOCK DEFINITIONS ############################
key_bindings_ShiftLock = {
    'A': lambda: specialFunctions.asyncAnswerVisableQuizQuestion(),
    'B': lambda: specialFunctions.asyncShowIcecreamCode(),
    'D': lambda: specialFunctions.showRemoteClipboardIP(),
    'H': lambda: specialFunctions.asyncHostClipboard(),
    'I': lambda: specialFunctions.asyncShowIPAddress(),
    'K': lambda: specialFunctions.killAllSubprocesses(),
    'Q': lambda: specialFunctions.asyncAnswerVisableQuizQuestion(verbose=True),
    'R': lambda: specialFunctions.asyncReadRemoteClipboard(globals.data['remoteClipboardIP']),
    'S': lambda: specialFunctions.asyncSetRemoteClipboardIP(),
    'T': lambda: specialFunctions.asyncCountToTheMoon(),
    'Z': lambda: specialFunctions.asyncAnswerVisableExtendedResponseQuestion(stealthy=True),
}
def onPress_ShiftLock(event):
    global key_bindings_ShiftLock, keypress_bypass
    keyaction = key_bindings_ShiftLock.get(event.Key, lambda: 'no binding found')
    keyaction()




###################### START OF THE CAPMODE DEFINITIONS ############################
key_bindings_CapMode = {
# RIGHT HAND BINDINGS
'J': lambda: pressAndReleaseKey('Left'),
'K': lambda: pressAndReleaseKey('Down'),
'L': lambda: pressAndReleaseKey('Up'),
'Oem_1': lambda: pressAndReleaseKey('Right'),  # semicolon
'Oem_7': lambda: pressKeyCombo('Lmenu+Tab'),  # apostrophe
'O': lambda: pressKeyCombo('Lcontrol+Lwin+Left'),
'P': lambda: pressKeyCombo('Lcontrol+Lwin+Right'),
'Return': lambda: pressAndReleaseKeys('End_Return'),
'N': lambda: specialFunctions.capitalizeWord('Left'),
'M': lambda: specialFunctions.capitalizeWord('Right'),
'Oem_Period': lambda: pressKeyCombo('Lcontrol+Lshift+Tab'),
'Oem_2': lambda: pressKeyCombo('Lcontrol+Tab'),
'Rmenu': lambda: pressKeyCombo('Lshift+Lcontrol+Right'),
'Back': lambda: pressAndReleaseKey('Delete'),

# LEFT HAND BINDINGS
'S': lambda: pressKeyCombo('Lcontrol+Left'),
'F': lambda: pressKeyCombo('Lcontrol+Right'),
'E': lambda: pressAndReleaseKey('Home'),
'D': lambda: pressAndReleaseKey('End'),
'G': lambda: typeTemplate('{% | %}'),
'R': lambda: typeTemplate(\
"""print(f"|") # Beans
print('*'*1000)"""),
'Lmenu': lambda: pressKeyCombo('Lshift+Lcontrol+Left'),
}
key_mimics_CapMode = {
    'Space': 'Lshift',
}
def onPress_CapMode(event):
    global key_bindings_CapMode, key_mimics_CapMode
    keyaction = key_bindings_CapMode.get(event.Key, lambda: 'no binding found')
    if keyaction() != 'no binding found':
        cap_mode_used.value = True
        return

    keyToMimic = key_mimics_CapMode.get(event.Key)
    if keyToMimic:
        if event.Key not in active_mimics:
            holdKey(keyToMimic)
            active_mimics.append(event.Key)
        return


def onRelease_CapMode(event):
    global key_mimics_CapMode
    keyToMimic = key_mimics_CapMode.get(event.Key)
    if keyToMimic:
        if event.Key in active_mimics and keyToMimic in held_keys:
            releaseKey(keyToMimic)
            active_mimics.remove(event.Key)
        return



###################### START OF THE CTRLMODE DEFINITIONS ############################

ctrlMode_payload = ""
ctrlMode_next_key_index = 0

def load_payload_from_clipboard():
    """
    Loads a value from the clipboard into the ctrlMode_payload variable.
    
    Return:
      bool | returns whether or not the payload has been altered on load
    """
    global ctrlMode_payload
    old_payload = ctrlMode_payload
    if isinstance(payload := pyperclip.paste(), str):
        ctrlMode_payload = payload

    return old_payload != ctrlMode_payload



def onPress_CtrlMode(event):
    global ctrlMode_payload, ctrlMode_next_key_index
    if entering_ctrl_mode.value: # Todo, replace al the nodes with key value pairs in the globals.data dictionary
        payloadChanged = load_payload_from_clipboard()
        if payloadChanged: ctrlMode_next_key_index = 0
            
    if event.Key == "Escape":
        load_payload_from_clipboard()
        ctrlMode_next_key_index = 0
    else:
        if ctrlMode_next_key_index < len(ctrlMode_payload):
            typeCharacter(ctrlMode_payload[ctrlMode_next_key_index])
            ctrlMode_next_key_index += 1
        else:
            print("Reached the end of the message.")
    




