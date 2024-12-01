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
        self.root.configure(bg="#f7f7f7")

        # Etiqueta de título
        self.label = tk.Label(root, text="Pedidos en Caja", font=("Arial", 18, 'bold'), bg="#f7f7f7", fg="#3b1d14")
        self.label.pack(pady=20)

        # Estilo del Treeview para mostrar los pedidos
        self.style = ttk.Style()
        self.style.configure("Treeview", font=("Arial", 12), background="#f9f9f9", foreground="#3b1d14", rowheight=40)
        self.style.configure("Treeview.Heading", font=("Arial", 14, 'bold'), background="#f7f7f7", foreground="black")
        self.style.map("Treeview", background=[('selected', '#3b1d14')], foreground=[('selected', 'white')])

        # Treeview para mostrar los pedidos
        self.tree = ttk.Treeview(root, columns=("ID", "Cliente", "Platos", "Total", "Tipo Cuenta"), show='headings', style="Treeview")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Cliente", text="Cliente")
        self.tree.heading("Platos", text="Platos")
        self.tree.heading("Total", text="Total")
        self.tree.heading("Tipo Cuenta", text="Tipo Cuenta")
        self.tree.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Frame para contener los botones uno al lado del otro
        button_frame = tk.Frame(root, bg="#f7f7f7")
        button_frame.pack(pady=10)

        # Botón para generar la boleta del pedido (solo para cuentas cliente)
        self.button_generate = tk.Button(button_frame, text="Generar Boleta (Clientes)", command=self.generate_selected_bill, width=25, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
        self.button_generate.pack(side=tk.LEFT, padx=10)

        # Botón para procesar pedidos de cuentas panel
        self.button_process_panel = tk.Button(button_frame, text="Procesar Pedido de Panel", command=self.process_selected_panel_order, width=25, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
        self.button_process_panel.pack(side=tk.LEFT, padx=10)

        self.load_orders()

    def load_orders(self):
        """Cargar los pedidos en la caja"""
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_en_caja_orders()
        for order in orders:
            # Asegurarse de que los platos estén formateados correctamente, con saltos de línea entre cada uno
            formatted_platos = "\n".join(order[2].split(","))
            self.tree.insert("", tk.END, values=(order[0], order[1], formatted_platos, order[3], order[4]))

    def generate_selected_bill(self):
        """Generar la boleta para el pedido seleccionado"""
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
        """Procesar el pedido de panel seleccionado"""
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
