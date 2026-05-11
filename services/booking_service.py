"""
booking_service.py - Service layer for booking management in the Car Rental System.

Handles all business logic and database operations related to rental bookings,
including creation, retrieval, status updates (approve/reject), and fee calculation.
"""

from models.booking import Booking
from models.car import Car
from data.db import get_connection


class BookingService:
    """
    Provides business logic for managing rental bookings.

    Responsibilities:
        - Creating new bookings
        - Viewing all bookings (admin) or per-user bookings (customer)
        - Approving or rejecting bookings (admin)
        - Calculating rental fees
    """

    def create_booking(self, booking: Booking) -> None:
        """
        Persist a new booking record to the database.

        The booking is saved with a 'PENDING' status awaiting admin approval.

        Args:
            booking (Booking): The Booking object containing rental details.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bookings (username, car_id, days, start_date, status)
        VALUES (?, ?, ?, ?, ?)
        """, (
            booking.get_username(),
            booking.get_car_id(),
            booking.get_days(),
            booking.get_start_date(),
            "PENDING"
        ))

        conn.commit()
        conn.close()
        print("[BookingService] Booking created successfully.")

    def view_bookings(self) -> None:
        """
        Display all bookings in the system (admin function).

        Prints each booking's ID, customer, car, duration, dates,
        and current status to the console.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No bookings found.")
            return

        print("\n--- All Bookings ---")
        for r in rows:
            print({
                "booking_id": r[0],
                "username": r[1],
                "car_id": r[2],
                "days": r[3],
                "start_date": r[4],
                "status": r[5]
            })

    def get_bookings_by_user(self, username: str) -> None:
        """
        Display all bookings belonging to a specific customer.

        Args:
            username (str): The customer's username to filter bookings by.
        """
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM bookings WHERE username=?",
            (username,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("You have no bookings.")
            return

        print(f"\n--- Bookings for '{username}' ---")
        for r in rows:
            print({
                "booking_id": r[0],
                "car_id": r[2],
                "days": r[3],
                "start_date": r[4],
                "status": r[5]
            })

    def update_status(self, booking_id: str, status: str) -> bool:
        """
        Update the status of a booking (approve or reject).

        Valid statuses are 'APPROVED' and 'REJECTED'. When a booking
        is rejected, the car is automatically made available again.

        Args:
            booking_id (str): The ID of the booking to update.
            status (str): New status — 'APPROVED' or 'REJECTED'.

        Returns:
            bool: True if the update succeeded, False if booking not found.
        """
        if status not in ("APPROVED", "REJECTED"):
            print(f"[BookingService] Invalid status '{status}'.")
            return False

        conn = get_connection()
        cursor = conn.cursor()

        # Fetch the booking to get the car_id for availability reset
        cursor.execute("SELECT car_id FROM bookings WHERE id=?", (booking_id,))
        row = cursor.fetchone()

        if not row:
            conn.close()
            return False

        car_id = row[0]

        # Update the booking status
        cursor.execute(
            "UPDATE bookings SET status=? WHERE id=?",
            (status, booking_id)
        )

        # If rejected, restore car availability
        if status == "REJECTED":
            cursor.execute(
                "UPDATE cars SET available=1 WHERE id=?",
                (car_id,)
            )
            print(f"[BookingService] Car {car_id} is now available again.")

        conn.commit()
        updated = cursor.rowcount > 0
        conn.close()

        return updated

    def calculate_rental_fee(self, car: Car, days: int) -> float:
        """
        Calculate the total rental fee for a given car and duration.

        Args:
            car (Car): The car being rented.
            days (int): Number of rental days.

        Returns:
            float: Total rental cost.

        Raises:
            ValueError: If the rental duration is outside the car's allowed range.
        """
        if days < car.get_min_days() or days > car.get_max_days():
            raise ValueError(
                f"Rental duration must be between {car.get_min_days()} "
                f"and {car.get_max_days()} days."
            )
        return car.get_price() * days
