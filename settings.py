"""
The settings module contains various settings for the application.

Variables:
- ACTUALIZE_RATE: Rate at which the tracking should be performed (in seconds).
- SQL_SAVE_RATE: Rate at which the tracker data should be saved to the SQL database (in minutes).
- CSV_SAVE_RATE: Rate at which the tracker data should be saved to the CSV file (in minutes).
- DATE_CHECK_RATE: Rate at which the current date should be checked (in seconds). It has to be at least 2 seconds shorter than the save rate, else it will not work properly.
- AUTOCLICKER: Threshold for detecting autoclickers (in KPM).
- VERY_ACTIVE: Threshold for detecting very active users (in KPM).
- ACTIVE: Threshold for detecting active users (in KPM).
- MODERATE: Threshold for detecting moderately active users (in KPM).
- PASSIVE: Threshold for detecting passive users (in KPM).
- INACTIVE: Threshold for detecting inactive users (in seconds).
- ACTIVITY_RESET_TIME: How often the KPM are reset (in seconds).
- DATA_ROOT: Root directory for storing data.
- AUTOSTART_METHOD: Method for autostarting the application ('registry' or 'other').
- AUTOSTART_REGISTRY_NAME: Name for the autostart registry entry.
- TRACKER_CSV_FILE: Name for the tracker CSV file.
- NOTIFICATION_CSV_FILE: Name for the notifications CSV file.
- TRACKER_CSV_PATH: Path for the tracker CSV file.
- NOTIFICATION_CSV_PATH: Path for the notifications CSV file.
- SQL_FILE: Name for the SQL database file.
- SQL_PATH: Path for the SQL database file.
- DEFAULT_TABLE_NAME: Default name for the SQL table.
- TABLE_COLUMNS: Dictionary containing the columns for the SQL table.
"""

import os

# Tracker
ACTUALIZE_RATE = 1
SQL_SAVE_RATE = 15
CSV_SAVE_RATE = 60
DATE_CHECK_RATE = 1  # Has to be at least 2 seconds shorter than SAVE_RATE, else it will not work properly!

# Activity Thresholds
AUTOCLICKER = 500  # KPM
VERY_ACTIVE = 60  # KPM
ACTIVE = 30  # KPM
MODERATE = 15  # KPM
PASSIVE = 5  # KPM
INACTIVE = 300  # seconds
ACTIVITY_RESET_TIME = 120 # seconds

### Data
DATA_ROOT = "data"
## Autostart
AUTOSTART_METHOD = 'registry'
AUTOSTART_REGISTRY_NAME = "TrackMind"
## Csv
TRACKER_CSV_FILE = "tracker.csv"
NOTIFICATION_CSV_FILE = "notifications.csv"
TRACKER_CSV_PATH = os.path.join(DATA_ROOT, TRACKER_CSV_FILE)
NOTIFICATION_CSV_PATH = os.path.join(DATA_ROOT, NOTIFICATION_CSV_FILE)
## Sql
# Path
SQL_FILE = "app_usage"
SQL_PATH = os.path.join(DATA_ROOT, SQL_FILE)
# Table
DEFAULT_TABLE_NAME = "tracker_table"
TABLE_COLUMNS = {"id": "INTEGER PRIMARY KEY AUTOINCREMENT", "app_name": "TEXT NOT NULL",
                 "timestamp": "INTEGER DEFAULT 0", "category": "TEXT NOT NULL", "activity": "TEXT NOT NULL",
                 "opened_time": "INTEGER DEFAULT 0", "active_time": "INTEGER DEFAULT 0",
                 "total_active_time": "INTEGER DEFAULT 0"}
