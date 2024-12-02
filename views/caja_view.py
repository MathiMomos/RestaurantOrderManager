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
        self.tree = ttk.Treeview(root, columns=("ID", "Cliente", "Platos", "Total", "Tipo Cuenta"), show='headings',
                                 style="Treeview")
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
        self.button_generate = tk.Button(button_frame, text="Generar Boleta (Clientes)",
                                         command=self.generate_selected_bill, width=25, height=2, font=("Arial", 12),
                                         bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2,
                                         relief="solid")
        self.button_generate.pack(side=tk.LEFT, padx=10)

        # Botón para procesar pedidos de cuentas panel
        self.button_process_panel = tk.Button(button_frame, text="Procesar Pedido de Panel",
                                              command=self.controller.process_panel_order(self.user_id), width=25, height=2,
                                              font=("Arial", 12), bg="#3b1d14", fg="white",
                                              highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
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
            total = order[3]
            tipo_cuenta = order[4]

            if tipo_cuenta == 'cliente':
                # Abre la ventana para ingresar el método de pago
                self.open_payment_window(order_id, cliente, total)
            else:
                messagebox.showwarning("Advertencia", "Solo se puede generar boleta para pedidos de clientes.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un pedido para generar la boleta.")

    def open_payment_window(self, order_id, cliente, total):
        """Abre una ventana emergente para ingresar el método de pago"""
        payment_window = tk.Toplevel(self.root)
        payment_window.title("Método de Pago")
        payment_window.geometry("400x300")

        tk.Label(payment_window, text=f"ID Pedido: {order_id}", font=("Arial", 12)).pack(pady=10)
        tk.Label(payment_window, text=f"Cliente: {cliente}", font=("Arial", 12)).pack(pady=10)
        tk.Label(payment_window, text=f"Total a Pagar: {total}", font=("Arial", 12)).pack(pady=10)

        # Selección del metodo de pago
        payment_method_label = tk.Label(payment_window, text="Método de Pago:", font=("Arial", 12))
        payment_method_label.pack(pady=10)
        payment_methods = ["Tarjeta", "Yape", "Plin", "Sencillo"]
        method_var = tk.StringVar()
        method_dropdown = ttk.Combobox(payment_window, textvariable=method_var, values=payment_methods,
                                       state="readonly")
        method_dropdown.pack(pady=10)
        method_dropdown.set(payment_methods[0])  # Establecer valor por defecto

        # Botón para confirmar el pago y generar la boleta
        confirm_button = tk.Button(payment_window, text="Generar Boleta",
                                   command=lambda: self.confirm_payment(payment_window, order_id, method_var.get(),
                                                                        total))
        confirm_button.pack(pady=20)

    def confirm_payment(self, payment_window, order_id, method_pay, total):
        """Confirma el pago, inserta en la tabla caja y finaliza la orden"""
        success = self.controller.generate_bill(order_id, method_pay)
        if success:
            messagebox.showinfo("Éxito", "Boleta generada y orden finalizada.")
            self.load_orders()
            payment_window.destroy()  # Cerrar ventana de pago
        else:
            messagebox.showerror("Error", "No se pudo generar la boleta.")