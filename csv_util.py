import csv


def save_data_to_csv(csv_file, last_data):
    if not last_data:
        return

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "timestamp", "app_name", "category", "activity", "opened_time",
                                                  "active_time", "total_active_time"])

        if file.tell() == 0:
            writer.writeheader()

        for data in last_data:
            writer.writerow(
                {"id": data[0], "timestamp": data[2], "app_name": data[1], "category": data[3], "activity": data[4],
                 "opened_time": data[5], "active_time": data[6], "total_active_time": data[7]})


def save_notification_to_csv(csv_file, notification):
    if not notification:
        return

    with open(csv_file, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["id", "timestamp", "app_name", "category", "activity", "opened_time",
                                                  "active_time", "total_active_time", "timestamp", "notification_text",
                                                  "notification_type", "like"])

        if file.tell() == 0:
            writer.writeheader()

        writer.writerow(notification)
