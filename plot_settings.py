"""
The plot_settings module contains various settings for configuring the plots, used mainly in data_analysis.py.

Variables:
- PLOT_WIDTH, PLOT_HEIGHT: Width and height of the plots.
- PLOT_TITLE_SIZE, PLOT_COLUMN_SIZE, PLOT_LABEL_SIZE: Font sizes for the plot title, column labels, and labels.
- PLOT_TITLE_COLOR, PLOT_COLUMN_COLOR: Colors for the plot title and column labels.
- MAX_LENGTH_BEFORE_ROTATION, MAX_LENGTH_BEFORE_STRONG_ROTATION: Maximum lengths before rotating x-axis labels.
- ROTATION, STRONG_ROTATION: Rotation angles for x-axis labels.
- PLOT_RC_PARAMS: Dictionary containing overall design settings for the plots.
- PLOT_MAPPING: Dictionary containing the plots that will be made in data_analysis.py, along with their important values.
"""

import matplotlib.pyplot as plt
import seaborn as sns

## Plot
# Size
PLOT_WIDTH, PLOT_HEIGHT = 11.55, 6.654
PLOT_TITLE_SIZE = 20
PLOT_COLUMN_SIZE = 16
PLOT_LABEL_SIZE = 12
# Color
PLOT_TITLE_COLOR = '#FFAA33'
PLOT_COLUMN_COLOR = '#4488FF'
# Rotation
MAX_LENGTH_BEFORE_ROTATION, MAX_LENGTH_BEFORE_STRONG_ROTATION = 7, 12
ROTATION, STRONG_ROTATION = 15, 30

# Style
sns.set_theme(style='darkgrid')  # Don't know if this is necessary, but just do it for auto-formats sake
PLOT_RC_PARAMS = {  # Overall Design
    'figure.figsize': (8, 5), 'figure.dpi': 100, 'figure.autolayout': True, 'font.size': 10,
    'font.family': 'sans-serif', 'axes.titlesize': 14, 'axes.labelsize': 12, 'axes.labelcolor': 'white',
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.color': '#cccccc', 'axes.edgecolor': '#444444', 'text.color': 'white',

    # Font
    'axes.titlesize': PLOT_TITLE_SIZE, 'axes.titleweight': 'bold', 'axes.titlecolor': PLOT_TITLE_COLOR,
    'axes.labelsize': PLOT_COLUMN_SIZE, 'axes.labelcolor': PLOT_COLUMN_COLOR,

    # Lines and Markers
    'lines.linewidth': 2, 'lines.markersize': 8,

    # Legends
    'legend.fontsize': 10, 'legend.frameon': True, 'legend.framealpha': 0.9, 'legend.edgecolor': '#333333',

    # Ticks (Skala)
    'xtick.labelsize': 10, 'ytick.labelsize': 10, 'xtick.direction': 'out', 'ytick.direction': 'out',
    'xtick.color': 'white', 'ytick.color': 'white',

    # Colorpalettes
    'axes.prop_cycle': plt.cycler(color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd']),

    # Background and Grid
    'figure.facecolor': '#2e2e2e', 'axes.facecolor': '#3e3e3e', 'axes.grid': True, 'grid.linestyle': '--',
    'axes.xmargin': 0.02, }

# Mapping
PLOT_MAPPING = {"App Usage": {
    "Most Used Apps": {"x": "app_name", "y": "total_active_time", "hue": None, "plot_name": "Most Used Apps",
                       "x_name": "App", "y_name": "Usage Time", "legend_name": None, "plot_type": "bar",
                       "sort": "total_active_time"},
    "Activity Tracking": {"x": "date", "y": "activity", "hue": "category", "plot_name": "Activity Tracking",
                          "x_name": "Date", "y_name": "Activity", "legend_name": "App Category", "plot_type": "line",
                          "sort": "date"},
    "Productivity": {"x": "date", "y": "productivity", "hue": None, "plot_name": "Productivity Score", "x_name": "Date",
                     "y_name": "Score", "legend_name": None, "plot_type": "line", "sort": "date"},
    "Total Active Time": {"x": "date", "y": "total_active_time", "hue": "category",
                          "plot_name": "Total Active Time by Category", "x_name": "Date",
                          "y_name": "Active Time (hours)", "legend_name": "App Category", "plot_type": "line",
                          "sort": "date"},
    "Cumulative Progress": {"x": "date", "y": "total_active_time", "hue": None, "plot_name": "Cumulative Progress",
                            "x_name": "Date", "y_name": "Cumulative Usage Time", "legend_name": None,
                            "plot_type": "line", "sort": "date"},
    "Usage Distribution": {"x": "category", "y": "total_active_time", "hue": None, "plot_name": "Usage Distribution",
                           "x_name": "Category", "y_name": "Usage Time", "legend_name": None, "plot_type": "box",
                           "sort": "total_active_time"},
    "Usage Density": {"x": "category", "y": "total_active_time", "hue": None, "plot_name": "Usage Density",
                      "x_name": "Category", "y_name": "Usage Time", "legend_name": None, "plot_type": "violin",
                      "sort": "total_active_time"}}, "Notifications": {
    "Message Count": {"x": "date", "y": "notification_count", "hue": "notification_type",
                      "plot_name": "Message History", "x_name": "Time", "y_name": "Message Count",
                      "legend_name": "Message Type", "plot_type": "line", "sort": "date"},
    "Message Type": {"x": "notification_type", "y": "total_active_time", "hue": "like",
                     "plot_name": "Message Type by Usage Time", "x_name": "Message Type", "y_name": "Usage Time",
                     "legend_name": "Approved?", "plot_type": "scatter", "sort": "total_active_time"},
    "Activity": {"x": "category", "y": "like", "hue": "activity", "plot_name": "Approval by Activity",
                 "x_name": "App Category", "y_name": "Approvals", "legend_name": "Activity", "plot_type": "bar",
                 "sort": "like"},
    "Likes": {"x": "like", "y": "notification_count", "hue": "like", "plot_name": "Approvals Over Time",
              "x_name": "Date", "y_name": "Message Count", "legend_name": "Approved?", "plot_type": "bar",
              "sort": "like"}, "Likes Corr": {
        "pivot": ["like", "category", "activity", "active_time", "total_active_time", "notification_count",
                  "notification_type"], "plot_name": "Approval Correlation", "plot_type": "heatmap", "sort": "like"}},
    "Time": {"Last Hour": {"filter": "last_hour"}, "Last 4 Hours": {"filter": "last_4_hours"},
             "Today": {"filter": "today"}, "This Week": {"filter": "this_week"}, "This Month": {"filter": "this_month"},
             "This Year": {"filter": "this_year"}, "Total": {"filter": "total"}}}
