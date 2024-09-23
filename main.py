from data.database import crear_tablas

def main():
    crear_tablas()  # Crea la base de datos y las tablas si no existen
    from views.login_view import main as login
    login()  # Ejecutar el proceso de login

if __name__ == "__main__":
    main()
