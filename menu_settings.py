"""
The menu_settings module contains various settings for configuring the TKinter app, used mainly in tkmanager.py.

Variables:
- Universal: Colors, font, size values, and dropdown content for the app.
- Menu Window: Icon path, frame size, resizable, close button, title, title font, size, listbox size, font, button font, size, listbox font, size, dropdown font, size, dropdown width, caption, caption font, size, startup button colors.
- Notification: Open time, frame size, resizable, close button, font, font size.
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
DROPDOWN_CONTENT = {'App Usage': (
'Most Used Apps', 'Activity Tracking', 'Productivity', 'Total Active Time', 'Usage Distribution', 'Usage Density'),
                    'Tracker': (
                    'Most Used Apps', 'Activity Tracking', 'Productivity', 'Total Active Time', 'Usage Distribution',
                    'Usage Density'),
                    'Notifications': ('Message Count', 'Message Type', 'Activity', 'Likes', 'Likes Corr'),
                    'Direction': ('Top', 'Last'),
                    'Part': ('Full', '50%', '25%', '10%', '10', '5', '3'),
                    'Time': ('Last Hour', 'Last 4 Hours', 'Today', 'This Week', 'This Month', 'This Year', 'Total'),}

## Menu Window
# Icon
MENU_ICON_PATH = 'img/scaled_dark_glitchy_ai_hourglass.png'
# Frame
MENU_WIDTH, MENU_HEIGHT = 1300, 975
MENU_RESIZABLE = (False, False)
MENU_CLOSE_BUTTON = 'Escape'
# Title
MENU_TITLE = 'Track Mind'
MENU_TITLE_FONT, MENU_TITLE_FONT_SIZE = 'sans_serif', 20
# Size
MENU_LISTBOX_WIDTH, MENU_LISTBOX_HEIGHT = 91, 27
# Font
MENU_FONT, MENU_FONT_SIZE = 'sans_serif', 20
MENU_BUTTON_FONT, MENU_BUTTON_FONT_SIZE = 'sans_serif', 16
MENU_LISTBOX_FONT, MENU_LISTBOX_FONT_SIZE = 'sans_serif', 14
MENU_DROPDOWN_FONT, MENU_DROPDOWN_FONT_SIZE = 'sans_serif', 14
MENU_DROPDOWN_WIDTH = 10
# Caption
MENU_CAPTION = 'Welcome to TrackMind'
MENU_CAPTION_FONT, MENU_CAPTION_FONT_SIZE = 'sans_serif', 30
# Startup Button
BUTTON_GREEN_BG, BUTTON_GREEN_HOVER_BG = '#4CAF50', '#66BB6A'
BUTTON_RED_BG, BUTTON_RED_HOVER_BG = '#E53935', '#EF5350'

## Notification
# Main settings
NOTIFICATION_OPEN_TIME = 60000  # In Milliseconds
# Frame
NOTIFICATION_WIDTH, NOTIFICATION_HEIGHT = 500, 325
NOTIFICATION_RESIZABLE = (False, False)
NOTIFICATION_CLOSE_BUTTON = 'Escape'
# Font
NOTIFICATION_FONT, NOTIFICATION_FONT_SIZE = 'sans_serif', 20
