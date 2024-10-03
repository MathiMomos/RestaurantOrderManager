import tkinter as tk
from tkinter import messagebox

class LoginView:
    def __init__(self, root, on_login):
        self.root = root
        self.root.title("Login")
        self.root.geometry("1000x500")  # Tamaño de la ventana: Ancho 1000, Alto 500
        self.root.configure(bg="white")  # Fondo blanco

        # Título LOGIN centrado y más grande
        title = tk.Label(self.root, text="LOGIN", fg="black", bg="white", font=("Arial", 60, "bold"))  # Doble de tamaño
        title.pack(pady=(40, 10))  # Espacio superior y inferior

        # Usuario
        tk.Label(self.root, text="Usuario", fg="black", bg="white", font=("Arial", 16)).pack(pady=(20, 5))  # Más espacio
        self.username_entry = tk.Entry(self.root, bg="white", fg="black", font=("Arial", 14), width=30, highlightbackground="black", highlightcolor="black")
        self.username_entry.pack(ipady=5)  # Aumenta la altura del cuadro

        # Contraseña
        tk.Label(self.root, text="Contraseña", fg="black", bg="white", font=("Arial", 16)).pack(pady=(20, 5))  # Más espacio
        self.password_entry = tk.Entry(self.root, show="*", bg="white", fg="black", font=("Arial", 14), width=30, highlightbackground="black", highlightcolor="black")
        self.password_entry.pack(ipady=5)

        # Checkbutton para mostrar/ocultar contraseña
        self.show_password_var = tk.IntVar()  # Variable que controlará el estado del Checkbutton
        self.show_password_checkbutton = tk.Checkbutton(self.root, text="Mostrar contraseña", bg="white", fg="black", font=("Arial", 12), variable=self.show_password_var, command=self.toggle_password)
        self.show_password_checkbutton.pack(pady=10)

        # Botón de login
        login_button = tk.Button(self.root, text="Login", command=self.login, bg="white", fg="black", font=("Arial", 14), width=20)
        login_button.pack(pady=30)

        # Callback para el login
        self.on_login = on_login

    def toggle_password(self):
        """Función para mostrar u ocultar la contraseña según el estado del Checkbutton"""
        if self.show_password_var.get():
            self.password_entry.config(show="")  # Muestra la contraseña como texto normal
        else:
            self.password_entry.config(show="*")  # Oculta la contraseña con asteriscos

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.on_login(username, password):
            messagebox.showinfo("Éxito", "Inicio de sesión exitoso")
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    def run(self):
        self.root.mainloop()
