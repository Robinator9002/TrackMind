from util import map_activity

## Cases (values)
# Category/Activity
CATEGORY_ACTIVITY_MESSAGE = "You seem distracted. Try focusing more!"
CATEGORY_ACTIVITY_MIN_TIME = 60  # Only check after n seconds
category_activity = {['coding', 'developing', 'gaming']: 'active',
    ['social_media', 'music', 'entertainment']: 'passive', ['util', 'browser', 'modeling', 'communication']: 'moderate'}
# Less important Category
LESS_IMPORTANT_CATEGORY_ACTIVE_MESSAGE = "You are @time@ active in @category@. Probably try something more productive?"
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_MESSAGE = "You are @time@ time active in @category@. Try making something more productive!"
LESS_IMPORTANT_CATEGORY = ['social_media', 'browser', 'communication', 'gaming']
LESS_IMPORTANT_CATEGORY_ACTIVE_TIME = 3600  # 1h
LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME = 10800  # 3h


# Function
def get_cases(data):
    cases = []

    category, activity, opened_time, active_time, total_active_time = data['category'], data['activity'], data[
        'opened_time'], data['active_time'], data['total_active_time']
    activity = map_activity(activity)

    ### Categories
    for cat in str(category).split('/'):
        ## Category/Activity
        for key, value in category_activity.items():
            if cat in key and activity >= map_activity(value) and active_time >= CATEGORY_ACTIVITY_MIN_TIME:
                cases.append(CATEGORY_ACTIVITY_MESSAGE)
        ## Less important Category
        # Less important Category (Active Time)
        if cat in LESS_IMPORTANT_CATEGORY and active_time >= LESS_IMPORTANT_CATEGORY_ACTIVE_TIME:
            message = str(LESS_IMPORTANT_CATEGORY_ACTIVE_TIME).replace('@category@', f'{category}').replace('@time@',
                                                                                                            f'{active_time}')
            cases.append(message)
        # Less important Category (Total Active Time)
        if cat in LESS_IMPORTANT_CATEGORY and total_active_time >= LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME:
            message = str(LESS_IMPORTANT_CATEGORY_TOTAL_ACTIVE_TIME).replace('@category@', f'{category}').replace(
                '@time@', f'{total_active_time}')
            cases.append(message)

    return None
