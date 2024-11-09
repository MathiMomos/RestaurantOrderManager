import tkinter as tk
from tkinter import messagebox, ttk
from controllers.admin_controller import AdminController

class AdminView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Administrador - Restaurant Order Manager")
        self.controller = AdminController()
        self.user_id = user_id

        # Colores de fondo y estilos (igual que en el primer diseño)
        bg_color = "#f8f5f2"  # Fondo claro para todo
        header_bg = "#c05a2c"  # Fondo de la cabecera
        button_color = "#c05a2c"  # Botones de acción (Agregar, Editar, Eliminar)
        button_text_color = "white"
        label_color = "#53372d"  # Color para etiquetas y texto
        entry_bg_color = "white"

        # Cabecera
        header_frame = tk.Frame(root, bg=header_bg, height=50)
        header_frame.pack(fill="x")

        header_label = tk.Label(header_frame, text="ADMINISTRADOR", bg=header_bg, fg="white", font=("Arial", 14, "bold"))
        header_label.pack(pady=10)

        # Marco para el formulario de creación de usuario
        self.frame_create = tk.Frame(root, bg=bg_color, padx=20, pady=10)
        self.frame_create.pack(pady=10, fill="x")

        # Etiqueta y entrada de usuario
        self.label_username = tk.Label(self.frame_create, text="Nuevo Usuario:", bg=bg_color, fg=label_color)
        self.label_username.grid(row=0, column=0, padx=10, pady=5, sticky="e")

        self.entry_username = tk.Entry(self.frame_create, bg=entry_bg_color)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        # Etiqueta y entrada de contraseña
        self.label_password = tk.Label(self.frame_create, text="Contraseña:", bg=bg_color, fg=label_color)
        self.label_password.grid(row=1, column=0, padx=10, pady=5, sticky="e")

        self.entry_password = tk.Entry(self.frame_create, show="*", bg=entry_bg_color)
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        # Etiqueta y menú de selección de rol
        self.label_role = tk.Label(self.frame_create, text="Rol:", bg=bg_color, fg=label_color)
        self.label_role.grid(row=2, column=0, padx=10, pady=5, sticky="e")

        self.role_var = tk.StringVar(root)
        self.role_var.set("cliente")
        self.option_role = tk.OptionMenu(self.frame_create, self.role_var, "cliente", "chef", "caja", "panel")
        self.option_role.config(bg=button_color, fg=button_text_color, activebackground="#45a049")
        self.option_role.grid(row=2, column=1, padx=10, pady=5)

        # Botón para crear usuario
        self.button_create = tk.Button(
            self.frame_create, text="Crear Usuario", command=self.create_user,
            bg=button_color, fg=button_text_color, activebackground="#45a049", activeforeground=button_text_color
        )
        self.button_create.grid(row=3, column=0, columnspan=2, pady=10, ipadx=10, ipady=5)

        # Marco para la lista de usuarios
        self.frame_list = tk.Frame(root, bg=bg_color, padx=20, pady=10)
        self.frame_list.pack(pady=10, fill="both", expand=True)

        # Etiqueta de lista de usuarios
        self.label_users = tk.Label(self.frame_list, text="Usuarios Existentes:", bg=bg_color, fg=label_color, font=("Arial", 12, "bold"))
        self.label_users.pack(pady=5)

        # Árbol de visualización de usuarios
        self.tree_users = ttk.Treeview(self.frame_list, columns=("ID", "Usuario", "Rol"), show='headings')
        self.tree_users.heading("ID", text="ID")
        self.tree_users.heading("Usuario", text="Usuario")
        self.tree_users.heading("Rol", text="Rol")
        self.tree_users.column("ID", width=50, anchor="center")
        self.tree_users.column("Usuario", width=150, anchor="center")
        self.tree_users.column("Rol", width=100, anchor="center")
        self.tree_users.pack(padx=10, pady=5, fill="both", expand=True)

        # Botones para editar y eliminar usuarios
        self.tree_users.bind("<ButtonRelease-1>", self.on_treeview_select)

        # Cargar usuarios
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
        # Limpiar los datos actuales
        for row in self.tree_users.get_children():
            self.tree_users.delete(row)
        # Obtener todos los usuarios
        users = self.controller.get_all_users()
        for user in users:
            self.tree_users.insert("", tk.END, values=user)

    def on_treeview_select(self, event):
        selected_item = self.tree_users.selection()
        if selected_item:
            # Obtener el ID del usuario seleccionado
            self.selected_user = self.tree_users.item(selected_item, "values")[0]
            # Crear botones de edición y eliminación
            self.show_edit_delete_buttons()

    def show_edit_delete_buttons(self):
        # Eliminar botones anteriores si existen
        for widget in self.frame_list.winfo_children():
            if isinstance(widget, tk.Button) and widget not in [self.button_create]:
                widget.destroy()

        # Botón para editar usuario
        edit_button = tk.Button(self.frame_list, text="Editar Usuario", command=self.edit_user, bg="#c05a2c", fg="white")
        edit_button.pack(side="left", padx=10)

        # Botón para eliminar usuario
        delete_button = tk.Button(self.frame_list, text="Eliminar Usuario", command=self.delete_user, bg="#ff4d4d", fg="white")
        delete_button.pack(side="left", padx=10)

    def edit_user(self):
        # Aquí se manejaría la edición del usuario
        messagebox.showinfo("Editar Usuario", f"Función para editar usuario con ID: {self.selected_user}.")

    def delete_user(self):
        # Confirmar antes de eliminar
        confirmation = messagebox.askyesno("Confirmación", "¿Estás seguro de que deseas eliminar este usuario?")
        if confirmation:
            success = self.controller.delete_user(self.selected_user)
            if success:
                messagebox.showinfo("Éxito", "Usuario eliminado exitosamente.")
                self.load_users()
            else:
                messagebox.showerror("Error", "No se pudo eliminar el usuario.")
