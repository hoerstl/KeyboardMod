import ctypes


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_long), ("y", ctypes.c_long)]



class Point:

    def __init__(self, x=0, y=0):
        self.x = round(x)
        self.y = round(y)

    def set(self, x, y):
        self.x = round(x)
        self.y = round(y)



screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

major_tile_pos = Point()

def performSecondaryAction(event):
    global screen_width, screen_height, major_tile_pos

    left_hand = [*"QWERTASDFGZXCVB"]
    major_cols = 5
    major_rows = 3
    if len(left_hand) / major_cols != major_rows:
        raise Exception('The left hand grid is not defined as a proper rectangle.')
    major_column_width = screen_width // major_cols
    major_row_height = screen_height // major_rows
    if event.Key in left_hand:
        major_grid_index = left_hand.index(event.Key)
        row_index = major_grid_index // major_cols
        column_index = major_grid_index % major_cols

        major_tile_pos.set(column_index * major_column_width, row_index * major_row_height)

        ctypes.windll.user32.SetCursorPos(major_tile_pos.x, major_tile_pos.y)

    right_hand = [*'YUIOPHJKL', 'Oem_1', *'NM', 'Oem_Comma', 'Oem_Period', 'Oem_2']
    minor_cols = 5
    minor_rows = 3
    if len(right_hand) / minor_cols != minor_rows:
        raise Exception('The right hand grid is not defined as a proper rectangle.')
    minor_column_width = major_column_width // minor_cols
    minor_row_height = major_row_height // minor_rows
    if event.Key in right_hand:
        minor_grid_index = right_hand.index(event.Key)
        row_index = minor_grid_index // minor_cols
        column_index = minor_grid_index % minor_cols  # May need to stretch out these columns to fit all the way to the right

        ctypes.windll.user32.SetCursorPos(major_tile_pos.x + (column_index * minor_column_width), major_tile_pos.y + (row_index * minor_row_height))


    if event.Key == "Space":
        MOUSEEVENTF_LEFTDOWN = 0x0002
        MOUSEEVENTF_LEFTUP = 0x0004

        # Call the mouse_event function from the Windows API
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    if event.Key in ["Rcontrol", "Lcontrol"]:
        exit(0)



# cursor_position = POINT()
# ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor_position))







