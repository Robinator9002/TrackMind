from settings import *


def format_time(seconds: float) -> str:
    """Format a time in Seconds as s, m or h based on the Size of the Number."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    elif seconds < 3600:
        return f"{seconds / 60:.2f}m"
    else:
        return f"{seconds / 3600:.2f}h"

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

