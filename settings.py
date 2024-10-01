import tkinter as tk
from tkinter import ttk

class PaginatedSettingsWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Settings")
        self.geometry("400x400")

        # Set up navigation frame
        self.nav_frame = ttk.Frame(self)
        self.nav_frame.pack(side="top", fill="x")

        self.prev_button = ttk.Button(self.nav_frame, text="Previous", command=self.show_previous_page)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.next_button = ttk.Button(self.nav_frame, text="Next", command=self.show_next_page)
        self.next_button.pack(side="right", padx=10, pady=10)

