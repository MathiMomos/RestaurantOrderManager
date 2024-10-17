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
        self.tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

        # Botón para confirmar el pedido seleccionado
        self.button_confirm = tk.Button(root, text="Confirmar Pedido", command=self.confirm_selected_order)
        self.button_confirm.pack(pady=10)

        self.button_confirm = tk.Button(root, text="Añadir Plato" , command=self.add_plato)
        self.button_confirm.pack(side=tk.LEFT, padx=10, pady=10)

        self.button_confirm = tk.Button(root, text="Eliminar plato" , command = self.delete_plato)
        self.button_confirm.pack(side=tk.LEFT, padx=10, pady=10)

        self.label_menu = tk.Label(root, text="Registros de Platos/Bebidas del local")
        self.label_menu.pack(pady=10)

        # Treeview para mostrar el menú
        self.tree_menu = ttk.Treeview(root, columns=("ID", "Categoria", "Platos/Bebidas", "Costo"), show='headings')
        self.tree_menu.heading("ID", text="ID")
        self.tree_menu.heading("Categoria", text="Categoría")
        self.tree_menu.heading("Platos/Bebidas", text="Platos/Bebidas")
        self.tree_menu.heading("Costo", text="Costo")
        self.tree_menu.pack(padx=10, pady=10, fill=tk.BOTH, expand=False)

        self.load_orders()
        self.load_menu()

    def load_orders(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        orders = self.controller.get_confirmed_orders()
        for order in orders:
            self.tree.insert("", tk.END, values=order)

    def load_menu(self):
        for row in self.tree_menu.get_children():
            self.tree_menu.delete(row)
        menu_items = self.controller.get_menu_items()
        for item in menu_items:
            self.tree_menu.insert("", tk.END, values=item)

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

    def add_plato(self):
        # Ventana emergente para añadir un nuevo plato
        add_window = tk.Toplevel(self.root)
        add_window.title("Añadir Plato")

        tk.Label(add_window, text="Categoría").pack(pady=5)
        category_entry = tk.Entry(add_window)
        category_entry.pack(pady=5)

        tk.Label(add_window, text="Nombre del Plato/Bebida").pack(pady=5)
        name_entry = tk.Entry(add_window)
        name_entry.pack(pady=5)

        tk.Label(add_window, text="Precio").pack(pady=5)
        price_entry = tk.Entry(add_window)
        price_entry.pack(pady=5)

        def save_dish():
            category = category_entry.get()
            name = name_entry.get()
            price = price_entry.get()

            if category and name and price:
                try:
                    price = float(price)
                    success = self.controller.anadir_plato(category, name, price)
                    if success:
                        messagebox.showinfo("Éxito", "Plato añadido correctamente.")
                        self.load_menu()
                        add_window.destroy()
                    else:
                        messagebox.showerror("Error", "No se pudo añadir el plato.")
                except ValueError:
                    messagebox.showerror("Error", "Por favor, ingrese un precio válido.")
            else:
                messagebox.showwarning("Advertencia", "Por favor, complete todos los campos.")

        save_button = tk.Button(add_window, text="Guardar", command=save_dish)
        save_button.pack(pady=10)

    def delete_plato(self):
        selected = self.tree_menu.focus()
        if selected:
            dish = self.tree_menu.item(selected, 'values')
            dish_id = dish[0]
            confirm = messagebox.askyesno("Eliminar Plato", f"¿Deseas eliminar el plato ID {dish_id}?")
            if confirm:
                success = self.controller.eliminar_plato(dish_id)
                if success:
                    messagebox.showinfo("Éxito", f"Plato ID {dish_id} eliminado correctamente.")
                    self.load_menu()
                else:
                    messagebox.showerror("Error", "No se pudo eliminar el plato.")
        else:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un plato para eliminar.")
