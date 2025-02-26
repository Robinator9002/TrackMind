import tkinter as tk
from tkinter import ttk

from menu_settings import *
from settings import os
from util import remove_values


class TKManager:
    """
    TKManager is a class responsible for managing the graphical user interface (GUI) of a Python application.

    Attributes:
    - tracker: An instance of the Tracker class, used for managing the application's data and functionality.
    - root: The main Tkinter window object.
    - width: The width of the main window.
    - height: The height of the main window.
    - style: A Tkinter style object used for configuring the appearance of various GUI elements.
    - plot: A reference to the currently displayed plot widget.

    Methods:
    - __init__(self, tracker, title="TrackMind", size=(MENU_WIDTH, MENU_HEIGHT)): Initializes the TKManager class.
    - run(self): Starts the Tkinter main loop, allowing the GUI to be displayed and responsive to user interactions.
    - show_notification(self, notification): Displays a pop-up window (without sound) with the given notification message.
    - show_custom_notificationbox(self, notification): Creates a custom pop-up notification window, centered on the screen, and closes with Escape.
    - add_button(self, text, command, x, y, frame=None): Creates a button with the given text and command, and places it at the specified coordinates in the given frame.
    - add_label(self, text, x, y, font=(MENU_FONT, MENU_FONT_SIZE), frame=None): Creates a label with the given text and font, and places it at the specified coordinates in the given frame.
    - add_entry(self, x, y, frame=None): Creates an input field (Entry) at the specified coordinates in the given frame.
    - add_listbox(self, x, y, height=5, width=30, items=None, frame=None): Creates a listbox with the given items and dimensions, and places it at the specified coordinates in the given frame.
    - add_dropdown(self, values, x, y, func=None, default_index=0, frame=None): Creates a styled dropdown (OptionMenu) with the given values, and places it at the specified coordinates in the given frame.
    - close_notification(self, frame=None, notification=None, like=False, idx=None): Closes a frame, should mainly be used for notifications. Also calls the `on_notification_qualified` function, to save the notification and 'liked?'.
    - clear_plot(self): Deletes the plot widget and closes the plot via `PlotManager.close_plot()` for a smooth exit.
    - create_plot(self): Disables the Dropdowns and calls `self.tracker.plot_manager.create_plot()`, using the current dropdown values.
    - get_next_dropdown_values(self, current): Returns a list of values for the dropdown based on the given current selection.
    """

    def __init__(self, tracker, title="TrackMind", size=(MENU_WIDTH, MENU_HEIGHT)):
        """
        Initialize the TKManager class.

        Parameters:
        - tracker: An instance of the Tracker class, used for managing the application's data and functionality.
        - title (str): The title of the main window. Default is "TrackMind".
        - size (tuple): The size of the main window. Default is (MENU_WIDTH, MENU_HEIGHT).
        """
        self.tracker = tracker

        self.width, self.height = size[0], size[1]
        self.root = tk.Tk()
        self.root.title(title)
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(*MENU_RESIZABLE)
        self.root.overrideredirect(True)

        x_offset, y_offset = self.get_offset()

        # Set window geometry
        self.root.geometry(f"{self.width}x{self.height}+{x_offset}+{y_offset}")

        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)

        self.setup_ui()

    def setup_ui(self):
        """Creates the basic structure of the window."""

        # Configure Style
        self.config_style()

        # Icon Images
        self.icon_imgs = []

        # Create Titlebar
        self.titlebar, self.close_button = self.create_titlebar(self.root)

        # Create Main Window
        self.main_frame = ttk.Frame(self.root, style='TFrame', padding=10)
        self.main_frame.pack(fill='both', expand=True)  # Main frame spans full window

        # Add Items
        self.add_items()

    def config_style(self):
        """Sets the style, mainly using color and font values from menu_settings.py"""
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

        self.style = ttk.Style()
        self.style.theme_use("clam")
        self.style.configure("TButton", font=(MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE), padding=10, relief='flat',
                             background=self.button_bg, foreground=self.button_fg, borderwidth=1)
        self.style.map("TButton", background=[("active", self.button_hover_bg)])
        self.style.configure("TLabel", font=(MENU_FONT, MENU_FONT_SIZE), background=self.bg_color,
                             foreground=self.text_color)
        self.style.configure("TFrame", background=self.bg_color)

    def create_titlebar(self, frame, title=MENU_TITLE, is_msg=False, icon_fp=MENU_ICON_PATH):
        """Creates a custom titlebar for the window, works for every frame, if it is called for a notification window is_msg should be true,
        so it can sync the closing to likes and important functions."""
        title_bar = tk.Frame(frame, bg=self.title_bg, relief="raised", bd=2)
        title_bar.pack(fill="x", padx=0, pady=0)
        idx = len(self.icon_imgs)
        full_icon_fp = os.path.join(self.tracker.app.autostart_manager.current_abs_path[0], icon_fp)
        self.icon_imgs.append(tk.PhotoImage(file=full_icon_fp))
        icon_label = tk.Label(title_bar, image=self.icon_imgs[idx], background=self.title_bg)
        icon_label.pack(side="left", padx=10)
        title_label = tk.Label(title_bar, text=title, fg=self.text_color, bg=self.title_bg,
                               font=(MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE, "bold"))
        title_label.pack(side="left", padx=10)
        close_func = lambda: self.close_notification(frame, None, False, idx) if is_msg else self.hide_window()
        close_button = tk.Button(title_bar, text="✖", font=(MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE), fg=self.text_color,
                                 bg=self.button_bg, relief="flat", command=close_func)
        close_button.pack(side="right", padx=10)

        # Make Window Moveable (Drag & Drop)
        title_bar.bind("<ButtonPress-1>", lambda event: self.start_move(event, frame))
        title_bar.bind("<ButtonRelease-1>", lambda event: self.stop_move(event, frame))
        title_bar.bind("<B1-Motion>", lambda event: self.do_move(event, frame))

        return title_bar, close_button

    def add_items(self):
        """Creates all the Items for the App, from labels to dropdowns, and adds them. Mainly uses the add_*element* functions from the TKManager class."""
        ## Labels
        # Main Labels
        self.startup_label = self.add_label('Startup', 1250, 160)
        self.notification_label = self.add_label("Welcome to TrackMind!", 400, 80,
                                                 font=(MENU_CAPTION_FONT, MENU_CAPTION_FONT_SIZE))
        # Dropdown Labels
        self.data_label = self.add_label('Data', 75, 200)
        self.analysis_label = self.add_label('Analysis', 250, 200)
        self.part_label = self.add_label('Part', 525, 200)
        self.time_label = self.add_label('Time', 750, 200)
        # Plot Labels
        self.plot_label = self.add_label('Plot', 1250, 300)
        self.data_label = self.add_label('Data', 1250, 600)
        self.quit_label = self.add_label('Quit', 1250, 850)

        ## List
        self.notification_list = self.add_listbox(40, 325, width=MENU_LISTBOX_WIDTH, height=MENU_LISTBOX_HEIGHT)

        ## Buttons
        # Reset Button
        def reset():
            self.tracker.reset = True

        self.reset_button = self.add_button("Reset", reset, 1250, 650)
        # Startup Button
        self.startup_button = self.add_button("Off", self.startup_button_pressed, 1250, 200)
        self.config_startup_button()
        # Plot Buttons
        self.actualize_button = self.add_button("Actualize", self.create_plot, 1250, 350)
        self.clear_button = self.add_button('Clear', self.clear_plot, 1250, 425)
        self.quit_button = self.add_button("Quit", self.hide_window, 1250, 900)

        ## Plot
        self.plot = None

        ## Dropdowns
        # Data Dropdown
        values = list(DROPDOWN_CONTENT.keys())
        values = remove_values(values, ['Time', 'Direction', 'Part'])
        self.data_dropdown = self.add_dropdown(values, 75, 250, self.on_data_dropdown_change, 0)
        # Analyse Dropdown
        self.analysis_dropdown = self.add_dropdown(DROPDOWN_CONTENT["App Usage"], 250, 250, self.on_dropdown_change, 0)
        # Direction and Part Dropdown
        self.direction_dropdown = self.add_dropdown(DROPDOWN_CONTENT["Direction"], 525, 250, self.on_dropdown_change, 0)
        self.part_dropdown = self.add_dropdown(DROPDOWN_CONTENT["Part"], 575, 250, self.on_dropdown_change, 0)
        # Time Dropdown
        self.time_dropdown = self.add_dropdown(DROPDOWN_CONTENT["Time"], 750, 250, self.on_dropdown_change, 0)

    def show_notification(self, notification):
        """Displays a pop-up window (without sound)."""
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
        self.add_button("Like", lambda: self.close_notification(msg_window, notification, True), 75, 225, msg_window)
        self.add_button("Dislike", lambda: self.close_notification(msg_window, notification, False), 275, 225,
                        msg_window)

        # Close on Escape key
        msg_window.bind(f"<{NOTIFICATION_CLOSE_BUTTON}>",
                        lambda event: self.close_notification(msg_window, notification, False))

        # Focus to ensure Escape works immediately
        msg_window.focus_force()

        # Close after delay
        msg_window.after(NOTIFICATION_OPEN_TIME, lambda: self.close_notification(msg_window, notification, False))

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

    def add_dropdown(self, values, x, y, func=None, default_index=0, frame=None):
        """Creates a styled dropdown (OptionMenu) at (x, y),
        with dropdown values 'values', default_index 'default_index' and bind to the function 'func'."""
        if frame is None:
            frame = self.root

        # Dropdown Var
        dropdown_var = tk.StringVar()
        dropdown_var.set(values[default_index])  # Set default selection
        dropdown_var.trace_add("write", func)  # Bind function to dropdown changes

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

    def close_notification(self, frame=None, notification=None, like=False, idx=None):
        """Closes a frame, should mainly be used for notifications. Also calls the on_notification_qualified function, to save the notification and 'liked?'."""
        if frame is None:
            frame = self.root
        if not notification:
            frame.destroy()
            return
        self.tracker.on_notification_qualified(notification, like)
        if idx:
            self.icon_imgs.remove(self.icon_imgs[idx])
        if frame is self.root:
            self.tracker.app.quit()
        frame.destroy()

    def clear_plot(self):
        """Deletes the plot widget and closes the plot via PlotManager.close_plot() for a smooth exit."""
        if self.plot:
            self.tracker.plot_manager.close_plot(self.plot)
            self.plot.get_tk_widget().destroy()

    @staticmethod
    def start_move(event, frame):
        """Sets the frames position to the events position (mouse drag)."""
        frame.x = event.x
        frame.y = event.y

    @staticmethod
    def stop_move(event, frame):
        """Resets the Frame positions."""
        frame.x = None
        frame.y = None

    @staticmethod
    def do_move(event, frame):
        """Applies Movement by settings the Frames coordinates by using the frames and events coordinates."""
        x = frame.winfo_x() + (event.x - frame.x)
        y = frame.winfo_y() + (event.y - frame.y)
        frame.geometry(f"+{x}+{y}")

    def get_offset(self):
        """Gets the offset from every side to center of the screen using the screen_width from winfo_screen and the width and height values."""
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

    def config_startup_button(self):
        """
        Configures the Style and Text of self.startup_button based on the state of autostart.
        Uses the Values self.style and
        MENU_FONT, MENU_BUTTON_FONT_SIZE, BUTTON_GREEN_BG, BUTTON_GREEN_HOVER_BG, BUTTON_RED_BG, BUTTON_RED_HOVER_BG
        from menu_settings
        """
        asm_ref = self.tracker.app.autostart_manager
        if not asm_ref:
            return "Off", "Startup.TButton"
        if self.tracker.app.autostart_manager.is_in_startup:
            text = "On"
            self.style.configure("Startup.TButton", font=(MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE), padding=10,
                                 relief='flat', background=BUTTON_GREEN_BG, foreground=self.button_fg, borderwidth=1)
            self.style.map("Startup.TButton", background=[("active", BUTTON_GREEN_HOVER_BG)])
        else:
            text = "Off"
            self.style.configure("Startup.TButton", font=(MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE), padding=10,
                                 relief='flat', background=BUTTON_RED_BG, foreground=self.button_fg, borderwidth=1)
            self.style.map("Startup.TButton", background=[("active", BUTTON_RED_HOVER_BG)])

        self.startup_button.config(text=text, style="Startup.TButton")

    def startup_button_pressed(self):
        """Checks if the current file is in startup, if so then add or remove the app from startup."""
        asm_ref = self.tracker.app.autostart_manager
        if not asm_ref:
            return

        if asm_ref.is_in_startup:
            asm_ref.remove_from_startup()
        else:
            asm_ref.add_to_startup()

        self.config_startup_button()

    def on_data_dropdown_change(self, *args):
        """Called if the data dropdown value changes"""
        current = (self.data_dropdown[1].get(), self.analysis_dropdown[1].get(), self.time_dropdown[1].get())

        # Get new Values based on the selection
        values = self.get_next_dropdown_values((list(DROPDOWN_CONTENT.keys()).index(current[0]),))

        # Actualize the Analyze Dropdown
        self.analysis_dropdown[1].set(values[1][0])  # Reset to default
        self.analysis_dropdown[0]["menu"].delete(0, "end")
        for value in values[1]:
            self.analysis_dropdown[0]["menu"].add_command(label=value,
                                                          command=lambda v=value: self.analysis_dropdown[1].set(v))

    def create_plot(self):
        """Disables the Dropdowns and calls self.tracker.plot_manager.create_plot(), using the current dropdown values."""
        self.set_dropdowns('disabled')
        self.tracker.plot_manager.create_plot(self.get_current_dropdown_values(), self.root)

    @staticmethod
    def get_next_dropdown_values(current):
        """Returns a list of values for the dropdown based on the given current selection.
        It checks the DROPDOWN_CONTENT list to get the actual values, like if you swap the First dropdown it gets the fitting values for the rest.
        The time_values, direction_values and part_values aren't effected by this, so use it only for the analysis_values if the data_values have changed!"""
        content = DROPDOWN_CONTENT

        data_values = list(content.keys())
        data_values = remove_values(data_values, ['Time', 'Direction', 'Part'])

        valid_keys = list(content.keys())
        selected_key = valid_keys[current[0]]
        analysis_values = list(content[selected_key])

        time_values = list(content["Time"])
        direction_values, part_values = list(content["Direction"]), list(content["Part"])

        return data_values, analysis_values, time_values, direction_values, part_values

    def get_current_dropdown_values(self):
        """Returns all Dropdown Values"""
        return self.data_dropdown[1].get(), self.analysis_dropdown[1].get(), self.time_dropdown[1].get(), \
            self.direction_dropdown[1].get(), self.part_dropdown[1].get()

    def set_dropdowns(self, state, data=True, analysis=True, part=True, time=True):
        """Sets chosen dropdowns to the selected state
        The dropdowns that will be changed depend on the parameters, defaults to all.
        - data (1): data_dropdown
        - analysis (2): analysis_dropdown
        - part (3): direction_dropdown, part_dropdown
        - time (4): time_dropdown
        So e.g. True,True,False,True would mean all but the part dropdowns would be changed."""
        if data:
            self.data_dropdown[0]['state'] = state
        if analysis:
            self.analysis_dropdown[0]['state'] = state
        if part:
            self.direction_dropdown[0]['state'] = state
            self.part_dropdown[0]['state'] = state
        if time:
            self.time_dropdown[0]['state'] = state

    def show_plot(self, plot, plot_type):
        """First clears the current plot if exists (by calling self.clear_plot), then places the new Plot
        If plot_type equals 'heatmap' then don't enable part_dropdowns, otherwise enable all of them.
        This is to avoid any misconception over the part dropdowns not working, because they are NOT used in heatmap plots!
        For further detail look into data_analysis/create_plot and data_analysis/create_tkinter_plot"""
        self.clear_plot()
        self.plot = plot
        plot.get_tk_widget().place(x=40, y=325)

        # Enable Dropdowns, but dont enable part dropdowns if plot type is 'heatmap'
        if plot_type == 'heatmap':
            self.set_dropdowns('normal', True, True, False, True)
        else:
            self.set_dropdowns('normal') # Defaults to all being true, no settings needed

    def on_closing(self, event):
        """Sets state to quiting, the app will be closed next frame."""
        self.tracker.app.quiting = True

    def hide_window(self):
        """Hide the window instead of closing it."""
        self.root.withdraw()
        self._send_to_background()

    def bring_to_foreground(self, tray_icon, item):
        """Bring the app to the foreground - called from the tray menu."""
        # Since pystray runs in its own thread, we must call Tkinter methods thread-safely
        self.root.after(0, self._bring_to_foreground)

    def _bring_to_foreground(self):
        """Brings the root app to the foreground, by deiconifying it."""
        self.root.deiconify()  # Restore the window if it was hidden
        self.root.lift()  # Bring it to the top of other windows
        self.root.focus_force()  # Force focus on the window

    def send_to_background(self, tray_icon, item):
        """Send the app to the background - called from the tray menu."""
        self.root.after(0, self._send_to_background)

    def _send_to_background(self):
        """Send the app to the background - called from the tray menu."""
        self.root.overrideredirect(False)  # Temporarily disable the custom title bar
        self.root.iconify()  # Minimize the window
        self.root.after(100, lambda: self.root.overrideredirect(True))  # Re-enable after a small delay

    def update(self):
        """Will be called every Second"""
        self.tracker.update()
        self.root.after(1000, self.update)

    def run(self):
        """Starts the Tkinter main loop."""
        self.update()
        self.root.mainloop()
