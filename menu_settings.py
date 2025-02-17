"""
Settings to configure the App
"""

## Universal
BG_COLOR = "#1A1A1A"
TITLE_BG = "#333333"
BUTTON_BG = "#3A3A3A"
BUTTON_FG = "white"
BUTTON_HOVER_BG = "#505050"
TEXT_COLOR = "#E0E0E0"
LISTBOX_BG = "#1E1E1E"
LISTBOX_FG = "#E0E0E0"
DROPDOWN_BG = "#2A2A2A"
DROPDOWN_FG = "white"
DROPDOWN_HOVER_BG = "#3A3A3A"
DROPDOWN_ARROW = "white"

# Dropdown Content
DROPDOWN_CONTENT = {'App Usage': ('Most Used Apps', 'Activity Tracking', 'Productivity', 'Total Active Time'),
    'Notifications': ('Message Count', 'Message Type', 'Activity', 'Likes'),
    'Time': ('Last Hour', 'Last 4 Hours', 'Today', 'This Week', 'This Month', 'This Year', 'Total')}

## Menu Window
# Frame
MENU_WIDTH, MENU_HEIGHT = 1300, 950
MENU_RESIZABLE = (False, False)
MENU_CLOSE_BUTTON = 'Escape'
# Title
MENU_TITLE = 'TrackMind'
MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE = 'sans_serif', 18
# Font
MENU_FONT, MENU_FONT_SIZE = 'sans_serif', 16
MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE = 'sans_serif', 16
MENU_LISTBOX_FONT, MENU_LISTBOX_FONT_SIZE = 'sans_serif', 14
MENU_DROPDOWN_FONT, MENU_DROPDOWN_FONT_SIZE = 'sans_serif', 14
MENU_DROPDOWN_WIDTH = 10
# Caption
MENU_CAPTION = 'Welcome to TrackMind'
MENU_CAPTION_FONT, MENU_CAPTION_FONT_SIZE = 'sans_serif', 30

## Notification
# Frame
NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT = 600, 350
NOTIFICATION_RESIZABLE = (False, False)
NOTIFICATION_CLOSE_BUTTON = 'Escape'
# Font
NOTIFICATION_FONT, NOTIFICATION_FONT_SIZE = 'sans_serif', 20
