"""
The case.py file manages all the cases for notifications, which are mainly used in the notification.py file (in the NotificationManager).
It also contains functions to get notifications and tick the case_times.
The values will be managed in the NotificationManager!

Important Variables:
- BASE_DELAYS: A dictionary containing the base delays for different cases.
- CATEGORY_ACTIVITY_NOTIFICATION: A string representing the notification for category/activity cases.
- CATEGORY_ACTIVITY: A dictionary mapping categories to activity levels.
- ... (other important variables)

Methods:
- tick_delays(delays: dict) -> dict: Just ticks all delays, incrementing them by -1, with a minimum of zero, and then returning them.
- get_cases(data: dict, delays: dict, kpm: int = None) -> List[Tuple[str, str]], dict: Goes through all possible cases, also using delays, and returns new delays and active notifications.
"""

from category import get_categories_by_str
from util import map_activity, format_time, get_productivity_score_by_category

## Delays
BASE_DELAYS = {'min': 120, 'category_activity': 360, 'less_important_category': 600,
               'less_important_category_total': 1800, 'autoclicker': 120, 'over_active_time': 900,
               'over_total_active_time': 3600, }

## Cases (values)
# Category/Activity
CATEGORY_ACTIVITY_NOTIFICATION = "You seem distracted. Try focusing more!"
CATEGORY_ACTIVITY = {frozenset(('coding', 'developing')): 'active',
                     frozenset(('social_media', 'music', 'entertainment', 'unknown')): 'passive',
                     frozenset(('util', 'gaming', 'browser', 'modeling', 'communication')): 'moderate'}
CATEGORY_ACTIVITY_NOTIFICATION_TYPE = 'category_activity'
# Less important Category
LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION = "You are @time@ active in @category@. Probably try something more productive?"
LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION_TYPE = "less_important_category_active_time"
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION = "You are @time@ time active in @category@. Try making something more productive!"
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION_TYPE = "less_important_category_total_active_time"
MIN_PRODUCTIVITY = 1
LESS_IMPORTANT_CATEGORY_ACTIVE_TIME = 3600  # 1h
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME = 10800  # 3h
# Autoclicker
AUTOCLICKER_NOTIFICATION_KPM = "You have @kpm@ KPM. Maybe stop using autoclicker?"
AUTOCLICKER_NOTIFICATION = "You have over 500 KPM. Maybe stop using autoclicker?"
AUTOCLICKER_NOTIFICATION_TYPE = 'autoclicker'
# Active Time
OVER_ACTIVE_NOTIFICATION = "You are now about @time@ active (without break). Maybe try a short break."
OVER_TOTAL_ACTIVE_NOTIFICATION = "Today you were about @time@ active. Maybe stop for today, and do something else."
OVER_ACTIVE_NOTIFICATION_TYPE = 'over_active_time'
OVER_TOTAL_ACTIVE_NOTIFICATION_TYPE = 'over_total_active_time'
OVER_ACTIVE_TIME = 3600  # 1h
OVER_TOTAL_ACTIVE_TIME = 21600  # 6h


## Functions
# Tick Delay
def tick_delays(delays: dict):
    """Just ticks all delays, incrementing them by -1, with a minimum of zero, and then returning them."""
    for key in delays:
        delays[key] = max(0, delays[key] - 1)
    return delays


# Get Cases
def get_cases(data, delays, kpm=None):
    """Goes through all possible cases, also using delays, and returns new delays, active notifications and whether KPM where used for the message."""
    cases, types = [], []
    new_delays = {key: value for key, value in delays.items()}

    if delays['min'] > 0:
        return [], delays
    new_delays['min'] = BASE_DELAYS['min']

    category, activity, opened_time, active_time, total_active_time = data['category'], data['activity'], data[
        'opened_time'], data['active_time'], data['total_active_time']
    activity = map_activity(activity)
    productivity = get_productivity_score_by_category(category)

    opened_time_formated, active_time_formated, total_active_time_formated = format_time(opened_time), format_time(
        active_time), format_time(total_active_time)

    uses_kpm = False

    ### Categories
    for cat in get_categories_by_str(str(category)):
        ## Category/Activity
        for key, value in CATEGORY_ACTIVITY.items():
            if cat in key and activity < map_activity(value) and delays['category_activity'] <= 0:
                cases.append(CATEGORY_ACTIVITY_NOTIFICATION)
                types.append(CATEGORY_ACTIVITY_NOTIFICATION_TYPE)
                new_delays['category_activity'] = BASE_DELAYS['category_activity']
                uses_kpm = True
    ## Less important Category
    # First check if in other category (which will be ignored)
    if not productivity == -1:
        # Less important Category (Active Time)
        if productivity < MIN_PRODUCTIVITY and active_time >= LESS_IMPORTANT_CATEGORY_ACTIVE_TIME and delays[
            'less_important_category'] <= 0:
            notification = LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION.replace('@category@', f'{category}')
            notification = notification.replace('@time@', f'{active_time_formated}')
            cases.append(notification)
            types.append(LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION_TYPE)
            new_delays['less_important_category'] = BASE_DELAYS['less_important_category']

        # Less important Category (Total Active Time)
        if productivity < MIN_PRODUCTIVITY and total_active_time >= LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME and \
                delays['less_important_category_total'] <= 0:
            notification = (
                LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION.replace('@category@', f'{category}').replace('@time@',
                                                                                                               f'{total_active_time_formated}'))
            cases.append(notification)
            types.append(LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION_TYPE)
            new_delays['less_important_category_total'] = BASE_DELAYS['less_important_category_total']
    ### Activity
    if activity >= map_activity('autoclicker') and delays['autoclicker'] <= 0:
        notification = AUTOCLICKER_NOTIFICATION_KPM.replace('@kpm@', f'{kpm}') if kpm else AUTOCLICKER_NOTIFICATION
        cases.append(notification)
        types.append(AUTOCLICKER_NOTIFICATION_TYPE)
        new_delays['autoclicker'] = BASE_DELAYS['autoclicker']
        uses_kpm = True
    ### Active Time
    ## Active Time
    if active_time >= OVER_ACTIVE_TIME and delays['over_active_time'] <= 0:
        notification = OVER_ACTIVE_NOTIFICATION.replace('@time@', f'{active_time_formated}')
        cases.append(notification)
        types.append(OVER_ACTIVE_NOTIFICATION_TYPE)
        new_delays['over_active_time'] = BASE_DELAYS['over_active_time']
    ## Total Active Time
    if total_active_time >= OVER_TOTAL_ACTIVE_TIME and delays['over_total_active_time'] <= 0:
        notification = OVER_TOTAL_ACTIVE_NOTIFICATION.replace('@time@', f'{total_active_time_formated}')
        cases.append(notification)
        types.append(OVER_TOTAL_ACTIVE_NOTIFICATION_TYPE)
        new_delays['over_total_active_time'] = BASE_DELAYS['over_total_active_time']

    notifications = [[cases[i], types[i]] for i in range(len(cases))]
    return notifications, new_delays, uses_kpm
