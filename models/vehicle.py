"""
vehicle.py - Abstract base class for all vehicle types in the Car Rental System.

This module defines the Vehicle base class using OOP principles including
abstraction and encapsulation.
"""


class Vehicle:
    """
    Abstract base class representing a generic vehicle.

    Attributes:
        _vehicle_id (str): Unique identifier for the vehicle.
        _brand (str): Brand/make of the vehicle.
        _model (str): Model name of the vehicle.
        _price_per_day (float): Daily rental price.
    """

    def __init__(self, brand: str, model: str, price_per_day: float, vehicle_id: str = None):
        """
        Initialise a Vehicle instance.

        Args:
            brand (str): The vehicle brand/make.
            model (str): The vehicle model name.
            price_per_day (float): Daily rental cost.
            vehicle_id (str, optional): Unique vehicle ID. Defaults to None.
        """
        self._vehicle_id = vehicle_id
        self._brand = brand
        self._model = model
        self._price_per_day = price_per_day

    def get_id(self) -> str:
        """Return the vehicle's unique ID."""
        return self._vehicle_id

    def get_details(self) -> str:
        """
        Return a string representation of the vehicle's details.
        Must be implemented by subclasses.

        Raises:
            NotImplementedError: If not overridden in a subclass.
        """
        raise NotImplementedError("Subclasses must implement get_details()")
