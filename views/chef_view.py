# views/chef_view.py .
#perdon por la demora :v
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.chef_controller import ChefController

class ChefView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Chef - Pedidos Confirmados")
        self.controller = ChefController()
        self.user_id = user_id

        # Configuración de la interfaz
        self.label = tk.Label(root, text="Pedidos Confirmados para Preparar")
        self.label.pack(pady=10)

        # Treeview para mostrar los pedidos confirmados
        self.tree = ttk.Treeview(root, columns=("ID", "Cliente/Panel", "Platos", "Total", "Tipo Cuenta"), show='headings')
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente/Panel", text="Cliente/Panel")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Tipo Cuenta", text="Tipo Cuenta")
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Botón para confirmar el pedido seleccionado
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
            cliente_panel = order[1]
            tipo_cuenta = order[4]
            confirm = messagebox.askyesno("Confirmar Pedido", f"¿Deseas confirmar el pedido ID {order_id} de {cliente_panel}?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success == True:
                    messagebox.showinfo("Éxito", f"Pedido ID {order_id} confirmado y enviado a la caja.")
                    self.load_orders()
                elif success == 'panel_finalizado':
                    messagebox.showinfo("Pedido Completado", f"Pedido ID {order_id} completado.")
                    self.load_orders()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para confirmar.")
