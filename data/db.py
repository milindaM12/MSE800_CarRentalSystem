"""
db.py - Database connection utility for the Car Rental System.

Implements a simple connection factory (Factory pattern) for SQLite.
In a production system, this would be replaced with a connection pool
or ORM (e.g., SQLAlchemy).
"""

import sqlite3

# Database file path — centralised here for easy reconfiguration
DB_PATH = "car_rental.db"


def get_connection() -> sqlite3.Connection:
    """
    Create and return a new SQLite database connection.

    Uses the Factory pattern to centralise connection creation,
    making it easy to swap out the database backend in future.

    Returns:
        sqlite3.Connection: An active connection to the SQLite database.
    """
    return sqlite3.connect(DB_PATH)