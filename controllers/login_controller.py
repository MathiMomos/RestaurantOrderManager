# controllers/login_controller.py
#perdon por la demora :v
import hashlib
from data.database import create_connection

class LoginController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def hash_password(self, password):
        return hashlib.sha256(password.encode()).hexdigest()

    def validate_user(self, username, password):
        if not username or not password:
            return {'status': 'error', 'message': 'Por favor, ingresa tu usuario y contraseña.'}

        hashed_password = self.hash_password(password)
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id, role FROM users WHERE username = ? AND password = ?",
            (username, hashed_password)
        )
        result = cursor.fetchone()
        if result:
            return {'status': 'success', 'user_id': result[0], 'role': result[1]}
        else:
            return {'status': 'error', 'message': 'Usuario o contraseña incorrectos.'}

    def close_connection(self):
        if self.conn:
            self.conn.close()
