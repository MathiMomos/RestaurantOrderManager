from tkinter import Tk
from views.login_view import LoginView
from views.admin_view import AdminView

def iniciar_aplicacion():
    root = Tk()

    def login_callback(username, password):
        if username == "admin" and password == "admin":
            root.withdraw()  # Cerrar la ventana de login
            admin_root = Tk()
            admin_view = AdminView(admin_root)
            admin_view.run()
            return True
        return False

    # Iniciar la interfaz del login
    login_view = LoginView(root, on_login=login_callback)
    login_view.run()

if __name__ == "__main__":
    iniciar_aplicacion()
