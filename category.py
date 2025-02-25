"""
The category.py file contains a list of important apps and their equivalent categories.
It also includes helpful functions for getting those app categories through the app name, and also getting multiple categories.

Important Variables:
- categories: A dictionary mapping app names (lowercase) to their corresponding categories.

Important Methods:
- get_app_category(app_name: str) -> str: Gets all categories this app (lowercase) belongs to and adds them via string.
- get_categories_by_str(category_str: str) -> List[str]: Just splits the categories and returns all of them as a list.
"""

from util import percentage_of_str_in_other


# Util Function
def get_app_category(app_name):
    """Gets all categories this app (lowercase) belongs to and adds them via string.
    Makes sure there are no duplicates."""
    app_name = app_name.lower()
    app_cat = []
    for app in categories.keys():
        if app == app_name:  # This should only happen once
            app_cat = [categories[app]]
            break
        # This could happen multiple times
        if percentage_of_str_in_other(app, app_name) and not categories[app] in app_cat:
            app_cat.append(categories[app])

    return "/".join(app_cat) if app_cat else "unknown"


def get_categories_by_str(category_str):
    """Just splits the categories and returns all of them as array."""
    return category_str.split('/')


# Categories
categories = {'pycharm': 'coding', 'github': 'developing/coding/util', 'firefox': 'browser', 'chrome': 'browser',
              'sublime_text': 'coding', 'vscode': 'coding', 'chatgpt': 'util/developing',
              'discord': 'social_media/communication', 'cmd': 'util/developing', 'task': 'util', 'vivaldi': 'browser',
              'opera': 'browser', 'beebeep': 'social_media', 'photos': 'util', 'explorer': 'util',
              'notepad': 'util/coding', 'mediaplayer': 'music', 'comfy': 'entertainment', 'music': 'music',
              'teams': 'communication', 'word': 'util', 'excel': 'util', 'onenote': 'util', 'powerpoint': 'util',
              'searchapp': 'util', 'unreal': 'developing/coding', 'unity': 'developing/coding',
              'blender': 'developing/modeling', 'godot': 'developing/coding', 'steam': 'gaming/util',
              'epic_games': 'gaming/util', 'gog': 'gaming/util', 'battle_net': 'gaming/util', 'minecraft': 'gaming',
              'csgo': 'gaming', 'valorant': 'gaming', 'league': 'gaming', 'dota': 'gaming', 'skyrim': 'gaming',
              'cyberpunk': 'gaming', 'elden_ring': 'gaming', 'tetris': 'gaming', 'civilization': 'gaming',
              'factorio': 'gaming', 'sims': 'gaming', 'stardew': 'gaming', 'ck3': 'gaming', 'crusader kings': 'gaming',
              'red_dead_redemption': 'gaming', 'ubisoft': 'gaming/util', 'destiny': 'gaming', 'fortnite': 'gaming',
              'resident_evil': 'gaming', 'world_of_warcraft': 'gaming', 'hearthstone': 'gaming', 'overwatch': 'gaming',
              'rainbow_six_siege': 'gaming', 'warhammer': 'gaming', 'battlefield': 'gaming', 'apex': 'gaming',
              'code': 'coding/developing', 'launcher': 'util', 'game': 'gaming', 'app': 'util',
              'dev': 'coding/developing', 'engine': 'developing'}
