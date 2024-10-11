# views/panel_view.py .

import tkinter as tk
from tkinter import messagebox, ttk
from controllers.panel_controller import PanelController

class PanelView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Panel - Restaurant Order Manager")
        self.controller = PanelController()
        self.user_id = user_id

        # Menú
        self.label_menu = tk.Label(root, text="Menú")
        self.label_menu.pack(pady=10)

        self.tree_menu = ttk.Treeview(root, columns=("ID", "Plato", "Precio"), show='headings')
        self.tree_menu.heading("ID", text="ID")
        self.tree_menu.heading("Plato", text="Plato")
        self.tree_menu.heading("Precio", text="Precio")
        self.tree_menu.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_add = tk.Button(root, text="Agregar al Pedido", command=self.add_selected_item)
        self.button_add.pack(pady=5)

        # Pedido Actual
        self.label_order = tk.Label(root, text="Pedido Actual")
        self.label_order.pack(pady=10)

        self.tree_order = ttk.Treeview(root, columns=("Platos", "Total"), show='headings')
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Total", text="Total")
        self.tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.button_confirm = tk.Button(root, text="Confirmar Pedido", command=self.confirm_order)
        self.button_confirm.pack(pady=10)

        self.load_menu()
        self.load_order()

    def load_menu(self):
        """Carga los elementos del menú en el Treeview."""
        for row in self.tree_menu.get_children():
            self.tree_menu.delete(row)
        menu_items = self.controller.get_menu_items()
        for item in menu_items:
            self.tree_menu.insert("", tk.END, values=item)

    def add_selected_item(self):
        """Agrega el plato seleccionado al pedido."""
        selected = self.tree_menu.focus()
        if selected:
            item = self.tree_menu.item(selected, 'values')
            item_name = item[1]
            item_price = float(item[2])
            self.controller.add_item_to_order(self.user_id, item_name, item_price)
            messagebox.showinfo("Éxito", f"'{item_name}' agregado al pedido.")
            self.load_order()
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un plato para agregar.")

    def load_order(self):
        """Carga el pedido actual si existe."""
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        order = self.controller.get_user_order(self.user_id)
        if order:
            order_id, items, total = order
            platos = items.rstrip(", ")
            self.tree_order.insert("", tk.END, values=(platos, f"${total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedidos actuales.", "$0.00"))

    def confirm_order(self):
        """Confirma el pedido y lo envía a la caja."""
        order = self.controller.get_user_order(self.user_id)
        if order:
            order_id, items, total = order
            confirm = messagebox.askyesno("Confirmar Pedido", "¿Deseas confirmar tu pedido y enviarlo a la caja?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Pedido confirmado y enviado a la caja.")
                    self.load_order()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No tienes ningún pedido para confirmar.")
