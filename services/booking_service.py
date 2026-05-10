import json
from models import booking
from models.booking import Booking
from data.db import get_connection

class BookingService:
    # def __init__(self):
    #     self.file_path = file_path
    #     self.bookings = self.load_bookings()

    def get_bookings_by_user(self, username):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM bookings WHERE username=?",
            (username,)
        )
        rows = cursor.fetchall()
        conn.close()

        if not rows:
            print("No bookings found.")
            return

        for r in rows:
            print({
                "booking_id": r[0],
                "username": r[1],
                "car_id": r[2],
                "days": r[3],
                "status": r[4]
            })    

    def generate_booking_id(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM bookings")
        count = cursor.fetchone()[0]

        conn.close()
        return str(count + 1)    

    def load_bookings(self):
        try:
            with open(self.file_path, "r") as f:
                return [Booking.from_dict(b) for b in json.load(f)]
        except:
            return []

    def save_bookings(self):
        with open(self.file_path, "w") as f:
            json.dump([b.to_dict() for b in self.bookings], f, indent=4)

    # def create_booking(self, booking):
    #     self.bookings.append(booking)
    #     self.save_bookings()

    def create_booking(self, booking):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO bookings (username, car_id, days, status)
        VALUES (?, ?, ?, ?)
        """, (
            booking.get_username(),
            booking.get_car_id(),
            booking.get_days(),
            "PENDING"
        ))

        conn.commit()
        conn.close()

    # def view_bookings(self):
    #     for b in self.bookings:
    #         print(vars(b))

    def view_bookings(self):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM bookings")
        rows = cursor.fetchall()

        conn.close()

        for r in rows:
            print({
                "booking_id": r[0],  # auto ID
                "username": r[1],
                "car_id": r[2],
                "days": r[3],
                "status": r[4]
            })

    # def update_status(self, booking_id, status):
    #     for b in self.bookings:
    #         if b.booking_id == booking_id:
    #             b.status = status
    #             self.save_bookings()
    #             return

    # def update_status(self, booking_id, status):
    #     conn = get_connection()
    #     cursor = conn.cursor()

    #     cursor.execute(
    #         "UPDATE bookings SET status=? WHERE id=?",
    #         (status, booking_id)
    #     )

    #     conn.commit()
    #     conn.close()

    def update_status(self, booking_id, status):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE bookings SET status=? WHERE id=?",
            (status, booking_id)
        )

        conn.commit()
        conn.close()

        return cursor.rowcount > 0  # True if a row was updated, False if not found    
            
    def calculate_rental_fee(self, car, days):
        if days < car.get_min_days() or days > car.get_max_days():
            raise ValueError("Invalid rental duration")

        return car.get_price() * days