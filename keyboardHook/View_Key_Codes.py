import pythoncom
import pyWinhook

def on_key_press(event):
    print(event.Key)
    if event.Key == "Escape":
        exit()
    return False


def on_key_release(event):
    return False

def on_mouse(event):
    print(f"{event.GetMessageName()=}, {event.Injected=}, {event.Message=}, {event.MessageName=}, {event.Position}, {event.Time}, {event.Wheel}, {event.Window}, {event.WindowName}")
    return True
    


def start_hook():
    # Create an instance of the hook manager
    hook_manager = pyWinhook.HookManager()

    # Register the callback function for keyboard events
    hook_manager.KeyDown = on_key_press
    hook_manager.KeyUp = on_key_release

    # Register the callback for mouse events
    hook_manager.MouseAll = on_mouse

    # Set the hook and start the event loop
    hook_manager.HookKeyboard()
    hook_manager.HookMouse()
    pythoncom.PumpMessages()


if __name__ == '__main__':
    start_hook()
