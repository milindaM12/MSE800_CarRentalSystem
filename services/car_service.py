from data.db import get_connection
from models.car import Car

class CarService:
    
    def get_car_by_id(self, car_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars WHERE id=?", (car_id,))
        r = cursor.fetchone()

        conn.close()

        if not r:
            return None

        car = Car(
            r[0], r[1], r[2],
            r[3], r[4],
            r[5], r[6], r[7]
        )

        if r[8] == 0:
            car.rent()

        return car

    def add_car(self, car):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
        INSERT INTO cars VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            car.get_id(),
            car._brand,
            car._model,
            car._year,
            car._mileage,
            car._price_per_day,
            car._min_days,
            car._max_days,
            1
        ))

        conn.commit()
        conn.close()        

    def get_all_cars(self):

        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM cars")
        rows = cursor.fetchall()

        if not rows:
            print("No cars available.")
            return

        for r in rows:
            car = Car(
                r[0],  # id
                r[1],  # brand
                r[2],  # model
                r[3],  # year
                r[4],  # mileage
                r[5],  # price
                r[6],  # min_days
                r[7]   # max_days
            )

            # set availability manually
            if r[8] == 0:
                car.rent()  # mark as not available

            print(car.get_details())

        conn.close()


    def update_availability(self, car_id, available):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "UPDATE cars SET available=? WHERE id=?",
            (1 if available else 0, car_id)
        )

        conn.commit()
        conn.close()

 
    def delete_car(self, car_id):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("DELETE FROM cars WHERE id=?", (car_id,))

        conn.commit()
        conn.close()
        print("Car deleted")