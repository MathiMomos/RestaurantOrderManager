# views/chef_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.chef_controller import ChefController

class ChefView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Chef - Pedidos Confirmados")
        self.controller = ChefController()

        self.label = tk.Label(root, text="Pedidos Confirmados para Preparar")
        self.label.pack(pady=10)

        self.tree = ttk.Treeview(root, columns=("ID", "Cliente", "Platos", "Total"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_confirm = tk.Button(root, text="Confirmar Pedido", command=self.confirm_selected_order)
        self.button_confirm.pack(pady=10)

        self.load_orders()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_confirmed_orders()
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def confirm_selected_order(self):
        selected = self.tree.focus()
        if selected:
            order = self.tree.item(selected, 'values')
            order_id = order[0]
            cliente = order[1]
            confirm = messagebox.askyesno("Confirmar Pedido", f"¿Deseas confirmar el pedido ID {order_id} de {cliente}?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", f"Pedido ID {order_id} confirmado y enviado a la caja.")
                    self.load_orders()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para confirmar.")
