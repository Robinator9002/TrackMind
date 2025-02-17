import tkinter as tk
from tkinter import ttk

from menu_settings import *


class TKManager:
    def __init__(self, manager, title="TrackMind", size=(MENU_WIDTH, MENU_HEIGHT)):
        self.tracker = manager

        self.width, self.height = size[0], size[1]
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(*MENU_RESIZABLE)
        self.root.overrideredirect(True)

        x_offset, y_offset = self.get_offset()

        # Set window geometry
        self.root.geometry(f"{self.width}x{self.height}+{x_offset}+{y_offset}")

        self.root.bind(f"<{MENU_CLOSE_BUTTON}>", lambda event: self.on_closing(event))
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.on_closing(None))

        self.setup_ui()

    def setup_ui(self):
        """Creates the basic structure of the window."""

        # Configure Style
        self.config_style()

        # Create Titlebar
        self.titlebar, self.close_button = self.create_titlebar(self.root)

        # Create Main Window
        self.main_frame = ttk.Frame(self.root, style='TFrame', padding=10)
        self.main_frame.pack(fill='both', expand=True)  # Main frame spans full window

        # Add Items
        self.add_items()

    def config_style(self):
        # Configure Colors
        self.bg_color = BG_COLOR  # Dark Background
        self.title_bg = TITLE_BG
        self.button_bg = BUTTON_BG  # Dark Buttons
        self.button_fg = BUTTON_FG
        self.button_hover_bg = BUTTON_HOVER_BG  # Hover-Color for smoother transition
        self.text_color = TEXT_COLOR  # Light grey for better readability
        self.dropdown_bg = DROPDOWN_BG
        self.dropdown_fg = DROPDOWN_FG
        self.dropdown_arrow = DROPDOWN_ARROW

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton", font=(MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE), padding=10, relief='flat',
                        background=self.button_bg, foreground=self.button_fg, borderwidth=1)
        style.map("TButton", background=[("active", self.button_hover_bg)])
        style.configure("TLabel", font=(MENU_FONT, MENU_FONT_SIZE), background=self.bg_color,
                        foreground=self.text_color)
        style.configure("TFrame", background=self.bg_color)

    def create_titlebar(self, frame, title=MENU_TITLE, is_msg=False):
        """Creates a titlebar"""
        title_bar = tk.Frame(frame, bg=self.title_bg, relief="raised", bd=2)
        title_bar.pack(fill="x", padx=0, pady=0)
        title_label = tk.Label(title_bar, text=title, fg=self.text_color, bg=self.title_bg,
                               font=(MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE, "bold"))
        title_label.pack(side="left", padx=10)
        close_func = lambda: self.close_notification(frame, False) if is_msg else self.on_closing(None)
        close_button = tk.Button(title_bar, text="✖", font=(MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE), fg=self.text_color,
                                 bg=self.button_bg, relief="flat", command=close_func)
        close_button.pack(side="right", padx=10)

        # Make Window Moveable (Drag & Drop)
        title_bar.bind("<ButtonPress-1>", lambda event: self.start_move(event, frame))
        title_bar.bind("<ButtonRelease-1>", lambda event: self.stop_move(event, frame))
        title_bar.bind("<B1-Motion>", lambda event: self.do_move(event, frame))

        return title_bar, close_button

    def add_items(self):
        # Dropdowns
        self.create_dropdowns()

        # Labels
        self.data_label = self.add_label('Data', 75, 240)
        self.analysis_label = self.add_label('Analysis', 250, 240)
        self.time_label = self.add_label('Time', 600, 240)
        self.notification_label = self.add_label("Welcome to TrackMind!", 400, 80,
                                                 font=(MENU_CAPTION_FONT, MENU_CAPTION_FONT_SIZE))
        # List
        self.notification_list = self.add_listbox(40, 350, height=25, width=90)

        ## Buttons
        # Reset Button
        def reset():
            self.tracker.reset = True

        self.reset_button = self.add_button("Reset", reset, 1080, 375)
        self.actualize_button = self.add_button("Actualize", self.actualize, 1080, 450)
        self.quit_button = self.add_button("Quit", lambda: self.on_closing(None), 1080, 850)

        # Plot
        self.plot = None

    def create_dropdowns(self):
        # First Dropdown (Data)
        values = list(DROPDOWN_CONTENT.keys())
        values.remove('Time')
        self.data_dropdown = self.add_dropdown(values, 75, 275, 0)
        self.data_dropdown[1].trace_add("write", self.on_data_dropdown_change)

        # Second Dropdown (Analyse)
        self.analysis_dropdown = self.add_dropdown(DROPDOWN_CONTENT["App Usage"], 250, 275, 0)
        self.analysis_dropdown[1].trace_add("write", self.on_dropdown_change)

        # Third Dropdown (Time)
        self.time_dropdown = self.add_dropdown(DROPDOWN_CONTENT["Time"], 600, 275, 0)
        self.time_dropdown[1].trace_add("write", self.on_dropdown_change)

    def show_notification(self, notification="Test Notification"):
        """Displays a notification in the listbox and a separate pop-up window (without sound)."""
        self.notification_list.insert(tk.END, notification[0])
        self.notification_list.yview(tk.END)
        self.show_custom_notificationbox(notification)

    def show_custom_notificationbox(self, notification):
        """Creates a custom pop-up notification window, centered on the screen, and closes with Escape."""
        msg_window = tk.Toplevel(self.root, background=self.bg_color)
        msg_window.title("Notification")

        # Window size
        width, height = NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT

        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position (centered)
        x_offset = (screen_width // 2) - (width // 2)
        y_offset = (screen_height // 2) - (height // 2)

        # Set window geometry
        msg_window.geometry(f"{width}x{height}+{x_offset}+{y_offset}")
        msg_window.resizable(False, False)
        msg_window.overrideredirect(True)

        # Create Titlebar
        self.create_titlebar(msg_window, 'Notification', True)

        # Notification label
        msg_label = ttk.Label(msg_window, text=notification[0], font=(NOTIFICATION_FONT, NOTIFICATION_FONT_SIZE),
                              wraplength=280)
        msg_label.pack(pady=25, padx=10)

        # Like and Dislike Buttons
        self.add_button("Like", lambda: self.close_notification(msg_window, notification, True), 150, 250, msg_window)
        self.add_button("Dislike", lambda: self.close_notification(msg_window, notification, False), 350, 250,
                        msg_window)

        # Close on Escape key
        msg_window.bind(f"<{NOTIFICATION_CLOSE_BUTTON}>",
                        lambda event: self.close_notification(msg_window, notification, False))

        # Focus to ensure Escape works immediately
        msg_window.focus_force()

    def add_button(self, text, command, x, y, frame=None):
        """Creates a button and places it at (x, y) in the given frame."""
        if frame is None:
            frame = self.root  # Use root directly for absolute positioning
        button = ttk.Button(frame, text=text, command=command)
        button.place(x=x, y=y)
        return button

    def add_label(self, text, x, y, font=(MENU_FONT, MENU_FONT_SIZE), frame=None):
        """Creates a label with the given text and font at (x, y)."""
        if frame is None:
            frame = self.root
        label = ttk.Label(frame, text=text, font=font)
        label.place(x=x, y=y)
        return label

    def add_entry(self, x, y, frame=None):
        """Creates an input field (Entry) at (x, y)."""
        if frame is None:
            frame = self.root
        entry = ttk.Entry(frame)
        entry.place(x=x, y=y, width=200)  # Fixed width for better layout
        return entry

    def add_listbox(self, x, y, height=5, width=30, items=None, frame=None):
        """Creates a listbox with optional predefined items at (x, y)."""
        listbox_bg = LISTBOX_BG  # Listbox - Background Color
        listbox_fg = LISTBOX_FG  # Listbox - Text Color

        if frame is None:
            frame = self.root
        listbox = tk.Listbox(frame, height=height, width=width, background=listbox_bg, foreground=listbox_fg,
                             font=(MENU_LISTBOX_FONT, MENU_LISTBOX_FONT_SIZE), relief="flat", borderwidth=0,
                             highlightthickness=0, selectbackground="#404040", selectforeground="white")
        listbox.place(x=x, y=y)
        if items:
            for item in items:
                listbox.insert(tk.END, item)
        return listbox

    def add_dropdown(self, values, x, y, default_index=0, frame=None):
        """Creates a styled dropdown (OptionMenu) with given values at (x, y)."""
        if frame is None:
            frame = self.root

        dropdown_var = tk.StringVar()
        dropdown_var.set(values[default_index])  # Set default selection

        dropdown = tk.OptionMenu(frame, dropdown_var, *values)
        dropdown.config(bg=self.dropdown_bg, fg=self.dropdown_fg, activebackground=DROPDOWN_HOVER_BG,
                        activeforeground=self.dropdown_fg, font=(MENU_DROPDOWN_FONT, MENU_DROPDOWN_FONT_SIZE), bd=0,
                        relief="flat")

        # Access menu widget to style dropdown options
        menu = self.root.nametowidget(dropdown.menuname)
        menu.config(bg=self.dropdown_bg, fg=self.dropdown_fg, activebackground=DROPDOWN_HOVER_BG,
                    activeforeground=self.dropdown_fg, font=(MENU_DROPDOWN_FONT, MENU_DROPDOWN_FONT_SIZE))

        dropdown.place(x=x, y=y)
        return dropdown, dropdown_var  # Return both the dropdown and its variable

    def close_notification(self, frame=None, notification=None, like=False):
        if frame is None:
            frame = self.root
        if not notification:
            frame.destroy()
            return
        self.tracker.on_notification_qualified(notification, like)
        if frame is self.root:
            self.tracker.app.quit()
        frame.destroy()

    def actualize(self):
        self.create_plot()

    @staticmethod
    def start_move(event, frame):
        frame.x = event.x
        frame.y = event.y

    @staticmethod
    def stop_move(event, frame):
        frame.x = None
        frame.y = None

    @staticmethod
    def do_move(event, frame):
        x = frame.winfo_x() + (event.x - frame.x)
        y = frame.winfo_y() + (event.y - frame.y)
        frame.geometry(f"+{x}+{y}")

    def get_offset(self):
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        # Calculate position (centered)
        x_offset = (screen_width // 2) - (self.width // 2)
        y_offset = (screen_height // 2) - (self.height // 2)

        return x_offset, y_offset

    def on_dropdown_change(self, *args):
        """Called if a dropdown is changed"""
        self.create_plot()

    def on_data_dropdown_change(self, *args):
        """Called if the data dropdown value changes"""
        current = (self.data_dropdown[1].get(), self.analysis_dropdown[1].get(), self.time_dropdown[1].get())

        # Get new Values based on the selection
        values = self.get_next_dropdown_values((list(DROPDOWN_CONTENT.keys()).index(current[0]),))

        # Actualize the Analyze Dropdown
        self.analysis_dropdown[1].set(values[1][0]) # Reset to default
        self.analysis_dropdown[0]["menu"].delete(0, "end")
        for value in values[1]:
            self.analysis_dropdown[0]["menu"].add_command(label=value,
                                                       command=lambda v=value: self.analysis_dropdown[1].set(v))

    def create_plot(self):
        self.set_dropdowns('disabled')
        self.tracker.create_plot(self.get_current_dropdown_values(), self.root)

    @staticmethod
    def get_next_dropdown_values(current):
        """Returns a list of values for the dropdown based on the given current selection."""
        content = DROPDOWN_CONTENT

        data_values = list(content.keys())
        data_values.remove("Time")

        valid_keys = list(content.keys())
        selected_key = valid_keys[current[0]]
        analysis_values = list(content[selected_key])

        time_values = list(content["Time"])

        return data_values, analysis_values, time_values

    def get_current_dropdown_values(self):
        return self.data_dropdown[1].get(), self.analysis_dropdown[1].get(), self.time_dropdown[1].get()

    def set_dropdowns(self, state):
        self.data_dropdown[0]['state'] = state
        self.analysis_dropdown[0]['state'] = state
        self.time_dropdown[0]['state'] = state

    def show_plot(self, plot):
        if self.plot:
            self.tracker.plot_manager.close_plot(plot)
            self.plot.get_tk_widget().destroy()
        self.plot = plot
        plot.get_tk_widget().place(x=40, y=350)
        self.set_dropdowns('normal')

    def on_closing(self, event):
        self.tracker.app.handle_exit(None, None)

    def update(self):
        """Will be called every Second"""
        self.tracker.update()
        self.root.after(1000, self.update)

    def run(self):
        """Starts the Tkinter main loop."""
        self.update()
        self.root.mainloop()
