# controllers/login_controller.py
import hashlib
from data.database import create_connection

class LoginController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user(self, username, password):
        hashed_password = self.hash_password(password)
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, role FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        result = cursor.fetchone()
        return result  # Retorna (user_id, role) o None si no es válido

    def close_connection(self):
        if self.conn:
            self.conn.close()
