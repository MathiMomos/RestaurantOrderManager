# views/cliente_view.py
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Cliente - Realizar Pedido")
        self.controller = ClienteController()
        self.user_id = user_id
        self.current_order = None

        self.label_menu = tk.Label(root, text="Menú")
        self.label_menu.pack(pady=10)

        self.menu_items = self.controller.get_menu_items()
        self.menu_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE)
        for item in self.menu_items:
            self.menu_listbox.insert(tk.END, f"{item[1]} - ${item[2]:.2f}")
        self.menu_listbox.pack(padx=10, pady=10)

        self.button_add = tk.Button(root, text="Agregar al Pedido", command=self.add_to_order)
        self.button_add.pack(pady=10)

        self.button_confirm = tk.Button(root, text="Confirmar Pedido", command=self.confirm_order)
        self.button_confirm.pack(pady=10)

        self.label_order = tk.Label(root, text="Pedido Actual")
        self.label_order.pack(pady=10)

        self.tree_order = ttk.Treeview(root, columns=("Platos", "Total"), show='headings')
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Total", text="Total")
        self.tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.load_current_order()

    def load_current_order(self):
        self.current_order = self.controller.get_current_order(self.user_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, total = self.current_order
            platos = items.rstrip(", ")
            self.tree_order.insert("", tk.END, values=(platos, f"${total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedido actual.", "$0.00"))

    def add_to_order(self):
        selected_indices = self.menu_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("Advertencia", "Por favor, selecciona al menos un elemento del menú.")
            return
        selected_items = [self.menu_items[i] for i in selected_indices]
        for item in selected_items:
            self.controller.add_item_to_order(self.user_id, item[1], item[2])
        messagebox.showinfo("Éxito", "Elementos agregados al pedido.")
        self.load_current_order()

    def confirm_order(self):
        if self.current_order:
            order_id, items, total = self.current_order
            confirm = messagebox.askyesno("Confirmar Pedido", f"¿Deseas confirmar tu pedido ID {order_id}?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Pedido confirmado y enviado al chef.")
                    self.load_current_order()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No tienes ningún pedido para confirmar.")
