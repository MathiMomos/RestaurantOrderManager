from data.database import Database

class AdminController:
    def __init__(self):
        # Crear conexión con la base de datos
        self.db = Database()

    def show_admin_menu(self):
        print("\n=== Panel del Administrador ===")
        print("1. Crear cuenta para Chef")
        print("2. Crear cuenta para Caja")
        print("3. Establecer número de mesas")
        print("4. Crear cuenta para Panel")
        print("5. Salir")

        option = input("Seleccione una opción: ")

        if option == '1':
            self.create_chef_account()
        elif option == '2':
            self.create_caja_account()
        elif option == '3':
            self.set_num_mesas()
        elif option == '4':
            self.create_panel_account()
        elif option == '5':
            print("Saliendo del sistema...")
            self.db.close()  # Cerrar la conexión antes de salir
        else:
            print("Opción inválida. Intente de nuevo.")
            self.show_admin_menu()

    def create_chef_account(self):
        username = input("Ingrese el nombre de usuario del Chef: ")
        password = input("Ingrese la contraseña del Chef: ")
        self.db.add_user(username, password, 'chef')
        self.show_admin_menu()

    def create_caja_account(self):
        username = input("Ingrese el nombre de usuario para la Caja: ")
        password = input("Ingrese la contraseña para la Caja: ")
        self.db.add_user(username, password, 'caja')
        self.show_admin_menu()

    def create_panel_account(self):
        username = input("Ingrese el nombre de usuario para el Panel: ")
        password = input("Ingrese la contraseña para el Panel: ")
        self.db.add_user(username, password, 'panel')
        print(f"Cuenta de Panel '{username}' creada exitosamente.")
        self.show_admin_menu()

    def set_num_mesas(self):
        try:
            num_mesas = int(input("Ingrese el número de mesas: "))
            for i in range(1, num_mesas + 1):
                username = f'mesa{i}'
                password = f'password_mesa{i}'
                self.db.add_user(username, password, 'mesa')
                self.db.add_mesa(i, username, password)
            print(f"{num_mesas} mesas creadas exitosamente.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
        self.show_admin_menu()
