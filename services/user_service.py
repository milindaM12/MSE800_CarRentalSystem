"""
user_service.py - Service layer for user management in the Car Rental System.

Handles user registration, authentication, and retrieval.
Passwords are stored in plain text for this prototype; in production,
use bcrypt or argon2 for hashing.
"""

from models.user import User
from data.db import get_connection


class UserService:
    """
    Provides business logic for user account management.

    Responsibilities:
        - Registering new users
        - Authenticating existing users via login
    """

    def register(self, username: str, password: str, role: str) -> User | None:
        """
        Register a new user in the system.

        Validates that the username is not already taken and that
        the role is either 'admin' or 'customer'.

        Args:
            username (str): Desired username.
            password (str): User's password.
            role (str): User role — must be 'admin' or 'customer'.

        Returns:
            User: The newly created User object, or None on failure.
        """
        # Input validation
        if role not in ("admin", "customer"):
            print("[UserService] Invalid role. Must be 'admin' or 'customer'.")
            return None

        if not username.strip() or not password.strip():
            print("[UserService] Username and password cannot be empty.")
            return None

        conn = get_connection()
        cursor = conn.cursor()

        # Check for duplicate username
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            print("[UserService] Username already exists. Please choose another.")
            conn.close()
            return None

        # Insert the new user
        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        conn.close()

        print(f"[UserService] User '{username}' registered as '{role}'.")
        return User(username, password, role)

    def login(self, username: str, password: str) -> User | None:
        """
        Authenticate a user by username and password.

        Args:
            username (str): The user's login name.
            password (str): The user's password.

        Returns:
            User: The authenticated User object, or None if credentials are invalid.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            print("[UserService] Invalid username or password.")
            return None

        return User(row[0], row[1], row[2])
