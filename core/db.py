#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Enhanced Database Module for Improved Performance and Maintainability
This module provides a database handler with optimized query execution,
better modularity, and additional features.
"""

import sqlite3
import os
from typing import Any, Dict, List, Tuple, Union


class Database:
    """
    Database handler class for managing database operations.
    This class ensures better performance, modularity, and error handling.
    """

    def __init__(self, db_path: str = "database.db") -> None:
        """
        Initialize the database connection and setup the database.
        :param db_path: Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
        self.cursor = self.conn.cursor()
        if not os.path.exists(self.db_path):
            self._initialize_database()

    def _initialize_database(self) -> None:
        """
        Create the required tables in the database.
        """
        schema = [
            """CREATE TABLE IF NOT EXISTS geo (
                id TEXT PRIMARY KEY,
                city TEXT, country_code TEXT, country_name TEXT, ip TEXT,
                latitude TEXT, longitude TEXT, metro_code TEXT, region_code TEXT,
                region_name TEXT, time_zone TEXT, zip_code TEXT, isp TEXT,
                ua TEXT, connection TEXT, latitude_browser TEXT,
                longitude_browser TEXT, refer TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS networks (
                id TEXT, ip TEXT, public_ip INTEGER, network TEXT, date TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS requests (
                id TEXT, user_id TEXT, site TEXT, fid TEXT,
                name TEXT, value TEXT, date TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS victims (
                id TEXT, ip TEXT, date TEXT, time REAL,
                bVersion TEXT, browser TEXT, device TEXT, cpu TEXT,
                ports TEXT, status TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS victims_data (
                id TEXT, name TEXT, last_online DATE,
                gpu TEXT, donottrack TEXT, navigation_mode TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS victims_battery (
                id TEXT, charging TEXT, time_c REAL, time_d REAL, level REAL
            )""",
            """CREATE TABLE IF NOT EXISTS clicks (
                id TEXT, site TEXT, date TEXT
            )""",
            """CREATE TABLE IF NOT EXISTS hostsalive (
                id TEXT, remote_ip TEXT, ping TEXT, date TEXT
            )"""
        ]
        for table in schema:
            self.cursor.execute(table)
        self.conn.commit()

    def execute_query(self, query: str, params: Tuple[Any, ...] = ()) -> List[Tuple]:
        """
        Execute a SQL query and return all results.
        :param query: SQL query string
        :param params: Parameters for the query
        :return: Query results as a list of tuples
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return []

    def execute_insert(self, query: str, params: Tuple[Any, ...]) -> bool:
        """
        Execute an insert/update query.
        :param query: SQL query string
        :param params: Parameters for the query
        :return: True if query succeeded, False otherwise
        """
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error executing insert: {e}")
            return False

    def fetch_one(self, query: str, params: Tuple[Any, ...] = ()) -> Union[Tuple, None]:
        """
        Fetch a single row from the database.
        :param query: SQL query string
        :param params: Parameters for the query
        :return: A single row or None
        """
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error fetching row: {e}")
            return None

    def get_table_data(self, table_name: str) -> List[Tuple]:
        """
        Fetch all data from a specific table.
        :param table_name: Name of the table
        :return: List of rows from the table
        """
        return self.execute_query(f"SELECT * FROM {table_name}")

    def close_connection(self) -> None:
        """
        Close the database connection.
        """
        if self.conn:
            self.conn.close()


if __name__ == "__main__":
    # Example usage
    db = Database()

    # Insert example data
    db.execute_insert(
        "INSERT INTO geo (id, city, country_code) VALUES (?, ?, ?)",
        ("1", "Test City", "TC")
    )

    # Query example
    rows = db.execute_query("SELECT * FROM geo")
    print(rows)

    # Close connection
    db.close_connection()
