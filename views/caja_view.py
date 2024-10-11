# views/caja_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.caja_controller import CajaController

class CajaView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Caja - Pedidos en Caja")
        self.controller = CajaController()

        self.label = tk.Label(root, text="Pedidos en Caja")
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Cliente", "Platos", "Total"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_generate = tk.Button(root, text="Generar Boleta", command=self.generate_selected_bill)
        self.button_generate.pack(pady=10)

        self.load_orders()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_en_caja_orders()
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def generate_selected_bill(self):
        selected = self.tree.focus()
        if selected:
            order = self.tree.item(selected, 'values')
            order_id = order[0]
            cliente = order[1]
            confirm = messagebox.askyesno("Generar Boleta", f"¿Deseas generar la boleta para el pedido ID {order_id} de {cliente}?")
            if confirm:
                success = self.controller.generate_bill(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Boleta generada.")
                    self.load_orders()
                else:
                    messagebox.showerror("Error", "No se pudo generar la boleta.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para generar la boleta.")
