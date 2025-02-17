from settings import *


def format_time(seconds: float) -> str:
    """Format a time in Seconds as s, m or h based on the Size of the Number."""
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

def get_activity_level(kpm):
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


PRODUCTIVITY_PER_CATEGORY = {frozenset[('coding', 'developing', 'modeling')]: 'productive',
                             frozenset[('util', 'browser', 'communication')]: 'mediocre productivity',
                             frozenset[('social_media', 'entertainment', 'gaming', 'music')]: 'unproductive',
                             frozenset[('unknown',)]: 'other'}
def get_productivity_by_category(category):
    return PRODUCTIVITY_PER_CATEGORY.get(category, 'other')

def map_activity(activity):
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

