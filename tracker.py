import datetime
import threading

from PIL import Image
from pystray import Icon as TrayIcon, Menu as TrayMenu, MenuItem as TrayMenuItem

from category import get_app_category
from csv_util import save_data_to_csv, save_notification_to_csv
from data_analysis import PlotManager
from menu_settings import *
from notification import NotificationManager
from settings import *
from timemanager import TimeManager
from util import get_activity_level
from winmanager import WinManager


class Tracker:
    """
    The main tracker class that manages the application's data, time, notifications, and plots.

    Attributes:
        app: The main application class, which provides necessary methods and attributes.
        win_manager: An instance of WinManager, responsible for managing window-related operations.
        time_manager: An instance of TimeManager, responsible for managing time-related operations.
        notification_manager: An instance of NotificationManager, responsible for managing notifications.
        plot_manager: An instance of PlotManager, responsible for managing data plots.
        auto_save_time: An integer representing the time interval for auto-saving data to SQL.
        csv_save_time: An integer representing the time interval for saving data to CSV.
        date_check_rate: An integer representing the time interval for checking the date.
        last_app: A string representing the name of the last active application.
        last_data: A list representing the data of the last active application.
        reset: A boolean indicating whether the application should be reset.

    Methods:
        init_values(): Initializes most of the values of the Tracker class.
        check_latest_data(): Updates self.last_data by setting it to self.load_all().
        check_keyboard(): Creates a loop where check_keypress is executed permanently.
        check_app(): Checks if the app has changed or isn't set, and if so it updates and clears the current time_manager values.
        check_autosave(): Manages the auto_save and csv_save times, saves them if the timers are finished (and resets the timers).
        check_date(): Manages the date_check_timer, if reached zero then loads the new date.
        apply_time(): Loads the current time from SQL and then gives it to self.time_manager.
        start(): Starts all important threads and then runs the TKManager, which calls root.mainloop.
        create_tray_icon(): Creates the tray icon using pystray, using the MENU_ICON as icon.
        show_notifications(): Gets the notifications from notification_manager and if there are any then show them via tk_manager and update notification_manager so it can remove the notification (so it will only be called once).
        update(): Checks and updates values, and updates other child classes (time_manager and notification_manager).
        check_reset(): Checks if self.reset is true, and if it is then save all data and then reset the SQL Table and current values.
        check_quitting(): Checks if the app is currently quitting, then call handle_exit().
        get_current_app_data(): Loads, Configures and then returns the SQL data for the current (opened) app.
        load_time(): Loads the current app data via self.get_current_app_data, then returns only the time_values.
        load_all(): Loads all values from SQL, then creates a list of all elements from the SQL Stats and returns it.
        save_all(): Saves the current app values for the chosen app, defaults to self.last_app (the currently opened one).
        save_data_csv(): Saves self.last_data via a csv_util function as CSV File.
        save_notification_csv(): Saves a notification with the given detail via a csv_util function as CSV File.
        on_notification_qualified(): Saves a notification with like information, calling self.save_notification_csv.
    """
    def __init__(self, app):
        """
        Initializes the Tracker class.

        Sets up the necessary child classes, such as WinManager, TimeManager, NotificationManager, PlotManager,
        and initializes the values required for the Tracker to function properly.

        :param app: The main application class, which provides necessary methods and attributes.
        """
        self.app = app

        self.win_manager = WinManager(self)
        self.time_manager = TimeManager(self)
        self.notification_manager = NotificationManager(self)
        self.plot_manager = PlotManager(self)

        self.init_values()

    def init_values(self):
        """Intializes most of the values of the Tracker() class, should be called in __init__ or at complete reset."""
        self.auto_save_time = SQL_SAVE_RATE
        self.csv_save_time = CSV_SAVE_RATE
        self.date_check_rate = DATE_CHECK_RATE
        self.last_app = None
        self.last_data = None
        self.reset = False

    def check_latest_data(self):
        """Actualizes self.last_data by setting it to self.load_all()."""
        self.last_data = self.load_all()

    def check_keyboard(self):
        """Creates a loop where check_keypress is executed permanently.
        IMPORTANT: This should be executed in a separate thread!"""
        while True:
            self.win_manager.check_keypress()

    def check_app(self):
        """Checks if the app has changed or isn't set, and if so it actualizes, and clears the current time_manager values.
        Then loads values for the new app and gives them to self.time_manager.
        This should be called every frame!"""
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

    def check_autosave(self):
        """Manages the auto_save and csv_save times, saves them if the timers are finished (and resets the timers).
        If it saves to CSV it also resets SQL, to prevent double saving.
        This should be called every frame!"""
        self.auto_save_time -= 1
        self.csv_save_time -= 1
        if self.auto_save_time <= 0:
            self.save_all()
            self.auto_save_time = SQL_SAVE_RATE
        if self.csv_save_time <= 0:
            self.reset = True  # Will automatically Save everything
            self.csv_save_time = CSV_SAVE_RATE

    def check_date(self):
        """Manages the date_check_timer, if reached zero then loads the new date.
        This should be called every frame!"""
        self.date_check_rate -= 1
        if self.date_check_rate <= 0 and self.last_data:
            current_date = datetime.datetime.now().date()
            saved_dates = [datetime.datetime.fromisoformat(self.last_data[i][2]).date() for i in
                           range(len(self.last_data))]

            last_saved_date = max(saved_dates)

            if not (last_saved_date == current_date):
                self.reset = True

            self.date_check_rate = DATE_CHECK_RATE

    def apply_time(self):
        """Loads the current time from SQL and then gives it to self.time_manager."""
        opened_time, active_time, total_active_time = self.load_time()
        self.time_manager.load_time(opened_time, active_time, total_active_time)

    def start(self):
        """Starts all important threads and then runs the TKManager, which calls root.mainloop.
        The started threads are:
        - key_thread: managing key input, directly working with self.win_manager
        - pystray_thread: managing the tray icon and menu"""
        # Threads
        self.key_thread = threading.Thread(target=self.check_keyboard, daemon=True)
        self.pystray_thread = self.create_tray_icon()

        # Start
        self.key_thread.start()
        self.pystray_thread.start()
        self.app.tk_manager.run()

    def create_tray_icon(self):
        """Create the tray icon using pystray, using the MENU_ICON as icon."""
        # Create a simple icon using Pillow (a red square with a green inner square)
        full_image_path = os.path.join(self.app.autostart_manager.current_abs_path[0], MENU_ICON_PATH)
        image = Image.open(full_image_path)

        # Improvisation Function
        def set_quitting():
            self.app.quiting = True

        # Define the tray menu
        menu = TrayMenu(TrayMenuItem("Show App", self.app.tk_manager.bring_to_foreground),
                        TrayMenuItem("Minimize App", self.app.tk_manager.send_to_background),
                        TrayMenuItem("Quit", set_quitting))

        self.tray_icon = TrayIcon(MENU_TITLE, image, MENU_TITLE, menu)

        # Start the tray icon in its own thread so the Tkinter mainloop is not blocked
        return threading.Thread(target=self.tray_icon.run, daemon=True)

    def show_notifications(self):
        """Gets the notifications from notification_manager and if there are any then show them via tk_manager and
        update notification_manager so it can remove the notification (so it will only be called once)."""
        notifications = self.notification_manager.notifications
        if len(notifications) >= 1:
            self.app.tk_manager.show_notification(notifications[0])
            self.notification_manager.at_notification(notifications[0])

    def update(self):
        """Checks and updates values, and updates other child classes (time_manager and notification_manager).
        This should be called exactly every second, otherwise some functions and tracking wont work!"""
        self.check_reset()
        self.check_app()
        self.check_autosave()
        self.check_latest_data()
        self.check_date()
        self.check_quitting()
        self.time_manager.update()
        self.notification_manager.update()

    def check_reset(self):
        """Checks if self.reset ist true, and if it is then save all data and then reset the SQL Table and current values."""
        if self.reset:
            self.app.loader.clear_table()
            self.time_manager.reset_times()
            self.save_data_csv()
            self.save_all()

            self.reset = False

    def check_quitting(self):
        """Checks if the app is currently quitting, then call handle_exit(). This should be called every frame in the mainthread,
        so the tkinter and sql-classes can be closed even from another thread.
        IMPORTANT: Always quit via this Method!"""
        if self.app.quiting:
            self.app.handle_exit(None, None)

    def get_current_app_data(self):
        """Loads, Configures and then returns the SQL data for the current (opened) app."""
        column = self.app.loader.load_column('app_name', self.last_app)
        if not column:
            return None
        data = {'id': column[0], 'app_name': column[1], 'timestamp': column[2], 'category': column[3],
                'activity': column[4], 'opened_time': column[5], 'active_time': column[6],
                'total_active_time': column[7]}
        return data

    def load_time(self):
        """Loads the current app data via self.get_current_app_data, then returns only the time_values.
        Those are: opened_time, active_time and total_active_time"""
        current_app_data = self.get_current_app_data()
        if not current_app_data:
            return 0, 0, 0

        values = ['opened_time', 'active_time', 'total_active_time']
        opened_time, active_time, total_active_time = [current_app_data[value] for value in values]
        return opened_time, active_time, total_active_time

    def load_all(self):
        """Loads all values from SQL, then creates a list of all elements from the SQL Stats and returns it."""
        stats = self.app.loader.load_all_stats()
        if stats is None: return None

        reorganized_stats = []
        for i in range(len(stats)):
            reorganized_stats.append(stats[i])

        return reorganized_stats

    def save_all(self, app=None):
        """Saves the current app values for the chosen app, defaults to self.last_app (the currently opened one)."""
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

    def save_data_csv(self):
        """Saves self.last_data via a csv_util function as CSV File."""
        data = self.last_data
        abs_notification_path = os.path.join(self.app.autostart_manager.current_abs_path[0], TRACKER_CSV_PATH)
        save_data_to_csv(abs_notification_path, data)

    def save_notification_csv(self, not_text, not_type, like):
        """Saves a notification with the given detail via a csv_util function as CSV File."""
        current_data = next((data for data in self.last_data if data[1] == self.last_app), None)
        if not current_data:
            return
        data = {"id": current_data[0], "timestamp": current_data[2], "app_name": current_data[1],
                "category": current_data[3], "activity": current_data[4], "opened_time": current_data[5],
                "active_time": current_data[6], "total_active_time": current_data[7],
                'notification_text': f"'{not_text}'", 'notification_type': f"'{not_type}'", 'like': like}
        abs_notification_path = os.path.join(self.app.autostart_manager.current_abs_path[0], NOTIFICATION_CSV_PATH)
        save_notification_to_csv(abs_notification_path, data)

    def on_notification_qualified(self, notification, like):
        """Saves a notification with like information, calling self.save_notification_csv."""
        self.save_notification_csv(notification[0], notification[1], like)
