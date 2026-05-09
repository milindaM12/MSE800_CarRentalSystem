class User:
    def __init__(self, username, password, role):
        self._username = username
        self._password = password
        self._role = role  # admin or customer

    def get_username(self):
        return self._username

    def get_role(self):
        return self._role

    def check_password(self, password):
        return self._password == password

    def to_dict(self):
        return {
            "username": self._username,
            "password": self._password,
            "role": self._role
        }

    @staticmethod
    def from_dict(data):
        return User(data["username"], data["password"], data["role"])