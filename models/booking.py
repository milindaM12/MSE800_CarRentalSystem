"""
booking.py - Booking model class for the Car Rental System.

Represents a car rental booking made by a customer,
including rental period and approval status.
"""

from datetime import date


class Booking:
    """
    Represents a rental booking in the Car Rental System.

    Encapsulates all booking details including customer identity,
    chosen car, rental duration, dates, and admin-managed status.

    Attributes:
        username (str): Username of the customer making the booking.
        car_id (str): ID of the car being booked.
        days (int): Number of rental days.
        start_date (str): Rental start date (YYYY-MM-DD format).
        status (str): Booking status — 'PENDING', 'APPROVED', or 'REJECTED'.
    """

    # Valid status transitions
    VALID_STATUSES = {"PENDING", "APPROVED", "REJECTED"}

    def __init__(self, username: str, car_id: str, days: int,
                 start_date: str = None, status: str = "PENDING"):
        """
        Initialise a Booking instance.

        Args:
            username (str): Customer's username.
            car_id (str): The ID of the car being booked.
            days (int): Duration of the rental in days.
            start_date (str, optional): Start date as 'YYYY-MM-DD'.
                                        Defaults to today's date.
            status (str, optional): Initial booking status. Defaults to 'PENDING'.
        """
        self.username = username
        self.car_id = car_id
        self.days = days
        self.start_date = start_date or str(date.today())
        self.status = status if status in self.VALID_STATUSES else "PENDING"

    # -------------------- Getters --------------------

    def get_username(self) -> str:
        """Return the booking customer's username."""
        return self.username

    def get_car_id(self) -> str:
        """Return the booked car's ID."""
        return self.car_id

    def get_days(self) -> int:
        """Return the number of rental days."""
        return self.days

    def get_start_date(self) -> str:
        """Return the rental start date."""
        return self.start_date

    def get_status(self) -> str:
        """Return the current booking status."""
        return self.status

    # -------------------- Serialisation --------------------

    def to_dict(self) -> dict:
        """
        Serialise the Booking to a dictionary.

        Returns:
            dict: Booking data suitable for storage.
        """
        return {
            "username": self.username,
            "car_id": self.car_id,
            "days": self.days,
            "start_date": self.start_date,
            "status": self.status
        }

    @staticmethod
    def from_dict(data: dict) -> "Booking":
        """
        Deserialise a dictionary into a Booking object.

        Args:
            data (dict): Dictionary with booking fields.

        Returns:
            Booking: Reconstructed Booking instance.
        """
        return Booking(
            username=data["username"],
            car_id=data["car_id"],
            days=data["days"],
            start_date=data.get("start_date"),
            status=data.get("status", "PENDING")
        )
