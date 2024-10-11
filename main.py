# main.py
import tkinter as tk
from views.login_view import LoginView
from data.database import initialize_database

def main():
    # Inicializar la base de datos (solo la primera vez)
    initialize_database()

    # Crear la ventana principal para el login
    root = tk.Tk()
    LoginView(root)
    root.mainloop()

if __name__ == "__main__":
    main()
