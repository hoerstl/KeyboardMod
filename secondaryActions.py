import ctypes


def performSecondaryAction(event):

    if event.Key == "A":
        print("you just pressed the A key silly.")




        ctypes.windll.user32.SetCursorPos()


print(ctypes.windll.user32.GetCursorPos())
