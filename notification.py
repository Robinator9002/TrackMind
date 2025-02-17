
from case import get_cases, tick_delays, BASE_DELAYS


class NotificationManager:
    def __init__(self, manager):
        self.manager = manager

        self.notifications = [[]]
        self.data = None
        self.delays = {key: value for key, value in BASE_DELAYS.items()}

    def check_data(self):
        self.data = self.manager.get_current_app_data()

    def get_notifications(self):
        if not self.data:
            return None

        notifications, new_delays = get_cases(self.data, self.delays, self.manager.time_manager.kpm)
        if new_delays:
            self.delays = new_delays

        return notifications

    def at_notification(self, notification):
        self.notifications.remove(notification)

    def get_last_notification(self):
        return self.notifications[len(self.notifications)-1]

    def check_notifications(self):
        notifications = self.get_notifications()
        if notifications is not None:
            self.notifications = notifications

    def update(self):
        self.check_data()
        self.check_notifications()
        self.manager.show_notifications()
        tick_delays(self.delays) # Increment by -1
