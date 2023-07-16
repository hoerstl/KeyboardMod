import string
import time
import ctypes
import win32api
import win32con
def generate_key_mapping():
    key_mapping = {}

    # Letters A-Z
    for letter in string.ascii_uppercase:
        virtual_key_code = ord(letter)
        key_mapping[letter] = virtual_key_code

    # Numbers 0-9
    for digit in string.digits:
        virtual_key_code = ord(digit)
        key_mapping[digit] = virtual_key_code

    # Other special keys
    key_mapping.update({
        'F1': 0x70,
        'F2': 0x71,
        'F3': 0x72,
        'F4': 0x73,
        'F5': 0x74,
        'F6': 0x75,
        'F7': 0x76,
        'F8': 0x77,
        'F9': 0x78,
        'F10': 0x79,
        'F11': 0x7A,
        'F12': 0x7B,
        'BACKSPACE': 0x08,
        'TAB': 0x09,
        'ENTER': 0x0D,
        'SHIFT': 0x10,
        'CTRL': 0x11,
        'ALT': 0x12,
        'CAPSLOCK': 0x14,
        'ESCAPE': 0x1B,
        'SPACE': 0x20,
        'PAGEUP': 0x21,
        'PAGEDOWN': 0x22,
        'END': 0x23,
        'HOME': 0x24,
        'LEFT': 0x25,
        'UP': 0x26,
        'RIGHT': 0x27,
        'DOWN': 0x28,
        'INSERT': 0x2D,
        'DELETE': 0x2E,
        'NUMLOCK': 0x90,
        'SCROLLLOCK': 0x91,
        'PAUSE': 0x13,
        'PLUS': 0xBB,
        'MINUS': 0xBD,
        'MULTIPLY': 0x6A,
        'DIVIDE': 0x6F,
        'DECIMAL': 0x6E,
        'COMMA': 0xBC,
        'PERIOD': 0xBE,
        'GRAVE': 0xC0,
        'QUOTE': 0xDE,
        'LEFTBRACKET': 0xDB,
        'RIGHTBRACKET': 0xDD,
        'BACKSLASH': 0xDC,
        'FORWARDSLASH': 0xBF,
        'SEMICOLON': 0xBA,
        'EQUALS': 0xBB,
    })

    return key_mapping

# Generate the key mapping
key_mapping = generate_key_mapping()
print('{')
for key in key_mapping:
    print(f"'{key}': {key_mapping[key]},")
print('}')


key_mapping = {
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
    'BACKSPACE': 8,
    'TAB': 9,
    'ENTER': 13,
    'SHIFT': 16,
    'CTRL': 17,
    'ALT': 18,
    'CAPSLOCK': 20,
    'ESCAPE': 27,
    'SPACE': 32,
    'PAGEUP': 33,
    'PAGEDOWN': 34,
    'END': 35,
    'HOME': 36,
    'LEFT': 37,
    'UP': 38,
    'RIGHT': 39,
    'DOWN': 40,
    'INSERT': 45,
    'DELETE': 46,
    'NUMLOCK': 144,
    'SCROLLLOCK': 145,
    'PAUSE': 19,
    'PLUS': 187,
    'MINUS': 189,
    'MULTIPLY': 106,
    'DIVIDE': 111,
    'DECIMAL': 110,
    'COMMA': 188,
    'PERIOD': 190,
    'GRAVE': 192,
    'QUOTE': 222,
    'LEFTBRACKET': 219,
    'RIGHTBRACKET': 221,
    'BACKSLASH': 220,
    'FORWARDSLASH': 191,
    'SEMICOLON': 186,
    'EQUALS': 187
}
