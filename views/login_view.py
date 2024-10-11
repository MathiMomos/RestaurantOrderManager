# views/login_view.py
import tkinter as tk
from tkinter import messagebox
from controllers.login_controller import LoginController
from views.admin_view import AdminView
from views.chef_view import ChefView
from views.caja_view import CajaView
from views.cliente_view import ClienteView
from views.panel_view import PanelView

class LoginView:
    def __init__(self, root):
        self.root = root
        self.root.title("Login - Restaurant Order Manager")
        self.controller = LoginController()

        self.label_username = tk.Label(root, text="Usuario:")
        self.label_username.grid(row=0, column=0, padx=10, pady=10)

        self.entry_username = tk.Entry(root)
        self.entry_username.grid(row=0, column=1, padx=10, pady=10)

        self.label_password = tk.Label(root, text="Contraseña:")
        self.label_password.grid(row=1, column=0, padx=10, pady=10)

        self.entry_password = tk.Entry(root, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=10)

        self.button_login = tk.Button(root, text="Iniciar Sesión", command=self.login)
        self.button_login.grid(row=2, column=0, columnspan=2, pady=10)

    def login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        result = self.controller.validate_user(username, password)
        if result:
            user_id, role = result
            messagebox.showinfo("Éxito", f"Bienvenido, {username}!")
            self.root.destroy()
            root = tk.Tk()
            if role == 'admin':
                AdminView(root, user_id)
            elif role == 'chef':
                ChefView(root, user_id)
            elif role == 'caja':
                CajaView(root, user_id)
            elif role == 'cliente':
                ClienteView(root, user_id)
            elif role == 'panel':
                PanelView(root, user_id)
            else:
                messagebox.showerror("Error", "Rol no implementado aún.")
            root.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
