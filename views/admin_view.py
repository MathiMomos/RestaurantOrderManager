import tkinter as tk
from tkinter import messagebox

class AdminView:
    def __init__(self, root):
        self.root = root
        self.root.title("Panel del Administrador")
        self.root.geometry("1000x500")  # Tamaño de la ventana: Ancho 1000, Alto 500
        self.root.configure(bg="White")  # Fondo blanco

        # Título ADMINISTRADOR centrado y grande
        title = tk.Label(self.root, text="ADMINISTRADOR", fg="black", bg="white", font=("Arial", 60, "bold"))  # Tamaño grande
        title.pack(pady=(40, 10))  # Espacio superior e inferior

        # Botones para crear cuentas y gestionar mesas
        button_style = {
            'bg': 'white',
            'fg': 'black',
            'font': ('Arial', 14),
            'width': 30  # Aumento de ancho en un 50%
        }

        tk.Button(self.root, text="CREAR CUENTA PARA CHEF", command=self.create_chef_account, **button_style).pack(pady=10)
        tk.Button(self.root, text="CREAR CUENTA PARA CAJA", command=self.create_caja_account, **button_style).pack(pady=10)
        tk.Button(self.root, text="ESTABLECER NÚMERO DE MESAS", command=self.set_num_mesas, **button_style).pack(pady=10)
        tk.Button(self.root, text="CREAR CUENTA PARA PANEL", command=self.create_panel_account, **button_style).pack(pady=10)
        tk.Button(self.root, text="SALIR", command=self.root.quit, **button_style).pack(pady=10)

    def create_chef_account(self):
        messagebox.showinfo("Info", "Función para crear cuenta de Chef")

    def create_caja_account(self):
        messagebox.showinfo("Info", "Función para crear cuenta de Caja")

    def set_num_mesas(self):
        messagebox.showinfo("Info", "Función para establecer número de mesas")

    def create_panel_account(self):
        messagebox.showinfo("Info", "Función para crear cuenta de Panel")

