
import ctypes
from ctypes import wintypes


# Windows keyboard input constants
INPUT_KEYBOARD = 1
KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001

# Virtual-key codes that require the extended-key flag.
EXTENDED_KEYS = {
    0x21, 0x22, 0x23, 0x24,  # Page Up, Page Down, End, Home
    0x25, 0x26, 0x27, 0x28,  # Arrow keys
    0x2D, 0x2E,              # Insert, Delete
    0x5B, 0x5C,              # Left/Right Windows
    0x6F,                    # Numpad divide
    0xA3, 0xA5,              # Right Ctrl, Right Alt
}


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [("ki", KEYBDINPUT)]


class INPUT(ctypes.Structure):
    _anonymous_ = ("u",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("u", INPUTUNION),
    ]


user32 = ctypes.WinDLL("user32", use_last_error=True)

user32.SendInput.argtypes = [
    wintypes.UINT,
    ctypes.POINTER(INPUT),
    ctypes.c_int,
]
user32.SendInput.restype = wintypes.UINT


def inject_key(vk: int, action: str) -> None:
    """
    Simulate a key-down or key-up event.

    vk: Windows virtual-key code, such as 65 for A.
    action: "down" or "up".
    """
    if not isinstance(vk, int) or isinstance(vk, bool) or not 0 <= vk <= 255:
        raise ValueError(f"Invalid virtual-key code: {vk}")

    if action not in ("down", "up"):
        raise ValueError(f"Invalid key action: {action}")

    flags = 0

    if vk in EXTENDED_KEYS:
        flags |= KEYEVENTF_EXTENDEDKEY

    if action == "up":
        flags |= KEYEVENTF_KEYUP

    extra_info = ctypes.c_ulong(0)

    keyboard_input = KEYBDINPUT(
        wVk=vk,
        wScan=0,
        dwFlags=flags,
        time=0,
        dwExtraInfo=ctypes.pointer(extra_info),
    )

    native_input = INPUT(
        type=INPUT_KEYBOARD,
        ki=keyboard_input,
    )

    sent = user32.SendInput(
        1,
        ctypes.byref(native_input),
        ctypes.sizeof(INPUT),
    )

    if sent != 1:
        raise ctypes.WinError(ctypes.get_last_error())
