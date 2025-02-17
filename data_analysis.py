import os
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from plot_settings import *
from settings import NOTIFICATION_CSV_PATH
from util import format_time, get_productivity_by_category  # Assumed to be defined in util.py


class PlotManager:
    def __init__(self, manager):
        self.manager = manager

        sns.set_style("darkgrid")
        plt.rcParams.update({# Overall Design
            'figure.figsize': (8, 5), 'figure.dpi': 100, 'figure.autolayout': True, 'font.size': 10,
            'font.family': 'sans-serif', 'axes.titlesize': 14, 'axes.labelsize': 12, 'axes.labelcolor': 'white',
            'axes.grid': True, 'grid.alpha': 0.3, 'grid.color': '#cccccc', 'axes.edgecolor': '#444444',
            'text.color': 'white',

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
            'figure.facecolor': '#2e2e2e', 'axes.facecolor': '#3e3e3e', })
        plt.rcParams.update({'axes.grid': True, 'grid.linestyle': '--', 'axes.xmargin': 0.02, })

        self.dark_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
            '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94', '#f7b6d2',
            '#c7c7c7', '#dbdb8d', '#9edae5']

    def create_plot(self, values, root):
        """Gets the plot settings and calls create_tkinter_plot"""
        # Check Data
        data = None
        if os.path.exists(NOTIFICATION_CSV_PATH):
            data = self.load_data()
        if data is None or data.empty:
            self.manager.app.tk_manager.set_dropdowns('normal')
            return

        x, y, hue, plot_name, x_name, y_name, legend_name, plot_type, time_range = get_plot_settings(values)

        # Data processing steps
        data = self.prepare_data(data, time_range)

        self.create_tkinter_plot(data, x, y, hue, plot_name, x_name, y_name, legend_name, plot_type, root)

    def load_data(self):
        """Loads and prepares the raw data"""
        data = pd.read_csv(NOTIFICATION_CSV_PATH)
        data['timestamp'] = pd.to_datetime(data['timestamp'])
        return data

    def prepare_data(self, data, time_range):
        """Performs all data preparation steps"""
        # 1. Time filtering
        data = self.filter_by_time_range(data, time_range)

        # 2. Create date column
        data = self.create_date_column(data, time_range)

        # 3. Calculate productivity
        data = self.add_productivity(data)

        # 4. Calculate message count
        data = self.calculate_message_count(data)

        # 5. Format time
        if 'total_active_time' in data.columns:
            data['total_active_time'] = data['total_active_time'].apply(format_time)

        return data

    def filter_by_time_range(self, data, time_range):
        """Filters data based on the selected time range"""
        now = datetime.now()

        time_filters = {"last_hour": now - timedelta(hours=1), "last_4_hours": now - timedelta(hours=4),
                        "today": now.replace(hour=0, minute=0, second=0, microsecond=0),
                        "this_week": now - timedelta(days=now.weekday()), "this_month": now.replace(day=1),
                        "this_year": now.replace(month=1, day=1), "total": data['timestamp'].min()}

        start_time = time_filters.get(time_range, data['timestamp'].min())
        return data[data['timestamp'] >= start_time]

    def create_date_column(self, data, time_range):
        """Creates the date column based on the time range"""
        if time_range in ['last_hour', 'last_4_hours']:
            data['date'] = data['timestamp'].dt.strftime('%H:%M')
        elif time_range == 'today':
            data['date'] = data['timestamp'].dt.strftime('%H:%M')
        elif time_range == 'this_week':
            data['date'] = data['timestamp'].dt.strftime('%a %d.%m')
        elif time_range == 'this_month':
            data['date'] = data['timestamp'].dt.strftime('%d.%m')
        elif time_range == 'this_year':
            data['date'] = data['timestamp'].dt.strftime('%b %Y')
        else:
            data['date'] = data['timestamp'].dt.strftime('%d.%m.%Y')

        return data

    def add_productivity(self, data):
        """Adds productivity score"""
        data['productivity'] = data['category'].apply(get_productivity_by_category)
        return data

    def calculate_message_count(self, data):
        """Calculates the message count"""
        if 'notification_text' in data.columns:
            data['message_count'] = data.groupby('date')['notification_text'].transform('count')
        return data

    def create_tkinter_plot(self, data, x, y, hue, plot_name, x_name, y_name, legend_name, plot_type, root):
        """Creates the Matplotlib plot and returns a Tkinter Canvas"""
        fig = plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))

        # Seaborn plot selection
        plot_methods = {"line": [sns.lineplot, {'estimator': 'sum', 'marker': 'X'}],
                        "bar": [sns.barplot, {'estimator': 'sum', 'width': 0.8}],
                        "scatter": [sns.scatterplot, {'edgecolor': 'black'}]}

        if plot_type not in plot_methods:
            raise ValueError(f"Invalid plot type: {plot_type}")

        # Create plot
        plot_method = plot_methods[plot_type]
        plot_func = plot_method[0]
        if hue:
            plot_func(data, x=x, y=y, hue=hue, palette=self.dark_palette, **plot_method[1])
        else:
            plot_func(data, x=x, y=y, **plot_method[1])

        # Plot labels
        plt.suptitle(plot_name)
        plt.xlabel(x_name)
        plt.ylabel(y_name)

        # Position legend
        if legend_name:
            plt.legend(title=legend_name, loc='upper left', bbox_to_anchor=(1, 1))

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        self.manager.apply_plot(canvas)

    @staticmethod
    def close_plot(plot):
        plt.close(plot.figure)


