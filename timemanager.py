import datetime
import time

from settings import *


class TimeManager:
    """
    Manages time-related operations for the application.

    Attributes:
        tracker (object): The tracker object that provides necessary functionality for the TimeManager.
        inactive (boolean): Whether the user is currently inactive or not.
        opened_time (int): The time the application has been opened in seconds.
        active_time (int): The time the application has been actively used in seconds.
        total_active_time (int): The total time the application has been actively used in seconds.
        kp (int): The number of key presses.
        last_activity_time (float): The time of the last activity (keypress or app swap).
        subtracted_time (int): The time subtracted from the active time to calculate the total active time correctly.
        keypress_time (int): How long the key-presses are tracked (will be reset every ACTIVITY_RESET_TIME seconds)

    Methods:
        reset_times(app=None): Resets the active, opened, total_active, and last_activity time, also resets the key-presses.
        on_keypress(): Called when a key is pressed. Updates the active time and key-presses.
        on_app_swap(app): Called when the app is swapped. Saves and resets the times.
        check_inactivity(): Checks if the user is inactive based on the last activity, uses values like TimeManager.subtracted_time (self.subtracted_time) to calculate correct values for active and total_active time.
        kpm: Returns the current key-presses divided by the active time and multiplied by 60 (to get to minutes).
        reset_kpm: Resets the key-presses (kp) and the keypress-time timer
        timestamp: Returns the current datetime as timestamp in isoformat.
        load_time(opened_time, active_time, total_active_time): Actualizes time values to new values: opened_time, active_time, and total_active_time.
        update(): Called regularly to update the times.
    """

    def __init__(self, tracker):
        """
        Initializes the TimeManager with the provided tracker object,
        and sets base values for most of the classes variables
        """

        self.tracker = tracker

        self.inactive = False  # if is currently inactive
        self.opened_time = 0  # in seconds
        self.active_time = 0  # in seconds
        self.total_active_time = 0  # in seconds
        self.last_activity_time = None  # Time passed since the last activity (keypress or app swap)
        self.subtracted_time = 0  # Used to calculate self.total_active_time correctly
        self.kp = 0  # Key-presses
        self.keypress_time = 0  # Used to calculate Key-presses

    def reset_times(self, app=None):
        """Resets the active, opened, total_active and last_activity time, also resets the key-presses."""
        self.opened_time = 0
        self.active_time = 0
        self.total_active_time = 0
        self.last_activity_time = None

    def on_keypress(self):
        """Called when a key is pressed. Updates the active time and key-presses."""
        self.last_activity_time = time.time()  # Set the current time as the last activity
        self.kp += 1

    def on_app_swap(self, app):
        """Called when the app is swapped. Saves and resets the times. Also resets the KPM."""
        self.reset_times(app)  # Reset the times whenever the app is swapped
        self.reset_kpm()

    def check_inactivity(self):
        """Checks if the user is inactive based on the last activity, if so then sets self.inactive to True,
        also uses values like TimeManager.subtracted_time (self.subtracted_time) to calculate correct values for active and total_active time."""
        if self.last_activity_time is None: return
        # Get Time Values
        current_time = time.time()
        inactive_time = current_time - self.last_activity_time
        # Increment Time
        self.opened_time += 1
        if self.last_activity_time is not None and inactive_time > INACTIVE:
            # If the time since the last activity exceeds the inactivity threshold, the user is considered inactive
            self.inactive = True
            self.active_time = 0  # Reset Active Time, but not total_active_time
            self.total_active_time -= inactive_time - self.subtracted_time
            self.subtracted_time = inactive_time - self.subtracted_time
            self.reset_kpm()
        else:
            self.inactive = False
            self.subtracted_time = 0
            self.active_time += 1  # Otherwise, count 1 second of active time
            self.total_active_time += 1  # Count the total active time, won't be reset if inactive
            if self.keypress_time < ACTIVITY_RESET_TIME:
                self.keypress_time += 1
            else:
                self.reset_kpm()

    @property
    def kpm(self):
        """Returns the current key-presses divided by the active time and multiplied by 60 (to get to minutes)."""
        return int((max(self.kp, 1) / max(self.keypress_time, 1)) * 60)

    def reset_kpm(self):
        """Resets self.kp and self.keypress_time"""
        self.kp = 0
        self.keypress_time = 0

    @property
    def timestamp(self):
        """Returns the current datetime as timestamp in isoformat."""
        return datetime.datetime.now().isoformat()

    def load_time(self, opened_time, active_time, total_active_time):
        """Actualizes time values to new values:
        - opened_time, active_time and total_active_time."""
        self.opened_time = opened_time
        self.active_time = active_time
        self.total_active_time = total_active_time

    def update(self):
        """Called regularly to update the times."""
        self.check_inactivity()
