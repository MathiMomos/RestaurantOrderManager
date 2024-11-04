#perdon por la demora :v
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.panel_controller import PanelController


class PanelView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Panel - Restaurant Order Manager")
        self.controller = PanelController()
        self.user_id = user_id
        self.current_category_index = 0

        # Obtener los datos de los platos categorizados desde la base de datos
        self.menu_data = self.controller.get_menu_data()
        self.categories = list(self.menu_data.keys())

        # Título de categoría con texto más grande
        self.label_category = tk.Label(root, text=self.categories[self.current_category_index],font=("Arial", 20, 'bold'))
        self.label_category.pack(pady=20)

        # Título de categoría con texto más grande
        self.label_category = tk.Label(root, text=self.categories[self.current_category_index], font=("Arial", 20, 'bold'))
        self.label_category.pack(pady=20)

        # Contenedor de botones para los platos
        self.frame_menu_buttons = tk.Frame(root)
        self.frame_menu_buttons.pack(pady=10)

        self.load_menu_buttons()

        # Botones para cambiar de categoría
        self.button_previous = tk.Button(root, text="Anterior", command=self.show_previous_category, width=20, height=3, font=("Arial", 12))
        self.button_previous.pack(side=tk.LEFT, padx=20, pady=10)

        self.button_next = tk.Button(root, text="Siguiente", command=self.show_next_category, width=20, height=3, font=("Arial", 12))
        self.button_next.pack(side=tk.RIGHT, padx=20, pady=10)

        # Botón para ver el pedido con texto más grande
        self.button_view_order = tk.Button(root, text="Ver Pedido", command=self.view_order, width=20, height=3, font=("Arial", 12))
        self.button_view_order.pack(pady=20)

    def load_menu_buttons(self):
        """Cargar los botones de los platos para la categoría actual en una cuadrícula de 3x3"""
        # Limpiar botones actuales
        for widget in self.frame_menu_buttons.winfo_children():
            widget.destroy()

        # Crear botones para los platos de la categoría actual
        current_category = self.categories[self.current_category_index]
        menu_items = self.menu_data.get(current_category, [])

        # Limitar a un máximo de 9 platos por categoría para la cuadrícula 3x3
        for index, item in enumerate(menu_items[:9]):
            row = index // 3  # Fila de la cuadrícula (0, 1 o 2)
            col = index % 3  # Columna de la cuadrícula (0, 1 o 2)

            button = tk.Button(self.frame_menu_buttons, text=f"{item[0]}\nS/ {item[1]:.2f}",
                               command=lambda i=item: self.add_to_order(i), width=25, height=5, font=("Arial", 12))
            button.grid(row=row, column=col, padx=10, pady=10)

    def show_previous_category(self):
        """Mostrar la categoría anterior"""
        self.current_category_index = (self.current_category_index - 1) % len(self.categories)
        self.label_category.config(text=self.categories[self.current_category_index])
        self.load_menu_buttons()

    def show_next_category(self):
        """Mostrar la categoría siguiente"""
        self.current_category_index = (self.current_category_index + 1) % len(self.categories)
        self.label_category.config(text=self.categories[self.current_category_index])
        self.load_menu_buttons()

    def add_to_order(self, item):
        """Agregar el plato seleccionado al pedido"""
        item_name, item_price = item
        self.controller.add_item_to_order(self.user_id, item_name, item_price)
        messagebox.showinfo("Éxito", f"'{item_name}' agregado al pedido.")

    def view_order(self):
        """Ver el pedido actual"""
        order_window = tk.Toplevel(self.root)
        order_window.title("Pedido Actual")

        label_order = tk.Label(order_window, text="Pedido Actual", font=("Arial", 14, 'bold'))
        label_order.pack(pady=10)

        tree_order = ttk.Treeview(order_window, columns=("Platos", "Total"), show='headings')
        tree_order.heading("Platos", text="Platos")
        tree_order.heading("Total", text="Total")
        tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Cargar el pedido actual
        order = self.controller.get_user_order(self.user_id)
        if order:
            order_id, items, total = order
            platos = items.rstrip(", ")
            tree_order.insert("", tk.END, values=(platos, f"S/ {total:.2f}"))
        else:
            tree_order.insert("", tk.END, values=("No hay pedidos actuales.", "S/ 0.00"))

        # Botón para confirmar el pedido
        button_confirm = tk.Button(order_window, text="Confirmar Pedido",
                                   command=lambda: self.confirm_order(order_window), width=20, height=2, font=("Arial", 12))
        button_confirm.pack(side=tk.LEFT, padx=10, pady=10)

        # Botón para agregar más platos
        button_add_more = tk.Button(order_window, text="Agregar Platos", command=order_window.destroy, width=20, height=2, font=("Arial", 12))
        button_add_more.pack(side=tk.RIGHT, padx=10, pady=10)

    def confirm_order(self, window):
        """Confirmar el pedido y enviarlo a caja"""
        order = self.controller.get_user_order(self.user_id)
        if order:
            order_id, items, total = order
            confirm = messagebox.askyesno("Confirmar Pedido", "¿Deseas confirmar tu pedido y enviarlo a la caja?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Pedido confirmado y enviado a la caja.")
                    window.destroy()  # Cerrar la ventana de pedido después de confirmar
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No tienes ningún pedido para confirmar.")
