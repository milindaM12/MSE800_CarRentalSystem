class Vehicle:
    def __init__(self, vehicle_id, brand, model, price_per_day):
        self._vehicle_id = vehicle_id
        self._brand = brand
        self._model = model
        self._price_per_day = price_per_day

    def get_id(self):
        return self._vehicle_id

    def get_details(self):
        raise NotImplementedError("Subclasses must implement this method")