import tkinter as tk
from tkinter import ttk

class PaginatedSettingsWindow(tk.Tk):
    def __init__(self, on_change_callback):
        super().__init__()
        self.title("Settings")
        self.setGeometry()

        # Callback function for when a widget value changes
        self.on_change_callback = on_change_callback

        # Create a dictionary to hold pages and widgets
        self.pages = {}
        self.widget_values = {}  # To store the current values of each widget by key
        self.current_page = 1
        self.total_pages = 2

        # Frame for holding navigation and page content
        self.content_frame = ttk.Frame(self)
        self.content_frame.pack(fill="both", expand=True)

        # Navigation buttons
        self.navigation_frame = ttk.Frame(self)
        self.navigation_frame.pack(side="bottom", fill="x")

        self.prev_button = ttk.Button(self.navigation_frame, text="Previous", command=self.previous_page)
        self.prev_button.pack(side="left", padx=10, pady=10)

        self.page_label = ttk.Label(self.navigation_frame, text=f"Page {self.current_page} of {self.total_pages}")
        self.page_label.pack(side="left", padx=10, pady=10, expand=True, fill="x")

        self.next_button = ttk.Button(self.navigation_frame, text="Next", command=self.next_page)
        self.next_button.pack(side="right", padx=10, pady=10)

        # Initialize the first page
        for _ in range(self.total_pages):
            self.add_page()
        self.addPresetSettingsContent()
        self.update_navigation_buttons()
        self.show_page(1)

    def setGeometry(self):
        width = height = 400
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        # Calculate the position for the window to be centered
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        # Set the geometry of the window to center it
        self.geometry(f'{width}x{height}+{x}+{y}')

    def add_page(self):
        """Create a new page and add it to the pages dictionary."""
        page_frame = ttk.Frame(self.content_frame)
        page_frame.pack(fill="both", expand=True)
        self.pages[max(list(self.pages.keys()) + [0]) + 1] = page_frame

    def show_page(self, page_number):
        """Display the specified page and hide all others."""
        for page, frame in self.pages.items():
            if page == page_number:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()

        self.current_page = page_number
        self.page_label.config(text=f"Page {self.current_page} of {self.total_pages}")
        self.update_navigation_buttons()

    def next_page(self):
        """Go to the next page, or add a new one if we're on the last page."""
        if self.current_page < self.total_pages:
            self.show_page(self.current_page + 1)
        else:
            self.total_pages += 1
            self.add_page()

    def previous_page(self):
        """Go to the previous page if possible."""
        if self.current_page > 1:
            self.show_page(self.current_page - 1)

    def update_navigation_buttons(self):
        """Enable or disable the navigation buttons based on the current page."""
        if self.current_page == 1:
            self.prev_button.state(['disabled'])
        else:
            self.prev_button.state(['!disabled'])

        if self.current_page == self.total_pages:
            self.next_button.state(['disabled'])
        else:
            self.next_button.state(['!disabled'])

    def add_widget_to_page(self, page_number, widget_type, text=None, key=None):
        """Dynamically add a widget to a specific page and track its value with the given key."""
        if page_number in self.pages:
            page_frame = self.pages[page_number]

            if widget_type == "label":
                label = ttk.Label(page_frame, text=text)
                label.pack(padx=10, pady=10)

            elif widget_type == "entry":
                var = tk.StringVar()  # Use StringVar to track entry value
                entry = ttk.Entry(page_frame, textvariable=var)
                entry.pack(padx=10, pady=10)
                var.trace_add("write", lambda *args: self.on_value_change(key, var.get()))

                # Store the widget's key and variable
                self.widget_values[key] = var

            elif widget_type == "checkbox":
                var = tk.BooleanVar()  # Use BooleanVar to track checkbox state
                checkbox = ttk.Checkbutton(page_frame, text=text, variable=var)
                checkbox.pack(padx=10, pady=10)
                var.trace_add("write", lambda *args: self.on_value_change(key, var.get()))

                # Store the widget's key and variable
                self.widget_values[key] = var

    def on_value_change(self, key, value):
        """Called whenever a widget's value changes, triggers the callback with the key-value pair."""
        # Trigger the external callback function with the key and the updated value
        if self.on_change_callback:
            try:
                value = int(value)
            except:
                pass
            self.on_change_callback(key, value)

    def addPresetSettingsContent(self):
        # Page 1
        self.add_widget_to_page(1, "label", text="Linked Computer IP Address")
        self.add_widget_to_page(1, "entry", key="remoteServerIP")
        self.add_widget_to_page(1, "label", text="Times to click with command")
        self.add_widget_to_page(1, "entry", key="timesToClick")


        # type in code mode (bool)
        


if __name__ == "__main__":
    # Callback function to handle settings change
    def handle_settings_change(key, value):
        print(f"Setting changed - Key: {key}, Value: {value}, ValType: {type(value)}")

    # Create the settings window with the callback
    app = PaginatedSettingsWindow(on_change_callback=handle_settings_change)

    app.mainloop()