def get_plot_settings(values):
    """Determines the plot settings based on the dropdown selections"""
    data_dd_v, analysis_dd_v, time_dd_v = values

    try:
        plot_config = PLOT_MAPPING[data_dd_v][analysis_dd_v]
        time_range = PLOT_MAPPING["Time"][time_dd_v]['filter']
    except KeyError as e:
        raise ValueError(f"Invalid dropdown selection: {values}") from e

    return (plot_config['x'], plot_config['y'], plot_config['hue'], plot_config['plot_name'], plot_config['x_name'],
            plot_config['y_name'], plot_config['legend_name'], plot_config['plot_type'], time_range)


PLOT_MAPPING = {"App Usage": {
    "Most Used Apps": {"x": "app_name", "y": "total_active_time", "hue": None, "plot_name": "Most Used Apps",
                       "x_name": "App", "y_name": "Usage Time", "legend_name": None, "plot_type": "bar"},
    "Activity Tracking": {"x": "date", "y": "activity", "hue": "category", "plot_name": "Activity Tracking",
                          "x_name": "Date", "y_name": "Activity", "legend_name": "App Category", "plot_type": "line"},
    "Productivity": {"x": "date", "y": "productivity", "hue": None, "plot_name": "Productivity Score", "x_name": "Date",
                     "y_name": "Score", "legend_name": None, "plot_type": "line"},
    "Total Active Time": {"x": "date", "y": "total_active_time", "hue": "category",
                          "plot_name": "Total Active Time by Category", "x_name": "Date",
                          "y_name": "Active Time (hours)", "legend_name": "App Category", "plot_type": "line"}},
    "Notifications": {
        "Message Count": {"x": "date", "y": "message_count", "hue": "notification_type", "plot_name": "Message History",
                          "x_name": "Time", "y_name": "Message Count", "legend_name": "Message Type",
                          "plot_type": "line"},
        "Message Type": {"x": "notification_type", "y": "total_active_time", "hue": "like",
                         "plot_name": "Message Type by Usage Time", "x_name": "Message Type", "y_name": "Usage Time",
                         "legend_name": "Approved?", "plot_type": "scatter"},
        "Activity": {"x": "category", "y": "like", "hue": "activity", "plot_name": "Approval by Activity",
                     "x_name": "App Category", "y_name": "Approvals", "legend_name": "Activity", "plot_type": "bar"},
        "Likes": {"x": "like", "y": "message_count", "hue": "like", "plot_name": "Approvals Over Time",
                  "x_name": "Date", "y_name": "Message Count", "legend_name": "Approved?", "plot_type": "bar"}},
    "Time": {"Last Hour": {"filter": "last_hour"}, "Last 4 Hours": {"filter": "last_4_hours"},
             "Today": {"filter": "today"}, "This Week": {"filter": "this_week"}, "This Month": {"filter": "this_month"},
             "This Year": {"filter": "this_year"}, "Total": {"filter": "total"}}}
