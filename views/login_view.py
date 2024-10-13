# views/login_view.py
#perdon por la demora :v
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
        self.root.geometry("1200x600")
        self.root.configure(bg="white")
        self.controller = LoginController()

        # Crear el marco centralizado
        self.frame_login = tk.Frame(root, bg="white", bd=2, relief=tk.RIDGE)
        self.frame_login.place(relx=0.5, rely=0.5, anchor='center', width=400, height=400)

        # Título de Login
        self.label_title = tk.Label(self.frame_login, text="LOGIN", font=("Helvetica", 20, "bold"), bg="white")
        self.label_title.pack(pady=(20, 20))

        # Usuario
        self.label_username = tk.Label(self.frame_login, text="USUARIO", font=("Helvetica", 12), bg="white")
        self.label_username.pack(pady=(10, 5))

        self.entry_username = tk.Entry(self.frame_login, font=("Helvetica", 12))
        self.entry_username.pack(pady=5, padx=20, fill=tk.X)

        # Contraseña
        self.label_password = tk.Label(self.frame_login, text="CONTRASEÑA", font=("Helvetica", 12), bg="white")
        self.label_password.pack(pady=(10, 5))

        self.entry_password = tk.Entry(self.frame_login, show="*", font=("Helvetica", 12))
        self.entry_password.pack(pady=5, padx=20, fill=tk.X)

        # Mostrar Contraseña
        self.var_show = tk.IntVar()
        self.check_show = tk.Checkbutton(
            self.frame_login,
            text="Mostrar Contraseña",
            variable=self.var_show,
            command=self.toggle_password,
            font=("Helvetica", 10),
            bg="white"
        )
        self.check_show.pack(pady=5)

        # Botón de Login
        self.button_login = tk.Button(
            self.frame_login,
            text="Iniciar Sesión",
            command=self.login,
            font=("Helvetica", 12, "bold"),
            bg="#4CAF50",
            fg="white",
            width=20,
            cursor="hand2"
        )
        self.button_login.pack(pady=20)

    def toggle_password(self):
        """Alterna la visibilidad de la contraseña."""
        if self.var_show.get():
            self.entry_password.config(show="")
        else:
            self.entry_password.config(show="*")

    def login(self):
        """Maneja el proceso de login delegando la lógica al controlador."""
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        result = self.controller.validate_user(username, password)

        if result['status'] == 'success':
            user_id = result['user_id']
            role = result['role']
            messagebox.showinfo("Éxito", f"Bienvenido, {username}!")
            self.root.destroy()
            root = tk.Tk()
            root.geometry("1200x600")
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
        elif result['status'] == 'error':
            messagebox.showerror("Error", result['message'])
