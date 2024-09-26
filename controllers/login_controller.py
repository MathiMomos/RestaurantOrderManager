from controllers.admin_controller import AdminController
from data.database import Database

class LoginController:
    def __init__(self):
        # Crear conexión con la base de datos
        self.db = Database()
        # Verificar si la cuenta admin existe, si no, crearla
        if not self.db.get_user('admin'):
            self.db.add_user('admin', 'admin', 'admin')

    def login(self):
        print("=== Iniciar Sesión ===")
        username = input("Usuario: ")
        password = input("Contraseña: ")

        user = self.db.get_user(username)
        if user and user[2] == password:
            print(f"Bienvenido, {username}")
            # Redirigir al menú del administrador si el login es correcto
            if user[3] == 'admin':
                admin_controller = AdminController()
                admin_controller.show_admin_menu()
            elif user[3] == 'panel':
                print("Acceso al panel externo.")
                # Aquí se podría redirigir a una interfaz especial de panel si es necesario
        else:
            print("Usuario o contraseña incorrectos. Inténtalo de nuevo.")
            self.login()
