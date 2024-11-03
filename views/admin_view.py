# views/admin_view.py .


import tkinter as tk
from tkinter import messagebox, ttk
from controllers.admin_controller import AdminController

class AdminView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Administrador - Restaurant Order Manager")
        self.controller = AdminController()
        self.user_id = user_id

        self.frame_create = tk.Frame(root)
        self.frame_create.pack(pady=10)

        self.label_username = tk.Label(self.frame_create, text="Nuevo Usuario:")
        self.label_username.grid(row=0, column=0, padx=10, pady=5)

        self.entry_username = tk.Entry(self.frame_create)
        self.entry_username.grid(row=0, column=1, padx=10, pady=5)

        self.label_password = tk.Label(self.frame_create, text="Contraseña:")
        self.label_password.grid(row=1, column=0, padx=10, pady=5)

        self.entry_password = tk.Entry(self.frame_create, show="*")
        self.entry_password.grid(row=1, column=1, padx=10, pady=5)

        self.label_role = tk.Label(self.frame_create, text="Rol:")
        self.label_role.grid(row=2, column=0, padx=10, pady=5)

        self.role_var = tk.StringVar(root)
        self.role_var.set("cliente")
        self.option_role = tk.OptionMenu(self.frame_create, self.role_var, "cliente", "chef", "caja", "panel")
        self.option_role.grid(row=2, column=1, padx=10, pady=5)

        self.button_create = tk.Button(self.frame_create, text="Crear Usuario", command=self.create_user)
        self.button_create.grid(row=3, column=0, columnspan=2, pady=10)

        self.frame_list = tk.Frame(root)
        self.frame_list.pack(pady=10)

        self.label_users = tk.Label(self.frame_list, text="Usuarios Existentes:")
        self.label_users.pack(pady=5)

        self.tree_users = ttk.Treeview(self.frame_list, columns=("ID", "Usuario", "Rol"), show='headings')
        self.tree_users.heading("ID", text="ID")
        self.tree_users.heading("Usuario", text="Usuario")
        self.tree_users.heading("Rol", text="Rol")
        self.tree_users.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)

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
