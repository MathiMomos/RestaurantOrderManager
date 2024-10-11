from data.database import Database

class LoginController:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        user = self.db.get_user(username, password)
        print(f"Intento de inicio de sesión: {username}, contraseña: {password}")

        if user:
            return {"username": user[1], "role": user[3]}
        else:
            return {"error": "Usuario o contraseña incorrectos"}

    def close(self):
        self.db.close()
