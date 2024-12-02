import tkinter as tk
from tkinter import PhotoImage, messagebox
from controllers.login_controller import LoginController
from views.admin_view import AdminView
from views.chef_view import ChefView
from views.caja_view import CajaView
from views.cliente_view import ClienteView
from views.panel_view import PanelView

class LoginView:
    def __init__(self, root):
        # Configuración básica de la ventana
        self.root = root
        self.root.title("Login - Restaurant Order Manager")
        self.root.geometry("1200x600")
        self.root.configure(bg="#F5F5F5")
        self.controller = LoginController()

        # Cargar la imagen de título
        self.titulo_image = PhotoImage(file="recursos/titulo.png")  # Ruta relativa a la carpeta recursos

        # Marco principal centrado
        self.frame = tk.Frame(
            self.root, bg="white", bd=2, relief="solid",
            highlightbackground="#efeeeb", highlightcolor="#efeeeb"
        )
        self.frame.place(relx=0.5, rely=0.7, anchor='center', width=700, height=300)

        # Etiqueta de imagen del título
        self.label_titulo = tk.Label(self.root, image=self.titulo_image, bg="#F5F5F5")
        self.label_titulo.place(relx=0.5, rely=0.25, anchor='center')

        # Etiqueta y entrada de "Nombre de usuario"
        self.label_username = tk.Label(
            self.frame, text="Nombre de usuario", font=("Helvetica", 12, "bold"), bg="white", fg="#333"
        )
        self.label_username.place(relx=0.5, rely=0.2, anchor='center')

        self.entry_username = tk.Entry(
            self.frame, font=("Helvetica", 14), relief="solid", bd=1, justify="center", fg="#333", bg="white",
            highlightbackground="#efeeeb", highlightthickness=1
        )
        self.entry_username.insert(0, "Ingrese su usuario")
        self.entry_username.config(fg="#AAA")
        self.entry_username.bind("<FocusIn>", self.clear_username)
        self.entry_username.bind("<FocusOut>", self.restore_username)
        self.entry_username.place(relx=0.5, rely=0.3, anchor='center', width=500, height=35)

        # Etiqueta y entrada de "Contraseña"
        self.label_password = tk.Label(
            self.frame, text="Contraseña", font=("Helvetica", 12, "bold"), bg="white", fg="#333"
        )
        self.label_password.place(relx=0.5, rely=0.45, anchor='center')

        self.password_frame = tk.Frame(
            self.frame, bg="white", relief="solid", bd=1, highlightbackground="#efeeeb", highlightthickness=1
        )
        self.password_frame.place(relx=0.5, rely=0.55, anchor='center', width=500, height=35)

        self.entry_password = tk.Entry(
            self.password_frame, font=("Helvetica", 14), relief="flat", bd=0, justify="center", fg="#AAA", bg="white"
        )
        self.entry_password.insert(0, "Ingrese su contraseña")
        self.entry_password.bind("<FocusIn>", self.clear_password)
        self.entry_password.bind("<FocusOut>", self.restore_password)
        self.entry_password.pack(side="left", fill="both", expand=True, padx=(10, 0))

        self.show_password_icon = tk.Label(
            self.password_frame, text="👁", cursor="hand2", bg="white", fg="#888"
        )
        self.show_password_icon.pack(side="right", padx=(0, 10))
        self.show_password_icon.bind("<Button-1>", self.toggle_password)

        # Botón para iniciar sesión
        self.button_login = tk.Button(
            self.frame, text="Iniciar Sesión", command=self.login, bg="#3c1d15", fg="white",
            font=("Helvetica", 12, "bold"), relief="solid", bd=1, cursor="hand2"
        )
        self.button_login.place(relx=0.5, rely=0.8, anchor='center', width=200, height=40)

        self.password_shown = False

    # Métodos auxiliares
    def clear_username(self, event):
        if self.entry_username.get() == "Ingrese su usuario":
            self.entry_username.delete(0, tk.END)
            self.entry_username.config(fg="#333")

    def restore_username(self, event):
        if not self.entry_username.get():
            self.entry_username.insert(0, "Ingrese su usuario")
            self.entry_username.config(fg="#AAA")

    def clear_password(self, event):
        if self.entry_password.get() == "Ingrese su contraseña":
            self.entry_password.delete(0, tk.END)
            self.entry_password.config(show="*", fg="#333")

    def restore_password(self, event):
        if not self.entry_password.get():
            self.entry_password.insert(0, "Ingrese su contraseña")
            self.entry_password.config(show="", fg="#AAA")

    def toggle_password(self, event):
        if self.password_shown:
            self.entry_password.config(show="*")
            self.show_password_icon.config(text="👁")
        else:
            self.entry_password.config(show="")
            self.show_password_icon.config(text="🙈")
        self.password_shown = not self.password_shown

    def login(self):
        username = self.entry_username.get().strip()
        password = self.entry_password.get().strip()

        if username in ("", "Ingrese su usuario") or password in ("", "Ingrese su contraseña"):
            messagebox.showwarning("Advertencia", "Por favor, completa todos los campos.")
            return

        result = self.controller.validate_user(username, password)

        if result['status'] == 'success':
            user_id = result['user_id']
            role = result['role']
            self.root.destroy()
            self.open_role_view(role, user_id)
        else:
            messagebox.showerror("Error", result['message'])

    def open_role_view(self, role, user_id):
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
            messagebox.showerror("Error", "Rol no implementado.")
        root.mainloop()

