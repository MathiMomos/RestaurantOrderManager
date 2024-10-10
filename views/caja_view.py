# caja_view.py

import tkinter as tk
from tkinter import messagebox
from controllers.caja_controller import CajaController

class CajaView:
    def __init__(self, root):
        self.root = root
        self.root.title("Caja Panel")
        self.controller = CajaController()

        self.order_listbox = tk.Listbox(root)
        self.order_listbox.pack()

        self.refresh_orders()

        tk.Button(root, text="Eliminar Pedido", command=self.delete_order).pack()

    def refresh_orders(self):
        orders = self.controller.get_orders()
        self.order_listbox.delete(0, tk.END)  # Limpiar lista
        for order in orders:
            self.order_listbox.insert(tk.END, f"ID: {order[0]}, Mesa: {order[1]}, Total: {order[3]}")

    def delete_order(self):
        selected = self.order_listbox.curselection()
        if selected:
            order_id = self.controller.get_orders()[selected[0]][0]  # Obtener ID
            self.controller.delete_order(order_id)
            messagebox.showinfo("Éxito", "Pedido eliminado.")
            self.refresh_orders()  # Actualizar la lista
        else:
            messagebox.showerror("Error", "Selecciona un pedido.")

    def close(self):
        self.controller.close()
