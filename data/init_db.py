"""
init_db.py - Database initialisation script for the Car Rental System.

Creates all required tables if they do not already exist.
Should be called once at application startup via main.py.
"""

from data.db import get_connection


def init_db() -> None:
    """
    Initialise the SQLite database by creating all required tables.

    Tables created:
        - cars: Stores vehicle inventory details.
        - users: Stores user credentials and roles.
        - bookings: Stores rental booking records.

    This function is idempotent — safe to call multiple times.
    """
    conn = get_connection()
    cursor = conn.cursor()

    # --- Cars table: vehicle inventory ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS cars (
        id TEXT PRIMARY KEY,
        brand TEXT NOT NULL,
        model TEXT NOT NULL,
        year INTEGER NOT NULL,
        mileage INTEGER NOT NULL,
        price REAL NOT NULL,
        min_days INTEGER NOT NULL,
        max_days INTEGER NOT NULL,
        available INTEGER NOT NULL DEFAULT 1
    )
    """)

    # --- Users table: authentication and role management ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        password TEXT NOT NULL,
        role TEXT NOT NULL CHECK(role IN ('admin', 'customer'))
    )
    """)

    # --- Bookings table: rental booking records ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bookings (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        car_id TEXT NOT NULL,
        days INTEGER NOT NULL,
        start_date TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'PENDING',
        FOREIGN KEY (username) REFERENCES users(username),
        FOREIGN KEY (car_id) REFERENCES cars(id)
    )
    """)

    conn.commit()
    conn.close()
    print("[DB] Database initialised successfully.")