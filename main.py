from services.car_service import CarService
from services.user_service import UserService
from services.booking_service import BookingService
from models.car import Car
from models.booking import Booking
from data.init_db import init_db


def calculate_rental_fee(car, days):
    if days < car.get_min_days() or days > car.get_max_days():
        raise ValueError("Invalid rental duration")
    return car.get_price() * days


def main():
    init_db()

    car_service = CarService()
    user_service = UserService()
    booking_service = BookingService()

    while True:
        print("\n--- Welcome To The Car Rental Company---")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        try:
            choice = int(input("Enter choice: "))
        except:
            print("Invalid input")
            continue

        # ---------------- REGISTER ----------------
        if choice == 1:
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (admin/customer): ")

            user = user_service.register(username, password, role)
            if user:
                print("Registered successfully!")

        # ---------------- LOGIN ----------------
        elif choice == 2:
            username = input("Username: ")
            password = input("Password: ")

            user = user_service.login(username, password)
            if not user:
                print("Invalid login")
                continue

            print(f"Welcome {username} ({user.get_role()})")

            # ================= ADMIN MENU =================
            if user.get_role() == "admin":
                while True:
                    print("\n--- Admin Menu ---")
                    print("1. Add Car")
                    print("2. View Cars")
                    print("3. Delete Car")
                    print("4. View Bookings")
                    print("5. Approve Booking")
                    print("6. Logout")

                    try:
                        choice = int(input("Enter choice: "))
                    except:
                        print("Invalid input")
                        continue

                    # Add Car
                    if choice == 1:
                        try:
                            car = Car(
                                # input("ID: "),
                                input("Brand: "),
                                input("Model: "),
                                int(input("Year: ")),
                                int(input("Mileage: ")),
                                float(input("Price per day: ")),
                                int(input("Min days: ")),
                                int(input("Max days: "))
                            )
                            car_service.add_car(car)
                            print("Car added!")
                        except:
                            print("Error adding car")

                    # View Cars
                    elif choice == 2:
                        car_service.get_all_cars()

                    # Delete Car
                    elif choice == 3:
                        car_id = input("Enter Car ID: ")
                        car_service.delete_car(car_id)

                    # View Bookings
                    elif choice == 4:
                        booking_service.view_bookings()

                    # Approve Booking (FIXED)
                    # elif choice == 5:
                    #     booking_id = input("Enter Booking ID: ")
                    #     booking_service.update_status(booking_id, "APPROVED")
                    #     print("Booking approved!")
                    elif choice == 5:
                        booking_id = input("Enter Booking ID: ")
                        success = booking_service.update_status(booking_id, "APPROVED")
                        if success:
                            print("Booking approved!")
                        else:
                            print("Booking not found.")

                    elif choice == 6:
                        break

            # ================= CUSTOMER MENU =================
            elif user.get_role() == "customer":
                while True:
                    print("\n--- Customer Menu ---")
                    print("1. View Cars")
                    print("2. Book Car")
                    print("3. View Bookings")
                    print("4. Logout")

                    try:
                        choice = int(input("Enter choice: "))
                    except:
                        print("Invalid input")
                        continue

                    # View Cars
                    if choice == 1:
                        car_service.get_all_cars()

                    # Book Car (FIXED)
                    elif choice == 2:
                        try:
                            car_id = input("Car ID: ")
                            # days = int(input("Number of days: "))

                            car = car_service.get_car_by_id(car_id)

                            if not car:
                                print("Car not found")
                                continue

                            days = int(input("Number of days: "))  # only asked if car exists

                            if not car.is_available():
                                print("Car is not available")
                                continue

                            fee = calculate_rental_fee(car, days)
                            print(f"Total Fee: ${fee}")

                            booking = Booking(
                                username=username,
                                car_id=car_id,
                                days=days
                            )

                            booking_service.create_booking(booking)

                            # mark car unavailable
                            car_service.update_availability(car_id, False)

                            print("Booking created! Waiting for approval.")

                        except Exception as e:
                            print("Error:", e)

                    # View Bookings (OPTIONAL IMPROVEMENT)
                    elif choice == 3:
                        booking_service.get_bookings_by_user(username)

                    elif choice == 4:
                        break

        elif choice == 3:
            print("Exiting from the system...")
            break


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nExited safely.")