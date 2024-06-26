import tkinter as tk
from tkinter import simpledialog


class Popup:
    def __init__(self, title, text, desiredWidth=500, desiredHeight=100):
        self.text = text
        self.title = title
        self.root = tk.Tk()
        self.root.title(title)

        self.desiredWidth = desiredWidth
        self.desiredHeight = desiredHeight

        self.configure()
        self.populateElements()


    def configure(self):
        x = self.root.winfo_screenwidth() // 2
        y = self.root.winfo_screenheight() // 2
        self.root.geometry(f'{self.desiredWidth}x{self.desiredHeight}+{x - (self.desiredWidth//2)}+{y - (self.desiredHeight//2)}')

    def populateElements(self):
        large_font = ("Comic Sans", 30)
        mainInfo = tk.Label(self.root, text=self.text, font=large_font)
        mainInfo.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor="center")

    def mainloop(self):
        self.root.mainloop()


def displayToUser(title, text, desiredWidth=500, desiredHeight=100):
    pop = Popup(title, text, desiredWidth, desiredHeight)
    pop.mainloop()


def getString(title, prompt):
    # Create a Tkinter root window
    root = tk.Tk()
    root.withdraw()  # Hide the root window

    # Prompt the user for text input
    text = simpledialog.askstring(title, prompt)

    return text





if __name__ == '__main__':
    pop = Popup('This is a test window', 'test')
    pop.mainloop()
