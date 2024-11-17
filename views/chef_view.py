import tkinter as tk
from tkinter import messagebox, ttk
from controllers.chef_controller import ChefController

class ChefView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Chef - Pedidos Confirmados")
        self.controller = ChefController()
        self.user_id = user_id

        # Configuración del fondo y color principal
        self.root.configure(bg="#f7f7f7")

        # Etiqueta del título
        self.label = tk.Label(root, text="Pedidos Confirmados para Preparar", font=("Arial", 18, 'bold'), bg="#f7f7f7", fg="#3b1d14")
        self.label.pack(pady=20)

        # Estilo del Treeview para mostrar los pedidos
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Arial", 12), background="#f9f9f9", foreground="#3b1d14", rowheight=40)
        self.style.configure("Treeview.Heading", font=("Arial", 14, 'bold'), background="#f7f7f7", foreground="black")
        self.style.map("Treeview", background=[('selected', '#3b1d14')], foreground=[('selected', 'white')])

        # Treeview para mostrar los pedidos confirmados
        self.tree = ttk.Treeview(root, columns=("ID", "Cliente/Panel", "Platos", "Total", "Tipo Cuenta"), show='headings', style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente/Panel", text="Cliente/Panel")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Tipo Cuenta", text="Tipo Cuenta")
        self.tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Botón para confirmar el pedido seleccionado
        self.button_confirm = tk.Button(root, text="Confirmar Pedido", command=self.confirm_selected_order, width=20, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
        self.button_confirm.pack(pady=20)

        self.load_orders()

    def load_orders(self):
        """Cargar los pedidos confirmados en el Treeview"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_confirmed_orders()
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def confirm_selected_order(self):
        """Confirmar el pedido seleccionado"""
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
