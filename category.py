from util import percentage_of_str_in_other


def get_app_category(app_name):
    app_cat = []
    for app in categories.keys():
        if app == app_name:
            app_cat = [categories[app]]
            break
        if percentage_of_str_in_other(app, app_name):
            app_cat.append(app)

    app_cat = [categories[app] for app in app_cat if categories[app] not in app_cat]

    return "/".join(app_cat) if app_cat else "unknown"


categories = {'pycharm': 'coding', 'firefox': 'browser', 'chrome': 'browser', 'sublime_text': 'coding',
              'vscode': 'coding', 'chatgpt': 'util/developing', 'discord': 'social_media/communication',
              'cmd': 'util/developing', 'task': 'util', 'vivaldi': 'browser', 'opera': 'browser',
              'beebeep': 'social_media', 'photos': 'util', 'explorer': 'util', 'notepad': 'util/coding',
              'mediaplayer': 'music', 'comfy': 'entertainment/creative', 'music': 'music', 'teams': 'communication',
              'word': 'util', 'excel': 'util', 'onenote': 'util', 'powerpoint': 'util', 'searchapp': 'util', 'unreal': 'developing/coding',
              'unity': 'developing/coding', 'blender': 'developing/modeling', 'godot': 'developing/coding',
              'steam': 'gaming/util', 'epic_games': 'gaming/util', 'gog': 'gaming/util', 'battle_net': 'gaming/util',
              'minecraft': 'gaming', 'csgo': 'gaming', 'valorant': 'gaming', 'league': 'gaming', 'dota': 'gaming',
              'skyrim': 'gaming', 'cyberpunk': 'gaming', 'elden_ring': 'gaming', 'tetris': 'gaming',
              'civilization': 'gaming', 'factorio': 'gaming', 'sims': 'gaming', 'stardew': 'gaming',
              'red_dead_redemption': 'gaming', 'ubisoft': 'gaming/util', 'destiny': 'gaming', 'fortnite': 'gaming',
              'resident_evil': 'gaming', 'world_of_warcraft': 'gaming', 'hearthstone': 'gaming', 'overwatch': 'gaming',
              'rainbow_six_siege': 'gaming', 'warhammer': 'gaming', 'battlefield': 'gaming', 'apex': 'gaming',
              'code': 'coding/developing', 'launcher': 'util', 'game': 'gaming', 'app': 'util',
              'dev': 'coding/developing', 'engine': 'developing'}
