from data.database import Database

class ClienteController:
    def __init__(self):
        self.database = Database()

    def ingresoNombreCliente(self):
        print("\n--------------------------")
        nom = input("Ingrese su nombre: ")
        dni = input("Ingrese su DNI: ")

        # Verificar si el cliente ya existe en la base de datos
        cliente_existente = self.database.get_cliente_por_dni(dni)

        if cliente_existente:
            print(f"Bienvenido de nuevo, {cliente_existente['nombre']}.")
        else:
            # Agregar cliente a la base de datos si no existe
            self.database.add_cliente(nom, dni)
            print(f"Cliente '{nom}' con DNI '{dni}' ha sido registrado exitosamente.")


        self.cliente_menu()

    def cliente_menu(self):
        print("\n----------------------")
        print("1. Menú y Combos")  # muestra el menú y combos
        print("2. Pedido")  # muestra la cantidad de pedidos que hizo y el costo actual
        print("3. Salir")  # salir de la sesión y retornar a ingresar nombre cliente

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            self.add_menu()
        elif opcion == "2":
            self.info_pedido()
        elif opcion == "3":
            self.ingresoNombreCliente()

    def info_pedido(self):
        print("La información de su pedido es la siguiente.")
        # Aquí iría la lógica para mostrar el pedido actual

    def add_menu(self):
        print("Mostrando el menú y combos...")
        # Aquí iría la lógica para mostrar el menú al cliente