import tkinter as tk
from tkinter import messagebox, ttk
from controllers.admin_controller import AdminController

class AdminView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Administrador - Restaurant Order Manager")
        self.controller = AdminController()
        self.user_id = user_id

        # Colores y fuentes
        bg_color = "#FCE4B5"  # Color de fondo cálido (temático para restaurante)
        header_color = "#D35400"  # Color de encabezado
        texto_color = "#000000"  # Color negro para texto
        fuente_general = ("Helvetica", 12)
        fuente_titulo = ("Helvetica", 14, "bold")
        fuente_header = ("Helvetica", 20, "bold")

        # Configuración de la ventana principal
        self.root.configure(bg=bg_color)

        # Encabezado principal
        self.label_header = tk.Label(
            self.root, text="EL CRIOLLITO RESTAURANT", bg=header_color, fg="white",
            font=fuente_header, pady=10
        )
        self.label_header.pack(fill="x")

        # Marco para crear usuarios (izquierda)
        self.frame_create = tk.Frame(root, bg=bg_color)
        self.frame_create.pack(side="left", padx=20, pady=20, fill="both", expand=True)

        # Submarco para centrar verticalmente
        self.inner_frame = tk.Frame(self.frame_create, bg=bg_color)
        self.inner_frame.place(relx=0.5, rely=0.5, anchor="center")  # Centrado en X y Y

        # Entrada de nombre de usuario
        self.label_username = tk.Label(
            self.inner_frame, text="Nombre Usuario:", bg=bg_color, fg=texto_color, font=fuente_general
        )
        self.label_username.pack(anchor="w", pady=(5, 0))

        self.entry_username = tk.Entry(self.inner_frame, font=fuente_general, width=25)
        self.entry_username.pack(pady=(0, 10), fill="x")

        # Entrada de contraseña
        self.label_password = tk.Label(
            self.inner_frame, text="Contraseña:", bg=bg_color, fg=texto_color, font=fuente_general
        )
        self.label_password.pack(anchor="w", pady=(5, 0))

        self.entry_password = tk.Entry(self.inner_frame, show="*", font=fuente_general, width=25)
        self.entry_password.pack(pady=(0, 10), fill="x")

        # Menú desplegable para roles
        self.role_var = tk.StringVar(root)
        self.role_var.set("cliente")  # Valor predeterminado
        self.option_role = tk.OptionMenu(self.inner_frame, self.role_var, "cliente", "chef", "caja", "panel")
        self.option_role.config(font=fuente_general)
        self.option_role.pack(pady=10)

        # Botón para crear usuario
        self.button_create = tk.Button(
            self.inner_frame, text="Crear Usuario", font=fuente_general, bg="#D35400", fg="white",
            command=self.create_user
        )
        self.button_create.pack(pady=10)

        # Marco para lista de usuarios (derecha)
        self.frame_list = tk.Frame(root, bg=bg_color, bd=2, relief="solid", padx=10, pady=10)
        self.frame_list.pack(side="right", padx=20, pady=20, fill="both", expand=True)

        self.label_users = tk.Label(
            self.frame_list, text="Usuarios Existentes:", bg=bg_color, fg=texto_color, font=fuente_titulo
        )
        self.label_users.pack(pady=5)

        # Configuración del Treeview
        style = ttk.Style()
        style.configure("Treeview", font=fuente_general, rowheight=25)
        style.configure("Treeview.Heading", font=fuente_titulo, background="#D35400", foreground="white")
        style.map("Treeview", background=[("selected", "#D35400")], foreground=[("selected", "white")])

        self.tree_users = ttk.Treeview(self.frame_list, columns=("ID", "Usuario", "Rol"), show='headings', height=10)
        self.tree_users.heading("ID", text="ID")
        self.tree_users.heading("Usuario", text="Usuario")
        self.tree_users.heading("Rol", text="Rol")
        self.tree_users.column("ID", width=50, anchor="center")
        self.tree_users.column("Usuario", width=150, anchor="center")
        self.tree_users.column("Rol", width=100, anchor="center")
        self.tree_users.pack(pady=10, fill="both", expand=True)

        # Cargar usuarios en el Treeview
        self.load_users()

    def create_user(self):
        username = self.entry_username.get()
        password = self.entry_password.get()
        role = self.role_var.get()
        if username and password:
            success = self.controller.create_user(username, password, role)
            if success:
                messagebox.showinfo("Éxito", "Usuario creado exitosamente.")
                self.load_users()
                self.entry_username.delete(0, tk.END)
                self.entry_password.delete(0, tk.END)
            else:
                messagebox.showerror("Error", "No se pudo crear el usuario. Puede que el nombre de usuario ya exista.")
        else:
            messagebox.showerror("Error", "Por favor, completa todos los campos.")

    def load_users(self):
        for row in self.tree_users.get_children():
            self.tree_users.delete(row)
        users = self.controller.get_all_users()
        for user in users:
            self.tree_users.insert("", tk.END, values=user)

