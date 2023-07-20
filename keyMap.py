key_map = {
    'A': 65,
    'B': 66,
    'C': 67,
    'D': 68,
    'E': 69,
    'F': 70,
    'G': 71,
    'H': 72,
    'I': 73,
    'J': 74,
    'K': 75,
    'L': 76,
    'M': 77,
    'N': 78,
    'O': 79,
    'P': 80,
    'Q': 81,
    'R': 82,
    'S': 83,
    'T': 84,
    'U': 85,
    'V': 86,
    'W': 87,
    'X': 88,
    'Y': 89,
    'Z': 90,
    '0': 48,
    '1': 49,
    '2': 50,
    '3': 51,
    '4': 52,
    '5': 53,
    '6': 54,
    '7': 55,
    '8': 56,
    '9': 57,
    'F1': 112,
    'F2': 113,
    'F3': 114,
    'F4': 115,
    'F5': 116,
    'F6': 117,
    'F7': 118,
    'F8': 119,
    'F9': 120,
    'F10': 121,
    'F11': 122,
    'F12': 123,
    'Back': 8,  # Backspace
    'Tab': 9,
    'Return': 13,  # Enter
    'Lshift': 16,  # Shift
    'Rshift': 16,  # Shift
    'Lcontrol': 17,  # Control
    'Rcontrol': 17,  # Control
    'Lmenu': 18,  # Alt
    'Rmenu': 18,  # Alt
    'Capital': 20,  # Capslock
    'Escape': 27,
    'Space': 32,
    'Prior': 33,  # Pageup
    'Next': 34,  # Pagedown
    'End': 35,
    'Home': 36,
    'Left': 37,
    'Up': 38,
    'Right': 39,
    'Down': 40,
    'Insert': 45,
    'Delete': 46,
    'Numlock': 144,  # Still needs testing. I have numlock disabled so I couldn't get the keyname
    'Scroll': 145,  # Scroll Lock
    'Pause': 19,
    'Add': 187,
    'Subtract': 189,
    'Multiply': 106,
    'Divide': 111,
    'Decimal': 110,
    'Oem_Comma': 188,  # Comma
    'Oem_Period': 190,  # Period
    'GRAVE': 192,  # TODO: find the grave button on my keyboard
    'Oem_7': 222,  # Single quote
    'Oem_4': 219,  # Left Bracket
    'Oem_6': 221,  # Right bracket
    'Oem_5': 220,  # Backslash
    'Oem_2': 191,  # Forward slash
    'Oem_1': 186,  # Semicolon
    'Oem_Plus': 187,  #Equals,
    'Lwin': 91,
    'Rwin': 92
}

combo_key_map = {
    '(': 'Lshift+9',
    ')': 'Lshift+0',
    '"': 'Lshift+Oem_7',
    '?': 'Lshift+Oem_2',
    '{': 'Lshift+Oem_4',
    '}': 'Lshift+Oem_6',
    '%': 'Lshift+5'
}

common_character_map = {
    "'": 'Oem_7',
    '[': 'Oem_4',
    ']': 'Oem_6',
    '\\': 'Oem_5',
    '/': 'Oem_2',
    ';': 'Oem_1',
    '=': 'Oem_Plus',
    "\n": 'Return',
    ' ': 'Space'
}
