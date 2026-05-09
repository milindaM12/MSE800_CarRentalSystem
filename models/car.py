from models.vehicle import Vehicle

class Car(Vehicle):
    def __init__(self, car_id, brand, model, year, mileage, price_per_day, min_days, max_days):
        super().__init__(car_id, brand, model, price_per_day)
        self._year = year
        self._mileage = mileage
        self._min_days = min_days
        self._max_days = max_days
        self.__is_available = True

    def get_details(self):
        status = "Available" if self.__is_available else "Not Available"
        return (
            f"ID: {self._vehicle_id} | {self._brand} {self._model} ({self._year}) | "
            f"Mileage: {self._mileage} | ${self._price_per_day}/day | "
            f"Min:{self._min_days} Max:{self._max_days} | {status}"
        )

    def is_available(self):
        return self.__is_available

    def get_price(self):
        return self._price_per_day

    def get_min_days(self):
        return self._min_days

    def get_max_days(self):
        return self._max_days
    
    def rent(self):
        if self.__is_available:
            self.__is_available = False
            return True
        return False

    def return_car(self):
        self.__is_available = True

    def to_dict(self):
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
    def from_dict(data):
        car = Car(
            data["id"], data["brand"], data["model"],
            data["year"], data["mileage"],
            data["price"], data["min_days"], data["max_days"]
        )
        car.__is_available = data["available"]
        return car