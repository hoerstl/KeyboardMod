import tkinter as tk
from tkinter import simpledialog
import ctypes


def clickAt(x, y, returnToPos=False, window=None):
    """
    window Tk(): An optional window. If truthy, waits until the window is visable before clicking. 
    """
    if window and not window.winfo_viewable():
        window.after(10, lambda: clickAt(x, y, returnToPos, window))
        return

    # Define constants for mouse events
    MOUSEEVENTF_LEFTDOWN = 0x0002
    MOUSEEVENTF_LEFTUP = 0x0004

    # Get the current mouse position
    cursor = ctypes.wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(cursor))
    original_x, original_y = cursor.x, cursor.y

    # Move the mouse to x, y
    ctypes.windll.user32.SetCursorPos(x, y)

    # Simulate left-click
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

    if returnToPos:
        # Move the mouse back to the original position
        ctypes.windll.user32.SetCursorPos(original_x, original_y)



class OverlayEditModal:
    def __init__(self, title='Unnamed Modal', text='', fontSize='small', windowWidth=600, windowHeight=500, cancelCallback=(lambda: None), saveCallback=(lambda text: text), checkActionQueue=(lambda: None)):
        self.title = title
        self.text = text
        self.fontSize = fontSize
        self.windowWidth = windowWidth
        self.windowHeight = windowHeight
        self.cancelCallback = cancelCallback
        self.saveCallback = saveCallback
        self.checkActionQueue = checkActionQueue

        # Create a root window that acts as the greyed-out background
        self.root = tk.Tk()
        
        # Create a top level modal that sits on top of it
        self.modal = tk.Toplevel(self.root)
        self.modal.protocol("WM_DELETE_WINDOW", lambda: self.saveAndExit(forceExit=True))
        
        
        self.populateElements()
        self.configure()

        self.root.after(250, self.checkQueue)
        self.root.after(10, lambda: clickAt(0, 0, returnToPos=True, window=self.root))
    
        


    def populateElements(self):
        # Create the notepad body that you write in
        selected_font = ("Comic Sans", 10 + 10 * ['small', 'medium', 'large'].index(self.fontSize))
        self.notepadBody = tk.Text(self.modal, font=selected_font, wrap=tk.WORD)
        self.notepadBody.insert(tk.INSERT, self.text)
        self.notepadBody.pack(fill=tk.BOTH, expand=True, padx=20, pady=(20, 0), anchor="center")


        # Add save and cancel buttons to the modal
        # Create a frame to hold the buttons
        button_frame = tk.Frame(self.modal)
        button_frame.pack(fill=tk.BOTH, anchor="center", pady=10, padx=20)

        # Add save and cancel buttons to the button_frame
        cancel_button = tk.Button(button_frame, text="Cancel", command=self.cancelAndExit)
        cancel_button.pack(side=tk.LEFT)

        save_button = tk.Button(button_frame, text="Save", command=self.saveAndExit)
        save_button.pack(side=tk.RIGHT)


    def configure(self):
        ## Configure background (root)
        self.root.geometry(f"{self.root.winfo_screenwidth()}x{self.root.winfo_screenheight()}")
        self.root.overrideredirect(1)  # Removes window borders
        self.root.attributes("-alpha", 0.5)  # Makes the background semi-transparent (greyed out)
        self.root.configure(bg='grey')  # Grey background
        self.root.attributes("-topmost", True)
        self.root.lift()  # Brings it to the top of its own stacking order
        self.root.after(1000, lambda: self.root.attributes("-topmost", False))  # Remove always-on-top after 1 second
        
        
        ## Configure the foreground modal (modal)
        self.modal.title(self.title)
        self.modal.geometry("300x200")  # Size of the modal
        self.modal.transient(self.root)  # Set it to always be on top of the root
        self.notepadBody.focus_set()

        self.modal.grab_set()  # Block interactions with the root window
        # Center the modal on the screen
        screen_width = self.modal.winfo_screenwidth()
        screen_height = self.modal.winfo_screenheight()

        x_cordinate = int((screen_width/2) - (self.windowWidth/2))
        y_cordinate = int((screen_height/2) - (self.windowHeight/2))

        self.modal.geometry(f"{self.windowWidth}x{self.windowHeight}+{x_cordinate}+{y_cordinate}")
        

    def checkQueue(self):
        nextAction = self.checkActionQueue()
        if nextAction is None:
            pass
        elif nextAction == "forcedSaveAndExit":
            self.root.after(10, lambda: self.saveAndExit(forceExit=True))
            return
        elif nextAction == "saveAndExit":
            self.root.after(10, self.saveAndExit())
        else:
            print(f"Overlay edit modal got an unexpected action '{nextAction}'")


        self.root.after(10, self.checkQueue)


    def save(self):
        notepad_content = self.notepadBody.get("1.0", tk.END)[:-1]  # Remove the ever-present newline character at the end of the text input for some reason
        try:
            self.saveCallback(notepad_content)
            return True
        except Exception as e:
            print(f"There was an error when we tried to save: {e}")
            return False
        
    def saveAndExit(self, forceExit=False):
        if self.save() or forceExit:
            for id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(id)
            self.root.destroy()


    def cancel(self):
        try:
            self.cancelCallback()
            return True
        except Exception as e:
            print(f"There was an error when we tried to cancel: {e}")
            return False
        
    def cancelAndExit(self, forceExit=False):
        if self.cancel() or forceExit and not self.destroyed:
            for id in self.root.tk.call('after', 'info'):
                self.root.after_cancel(id)
            self.root.destroy()


    def startMainLoop(self):
        """ 
        Starts the overlaid modal
        """
        self.root.mainloop()


    # def focusWindow(self, _calls=0):
    #     # ################# print all windows ################
    #     # def enum_handler(hwnd, ctx):
    #     #     if win32gui.IsWindowVisible(hwnd):
    #     #         window_text = win32gui.GetWindowText(hwnd)
    #     #         if window_text:  # Only print windows that have a title
    #     #             print(f"Window Handle: {hwnd} | Title: {window_text}")

    #     # # Enumerate all windows
    #     # win32gui.EnumWindows(enum_handler, None)
    #     # ####################################################
        
    #     try:
    #         # Get the current thread ID
    #         modal_hwnd = self.modal.winfo_id()
    #         current_thread_id = win32process.GetWindowThreadProcessId(modal_hwnd)[0]

    #         # Get the thread ID of the window to bring to the foreground
    #         focused_hwind = ctypes.windll.user32.GetForegroundWindow()
    #         target_thread_id = win32process.GetWindowThreadProcessId(focused_hwind)[0]

    #         print(f"{modal_hwnd=} | {focused_hwind=}")
    #         print(f"{target_thread_id=} | {current_thread_id=}")

    #         # Attach
    #         ctypes.windll.user32.AttachThreadInput(current_thread_id, target_thread_id, True)
    #         ctypes.windll.user32.AttachThreadInput(target_thread_id, current_thread_id, True)
    #         # Set the target window as the foreground window
    #         ctypes.windll.user32.SetForegroundWindow(modal_hwnd)
    #         # Detach
    #         ctypes.windll.user32.AttachThreadInput(current_thread_id, target_thread_id, False)
    #         ctypes.windll.user32.AttachThreadInput(target_thread_id, current_thread_id, False)

    #         # Get the title of the current foreground window
    #         hwnd = win32gui.GetForegroundWindow()
    #         window_title = win32gui.GetWindowText(hwnd)
    #         print(f"Current Foreground Window Title: {window_title}")
    #     except pywintypes.error as e:
    #         if _calls < 100:
    #             self.root.after(10, lambda: self.focusWindow(_calls=_calls+1))
    #             print("calling again")
    #         else:
    #             raise e
            


