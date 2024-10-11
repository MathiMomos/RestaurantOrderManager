# views/caja_view.py .
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.caja_controller import CajaController

class CajaView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Caja - Pedidos en Caja")
        self.controller = CajaController()
        self.user_id = user_id

        # Configuración de la interfaz
        self.label = tk.Label(root, text="Pedidos en Caja")
        self.label.pack(pady=10)

        # Treeview para mostrar los pedidos
        self.tree = ttk.Treeview(root, columns=("ID", "Cliente", "Platos", "Total", "Tipo Cuenta"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Tipo Cuenta", text="Tipo Cuenta")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Botón para generar la boleta del pedido (solo para cuentas cliente)
        self.button_generate = tk.Button(root, text="Generar Boleta (Clientes)", command=self.generate_selected_bill)
        self.button_generate.pack(pady=5)

        # Botón para procesar pedidos de cuentas panel
        self.button_process_panel = tk.Button(root, text="Procesar Pedido de Panel", command=self.process_selected_panel_order)
        self.button_process_panel.pack(pady=5)

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
            tipo_cuenta = order[4]
            if tipo_cuenta == 'cliente':
                confirm = messagebox.askyesno("Generar Boleta", f"¿Deseas generar la boleta para el pedido ID {order_id} de {cliente}?")
                if confirm:
                    success = self.controller.generate_bill(order_id)
                    if success:
                        messagebox.showinfo("Éxito", "Boleta generada.")
                        self.load_orders()
                    else:
                        messagebox.showerror("Error", "No se pudo generar la boleta.")
            else:
                messagebox.showwarning("Advertencia", "Solo se puede generar boleta para pedidos de clientes.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para generar la boleta.")

    def process_selected_panel_order(self):
        selected = self.tree.focus()
        if selected:
            order = self.tree.item(selected, 'values')
            order_id = order[0]
            panel = order[1]
            tipo_cuenta = order[4]
            if tipo_cuenta == 'panel':
                confirm = messagebox.askyesno("Procesar Pedido de Panel", f"¿Deseas procesar el pedido ID {order_id} de {panel} y enviarlo al chef?")
                if confirm:
                    success = self.controller.process_panel_order(order_id)
                    if success:
                        messagebox.showinfo("Éxito", f"Pedido ID {order_id} procesado y enviado al chef.")
                        self.load_orders()
                    else:
                        messagebox.showerror("Error", "No se pudo procesar el pedido de panel.")
            else:
                messagebox.showwarning("Advertencia", "Este botón es solo para pedidos de panel.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido de panel para procesarlo.")
