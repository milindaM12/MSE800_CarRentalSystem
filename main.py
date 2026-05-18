"""
main.py - Entry point for the Car Rental System.

This CLI application provides a menu-driven interface for two user roles:
    - Admin: manage cars and bookings (add, update, delete, approve/reject)
    - Customer: browse cars, make bookings, view booking history

Innovative Feature:
    LOYALTY POINTS SYSTEM — customers earn 10 points per rental day.
    Accumulated points are displayed on login and can be redeemed
    for discounts (100 points = $5 off next rental fee).

Usage:
    python main.py

Author: [Yasas Milinda Manamperi]
Version: 1.1.0
"""

from services.car_service import CarService
from services.user_service import UserService
from services.booking_service import BookingService
from models.car import Car
from models.booking import Booking
from data.init_db import init_db
from data.db import get_connection


# ─────────────────────────────────────────────
# Innovative Feature: Loyalty Points System
# ─────────────────────────────────────────────

def get_loyalty_points(username: str) -> int:
    """
    Retrieve the total loyalty points earned by a customer.

    Points are calculated from all APPROVED bookings:
    10 points per rental day.

    Args:
        username (str): The customer's username.

    Returns:
        int: Total loyalty points accumulated.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT SUM(days) FROM bookings WHERE username=? AND status='APPROVED'",
        (username,)
    )
    result = cursor.fetchone()[0]
    conn.close()
    total_days = result if result else 0
    return total_days * 10  # 10 points per day


def apply_loyalty_discount(points: int, fee: float) -> tuple[float, int]:
    """
    Apply a loyalty points discount to a rental fee.

    100 points = $5 discount. Points are consumed in multiples of 100.

    Args:
        points (int): Available loyalty points.
        fee (float): Original rental fee.

    Returns:
        tuple[float, int]: (discounted_fee, points_used)
    """
    redeemable_sets = points // 100
    discount = redeemable_sets * 5.0
    discount = min(discount, fee)  # Cannot discount more than the total fee
    points_used = int(discount / 5) * 100
    return max(0.0, fee - discount), points_used


# ─────────────────────────────────────────────
# Fee Calculation
# ─────────────────────────────────────────────

def calculate_rental_fee(car: Car, days: int) -> float:
    """
    Calculate the total rental fee.

    Args:
        car (Car): The car being rented.
        days (int): Number of rental days.

    Returns:
        float: Total rental fee.

    Raises:
        ValueError: If days is outside the car's allowed rental period.
    """
    if days < car.get_min_days() or days > car.get_max_days():
        raise ValueError(
            f"Invalid rental duration. Must be between "
            f"{car.get_min_days()} and {car.get_max_days()} days."
        )
    return car.get_price() * days


# ─────────────────────────────────────────────
# Main Application
# ─────────────────────────────────────────────

def main():
    """
    Main application loop providing the CLI menu interface.

    Initialises the database, then enters a loop offering
    Register, Login, and Exit options. After login, routes
    to the appropriate role menu (admin or customer).
    """
    init_db()

    # Instantiate service layer objects
    car_service = CarService()
    user_service = UserService()
    booking_service = BookingService()

    while True:
        print("\n" + "=" * 40)
        print("   Welcome To The Car Rental System")
        print("=" * 40)
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        try:
            choice = int(input("Enter choice: "))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        # ─── REGISTER ───
        if choice == 1:
            username = input("Username: ").strip()
            password = input("Password: ").strip()
            role = input("Role (admin/customer): ").strip().lower()

            user = user_service.register(username, password, role)
            if user:
                print("✓ Registered successfully!")

        # ─── LOGIN ───
        elif choice == 2:
            username = input("Username: ").strip()
            password = input("Password: ").strip()

            user = user_service.login(username, password)
            if not user:
                print("✗ Invalid login. Please try again.")
                continue

            print(f"\n✓ Welcome, {username}! (Role: {user.get_role()})")

            # ════════════════ ADMIN MENU ════════════════
            if user.get_role() == "admin":
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Add Car")
                    print("2. View Cars")
                    print("3. Update Car")
                    print("4. Delete Car")
                    print("5. View All Bookings")
                    print("6. Approve Booking")
                    print("7. Reject Booking")
                    print("8. Logout")

                    try:
                        choice = int(input("Enter choice: "))
                    except ValueError:
                        print("Invalid input.")
                        continue

                    # --- Add Car ---
                    if choice == 1:
                        try:
                            car = Car(
                                input("Brand: ").strip(),
                                input("Model: ").strip(),
                                int(input("Year: ")),
                                int(input("Mileage (km): ")),
                                float(input("Price per day ($): ")),
                                int(input("Min rental days: ")),
                                int(input("Max rental days: "))
                            )
                            car_service.add_car(car)
                            print("✓ Car added successfully!")
                        except ValueError as e:
                            print(f"✗ Error: {e}")

                    # --- View Cars ---
                    elif choice == 2:
                        car_service.get_all_cars()

                    # --- Update Car ---
                    elif choice == 3:
                        car_id = input("Enter Car ID to update: ").strip()
                        car = car_service.get_car_by_id(car_id)
                        if not car:
                            print("✗ Car not found.")
                            continue
                        print(f"Updating: {car.get_details()}")
                        try:
                            brand = input(f"Brand [{car._brand}]: ").strip() or car._brand
                            model = input(f"Model [{car._model}]: ").strip() or car._model
                            year = input(f"Year [{car._year}]: ").strip()
                            year = int(year) if year else car._year
                            mileage = input(f"Mileage [{car._mileage}]: ").strip()
                            mileage = int(mileage) if mileage else car._mileage
                            price = input(f"Price/day [{car._price_per_day}]: ").strip()
                            price = float(price) if price else car._price_per_day
                            min_d = input(f"Min days [{car._min_days}]: ").strip()
                            min_d = int(min_d) if min_d else car._min_days
                            max_d = input(f"Max days [{car._max_days}]: ").strip()
                            max_d = int(max_d) if max_d else car._max_days

                            success = car_service.update_car(
                                car_id, brand, model, year, mileage, price, min_d, max_d
                            )
                            print("✓ Car updated!" if success else "✗ Update failed.")
                        except ValueError as e:
                            print(f"✗ Error: {e}")

                    # --- Delete Car ---
                    elif choice == 4:
                        car_id = input("Enter Car ID to delete: ").strip()
                        car_service.delete_car(car_id)

                    # --- View All Bookings ---
                    elif choice == 5:
                        booking_service.view_bookings()

                    # --- Approve Booking ---
                    elif choice == 6:
                        booking_id = input("Enter Booking ID to approve: ").strip()
                        success = booking_service.update_status(booking_id, "APPROVED")
                        print("✓ Booking approved!" if success else "✗ Booking not found.")

                    # --- Reject Booking ---
                    elif choice == 7:
                        booking_id = input("Enter Booking ID to reject: ").strip()
                        success = booking_service.update_status(booking_id, "REJECTED")
                        if success:
                            print("✓ Booking rejected. Car availability restored.")
                        else:
                            print("✗ Booking not found.")

                    elif choice == 8:
                        print("Logged out.")
                        break

            # ════════════════ CUSTOMER MENU ════════════════
            elif user.get_role() == "customer":

                # Show loyalty points on login (Innovative Feature)
                points = get_loyalty_points(username)
                print(f"★ Loyalty Points: {points} pts "
                      f"(Redeem 100 pts = $5 off your next booking)")

                while True:
                    print("\n--- Customer Menu ---")
                    print("1. View Available Cars")
                    print("2. Book a Car")
                    print("3. View My Bookings")
                    print("4. Logout")

                    try:
                        choice = int(input("Enter choice: "))
                    except ValueError:
                        print("Invalid input.")
                        continue

                    # --- View Cars ---
                    if choice == 1:
                        car_service.get_all_cars()

                    # --- Book Car ---
                    elif choice == 2:
                        try:
                            car_id = input("Enter Car ID: ").strip()
                            car = car_service.get_car_by_id(car_id)

                            if not car:
                                print("✗ Car not found.")
                                continue

                            if not car.is_available():
                                print("✗ This car is currently unavailable.")
                                continue

                            days = int(input("Number of rental days: "))
                            start_date = input("Start date (YYYY-MM-DD, or press Enter for today): ").strip()

                            # Calculate fee
                            fee = calculate_rental_fee(car, days)
                            print(f"\n  Car: {car._brand} {car._model}")
                            print(f"  Duration: {days} day(s)")
                            print(f"  Base Fee: ${fee:.2f}")

                            # Innovative Feature: Offer loyalty points redemption
                            points = get_loyalty_points(username)
                            if points >= 100:
                                use_points = input(
                                    f"\n  You have {points} loyalty points. "
                                    f"Redeem for discount? (y/n): "
                                ).strip().lower()
                                if use_points == "y":
                                    fee, points_used = apply_loyalty_discount(points, fee)
                                    print(f" ✓ {points_used} points redeemed. "
                                          f"Discounted Fee: ${fee:.2f}")

                            confirm = input(f"\n  Confirm booking for ${fee:.2f}? (y/n): ").strip().lower()
                            if confirm != "y":
                                print("Booking cancelled.")
                                continue

                            # Create and save the booking
                            booking = Booking(
                                username=username,
                                car_id=car_id,
                                days=days,
                                start_date=start_date if start_date else None
                            )
                            booking_service.create_booking(booking)

                            # Mark car as unavailable
                            car_service.update_availability(car_id, False)

                            print("✓ Booking created! Awaiting admin approval.")

                        except ValueError as e:
                            print(f"✗ Error: {e}")

                    # --- View My Bookings ---
                    elif choice == 3:
                        booking_service.get_bookings_by_user(username)

                    elif choice == 4:
                        print("Logged out.")
                        break

        elif choice == 3:
            print("\nThank you for using the Car Rental System. Goodbye!")
            break


# ─────────────────────────────────────────────
# Application Entry Point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExited safely.")
