import keyboard
import psutil
import win32gui
import win32process
from pynput.mouse import Listener as MouseListener


class WinManager:
    """
    Manages the interaction with the Windows operating system.

    Attributes:
    - tracker: Reference to the main tracker object.
    - mouse_listener: Mouse listener object for capturing mouse clicks.

    Methods:
    - active_app: Checks the currently opened application in the foreground.
    - check_keypress: Checks if any key was pressed, and calls the appropriate method.
    - on_mouse_click: Callback method for handling mouse clicks.
    """

    def __init__(self, tracker):
        """
        Initializes the WinManager object with a reference to the tracker object.
        Starts a mouse listener to capture mouse clicks.

        Parameters:
        - tracker: Reference to the main tracker object.
        """
        self.tracker = tracker
        self.mouse_listener = MouseListener(on_click=self.on_mouse_click)
        self.mouse_listener.start()

    @property
    def active_app(self):
        """Checks the currently opened App in the foreground."""
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        try:
            if pid > 0:
                process = psutil.Process(pid)
                return process.name()
            else:
                return "Invalid PID"
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
            return "Unknown"
        except Exception as e:
            return f"Error: {e}"

    def check_keypress(self):
        """Checks if any key was pressed, if true call the self.tracker.time_manager.on_keypress() method."""
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:  # Only Keyboard Buttons
            self.tracker.time_manager.on_keypress()

    def on_mouse_click(self, x, y, button, pressed):
        """Calls the self.tracker.time_tracker.time_manager.on_keypress() method."""
        self.tracker.time_manager.on_keypress()
