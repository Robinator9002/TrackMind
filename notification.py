from case import get_cases, tick_delays, BASE_DELAYS


class NotificationManager:
    """
    Manages notifications for the application.

    Attributes:
        tracker (object): The tracker object that provides necessary functionality for the NotificationManager.
        notifications (list): A list of notifications currently being managed.
        data (object): The current data being used to generate notifications.
        delays (dict): A dictionary of delays used to control the frequency of notifications.

    Methods:
        check_data(): Sets the NotificationManager.data (self.data) to the current data, which is being pulled from self.tracker.
        get_notifications(): Uses get_cases from case.py to get all the current notifications, and then returns them.
        at_notification(notification): Removes the notification if it was shown, so it won't be shown again.
        check_notifications(): Actualizes NotificationManager.notifications (self.notifications) if new ones are available.
        update(): Updates and overviews class-values and checks for new notifications.
    """

    def __init__(self, tracker):
        self.tracker = tracker

        self.notifications = []
        self.data = None
        self.delays = {key: value for key, value in BASE_DELAYS.items()}

    def check_data(self):
        """Sets the NotificationManager.data (self.data) to the current data, which is being pulled from self.tracker."""
        self.data = self.tracker.get_current_app_data()

    def get_notifications(self):
        """Uses get_cases from case.py to get all the current notifications, and then returns them.
        Also actualizes NotificationManager.delays (self.delays) to the new value, where individual values will be reset if a notification is being shown.
        Checks if KPM (or activity) where used in the message (e.g. if the message is tracking if the user is distracted, or inactive),
        if so reset the kpm in the TimeManager (self.tracker.time_manager.reset_kpm())."""
        if not self.data:
            return None

        notifications, new_delays = get_cases(self.data, self.delays, self.tracker.time_manager.kpm)
        if new_delays:
            self.delays = new_delays
        for item in self.notifications:
            notifications.append(item)

        return notifications

    def at_notification(self, notification):
        """Just remove the notification if it was shown, so it won't be shown again."""
        self.notifications.remove(notification)

    def check_notifications(self):
        """Actualizes NotificationManager.notifications (self.notifications) if new ones are available."""
        notifications = self.get_notifications()
        if notifications is not None:
            self.notifications = notifications

    def update(self):
        """Updates and Overviews class-values and checks for new notifications.
        Also increments all delays in self.delays by -1."""
        self.check_data()
        self.check_notifications()
        self.tracker.show_notifications()
        self.delays = tick_delays(self.delays)  # Increment by -1
