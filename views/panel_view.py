# views/panel_view.py

import tkinter as tk
from tkinter import messagebox, ttk
from controllers.panel_controller import PanelController

class PanelView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Panel - Restaurant Order Manager")
        self.controller = PanelController()
        self.user_id = user_id  # No necesita name o document

        # Configuración de la ventana
        self.root.configure(bg="white")
        self.root.geometry("1280x720")  # Tamaño ampliado para mejor usabilidad
        self.root.resizable(False, False)

        # Datos de los platos categorizados
        self.categories = ["SOPAS", "BEBIDAS", "PLATOS PRINCIPALES", "GUARNICIONES", "POSTRES", "ENTRADAS"]
        self.menu_items = self.controller.get_menu_data()

        self.current_category = self.categories[0]

        self.setup_ui()

    def setup_ui(self):
        # Frame derecho (contiene la funcionalidad de pedidos)
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Botones de categorías en la parte superior del frame derecho
        self.category_buttons_frame = tk.Frame(self.right_frame, bg="white")
        self.category_buttons_frame.pack(pady=10)

        for category in self.categories:
            btn = tk.Button(
                self.category_buttons_frame,
                text=category,
                font=("Arial", 10, "bold"),
                bg="#3b1d14",  # Fondo colorido
                fg="white",    # Texto blanco
                height=2,
                width=17,
                relief="solid",
                command=lambda c=category: self.change_category(c)  # Cambiar categoría al hacer clic
            )
            btn.pack(side=tk.LEFT, padx=1)

        # Categoría de los platos
        self.label_category = tk.Label(
            self.right_frame,
            text=self.current_category,
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.label_category.pack(pady=(20, 10))

        # Frame para los botones de los platos
        self.frame_menu = tk.Frame(self.right_frame, bg="white")
        self.frame_menu.pack(pady=(20, 30))

        self.create_menu_buttons()

        # Frame izquierdo para mostrar el pedido actual
        self.left_frame = tk.Frame(self.root, bg="lightgray", width=400)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=20, pady=20)

        # Título del pedido
        self.label_order = tk.Label(
            self.left_frame,
            text="Pedido Actual",
            font=("Arial", 18, "bold"),
            bg="lightgray"
        )
        self.label_order.pack(pady=10)

        # Treeview para mostrar el pedido
        self.tree_order = ttk.Treeview(self.left_frame, columns=("Platos", "Precio", "Cantidad"), show='headings', height=15)
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Precio", text="Precio/Uni")
        self.tree_order.heading("Cantidad", text="Cantidad")

        self.tree_order.column("Platos", width=200)
        self.tree_order.column("Precio", width=100, anchor='center')
        self.tree_order.column("Cantidad", width=100, anchor='center')

        self.tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Frame para los botones de acción
        self.action_buttons_frame = tk.Frame(self.left_frame, bg="lightgray")
        self.action_buttons_frame.pack(pady=10)

        # Botón para confirmar el pedido
        self.button_confirm = tk.Button(
            self.action_buttons_frame,
            text="Confirmar Pedido",
            command=self.confirm_order,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14),
            width=15
        )
        self.button_confirm.pack(side=tk.LEFT, padx=10)

        # Botón para eliminar el plato seleccionado
        self.button_remove = tk.Button(
            self.action_buttons_frame,
            text="Eliminar Plato",
            command=self.remove_selected_item,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14),
            width=15
        )
        self.button_remove.pack(side=tk.LEFT, padx=10)

        self.load_current_order()

    def change_category(self, category):
        """Cambiar la categoría actual y actualizar los botones de platos."""
        if category in self.categories:
            self.current_category = category
            self.label_category.config(text=self.current_category)
            self.create_menu_buttons()

    def create_menu_buttons(self):
        """Crear botones para los platos de la categoría actual."""
        # Limpiar el frame para evitar superposición de botones
        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        # Crear botones para los platos de la categoría actual
        current_items = self.menu_items.get(self.current_category, [])
        row, col = 0, 0
        for idx, (plato, precio) in enumerate(current_items):
            btn = tk.Button(
                self.frame_menu,
                text=f"{plato}\nS/ {precio:.2f}",
                width=20,
                height=4,
                font=("Arial", 14),
                bg="white",
                fg="#3b1d14",
                highlightbackground="#3b1d14",
                highlightthickness=2,
                relief="solid",
                command=lambda p=plato, pr=precio: self.add_to_order(p, pr)
            )
            btn.grid(row=row, column=col, padx=10, pady=10)

            col += 1
            if col == 3:  # Solo tres botones por fila
                col = 0
                row += 1

    def add_to_order(self, plato, precio, cantidad=1):
        """Agregar un plato al pedido."""
        success = self.controller.add_item_to_order(self.user_id, plato, precio, cantidad)
        if success:
            self.load_current_order()
        else:
            messagebox.showerror("Error", "No se pudo agregar el plato al pedido.")

    def load_current_order(self):
        """Cargar y mostrar el pedido actual en el Treeview."""
        self.current_order = self.controller.get_current_order(self.user_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
            platos_lista = [plato.strip() for plato in items.split(',') if plato.strip()]
            precios_lista = [float(precio.strip()) for precio in item_prices.split(',') if precio.strip()]
            cantidades_lista = [int(cantidad.strip()) for cantidad in item_amounts.split(',') if cantidad.strip()]
            for plato, precio, cantidad in zip(platos_lista, precios_lista, cantidades_lista):
                self.tree_order.insert("", tk.END, values=(plato, f"S/ {precio:.2f}", f"{cantidad}"))
            # Mostrar el total al final
            self.tree_order.insert("", tk.END, values=("Total", "", f"S/ {total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedido actual.", "", "S/ 0.00"))

    def remove_selected_item(self):
        """Eliminar el plato seleccionado del pedido."""
        selected_item = self.tree_order.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un plato para eliminar.")
            return

        selected_values = self.tree_order.item(selected_item, "values")
        plato_seleccionado = selected_values[0]

        if plato_seleccionado == "Total" or plato_seleccionado == "No hay pedido actual.":
            messagebox.showwarning("Advertencia", "No puedes eliminar este elemento.")
            return

        # Llamar al método para eliminar el plato o decrementar la cantidad
        success = self.controller.remove_item_from_order(self.user_id, 1, plato_seleccionado)  # client_id=1 para Panel
        if success:
            self.load_current_order()
        else:
            messagebox.showerror("Error", "No se pudo eliminar el plato del pedido.")

    def confirm_order(self):
        """Confirmar el pedido actual y enviarlo a caja."""
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
            confirm = messagebox.askyesno("Confirmar Pedido", f"¿Deseas confirmar tu pedido ID {order_id}?")
            if confirm:
                success = self.controller.confirm_order(order_id)
                if success:
                    messagebox.showinfo("Éxito", "Pedido confirmado y enviado a caja.")
                    self.load_current_order()
                else:
                    messagebox.showerror("Error", "No se pudo confirmar el pedido.")
        else:
            messagebox.showwarning("Advertencia", "No tienes ningún pedido para confirmar.")
