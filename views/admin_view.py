from controllers.admin_controller import crear_cuenta, establecer_mesas, obtener_cuentas_mesas

def menu_admin():
    while True:
        print("\nMenú Administrador")
        print("1. Crear cuenta Caja")
        print("2. Crear cuenta Chef")
        print("3. Crear cuenta Panel")
        print("4. Establecer número de mesas")
        print("5. Salir")

        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            nombre = input("Nombre de la cuenta Caja: ")
            contraseña = input("Contraseña de la cuenta Caja: ")
            crear_cuenta(nombre, contraseña, 'caja')
        elif opcion == '2':
            nombre = input("Nombre de la cuenta Chef: ")
            contraseña = input("Contraseña de la cuenta Chef: ")
            crear_cuenta(nombre, contraseña, 'chef')
        elif opcion == '3':
            nombre = input("Nombre de la cuenta Panel: ")
            contraseña = input("Contraseña de la cuenta Panel: ")
            crear_cuenta(nombre, contraseña, 'cliente')
        elif opcion == '4':
            numero_mesas = int(input("Número de mesas: "))
            establecer_mesas(numero_mesas)
            cuentas = obtener_cuentas_mesas(numero_mesas)
            print(f"\nSe crearon {numero_mesas} cuentas de mesa:")
            for cuenta in cuentas:
                print(f"Usuario: {cuenta[0]}, Contraseña: {cuenta[1]}")
        elif opcion == '5':
            break
        else:
            print("Opción no válida, intenta de nuevo.")
