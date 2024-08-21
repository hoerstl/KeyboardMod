import tkinter as tk
from tkinter import simpledialog


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

    def populateElements(self):
        selected_font = ("Comic Sans", 10 + 10 * ['small', 'medium', 'large'].index(self.fontSize))
        mainInfo = tk.Text(self.root, font=selected_font, wrap=tk.WORD)
        mainInfo.insert(tk.INSERT, self.text)
        mainInfo.pack(fill=tk.BOTH, expand=True, padx=20, pady=20, anchor="center")

    def mainloop(self):
        self.root.mainloop()


def displayToUser(title, text, fontSize='small', desiredWidth=500, desiredHeight=100):
    """
    Acceptable font sizes are 'small', 'medium', and 'large'
    """
    pop = Popup(title, text, fontSize, desiredWidth, desiredHeight)
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