class Popup:
    def __init__(self, title, text, fontSize='small', desiredWidth=500, desiredHeight=100):
        self.text = text
        self.title = title
        self.root = tk.Tk()
        self.root.title(title)

        self.fontSize = fontSize
        self.desiredWidth = desiredWidth
        self.desiredHeight = desiredHeight

        self.configure()
        self.populateElements()


    def configure(self):
        x = self.root.winfo_screenwidth() // 2
        y = self.root.winfo_screenheight() // 2
        self.root.geometry(f'{self.desiredWidth}x{self.desiredHeight}+{x - (self.desiredWidth//2)}+{y - (self.desiredHeight//2)}')
        self.root.attributes("-topmost", True)
        self.root.lift()  # Brings it to the top of its own stacking order
        self.root.attributes("-topmost", False)
        self.root.after(10, lambda: clickAt(x, y, returnToPos=True, window=self.root))

    def populateElements(self):
        selected_font = ("Comic Sans", 10 + 10 * ['small', 'medium', 'large'].index(self.fontSize))
        mainInfo = tk.Text(self.root, font=selected_font, wrap=tk.WORD)
        mainInfo.insert(tk.INSERT, self.text)
        mainInfo.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor="center")

    def startMainLoop(self):
        self.root.mainloop()





def displayToUser(title, text, fontSize='small', desiredWidth=500, desiredHeight=100):
    """
    Acceptable font sizes are 'small', 'medium', and 'large'
    """
    pop = Popup(title, text, fontSize, desiredWidth, desiredHeight)
    pop.startMainLoop()


def getString(title, prompt):
    # Create a Tkinter root window
    root = tk.Tk()
    root.attributes('-alpha', 0)  # 0 = completely transparent, 1 = fully opaque
    root.overrideredirect(True)
    root.attributes("-topmost", True)
    root.lift()  # Brings it to the top of its own stacking order

    

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Calculate the position to center the window
    x = (screen_width - 400) // 2
    y = (screen_height - 300) // 2

    # Set the window geometry
    root.geometry(f"{400}x{300}+{x}+{y}")
    def clickSelf():
        if not root.winfo_viewable():
            root.after(10, clickSelf)
            return
        clickAt(x, y, returnToPos=True)

    clickSelf()

    # Prompt the user for text input
    text = simpledialog.askstring(title, prompt, parent=root)
    root.attributes("-topmost", False)
    return text





if __name__ == '__main__':
    # Demo code for the OverlayModal
    def errorCancel():
        raise ValueError("You will never cancel me")
    def errorSave(text):
        raise ValueError("You will never save me")
    modal = OverlayEditModal("Named Modal title", "Hi! I'm notes! Nice to meetcha~`", 'small', 600, 700, errorCancel, errorSave)
    modal.startMainLoop()


    pop = Popup('This is a test window', 'test')
    pop.startMainLoop()
