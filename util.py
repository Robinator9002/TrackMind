"""
The util module contains various useful functions and variables for the application.

Functions:
- format_time(seconds: float) -> str: Format a time in seconds based on the number of seconds.
- remove_values(array, values): Remove all values from an array.
- get_activity_level(kpm): Return the activity level based on the KPM (Key Presses per Minute).
- convert_last_data_to_dict(last_data): Convert tracker last data into a dictionary.
- convert_last_data_to_dataframe(last_data): Convert a data array into a pandas DataFrame.
- get_productivity_by_category(category): Return the productivity level based on the provided app category.
- get_productivity_score_by_category(category): Get the productivity score by category.
- one_hot_encode(df, column): Encode a pd.DataFrame column by mapping its unique_indexes.
- map_activity(activity): Map the activity to a numeric value.
- percentage_of_str_in_other(small, big): Calculate the percentage of the first string that is present in the second string in correct order.

Variables:
- AUTOCLICKER: Threshold for detecting autoclickers.
- VERY_ACTIVE: Threshold for detecting very active users.
- ACTIVE: Threshold for detecting active users.
- MODERATE: Threshold for detecting moderately active users.
- PASSIVE: Threshold for detecting passive users.
- INACTIVE: Threshold for detecting inactive users.
- PRODUCTIVITY_PER_CATEGORY: Dictionary mapping categories to productivity levels.
- SQL_COLUMNS: List of SQL columns for the tracker data.
- SQL_COLUMNS_WITH_ID: List of SQL columns for the tracker data, including the ID column.
- SQL_COLUMNS_WITH_TIMESTAMP: List of SQL columns for the tracker data, including the timestamp column.
"""

import pandas as pd

from settings import *


def format_time(seconds: float) -> str:
    """Format a time in Seconds based on the Number of Seconds, possible formats are:
    - s: Seconds
    - m: Minutes
    - h: Hours
    - d: Days
    - w: Weeks
    - y: Years."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.2f}m"
    elif seconds < 86400:
        return f"{seconds / 3600:.2f}h"
    elif seconds < 604800:
        return f"{seconds / 86400:.2f}d"
    elif seconds < 31536000:
        return f"{seconds / 604800:.2f}w"
    else:
        return f"{seconds / 31536000:.2f}y"


def remove_values(array, values):
    """Removes all values from an array.
    Args:
        array: Array to remove values from.
        values: Values to remove."""
    return [value for value in array if value not in values]


def get_activity_level(kpm):
    """
    Returns the activity level based on the KPM (Key Presses per Minute).
    Args:
        kpm: Key Presses per Minute.
    Returns:
        Activity level as a string."""
    if kpm >= AUTOCLICKER:
        return 'autoclicker'
    elif kpm >= VERY_ACTIVE:
        return 'very_active'
    elif kpm >= ACTIVE:
        return 'active'
    elif kpm >= MODERATE:
        return 'moderate'
    elif kpm >= PASSIVE:
        return 'passive'
    else:
        return 'inactive'


def convert_last_data_to_dict(last_data):
    """Specifically converts tracker_last_data into a dictionary.
    IMPORTANT: Only works with a directly specific format (the one from tracker.last_data). It has to be:
    last_data[0]: id
    last_data[1]: app_name
    last_data[2]: timestamp
    last_data[3]: category
    last_data[4]: activity
    last_data[5]: opened_time
    last_data[6]: active_time
    last_data[7]: total_active_time
    """
    return {"id": last_data[0], "timestamp": last_data[2], "app_name": last_data[1], "category": last_data[3],
            "activity": last_data[4], "opened_time": last_data[5], "active_time": last_data[6],
            "total_active_time": last_data[7]}


def convert_last_data_to_dataframe(last_data):
    """Converts a data array (which has to be a directly specific format) into a pandas DataFrame.
    The util.convert_last_data_to_dict functions is used to convert the data into a dictionary.
    IMPORTANT: Only works with a directly specific format (the one from tracker.last_data). It has to be:
    last_data[0]: id
    last_data[1]: app_name
    last_data[2]: timestamp
    last_data[3]: category
    last_data[4]: activity
    last_data[5]: opened_time
    last_data[6]: active_time
    last_data[7]: total_active_time
    """
    data = []
    for record in last_data:
        data.append(convert_last_data_to_dict(record))
    return pd.DataFrame(data)


PRODUCTIVITY_PER_CATEGORY = {frozenset[('coding', 'developing', 'modeling')]: 'productive',
                             frozenset[('util', 'browser', 'communication')]: 'mediocre productivity',
                             frozenset[('social_media', 'entertainment', 'gaming', 'music')]: 'unproductive',
                             frozenset[('unknown',)]: 'other'}


def get_productivity_by_category(category):
    """
    Returns the productivity level based on the provided app category.
    Therefor uses the PRODUCTIVITY_PER_CATEGORY Dictionary. Includes 'other' for 'unknown' app category.
    """
    return PRODUCTIVITY_PER_CATEGORY.get(category, 'other')


def get_productivity_score_by_category(category):
    """
    Gets the productivity score by category, by mapping the result of util.get_productivity_by_category to numbers.
    Ranges from 0 (unproductive) to 2 (productive), includes -1 for 'unknown' app category.
    Score is:
    - other:                -1
    - unproductive:         0
    - mediocre_productive   1
    - productive            2
    """
    mapping = {'productive': 2, 'mediocre_productive': 1, 'unproductive': 0, 'other': -1}
    productivity = get_productivity_by_category(category)
    return mapping[productivity]


def one_hot_encode(df, column):
    """Encodes a pd.DataFrame column by mapping its unique_indexes."""
    uniques = df[column].unique()
    feature_map = {uniques[i]: i for i in range(len(uniques))}
    df[column] = df[column].map(feature_map)
    return df


def map_activity(activity):
    """Maps the activity to a numeric value:
    - autoclicker:  5
    - very_active:  4
    - active:       3
    - moderate:     2
    - passive:      1
    - inactive:     0"""
    mapping = {'autoclicker': 5, 'very_active': 4, 'active': 3, 'moderate': 2, 'passive': 1, 'inactive': 0}
    return mapping.get(activity, -1)


def percentage_of_str_in_other(small, big):
    """Calculate the percentage of the first string that is present in the second string in correct order."""
    small_idx = 0
    small_len = len(small)

    for char in big:
        if char == small[small_idx]:
            small_idx += 1
        if small_idx == small_len:
            return 1

    return 0
