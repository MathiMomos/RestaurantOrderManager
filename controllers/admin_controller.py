# controllers/admin_controller.py .
import hashlib
from data.database import create_connection

class AdminController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username, password, role):
        hashed_password = self.hash_password(password)
        cursor = self.conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                           (username, hashed_password, role))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            return False

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, username, role FROM users")
        return cursor.fetchall()

    def close_connection(self):
        if self.conn:
            self.conn.close()
