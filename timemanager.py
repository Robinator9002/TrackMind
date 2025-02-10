import datetime
import time

from settings import *


class TimeManager:
    def __init__(self, manager):
        self.manager = manager
        self.opened_time = 0  # in seconds
        self.active_time = 0  # in seconds
        self.total_active_time = 0  # in seconds
        self.kp = 0
        self.last_activity_time = None  # Time passed since the last activity (keypress or app swap)

    def reset_times(self, app=None):
        """Resets the active and inactive time."""
        self.manager.save_all(app)
        self.opened_time = 0
        self.active_time = 0
        self.total_active_time = 0
        self.kp = 0
        self.last_activity_time = None

    def on_keypress(self):
        """Called when a key is pressed. Updates the active time."""
        self.last_activity_time = time.time()  # Set the current time as the last activity
        self.kp += 1

    def on_app_swap(self, app):
        """Called when the app is swapped. Saves and resets the times."""
        self.reset_times(app)  # Reset the times whenever the app is swapped

    def check_inactivity(self):
        """Checks if the user is inactive based on the last activity."""
        current_time = time.time()
        self.opened_time += 1
        if ((self.last_activity_time is None) or (
                self.last_activity_time is not None and (current_time - self.last_activity_time) > INACTIVE)):
            # If the time since the last activity exceeds the inactivity threshold, the user is considered inactive
            self.active_time = 0  # Reset Active Time, but not total_active_time
        else:
            self.active_time += 1  # Otherwise, count 1 second of active time
            self.total_active_time += 1  # Count the total active time, wont be reset if inactive

    @property
    def kpm(self):
        return int((self.kp / max(self.opened_time, 1)) * 60)

    @property
    def timestamp(self):
        return datetime.datetime.now().isoformat()

    def load_time(self, opened_time, active_time, total_active_time):
        """Loads the saved times."""
        self.opened_time = opened_time
        self.active_time = active_time
        self.total_active_time = total_active_time

    def update(self):
        """Called regularly to update the times."""
        self.check_inactivity()
