import atexit
import signal
import sys

from autostart import AutostartManager
from settings import *
from sql import SQLManager, SQLLoader
from tkmanager import TKManager
from tracker import Tracker


class App:
    """
    The main application class that manages the tracker, autostart manager, tk manager, SQL manager, SQL loader, and signal handling.

    Attributes:
        tracker: An instance of Tracker.
        autostart_manager: An instance of AutostartManager.
        tk_manager: An instance of TKManager.
        sql_manager: An instance of SQLManager.
        loader: An instance of SQLLoader.
        quiting: A boolean indicating whether the application is in the process of quitting.

    Methods:
        handle_exit(signum, frame): Handles the exit signal by calling self.quit() and then exiting the system.
        run(): Checks the data and then starts the app via Tracker.start.
        check_data(): Checks the data path, but does not check if images or other data is existent. If not, the app will crash!
        quit(): Saves all important data before quitting the application and ends the signal reading to prevent it from being called twice.
    """
    def __init__(self):
        """
        Initializes the App class.

        Sets up the tracker, autostart manager, tk manager, SQL manager, SQL loader, and signal handling.
        Checks the data path and adds the app to the startup if it's not already there.
        """
        self.tracker = Tracker(self)

        self.autostart_manager = AutostartManager(self.tracker)
        self.tk_manager = TKManager(self.tracker)

        sql_abs_path = os.path.join(self.autostart_manager.current_abs_path[0], SQL_PATH)
        self.autostart_manager.add_to_startup()
        self.sql_manager = SQLManager(sql_abs_path)
        self.loader = SQLLoader(self.sql_manager)

        self.quiting = False

        # Auto Save at Normal Quit
        atexit.register(self.quit)
        signal.signal(signal.SIGINT, self.handle_exit)  # CTRL+C
        signal.signal(signal.SIGTERM, self.handle_exit)  # Kill-Command

        # Check Data
        self.check_data()

    def handle_exit(self, signum, frame):
        """Calls self.quit() and then exits the system"""
        self.quit()
        sys.exit(0)  # Save Quit after Saving

    def run(self):
        """Checks the data and then starts the app via Tracker.start"""
        self.check_data()
        self.tracker.start()

    def check_data(self):
        """Checks the data path, but NOT checks if images or other data is existent, if not then the app WILL CRASH!"""
        # Data
        abs_data_path = os.path.join(self.autostart_manager.current_abs_path[0], DATA_ROOT)
        os.makedirs(abs_data_path, exist_ok=True)

    def quit(self):
        """Calls tracker.quit() to save all important data, and ends the signal reading to make sure it isn't called twice.
        Not checks if atexit fires twice, this won't be prevented by this function!"""
        print("Saving data before quitting...")

        # Prevents Double Signal-Handler Calls
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        # Save Data to SQL
        self.tracker.save_all()


if __name__ == "__main__":
    app = App()
    app.run()
