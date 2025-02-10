import datetime
import threading
import time

from category import get_app_category
from settings import *
from timemanager import TimeManager
from util import get_activity_level
from winmanager import WinManager
from csv_util import save_to_csv
from notification import NotificationManager


class Tracker:
    def __init__(self, app):
        self.app = app

        self.win_manager = WinManager(self)
        self.time_manager = TimeManager(self)
        self.notification_manager = NotificationManager(self)

        self.init_values()

    def init_values(self):
        self.auto_save_time = SAVE_RATE
        self.date_check_rate = DATE_CHECK_RATE
        self.last_app = None
        self.last_data = None
        self.reset = False

    def check_latest_data(self):
        self.last_data = self.load_all()

    def check_keyboard(self):
        while True:
            if self.app.quiting:
                break

            self.win_manager.check_keypress()

    def check_app(self):
        app = self.win_manager.active_app
        if self.last_app is None and app:
            last_app = self.last_app
            self.last_app = app
            self.apply_time()
            self.time_manager.on_app_swap(last_app)
            self.apply_time()
        if app and self.last_app != app:
            last_app = self.last_app
            self.last_app = app
            self.time_manager.on_app_swap(last_app)

            self.apply_time()

    def check_auto_save(self):
        self.auto_save_time -= 1
        if self.auto_save_time == 0:
            self.save_all()
            self.auto_save_time = SAVE_RATE

    def check_date(self):
        self.date_check_rate -= 1
        if self.date_check_rate <= 0 and self.last_data:
            current_date = datetime.datetime.now().date()
            saved_dates = [datetime.datetime.fromisoformat(self.last_data[i][2]).date() for i in range(len(self.last_data))]

            last_saved_date = max(saved_dates)

            if not (last_saved_date == current_date):
                self.reset = True

            self.date_check_rate = DATE_CHECK_RATE

    def apply_time(self):
        opened_time, active_time, total_active_time = self.load()
        self.time_manager.load_time(opened_time, active_time, total_active_time)

    def start(self):
        # Threads
        key_thread = threading.Thread(target=self.check_keyboard, daemon=True)
        console_thread = threading.Thread(target=self.run_console)

        # Start
        key_thread.start()
        console_thread.start()
        self.run()

    def print_menu(self):
        print("=" * 80)
        print("=" * 37, "Menu", "=" * 37)
        print("=" * 80)
        print("print: Print out all the Data")
        print("menu: Print the Menu again")
        print("reset: tracking")
        print("quit: Close the App")
        print("=" * 80)
        print()

    def print_items(self):
        print(self.last_data)

    def print_notifications(self):
        for notification in self.notification_manager.notifications:
            print(notification)
            print()
            self.notification_manager.notifications.remove(notification)

    def run_console(self):
        self.print_menu()
        while True:
            if self.app.quiting:
                break

            i = input("Choice: ")
            print()
            if i == "print":
                self.print_items()
            elif i == "menu":
                self.print_menu()
            elif i == "reset":
                self.reset = True
            elif i == "quit":
                print("Collecting Data...")
                self.app.quiting = True
            else:
                print("Invalid Choice!")
                print()
                continue

    def run(self):
        while True:
            if self.app.quiting:
                break
            self.update()
            time.sleep(ACTUALIZE_RATE)

    def update(self):
        self.check_reset()
        self.check_app()
        self.check_auto_save()
        self.check_latest_data()
        self.check_date()
        self.time_manager.update()
        self.notification_manager.update()

    def check_reset(self):
        if self.reset:
            self.app.loader.clear_table()
            self.time_manager.reset_times()
            self.save_csv()
            self.save_all()

            self.reset = False

    def get_current_app_data(self):
        column = self.app.loader.load_column('app_name', self.last_app)
        data = {
            'id': column[0],
            'app_name': column[1],
            'timestamp': column[2],
            'category': column[3],
            'activity': column[4],
            'opened_time': column[5],
            'active_time': column[6],
            'total_active_time': column[7]
        }
        return data

    def load(self):
        current_app_data = self.get_current_app_data()
        if not current_app_data:
            return 0,0,0

        values = ['opened_time', 'active_time', 'total_active_time']
        opened_time, active_time, total_active_time = [current_app_data[value] for value in values]
        return opened_time, active_time, total_active_time

    def load_all(self):
        stats = self.app.loader.load_all_stats()
        if stats is None: return None

        reorganized_stats = []
        for i in range(len(stats)):
            reorganized_stats.append(stats[i])

        return reorganized_stats

    def save_all(self, app=None):
        to_save = app if app else self.last_app
        if not to_save:
            return

        timestamp = self.time_manager.timestamp
        opened_time, active_time, total_active_time = self.time_manager.opened_time, self.time_manager.active_time, self.time_manager.total_active_time
        category = get_app_category(to_save)
        activity = get_activity_level(self.time_manager.kpm)

        stats = {'app_name': to_save, 'timestamp': timestamp, 'category': category, 'activity': activity,
                 'opened_time': opened_time, 'active_time': active_time, 'total_active_time': total_active_time}
        self.app.loader.save_column('app_name', to_save, stats)

    def save_csv(self):
        data = self.last_data
        save_to_csv(TRACKER_CSV_PATH, data)

    def on_keypress(self):
        self.time_manager.on_keypress()

    def quit(self):
        self.save_all()
