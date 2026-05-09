from models.user import User
from data.db import get_connection


class UserService:
    # def __init__(self, file_path="data/users.json"):
    #     self.file_path = file_path
    #     self.users = self.load_users()

    def load_users(self):
        try:
            with open(self.file_path, "r") as f:
                return [User.from_dict(u) for u in json.load(f)]
        except:
            return []

    def save_users(self):
        with open(self.file_path, "w") as f:
            json.dump([u.to_dict() for u in self.users], f, indent=4)

    def register(self, username, password, role):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        if cursor.fetchone():
            print("User already exists!")
            conn.close()
            return None

        cursor.execute(
            "INSERT INTO users VALUES (?, ?, ?)",
            (username, password, role)
        )
        conn.commit()
        conn.close()
        return User(username, password, role)

    def login(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE username=? AND password=?",
            (username, password)
        )
        row = cursor.fetchone()
        conn.close()

        if not row:
            return None
        return User(row[0], row[1], row[2])