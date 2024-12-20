# main.py .
import tkinter as tk
from views.login_view import LoginView
from data.database import initialize_database

def main():
    # inicializar la base de datos (solo la primera vez)
    initialize_database()

    # crear la ventana principal para el login
    root = tk.Tk()
    LoginView(root)
    root.mainloop()

    # para los que no le corre

if __name__ == "__main__":
    main()
