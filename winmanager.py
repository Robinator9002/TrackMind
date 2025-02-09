import keyboard
import psutil
import win32gui
import win32process
from pynput.mouse import Listener as MouseListener


class WinManager:
    def __init__(self, manager):
        self.manager = manager
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
        """Checks if any key was pressed, if true call the self.manager.on_keypress() method."""
        event = keyboard.read_event()
        if event.event_type == keyboard.KEY_DOWN:  # Only Keyboard Buttons
            self.manager.on_keypress()

    def on_mouse_click(self, x, y, button, pressed):
        self.manager.on_keypress()
