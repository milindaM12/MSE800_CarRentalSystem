"""
car.py - Car model class for the Car Rental System.

Inherits from Vehicle and adds car-specific attributes like year,
mileage, rental duration constraints, and availability tracking.
"""

from models.vehicle import Vehicle


class Car(Vehicle):
    """
    Represents a rental car, extending the Vehicle base class.

    Demonstrates OOP principles:
        - Inheritance (from Vehicle)
        - Encapsulation (private __is_available with name mangling)
        - Polymorphism (overrides get_details)

    Attributes:
        _year (int): Manufacturing year of the car.
        _mileage (int): Current mileage on the car.
        _min_days (int): Minimum rental duration in days.
        _max_days (int): Maximum rental duration in days.
        __is_available (bool): Availability flag (private).
    """

    def __init__(self, brand: str, model: str, year: int, mileage: int,
                 price_per_day: float, min_days: int, max_days: int,
                 car_id: str = None):
        """
        Initialise a Car instance.

        Args:
            brand (str): Car brand/make.
            model (str): Car model name.
            year (int): Year of manufacture.
            mileage (int): Current mileage.
            price_per_day (float): Daily rental price.
            min_days (int): Minimum rental period in days.
            max_days (int): Maximum rental period in days.
            car_id (str, optional): Unique car identifier.
        """
        super().__init__(brand, model, price_per_day, car_id)
        self._year = year
        self._mileage = mileage
        self._min_days = min_days
        self._max_days = max_days
        self.__is_available = True  # Private: use name mangling for encapsulation

    # -------------------- Getters --------------------

    def get_price(self) -> float:
        """Return the daily rental price."""
        return self._price_per_day

    def get_min_days(self) -> int:
        """Return the minimum rental duration in days."""
        return self._min_days

    def get_max_days(self) -> int:
        """Return the maximum rental duration in days."""
        return self._max_days

    def get_year(self) -> int:
        """Return the manufacturing year."""
        return self._year

    def get_mileage(self) -> int:
        """Return the current mileage."""
        return self._mileage

    def is_available(self) -> bool:
        """Return True if the car is available for rental."""
        return self.__is_available

    # -------------------- Polymorphic Method --------------------

    def get_details(self) -> str:
        """
        Return a formatted string of car details.

        Returns:
            str: Human-readable car information including availability status.
        """
        status = "Available" if self.__is_available else "Not Available"
        return (
            f"ID: {self._vehicle_id} | {self._brand} {self._model} ({self._year}) | "
            f"Mileage: {self._mileage} km | ${self._price_per_day:.2f}/day | "
            f"Min: {self._min_days} day(s) | Max: {self._max_days} day(s) | {status}"
        )

    # -------------------- State Management --------------------

    def rent(self) -> bool:
        """
        Mark the car as rented (unavailable).

        Returns:
            bool: True if successfully rented, False if already unavailable.
        """
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    def return_car(self) -> None:
        """Mark the car as returned (available)."""
        self.__is_available = True

    # -------------------- Serialisation --------------------

    def to_dict(self) -> dict:
        """
        Serialise the Car object to a dictionary.

        Returns:
            dict: Car data suitable for database storage.
        """
        return {
            "id": self._vehicle_id,
            "brand": self._brand,
            "model": self._model,
            "year": self._year,
            "mileage": self._mileage,
            "price": self._price_per_day,
            "min_days": self._min_days,
            "max_days": self._max_days,
            "available": self.__is_available
        }

    @staticmethod
    def from_dict(data: dict) -> "Car":
        """
        Deserialise a dictionary into a Car object.

        Args:
            data (dict): Dictionary containing car field values.

        Returns:
            Car: A reconstructed Car instance.
        """
        car = Car(
            data["brand"], data["model"],
            data["year"], data["mileage"],
            data["price"], data["min_days"], data["max_days"],
            car_id=data["id"]
        )
        # Access private attribute via name-mangled key
        car._Car__is_available = bool(data["available"])
        return car
