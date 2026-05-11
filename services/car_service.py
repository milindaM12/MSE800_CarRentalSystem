"""
car_service.py - Service layer for car management in the Car Rental System.

Handles all business logic and database operations related to cars,
including CRUD operations and availability management.

Design Pattern: Service Layer — separates business logic from UI (main.py)
and data access (db.py).
"""

from data.db import get_connection
from models.car import Car


class CarService:
    """
    Provides business logic for managing rental cars.

    Responsibilities:
        - Adding new cars to the inventory
        - Retrieving car records (all or by ID)
        - Updating car details and availability
        - Deleting cars from inventory
    """

    def add_car(self, car: Car) -> None:
        """
        Add a new car to the database inventory.

        Auto-generates a sequential car ID based on existing record count.

        Args:
            car (Car): The Car object to be added.
        """
        conn = get_connection()
        cursor = conn.cursor()

        # Auto-generate a sequential ID
        cursor.execute("SELECT COUNT(*) FROM cars")
        count = cursor.fetchone()[0]
        new_id = str(count + 1)

        cursor.execute("""
        INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id,
            car._brand,
            car._model,
            car._year,
            car._mileage,
            car._price_per_day,
            car._min_days,
            car._max_days,
            1  # available = True by default
        ))

        conn.commit()
        conn.close()
        print(f"[CarService] Car added with ID: {new_id}")

    def get_all_cars(self) -> None:
        """
        Retrieve and display all cars in the inventory.

        Prints each car's details to the console. If no cars exist,
        a message is displayed instead.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No cars available.")
            return

        print("\n--- Car Inventory ---")
        for r in rows:
            car = Car(
                r[1], r[2], r[3], r[4], r[5], r[6], r[7],
                car_id=r[0]
            )
            # Restore availability from DB (0 = not available)
            if r[8] == 0:
                car.rent()
            print(car.get_details())

    def get_car_by_id(self, car_id: str) -> Car | None:
        """
        Retrieve a single car by its unique ID.

        Args:
            car_id (str): The unique identifier of the car.

        Returns:
            Car: The matching Car object, or None if not found.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        r = cursor.fetchone()
        conn.close()

        if not r:
            return None

        car = Car(
            r[1], r[2], r[3], r[4], r[5], r[6], r[7],
            car_id=r[0]
        )
        if r[8] == 0:
            car.rent()
        return car

    def update_car(self, car_id: str, brand: str, model: str, year: int,
                   mileage: int, price: float, min_days: int, max_days: int) -> bool:
        """
        Update the details of an existing car record.

        Args:
            car_id (str): ID of the car to update.
            brand (str): New brand name.
            model (str): New model name.
            year (int): New year of manufacture.
            mileage (int): New mileage.
            price (float): New price per day.
            min_days (int): New minimum rental days.
            max_days (int): New maximum rental days.

        Returns:
            bool: True if a record was updated, False if car not found.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        UPDATE cars
        SET brand=?, model=?, year=?, mileage=?, price=?, min_days=?, max_days=?
        WHERE id=?
        """, (brand, model, year, mileage, price, min_days, max_days, car_id))

        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()
        return updated

    def update_availability(self, car_id: str, available: bool) -> None:
        """
        Update the availability status of a car.

        Args:
            car_id (str): ID of the car to update.
            available (bool): True to mark as available, False for unavailable.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cars SET available=? WHERE id=?",
            (1 if available else 0, car_id)
        )

        conn.commit()
        conn.close()

    def delete_car(self, car_id: str) -> bool:
        """
        Remove a car from the inventory.

        Args:
            car_id (str): ID of the car to delete.

        Returns:
            bool: True if a record was deleted, False if not found.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))

        conn.commit()
        deleted = cursor.rowcount > 0
        conn.close()

        if deleted:
            print(f"[CarService] Car {car_id} deleted successfully.")
        else:
            print(f"[CarService] Car {car_id} not found.")

        return deleted
