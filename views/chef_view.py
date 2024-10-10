import tkinter as tk
from tkinter import messagebox
from controllers.chef_controller import ChefController

class ChefView:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef Panel")
        self.root.geometry("1200x600")  # Establecer tamaño de ventana
        self.controller = ChefController()

        # Frame para los botones de los pedidos
        self.order_buttons_frame = tk.Frame(root)
        self.order_buttons_frame.pack(pady=20)

        # Listbox para mostrar detalles del pedido
        self.order_listbox = tk.Listbox(root, width=100, height=10)
        self.order_listbox.pack(pady=10)

        # Botón para confirmar el pedido
        self.confirm_button = tk.Button(root, text="Confirmar Pedido", command=self.confirm_order)
        self.confirm_button.pack(side=tk.LEFT, padx=20)

        # Botón para cerrar la ventana
        self.back_button = tk.Button(root, text="Volver", command=self.close)
        self.back_button.pack(side=tk.RIGHT, padx=20)

        # Cargar los pedidos al iniciar la interfaz
        self.load_orders()

    def load_orders(self):
        # Cargar todos los pedidos pendientes de la base de datos
        for widget in self.order_buttons_frame.winfo_children():
            widget.destroy()  # Limpiar botones anteriores

        orders = self.controller.get_orders()
        for order in orders:
            mesa_number = order[1]  # Número de mesa
            order_id = order[0]  # ID del pedido
            # Crear un botón por cada pedido pendiente
            button = tk.Button(self.order_buttons_frame, text=f"Mesa {mesa_number} - Pedido {order_id}",
                               command=lambda o=order: self.show_order_details(o))
            button.pack(pady=5)

    def show_order_details(self, order):
        # Mostrar los detalles del pedido seleccionado en la lista
        order_id = order[0]
        order_items = order[2]
        self.order_listbox.delete(0, tk.END)  # Limpiar la lista
        self.order_listbox.insert(tk.END, f"ID: {order_id}, Items: {order_items}")

    def confirm_order(self):
        # Confirmar el pedido seleccionado
        selected = self.order_listbox.curselection()
        if selected:
            order_id = self.controller.get_orders()[selected[0]][0]  # Obtener el ID del pedido seleccionado
            self.controller.confirm_order(order_id)
            messagebox.showinfo("Éxito", "Pedido confirmado.")
            self.load_orders()  # Recargar la lista de pedidos
        else:
            messagebox.showerror("Error", "Selecciona un pedido.")

    def close(self):
        # Cerrar la ventana del chef y la conexión a la base de datos
        self.controller.close()
        self.root.destroy()
