"""
db.py - Database connection utility for the Car Rental System.

Implements a simple connection factory (Factory pattern) for SQLite.
In a production system, this would be replaced with a connection pool
or ORM (e.g., SQLAlchemy).
"""

import sqlite3
import os
import sys


def get_db_path() -> str:
    """
    Get the correct database path for both development
    and PyInstaller executable environments.

    Returns:
        str: Absolute path to the SQLite database file.
    """

    # If running as a bundled PyInstaller executable
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(sys.executable)

    # If running normally in VS Code / Python
    else:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, "..", "car_rental.db")


# Centralised database path
DB_PATH = os.path.abspath(get_db_path())


def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite database connection.

    Uses the Factory pattern to centralise connection creation,
    making it easy to swap out the database backend in future.

    Returns:
        sqlite3.Connection: An active connection to the SQLite database.
    """

    return sqlite3.connect(DB_PATH)