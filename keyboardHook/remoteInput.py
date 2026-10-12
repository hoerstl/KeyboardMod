
import ctypes
from ctypes import wintypes

INPUT_KEYBOARD = 1
INPUT_MOUSE = 0
INPUT_HARDWARE = 2

KEYEVENTF_KEYUP = 0x0002
KEYEVENTF_EXTENDEDKEY = 0x0001

ULONG_PTR = ctypes.c_size_t

EXTENDED_KEYS = {
    0x21, 0x22, 0x23, 0x24,
    0x25, 0x26, 0x27, 0x28,
    0x2D, 0x2E,
    0x5B, 0x5C,
    0x6F,
    0xA3, 0xA5,
}


class KEYBDINPUT(ctypes.Structure):
    _fields_ = [
        ("wVk", wintypes.WORD),
        ("wScan", wintypes.WORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ULONG_PTR),
    ]


class HARDWAREINPUT(ctypes.Structure):
    _fields_ = [
        ("uMsg", wintypes.DWORD),
        ("wParamL", wintypes.WORD),
        ("wParamH", wintypes.WORD),
    ]


class INPUTUNION(ctypes.Union):
    _fields_ = [
        ("mi", MOUSEINPUT),
        ("ki", KEYBDINPUT),
        ("hi", HARDWAREINPUT),
    ]


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
    if (
        isinstance(vk, bool)
        or not isinstance(vk, int)
        or not 0 <= vk <= 255
    ):
        raise ValueError(f"Invalid virtual-key code: {vk}")

    if action not in ("down", "up"):
        raise ValueError(f"Invalid key action: {action}")

    flags = 0

    if vk in EXTENDED_KEYS:
        flags |= KEYEVENTF_EXTENDEDKEY

    if action == "up":
        flags |= KEYEVENTF_KEYUP

    keyboard_input = KEYBDINPUT(
        wVk=vk,
        wScan=0,
        dwFlags=flags,
        time=0,
        dwExtraInfo=0,
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

# print("Pointer size:", ctypes.sizeof(ctypes.c_void_p))
# print("KEYBDINPUT size:", ctypes.sizeof(KEYBDINPUT))
# print("MOUSEINPUT size:", ctypes.sizeof(MOUSEINPUT))
# print("INPUT size:", ctypes.sizeof(INPUT))
