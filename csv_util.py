"""
The csv_util.py file contains helpful functions for saving specific data into a CSV file.
It is especially designed for notification and tracker data.

Important Methods:
- save_data_to_csv(csv_file: str, last_data: List[Tuple]) -> None: Configures and saves tracker data as a CSV file.
- save_notification_to_csv(csv_file: str, notification: Dict) -> None: Configures and saves notification data as a CSV file.
"""

import csv

from util import convert_last_data_to_dict


def save_data_to_csv(csv_file, last_data):
    """Configures and Saves Tracker Data as CSV file."""
    if not last_data:
        return

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "timestamp", "app_name", "category", "activity", "opened_time",
                                                  "active_time", "total_active_time"])

        if file.tell() == 0:
            writer.writeheader()

        for data in last_data:
            writer.writerow(convert_last_data_to_dict(data))


def save_notification_to_csv(csv_file, notification):
    """Configures and Saves Notification Data as CSV file."""
    if not notification:
        return

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "timestamp", "app_name", "category", "activity", "opened_time",
                                                  "active_time", "total_active_time", "timestamp", "notification_text",
                                                  "notification_type", "like"])

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(notification)
