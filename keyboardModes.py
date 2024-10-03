import pyperclip
import globals
import convenienceFunctions as kbd
import specialFunctions
specialFunctions.init()


###################### START OF THE CAPMODE DEFINITIONS ############################
key_bindings_CapMode = {
# RIGHT HAND BINDINGS
'J': lambda: kbd.pressAndReleaseKey('Left'),
'K': lambda: kbd.pressAndReleaseKey('Down'),
'L': lambda: kbd.pressAndReleaseKey('Up'),
'Oem_1': lambda: kbd.pressAndReleaseKey('Right'),  # semicolon
'Oem_7': lambda: kbd.pressKeyCombo('Lmenu+Tab'),  # apostrophe
'O': lambda: kbd.pressKeyCombo('Lcontrol+Lwin+Left'),
'P': lambda: kbd.pressKeyCombo('Lcontrol+Lwin+Right'),
'Return': lambda: kbd.pressAndReleaseKeys('End_Return'),
'Oem_Period': lambda: kbd.pressKeyCombo('Lcontrol+Lshift+Tab'),
'Oem_2': lambda: kbd.pressKeyCombo('Lcontrol+Tab'),
'Rmenu': lambda: kbd.pressKeyCombo('Lshift+Lcontrol+Right'),
'Back': lambda: kbd.pressAndReleaseKey('Delete'),

# LEFT HAND BINDINGS
'S': lambda: kbd.pressKeyCombo('Lcontrol+Left'),
'F': lambda: kbd.pressKeyCombo('Lcontrol+Right'),
'E': lambda: kbd.pressAndReleaseKey('Home'),
'D': lambda: kbd.pressAndReleaseKey('End'),
'G': lambda: specialFunctions.typeTemplate('{% | %}'),
'R': lambda: specialFunctions.typeTemplate(\
"""print(f"|") # Beans
print('*'*1000)"""),
'Lmenu': lambda: kbd.pressKeyCombo('Lshift+Lcontrol+Left'),

'1': lambda: specialFunctions.toggleNotepad(1),
'2': lambda: specialFunctions.toggleNotepad(2),
'3': lambda: specialFunctions.toggleNotepad(3),
'4': lambda: specialFunctions.toggleNotepad(4),
'5': lambda: specialFunctions.toggleNotepad(5),
'6': lambda: specialFunctions.toggleNotepad(6),
'7': lambda: specialFunctions.toggleNotepad(7),
'8': lambda: specialFunctions.toggleNotepad(8),
'9': lambda: specialFunctions.toggleNotepad(9),
'0': lambda: specialFunctions.toggleNotepad(0),
}
key_mimics_CapMode = {
    'Space': 'Lshift',
}
def onPress_CapMode(event):
    global key_bindings_CapMode, key_mimics_CapMode
    keyaction = key_bindings_CapMode.get(event.Key, lambda: 'no binding found')
    if keyaction() != 'no binding found':
        globals.data['cap_mode_used'] = True
        return

    keyToMimic = key_mimics_CapMode.get(event.Key)
    if keyToMimic:
        if event.Key not in globals.active_mimics:
            kbd.holdKey(keyToMimic)
            globals.active_mimics.append(event.Key)
        return


def onRelease_CapMode(event):
    global key_mimics_CapMode
    keyToMimic = key_mimics_CapMode.get(event.Key)
    if keyToMimic:
        if event.Key in globals.active_mimics and keyToMimic in globals.held_keys:
            kbd.releaseKey(keyToMimic)
            globals.active_mimics.remove(event.Key)
        return


###################### START OF THE SHIFTMODE DEFINITIONS ############################
def is_shift_key(key_name):
    shift_names = [
        "shift",
        "Lshift",
        "Rshift"
    ]
    return key_name in shift_names

key_bindings_ShiftMode = {
    'A': lambda: specialFunctions.asyncAnswerVisableQuizQuestion(),
    'B': lambda: specialFunctions.asyncShowIcecreamCode(),
    'C': lambda: specialFunctions.asyncClickMouseXTimes(globals.settings['timesToClick']),
    'D': lambda: specialFunctions.showRemoteServerIP(),
    'H': lambda: specialFunctions.asyncHostServer(),
    'I': lambda: specialFunctions.asyncShowIPAddress(),
    'K': lambda: specialFunctions.killAllSubprocesses(),
    'L': lambda: specialFunctions.asyncSetRemoteServerIP(),
    'Q': lambda: specialFunctions.asyncAnswerVisableQuizQuestion(verbose=True),
    'R': lambda: specialFunctions.asyncReadRemoteClipboard(globals.settings['remoteServerIP']),
    'S': lambda: specialFunctions.asyncOpenSettingsMenu(globals.settings),
    'T': lambda: specialFunctions.asyncCountToTheMoon(),
    'V': lambda: specialFunctions.asyncDisplayRemoteScreenshot(globals.settings['remoteServerIP']),
    'X': lambda: specialFunctions.asyncSetTimesToClick(),
    'Z': lambda: specialFunctions.asyncAnswerVisableExtendedResponseQuestion(stealthy=True),
}
def onPress_ShiftMode(event):
    global key_bindings_ShiftMode
    keyaction = key_bindings_ShiftMode.get(event.Key)
    if keyaction is not None: 
        keyaction()
        globals.data['keyboardMode'] = 'Default'
        print("ShiftMode Off")


###################### START OF THE CTRLMODE DEFINITIONS ############################
def is_ctrl_key(key_name):
    ctrl_names = [
        "control",
        "Lcontrol",
        "Rcontrol",
    ]
    return key_name in ctrl_names

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
    newPayload = pyperclip.paste()
    normalized_content = newPayload.replace('\r\n', '\n').replace('\r', '\n')

    # Replace non-breaking spaces, em spaces, and en spaces with regular spaces
    normalized_content = normalized_content.replace('\u00A0', ' ')  # Non-breaking space
    normalized_content = normalized_content.replace('\u2002', ' ')  # En space
    normalized_content = normalized_content.replace('\u2003', ' ')  # Em space

    # Normalize tabs (replace 4 spaces or other sequences with \t)
    normalized_content = normalized_content.replace('    ', '\t')  # 4 spaces to \t


    if isinstance(normalized_content, str):
        ctrlMode_payload = normalized_content

    return old_payload != ctrlMode_payload

def type_next_payload_character():
    global ctrlMode_payload, ctrlMode_next_key_index
    if ctrlMode_next_key_index < len(ctrlMode_payload):
        kbd.typeCharacter(ctrlMode_payload[ctrlMode_next_key_index])
        ctrlMode_next_key_index += 1
    else:
        print("Reached the end of the message.")


def onPress_CtrlMode(event):
    global ctrlMode_payload, ctrlMode_next_key_index
    if globals.data.get('entering_ctrl_mode'):
        payloadChanged = load_payload_from_clipboard()
        if payloadChanged: ctrlMode_next_key_index = 0
            
    if event.Key == "Escape":
        load_payload_from_clipboard()
        ctrlMode_next_key_index = 0
    elif not is_ctrl_key(event.Key) and not is_shift_key(event.Key):
        type_next_payload_character()
    


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

