import sys
import winreg

from settings import *


class AutostartManager:
    """
    The AutostartManager class is responsible for managing and controlling the autostart functionality of a software application.

    Attributes:
        tracker (object): The tracker object that provides necessary functionality for the AutostartManager.
        method (str): The method used to manage autostart (either 'folder' or 'registry').
        registry_name (str): The name used in the Windows registry to store the file path.

    Methods:
        add_to_startup(self): Adds the found file to startup (using folder or registry).
        remove_from_startup(self): Removes the found file from startup (using folder or registry).
        is_in_startup(self): Checks if the found file is in startup (using folder or registry).
        actualize(self): Sets the AutostartManager (self) values to the current actualized ones.
        current_abs_path(self): Returns the current absolute path, which should lead to either a .exe or a .py file, otherwise this may not work.
    """
    def __init__(self, tracker):
        self.tracker = tracker

        self.actualize()
        self.method, self.registry_name = AUTOSTART_METHOD, AUTOSTART_REGISTRY_NAME

    def add_to_startup(self):
        """Adds the found file to startup (using folder or registry)"""
        self.actualize()
        if self.typ != 'exe':
            print("Only .exe files can be added to autostart!")
            return
        if self.method == "folder":
            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_folder, os.path.basename(self.file_name))
            print(shortcut_path)
            os.system(f'copy "{self.file_name}" "{shortcut_path}"')
            print(f"✔ File successfully copied to startup folder: {shortcut_path}")

        elif self.method == "registry":
            file_path = self.abs_file_path  # Use absolute File Path (with file_name)
            print(file_path)
            if not self.registry_name:
                print("You have to enter a registry_name if the chosen method is registry!")
                return
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                winreg.SetValueEx(reg_key, self.registry_name, 0, winreg.REG_SZ, file_path)
            print(f"✔ File successfully added to Windows registry: {file_path}")

        else:
            print("❌ Invalid method! Use 'folder' or 'registry'.")

    def remove_from_startup(self):
        """Removes the found file from startup (using folder or registry)"""
        self.actualize()
        if self.method == "folder":
            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_folder, os.path.basename(self.file_path))
            print(shortcut_path)
            if os.path.exists(shortcut_path):
                os.remove(shortcut_path)
                print(f"✔ File successfully removed from startup folder: {shortcut_path}")
            else:
                print("❌ File not found in startup folder.")

        elif self.method == "registry":
            file_path = self.abs_file_path  # Use absolute File Path (with file_name)
            print(file_path)
            if not self.registry_name:
                print("You have to enter a registry_name if the chosen method is registry!")
                return
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_SET_VALUE) as reg_key:
                    winreg.DeleteValue(reg_key, self.registry_name)
                print(f"✔ File successfully removed from Windows registry: {file_path}")
            except FileNotFoundError:
                print("❌ Registry entry not found.")

        else:
            print("❌ Invalid method! Use 'folder' or 'registry'.")

    @property
    def is_in_startup(self):
        """Checks if the found file is in startup (using folder or registry)"""
        self.actualize()
        if self.method == "folder":
            startup_folder = os.path.join(os.getenv('APPDATA'), r'Microsoft\Windows\Start Menu\Programs\Startup')
            shortcut_path = os.path.join(startup_folder, os.path.basename(self.file_name))
            if os.path.exists(shortcut_path):
                print("✔ File is in startup folder.")
                return True
            else:
                print("❌ File is NOT in startup folder.")
                return False

        elif self.method == "registry":
            if not self.registry_name:
                print("You have to enter a registry_name if the chosen method is registry!")
                return
            key = r"Software\Microsoft\Windows\CurrentVersion\Run"
            try:
                with winreg.OpenKey(winreg.HKEY_CURRENT_USER, key, 0, winreg.KEY_QUERY_VALUE) as reg_key:
                    reg_value, _ = winreg.QueryValueEx(reg_key, self.registry_name)
                    if reg_value.lower() == self.abs_file_path.lower():
                        print("✔ File is in Windows registry startup.")
                        return True
                    else:
                        print("❌ File is NOT in Windows registry startup.")
                        return False
            except FileNotFoundError:
                print("❌ Registry entry not found.")
                return False

        else:
            print("❌ Invalid method! Use 'folder' or 'registry'.")
            return False

    def actualize(self):
        """Sets the AutostartManager (self) values to the current actualized ones."""
        self.file_path, self.file_name, self.typ = self.current_abs_path
        self.abs_file_path = os.path.join(self.file_path, self.file_name)

    @property
    def current_abs_path(self):
        """Returns the current absolute path, which should lead to either a .exe or a .py file, otherwise this may not work."""
        if getattr(sys, 'frozen', False):
            # If .exe
            current_file = sys.executable
            typ = 'exe'
        else:
            # If .py
            typ = 'py'
            current_file = os.path.abspath(__file__)

        current_folder = os.path.dirname(current_file)
        filename = os.path.basename(current_file)

        return current_folder, filename, typ
