import os

# Tracker
ACTUALIZE_RATE = 1
SAVE_RATE = 15
DATE_CHECK_RATE = 1 # Has to be at least 2 seconds shorter than SAVE_RATE, else it will not work properly!

# Activity Thresholds
AUTOCLICKER = 500  # KPM
VERY_ACTIVE = 150  # KPM
ACTIVE = 80  # KPM
MODERATE = 30  # KPM
PASSIVE = 5  # KPM
INACTIVE = 300  # seconds

### Data
DATA_ROOT = "data"
## Csv
TRACKER_CSV_FILE = "tracker.csv"
MESSAGE_CSV_FILE = "messages.csv"
TRACKER_CSV_PATH = os.path.join(DATA_ROOT, TRACKER_CSV_FILE)
MESSAGE_CSV_PATH = os.path.join(DATA_ROOT, MESSAGE_CSV_FILE)
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
