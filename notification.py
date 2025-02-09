from settings import *


class NotificationManager:
    def __init__(self, manager):
        self.manager = manager

        self.notifications = []
        self.data = None

    def check_data(self):
        self.data = self.manager.get_current_app_data()

    def get_notification(self):
        if not self.data:
            return None
        notification = None

        # Use the helpful function in case.py

        return notification

    def get_last_notification(self):
        return self.notifications[len(self.notifications)-1]

    def check_notifications(self):
        notification = self.get_notification()
        if notification is not None:
            self.notifications.append(notification)
        else:
            return

    def update(self):
        self.check_data()
        self.check_notifications()
        self.manager.print_notifications()
