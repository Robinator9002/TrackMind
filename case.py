from util import map_activity, format_time

# ## Delays
# BASE_DELAYS = {'min': 120, 'category_activity': 180, 'less_important_category': 600,
#                'less_important_category_total': 1800, 'autoclicker': 120, 'over_active_time': 900,
#                'over_total_active_time': 3600, }
#
# ## Cases (values)
# # Category/Activity
# CATEGORY_ACTIVITY_NOTIFICATION = "You seem distracted. Try focusing more!"
# CATEGORY_ACTIVITY = {frozenset[('coding', 'developing', 'gaming')]: 'active',
#                      frozenset[('social_media', 'music', 'entertainment')]: 'passive',
#                      frozenset[('util', 'browser', 'modeling', 'communication')]: 'moderate'}
# CATEGORY_ACTIVITY_NOTIFICATION_TYPE = 'category_activity'
# # Less important Category
# LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION = "You are @time@ active in @category@. Probably try something more productive?"
# LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION_TYPE = "less_important_category_active_time"
# LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION = "You are @time@ time active in @category@. Try making something more productive!"
# LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION_TYPE = "less_important_category_total_active_time"
# LESS_IMPORTANT_CATEGORY = ['social_media', 'browser', 'communication', 'gaming']
# LESS_IMPORTANT_CATEGORY_ACTIVE_TIME = 3600  # 1h
# LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME = 10800  # 3h
# # Autoclicker
# AUTOCLICKER_NOTIFICATION_KPM = "You have @kpm@ KPM. Maybe stop using autoclicker?"
# AUTOCLICKER_NOTIFICATION = "You have over 500 KPM. Maybe stop using autoclicker?"
# AUTOCLICKER_NOTIFICATION_TYPE = 'autoclicker'
# # Active Time
# OVER_ACTIVE_NOTIFICATION = "You are now about @time@ active (without break). Maybe try a short break."
# OVER_TOTAL_ACTIVE_NOTIFICATION = "Today you were about @time@ active. Maybe stop for today, and make a workout."
# OVER_ACTIVE_NOTIFICATION_TYPE = 'over_active_time'
# OVER_TOTAL_ACTIVE_NOTIFICATION_TYPE = 'over_total_active_time'
# OVER_ACTIVE_TIME = 3600  # 1h
# OVER_TOTAL_ACTIVE_TIME = 21600  # 6h

# Delays
BASE_DELAYS = {'min': 12, 'category_activity': 18, 'less_important_category': 60,
               'less_important_category_total': 18, 'autoclicker': 12, 'over_active_time': 7,
               'over_total_active_time': 35, }

## Cases (values)
# Category/Activity
CATEGORY_ACTIVITY_NOTIFICATION = "You seem distracted. Try focusing more!"
CATEGORY_ACTIVITY = {frozenset[('coding', 'developing', 'gaming')]: 'active',
                     frozenset[('social_media', 'music', 'entertainment', 'unknown')]: 'passive',
                     frozenset[('util', 'browser', 'modeling', 'communication')]: 'moderate'}
CATEGORY_ACTIVITY_NOTIFICATION_TYPE = 'category_activity'
# Less important Category
LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION = "You are @time@ active in @category@. Probably try something more productive?"
LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION_TYPE = "less_important_category_active_time"
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION = "You are @time@ active in @category@. Try making something more productive!"
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION_TYPE = "less_important_category_total_active_time"
LESS_IMPORTANT_CATEGORY = ['social_media', 'browser', 'communication', 'gaming']
LESS_IMPORTANT_CATEGORY_ACTIVE_TIME = 36  # 1h
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME = 108  # 3h
# Autoclicker
AUTOCLICKER_NOTIFICATION_KPM = "You have @kpm@ KPM. Maybe stop using autoclicker?"
AUTOCLICKER_NOTIFICATION = "You have over 500 KPM. Maybe stop using autoclicker?"
AUTOCLICKER_NOTIFICATION_TYPE = 'autoclicker'
# Active Time
OVER_ACTIVE_NOTIFICATION = "You are now about @time@ active (without break). Maybe try a short break."
OVER_TOTAL_ACTIVE_NOTIFICATION = "Today you were about @time@ active. Maybe stop for today, and make a workout."
OVER_ACTIVE_NOTIFICATION_TYPE = 'over_active_time'
OVER_TOTAL_ACTIVE_NOTIFICATION_TYPE = 'over_total_active_time'
OVER_ACTIVE_TIME = 10  # 1h
OVER_TOTAL_ACTIVE_TIME = 216  # 6h


## Functions
# Tick Delay
def tick_delays(delays: dict):
    for key in delays:
        delays[key] = max(0, delays[key] - 1)


# Get Cases
def get_cases(data, delays, kpm=None):
    cases, types = [], []
    new_delays = {key: value for key, value in delays.items()}

    if delays['min'] > 0:
        return [], delays
    new_delays['min'] = BASE_DELAYS['min']

    category, activity, opened_time, active_time, total_active_time = data['category'], data['activity'], data[
        'opened_time'], data['active_time'], data['total_active_time']
    activity = map_activity(activity)

    opened_time_formated, active_time_formated, total_active_time_formated = format_time(opened_time), format_time(active_time), format_time(total_active_time)

    ### Categories
    for cat in str(category).split('/'):
        ## Category/Activity
        for key, value in CATEGORY_ACTIVITY.items():
            if cat in key and activity >= map_activity(value) and delays['category_activity'] <= 0:
                cases.append(CATEGORY_ACTIVITY_NOTIFICATION)
                types.append(CATEGORY_ACTIVITY_NOTIFICATION_TYPE)
                new_delays['category_activity'] = BASE_DELAYS['category_activity']
        ## Less important Category
        # Less important Category (Active Time)
        if cat in LESS_IMPORTANT_CATEGORY and active_time >= LESS_IMPORTANT_CATEGORY_ACTIVE_TIME and delays[
            'less_important_category'] <= 0:
            notification = LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION.replace('@category@', f'{category}')
            notification = notification.replace('@time@', f'{active_time_formated}')
            cases.append(notification)
            types.append(LESS_IMPORTANT_CATEGORY_ACTIVE_NOTIFICATION_TYPE)
            new_delays['less_important_category'] = BASE_DELAYS['less_important_category']

        # Less important Category (Total Active Time)
        if cat in LESS_IMPORTANT_CATEGORY and total_active_time >= LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME and delays[
            'less_important_category_total'] <= 0:
            notification = (LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION.replace('@category@', f'{category}').replace(
                '@time@', f'{total_active_time_formated}'))
            cases.append(notification)
            types.append(LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_NOTIFICATION_TYPE)
            new_delays['less_important_category_total'] = BASE_DELAYS['less_important_category_total']
    ### Activity
    if activity >= map_activity('autoclicker') and delays['autoclicker'] <= 0:
        notification = AUTOCLICKER_NOTIFICATION_KPM.replace('@kpm@', f'{kpm}') if kpm else AUTOCLICKER_NOTIFICATION
        cases.append(notification)
        types.append(AUTOCLICKER_NOTIFICATION_TYPE)
        new_delays['autoclicker'] = BASE_DELAYS['autoclicker']
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
    return notifications, new_delays
