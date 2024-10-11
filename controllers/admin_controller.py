from data.database import Database
#a
class AdminController:
    def __init__(self):
        self.db = Database()

    def create_user(self, role):
        try:
            count = self.db.get_user_count(role)
            username = f"{role}{count + 1}"
            password = f"{role}{count + 1}pass"
            success = self.db.create_user(username, password, role)
            if success:
                return {"username": username, "password": password}
            else:
                return {"error": "El usuario ya existe"}
        except Exception as e:
            return {"error": f"Error al crear usuario: {str(e)}"}

    def create_mesas(self, num_mesas):
        try:
            cuentas_creadas = []
            for i in range(1, num_mesas + 1):
                username = f"mesa{i}"
                password = f"mesa{i}pass"
                success = self.db.create_user(username, password, "cliente")
                if success:
                    cuentas_creadas.append(f"Usuario: {username}, Contraseña: {password}")
                else:
                    cuentas_creadas.append(f"Error al crear la cuenta de {username}: ya existe.")
            return "\n".join(cuentas_creadas)
        except Exception as e:
            return f"Error al crear mesas: {str(e)}"

    def close(self):
        self.db.close()
