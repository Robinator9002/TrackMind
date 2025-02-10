import sqlite3 as sql

from settings import *


class SQLLoader:
    def __init__(self, db_manager, table_name=DEFAULT_TABLE_NAME):
        """
        Initializes the SQLLoader with a reference to the SQLManager and table name.
        :param db_manager: An instance of SQLManager.
        :param table_name: Name of the table to load and save stats (default: DEFAULT_TABLE_NAME from menu_settings.py).
        """
        self.db_manager = db_manager
        self.table_name = table_name
        self._initialize_table()

    def clear_table(self):
        """
        Deletes all data in the table
        """
        query = f"DELETE FROM {self.table_name}"
        self.db_manager.query(query)
        self.db_manager.commit()
        self._initialize_table()

    def _initialize_table(self):
        """
        Ensures the stats table exists in the database.
        """
        columns = TABLE_COLUMNS
        self.db_manager.create_table(self.table_name, columns)

    def save_stat(self, stat_name, value):
        """
        Saves or updates a specific stat in the database.
        :param stat_name: Name of the stat to save (e.g., "score").
        :param value: Value to save for the stat.
        """
        existing = self.db_manager.fetch(f"SELECT id FROM {self.table_name} LIMIT 1")
        if existing:
            self.db_manager.update_object({stat_name: value}, f"id = {existing[0]}", self.table_name)
        else:
            self.db_manager.insert_object(self.table_name, {stat_name: value})

    def save_column(self, key_stat, key_value, stats):
        """
        Saves or updates all stats in the database.
        :param key_stat: Name of the stat that will be checked (e.g., "score").
        :param key_value: Value of the stat that will be checked (e.g., 100).
        :param stats: Dictionary of stats to save, e.g., {
                      "score": 100, "damage": 20, "health": 80, "fire_rate": 5}
        """
        existing = self.db_manager.fetch(f"SELECT * FROM {self.table_name} where {key_stat} = ? LIMIT 1", (key_value,))
        if existing:
            self.db_manager.update_object(stats, f"id = {existing[0]}", self.table_name)
        else:
            self.db_manager.insert_object(self.table_name, stats)

    def load_stat(self, stat_name):
        """
        Loads a specific stat from the database.
        :param stat_name: Name of the stat to load (e.g., "score").
        :return: The value of the stat or None if not found.
        """
        result = self.db_manager.fetch(f"SELECT {stat_name} FROM {self.table_name}")
        return result[0] if result else None

    def load_column(self, stat_name, value):
        """
        Loads a specific column from the database.
        :param stat_name: Name of the stat that will be checked (e.g., "score").
        :param value: The Value that will be searched for
        :return: The value that was found or None
        """
        result = self.db_manager.fetch(f"SELECT * FROM {self.table_name} where {stat_name} = ?", (value,))
        return result if result else None

    def save_all_stats(self, stats):
        """
        Saves or updates all stats at once.
        :param stats: Dictionary of stats to save, e.g., {
                      "score": 100, "damage": 20, "health": 80, "fire_rate": 5}
        """
        existing = self.db_manager.fetch(f"SELECT id FROM {self.table_name}")
        if existing:
            self.db_manager.update_object(stats, f"id = {existing[0]}", self.table_name)
        else:
            self.db_manager.insert_object(self.table_name, stats)

    def load_all_stats(self):
        """
        Loads all stats from the database.
        :return: Dictionary of all stats or None if not found.
        """
        result = self.db_manager.fetch_all(f"SELECT * FROM {self.table_name}")
        if result:
            # keys = [description[0] for description in
            #         self.db_manager.query(f"PRAGMA table_info({self.table_name})").fetchall()]
            keys = [i for i in range(len(result))]
            return {key: value for key, value in zip(keys, result) if key != "id"}

        return None


class SQLManager:
    def __init__(self, database_name=SQL_PATH):
        self.connection = sql.connect(database_name)

    def query(self, query, params=None):
        """
        Executes a query with optional parameters.
        """
        c = self.connection.cursor()
        try:
            c.execute(query, params or ())
            return c
        except sql.Error as e:
            print(f"An error occurred: {e}")
            return None

    def commit(self):
        """
        Commits the current transaction.
        """
        try:
            self.connection.commit()
        except sql.Error as e:
            print(f"Commit failed: {e}")

    def fetch(self, query, params=None):
        """
        Executes a query and fetches the first row of the result.
        """
        c = self.query(query, params)
        fetch = c.fetchone() if c else None
        return fetch

    def fetch_all(self, query, params=None):
        """
        Executes a query and fetches all rows of the result.
        """
        c = self.query(query, params)
        return c.fetchall() if c else []

    def create_table(self, table_name=DEFAULT_TABLE_NAME, columns=None):
        """
        Creates a table with the specified name and columns.
        :param table_name: Name of the table (default from menu_settings).
        :param columns: Dictionary of column names and their types.
                        Example: {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"}
        """
        if not columns:
            raise ValueError("Columns definition is required to create a table.")

        column_definitions = ", ".join(f"{col} {dtype}" for col, dtype in columns.items())
        query = f"CREATE TABLE IF NOT EXISTS {table_name} ({column_definitions})"
        self.query(query)
        self.commit()

    def update_object(self, updates, condition, table_name=DEFAULT_TABLE_NAME):
        """
        Updates an object in the table.
        :param table_name: Name of the table.
        :param updates: Dictionary of column-value pairs to update.
                        Example: {"name": "Alice", "age": 35}
        :param condition: SQL condition as a string, e.g., "id = 1".
        """
        set_clause = ", ".join(f"{col} = ?" for col in updates.keys())
        query = f"UPDATE {table_name} SET {set_clause} WHERE {condition}"
        self.query(query, tuple(updates.values()))
        self.commit()

    def drop_table(self, table_name=DEFAULT_TABLE_NAME):
        """
        Drops a table with the specified name.
        :param table_name: Name of the table (default from menu_settings).
        """
        query = f"DROP TABLE IF EXISTS {table_name}"
        self.query(query)
        self.commit()

    def insert_object(self, table_name=DEFAULT_TABLE_NAME, values=None):
        """
        Inserts an object (row) into the specified table.
        :param table_name: Name of the table (default from menu_settings).
        :param values: Dictionary of column-value pairs to insert.
                       Example: {"name": "Alice", "age": 30}
        """
        if not values:
            raise ValueError("Values are required to insert an object.")

        columns = ", ".join(values.keys())
        placeholders = ", ".join("?" for _ in values)
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        self.query(query, tuple(values.values()))
        self.commit()

    def delete_object(self, table_name=DEFAULT_TABLE_NAME, condition=None):
        """
        Deletes an object (row) from the specified table based on a condition.
        :param table_name: Name of the table (default from menu_settings).
        :param condition: SQL condition as a string, e.g., "id = 1".
                          If None, deletes all rows from the table.
        """
        query = f"DELETE FROM {table_name}"
        if condition:
            query += f" WHERE {condition}"
        self.query(query)
        self.commit()

    def close(self):
        """
        Closes the database connection.
        """
        self.connection.close()

    def __del__(self):
        """
        Ensures the connection is closed when the object is deleted.
        """
        self.close()
