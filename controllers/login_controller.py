from data.database import Database

class LoginController:
    def __init__(self):
        self.db = Database()

    def login(self, username, password):
        user = self.db.get_user(username, password)
        # Imprimir información del usuario para debugging
        print(f"Intento de inicio de sesión: {username}, contraseña: {password}")

        if user:
            # Asegúrate de que los índices son correctos
            return {"username": user[1], "role": user[3]}  # user[1] es el nombre de usuario, user[3] es el rol
        else:
            return {"error": "Usuario o contraseña incorrectos"}

    def close(self):
        self.db.close()
