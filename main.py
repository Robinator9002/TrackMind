import atexit
import os
import signal
import sys

from settings import *
from sql import SQLManager, SQLLoader
from tracker import Tracker


class App:
    def __init__(self):
        self.tracker = Tracker(self)

        self.sql_manager = SQLManager()
        self.loader = SQLLoader(self.sql_manager)

        self.quiting = False

        # Auto Save at Normal Quit
        atexit.register(self.quit)
        signal.signal(signal.SIGINT, self.handle_exit)  # CTRL+C
        signal.signal(signal.SIGTERM, self.handle_exit)  # Kill-Command

    def handle_exit(self, signum, frame):
        print(f"Received signal {signum}, saving before exit...")
        self.quit()
        sys.exit(0)  # Save Quit after Saving

    def run(self):
        self.check_data()
        self.tracker.start()

    @staticmethod
    def check_data():
        os.makedirs(DATA_ROOT, exist_ok=True)

    def quit(self):
        print("Saving data before quitting...")
        self.tracker.quit()

        # Prevents Double Signal-Handler Calls
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        signal.signal(signal.SIGTERM, signal.SIG_DFL)

        self.quiting = True


if __name__ == "__main__":
    app = App()
    app.run()
