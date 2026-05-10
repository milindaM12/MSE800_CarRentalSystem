class Booking:

    def __init__(self, username, car_id, days, status="PENDING"):
        self.username = username
        self.car_id = car_id
        self.days = days
        self.status = status

    def get_username(self): return self.username
    def get_car_id(self):   return self.car_id
    def get_days(self):     return self.days
    def get_status(self):   return self.status        

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Booking(**data)