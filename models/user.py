"""
user.py - User model class for the Car Rental System.

Represents a system user with role-based access (admin or customer).
Encapsulates credentials and role logic.
"""


class User:
    """
    Represents a system user with authentication and role attributes.

    Demonstrates encapsulation by protecting username, password, and role
    behind getter methods.

    Attributes:
        _username (str): The user's unique login name.
        _password (str): The user's password (stored as plain text; 
                         in production, use hashed passwords).
        _role (str): Either 'admin' or 'customer'.
    """

    def __init__(self, username: str, password: str, role: str):
        """
        Initialise a User instance.

        Args:
            username (str): Unique username for login.
            password (str): User's password.
            role (str): User role — 'admin' or 'customer'.
        """
        self._username = username
        self._password = password
        self._role = role

    # -------------------- Getters --------------------

    def get_username(self) -> str:
        """Return the user's username."""
        return self._username

    def get_role(self) -> str:
        """Return the user's role ('admin' or 'customer')."""
        return self._role

    def check_password(self, password: str) -> bool:
        """
        Verify if the given password matches the stored password.

        Args:
            password (str): Password to verify.

        Returns:
            bool: True if the password matches.
        """
        return self._password == password

    # -------------------- Serialisation --------------------

    def to_dict(self) -> dict:
        """
        Serialise the User to a dictionary.

        Returns:
            dict: User data suitable for storage.
        """
        return {
            "username": self._username,
            "password": self._password,
            "role": self._role
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        """
        Deserialise a dictionary into a User object.

        Args:
            data (dict): Dictionary with user fields.

        Returns:
            User: Reconstructed User instance.
        """
        return User(data["username"], data["password"], data["role"])
