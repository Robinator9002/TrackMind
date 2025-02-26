from datetime import datetime, timedelta

import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from menu_settings import DROPDOWN_CONTENT
from plot_settings import *
from settings import NOTIFICATION_CSV_PATH, os, TRACKER_CSV_PATH
from util import format_time, get_productivity_by_category, map_activity, one_hot_encode, convert_last_data_to_dataframe


class PlotManager:
    """
    The PlotManager class is responsible for managing and creating plots based on the data analysis.

    Attributes:
        tracker (object): The manager object that provides necessary functionality for the PlotManager.
        dark_palette (list): A list of dark color codes for plotting.

    Methods:
        __init__(self, manager): Initializes the PlotManager instance with the provided manager object.
        load_tracker_data(self): Loads and prepares the raw data from tracker.csv.
        load_notification_data(self): Loads and prepares the raw data from notifications.csv.
        prepare_data(self, data, plot_type, sort, time_range, part, values): Performs all data preparation steps.
        sort_data_by(self, data, sort): Sorts data based on the selected sort criteria.
        filter_by_part(self, data, part): Filters data based on user selection.
        filter_by_time_range(self, data, time_range): Filters data based on the selected time range.
        create_date_column(self, data, time_range): Creates the date column based on the time range.
        add_productivity(self, data): Adds productivity score.
        calculate_message_count(self, data): Calculates the message count.
        encode_data(self, data): Encodes values using the one_hot_encode, specifically targeting: activity, category, and notification_type columns from data.
        create_tkinter_plot(self, data, plot_settings, root): Creates the Matplotlib plot and shows the canvas in tkinter via self.tracker.app.tk_manager.show_plot(plot).
        close_plot(self, plot): Closes the plot.
        get_plot_settings(self, values): Determines the plot settings based on the dropdown selections.
    """

    def __init__(self, manager):
        """
        Initializes the PlotManager instance with the provided manager object.

        Args:
            manager (object): The manager object that provides necessary functionality for the PlotManager.
        """
        self.tracker = manager

        plt.rcParams.update(PLOT_RC_PARAMS)

        self.dark_palette = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f',
                             '#bcbd22', '#17becf', '#aec7e8', '#ffbb78', '#98df8a', '#ff9896', '#c5b0d5', '#c49c94',
                             '#f7b6d2', '#c7c7c7', '#dbdb8d', '#9edae5']

    def create_plot(self, dropdown_values, root):
        """Gets the plot settings, loads the data and calls prepare_data and create_tkinter_plot with the right values.
        Also configures the dropdown_values using DROPDOWN_CONTENT from menu_settings.
        It features using the SQL Data and loading both CSV Files (Tracker and Notifications).
        If the plot type is heatmap then disable the part dropdowns, so no misconceptions over the part dropdowns not working are made (they dont affect heatmap plots)!"""
        # Dropdown Keys
        dropdown_keys = list(DROPDOWN_CONTENT.keys())
        # Get Plot Settings
        values = [None for _ in dropdown_values]
        for idx, value in enumerate(dropdown_values):
            if value == dropdown_keys[1]:
                values[idx] = dropdown_keys[0]
                continue
            values[idx] = dropdown_values[idx]
        plot_settings = get_plot_settings(values)

        # Unpack Plot Settings
        if plot_settings[0] == 'heatmap':
            plot_type, pivot, plot_name, sort, time_range, part = plot_settings
            values = pivot
        else:
            plot_type, x, y, hue, plot_name, x_name, y_name, legend_name, sort, time_range, part = plot_settings
            values = [x, y, hue]

        # If heatmap disable TKManager's part dropdown
        if plot_type == 'heatmap':
            self.tracker.app.tk_manager.set_dropdowns('disabled', False, False, True, False) # Only Part Dropdowns! Parameters: data, analysis, part, time

        # Load Data
        data = None

        if dropdown_values[0] == dropdown_keys[0]:
            data = convert_last_data_to_dataframe(self.tracker.last_data)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
        elif dropdown_values[0] == dropdown_keys[1]:
            data = self.load_tracker_data()
        elif dropdown_values[0] == dropdown_keys[2]:
            data = self.load_notification_data()

        if data is None or data.empty:
            if plot_type == 'heatmap':
                self.tracker.app.tk_manager.set_dropdowns('normal', True, True, False, True)
            else:
                self.tracker.app.tk_manager.set_dropdowns('normal')
            return

        # Data processing steps
        data = self.prepare_data(data, plot_type, sort, time_range, part, values)

        # Create Plot
        self.create_tkinter_plot(data, plot_settings, root)

    def load_tracker_data(self):
        """Loads and prepares the raw data from tracker.csv"""
        tracker_abs_path = os.path.join(self.tracker.app.autostart_manager.current_abs_path[0], TRACKER_CSV_PATH)
        if os.path.exists(tracker_abs_path):
            data = pd.read_csv(tracker_abs_path)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            return data
        return None

    def load_notification_data(self):
        """Loads and prepares the raw data from notifications.csv"""
        notification_abs_path = os.path.join(self.tracker.app.autostart_manager.current_abs_path[0],
                                             NOTIFICATION_CSV_PATH)
        if os.path.exists(notification_abs_path):
            data = pd.read_csv(notification_abs_path)
            data['timestamp'] = pd.to_datetime(data['timestamp'])
            return data
        return None

    def prepare_data(self, data, plot_type, sort, time_range, part, values):
        """Performs all data preparation steps"""
        # 1. Time filtering
        data = self.filter_by_time_range(data, time_range)

        # 2. Create date column
        data = self.create_date_column(data, time_range)

        # 3. Calculate productivity
        data = self.add_productivity(data)

        # 4. Calculate message count
        data = self.calculate_message_count(data)

        # Grouping and Filtering will not be done in heatmap-plot!
        if not plot_type == 'heatmap':
            # 5. Group
            data = self.group_data_by(data, values)

            # 6. Filter by part
            data = self.filter_by_part(data, part)

        # 7. Sort
        data = self.sort_data_by(data, sort)

        # 8. Encode Data or Format time
        if plot_type == 'heatmap':
            # 8.1 Encode Data
            data = self.encode_data(data)
        else:
            # 8.2 Format Time
            if 'total_active_time' in data.columns:
                data['total_active_time'] = data['total_active_time'].apply(format_time)

        # 9. Drop Duplicates
        data = data.drop_duplicates()
        if 'date' in values:
            data = data.drop_duplicates('date')

        return data

    def sort_data_by(self, data, sort):
        """Sorts data based on the selected sort criteria"""
        if sort == 'date':
            data = data.sort_values('date', ascending=True)
        elif sort == 'productivity':
            data = data.sort_values('productivity', ascending=True)
        elif sort == 'total_active_time':
            data = data.sort_values('total_active_time', ascending=True)
        elif sort == 'total_messages':
            data = data.sort_values('total_messages', ascending=True)
        elif sort == 'activity':
            data['num_activity'] = data['activity'].apply(lambda x: map_activity(x))
            data = data.sort_values('num_activity', ascending=True)
            data = data.drop('num_activity', axis=1)
        elif sort == 'like':
            data = data.sort_values(by='like', ascending=False)

        return data

    def group_data_by(self, data, values):
        """Uses pd.DataFrame().groupby() to remove all unnecessary data and group the rest using sum as aggregation function.
        Only sums the y-axis. If like or is in axis just skip it. If hue ist the same as x or y then group only by x!"""
        x, y, hue = values
        # If x or y are not in data
        if x not in data.columns or y not in data.columns:
            return data

        # Define aggregation functions for y-axis
        agg_funcs = {y: "sum"}

        if hue and hue in data.columns and not hue in [x, y]:
            grouped_data = data.groupby([x, hue]).agg(agg_funcs).reset_index()
        else:
            grouped_data = data.groupby(x).agg(agg_funcs).reset_index()

        return grouped_data

    def filter_by_part(self, data, part):
        """
        Filter data based on user selection.

        Args:
            data (DataFrame): Sorted data.
            part (list): [direction, amount] e.g. ['top', '10%'] or ['last', '5'].

        Returns:
            DataFrame: Filtered data.
        """
        direction, amount = part[0].lower(), part[1]

        # If the amount is full then just do nothing and return the input data
        if amount == 'full':
            return data

        # Determine if amount is a percentage or absolute number
        if "%" in amount:
            try:
                percent = float(amount.strip("%"))
            except ValueError:
                raise ValueError("Invalid percentage value: " + amount)
            n = int(round(len(data) * (percent / 100)))
        else:
            try:
                n = int(amount)
            except ValueError:
                raise ValueError("Invalid numeric value: " + amount)

        # Ensure n is at least 1 and not more than the total data length
        n = max(1, min(n, len(data)))

        # Filter: top = first n rows, last = last n rows
        if direction == "top":
            filtered_data = data.head(n)
        elif direction == "last":
            filtered_data = data.tail(n)
        else:
            raise ValueError("Invalid direction: " + direction)

        return filtered_data

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
            data['notification_count'] = data.groupby('date')['notification_text'].transform('count')
        return data

    def encode_data(self, data):
        """Encodes values using the one_hot_encode, specifically targeting:
        - activity
        - category
        - notification_type
        columns from data"""
        data = one_hot_encode(data, 'activity')
        data = one_hot_encode(data, 'category')
        data = one_hot_encode(data, 'notification_type')
        return data

    def create_tkinter_plot(self, data, plot_settings, root):
        """Creates the Matplotlib plot and shows the canvas in tkinter via self.tracker.app.tk_manager.show_plot(plot).
        It features many different plot types, including:
        line, bar, scatter, heatmap, box, violin."""

        # Unpack Plot Settings based on Plot Type (plot_settings[0])
        if plot_settings[0] == 'heatmap':
            plot_type, pivot, plot_name, sort, time_range, part = plot_settings
            correlation = data[pivot].corr()
        else:
            plot_type, x, y, hue, plot_name, x_name, y_name, legend_name, sort, time_range, part = plot_settings

        ## Plot
        fig = plt.figure(figsize=(PLOT_WIDTH, PLOT_HEIGHT))
        # Seaborn plot selection
        plot_methods = {"line": [sns.lineplot, {'estimator': sum, 'marker': 'X'}],
                        "bar": [sns.barplot, {'estimator': sum, 'width': 0.8}],
                        "scatter": [sns.scatterplot, {'edgecolor': 'black'}],
                        "heatmap": [sns.heatmap, {'annot': True, 'cmap': 'YlGnBu'}], "box": [sns.boxplot, {}],
                        "violin": [sns.violinplot, {'inner': 'quartile'}]}

        if plot_type not in plot_methods:
            raise ValueError(f"Invalid plot type: {plot_type}")

        # Create plot
        plot_method = plot_methods[plot_type]
        plot_func = plot_method[0]
        if plot_type == 'heatmap':
            plot_func(correlation, **plot_method[1])
        else:
            if hue:
                plot_func(data, x=x, y=y, hue=hue, palette=self.dark_palette or 'dark', **plot_method[1])
            else:
                plot_func(data, x=x, y=y, **plot_method[1])

            # Plot labels
            plt.suptitle(plot_name, fontsize=PLOT_TITLE_SIZE, color=PLOT_TITLE_COLOR, fontweight='bold',
                         fontstyle='italic')
            plt.xlabel(x_name)
            plt.ylabel(y_name)
            plt.tight_layout()
            plt.grid()

            # Position legend
            if legend_name:
                plt.legend(title=legend_name, loc='upper left', bbox_to_anchor=(0, 1))

        # Rotation (Ticks)
        ax = plt.gca()
        if len(ax.get_xticklabels()) > MAX_LENGTH_BEFORE_STRONG_ROTATION:
            for label in ax.get_xticklabels():
                label.set_rotation(STRONG_ROTATION)
        elif len(ax.get_xticklabels()) > MAX_LENGTH_BEFORE_ROTATION:
            for label in ax.get_xticklabels():
                label.set_rotation(ROTATION)

        # Create canvas
        canvas = FigureCanvasTkAgg(fig, master=root)
        canvas.draw()
        self.tracker.app.tk_manager.show_plot(canvas, plot_type) # Give plot_type to correctly handle Part Plots!

    @staticmethod
    def close_plot(plot):
        """Closes the plot"""
        plt.close(plot.figure)


def get_plot_settings(values):
    """Determines the plot settings based on the dropdown selections"""
    data_dd_v, analysis_dd_v, time_dd_v, direction_dd_v, part_dd_v = values

    try:
        plot_config = PLOT_MAPPING[data_dd_v][analysis_dd_v]
        time_range = PLOT_MAPPING["Time"][time_dd_v]['filter']
    except KeyError as e:
        raise ValueError(f"Invalid dropdown selection: {values}") from e

    part = [str(direction_dd_v).lower(), str(part_dd_v).lower()]

    if plot_config['plot_type'] == "heatmap":
        return (
            plot_config['plot_type'], plot_config['pivot'], plot_config['plot_name'], plot_config['sort'], time_range,
            part)
    else:
        return (
            plot_config['plot_type'], plot_config['x'], plot_config['y'], plot_config['hue'], plot_config['plot_name'],
            plot_config['x_name'], plot_config['y_name'], plot_config['legend_name'], plot_config['sort'], time_range,
            part)
