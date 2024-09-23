from controllers.login_controller import autenticar_usuario

def main():
    nombre = input("Nombre de usuario: ")
    contraseña = input("Contraseña: ")

    usuario = autenticar_usuario(nombre, contraseña)

    if usuario:
        print(f"Bienvenido, {usuario.nombre}. Eres un {usuario.tipo}.")
        if usuario.tipo == 'admin':
            from views.admin_view import menu_admin
            menu_admin()
        # Agregar lógica para otros tipos de usuario
    else:
        print("Nombre de usuario o contraseña incorrectos.")
        main()  # Volver a intentar login
