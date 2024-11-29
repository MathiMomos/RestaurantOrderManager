import tkinter as tk
from tkinter import messagebox, ttk
from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Cliente - Realizar Pedido")
        self.root.geometry("1280x720")  # Tamaño fijo de la ventana
        self.controller = ClienteController()
        self.user_id = user_id
        self.current_order = None
        self.current_category = 0

        # Configuración del fondo
        self.root.configure(bg="white")

        # Datos de los platos categorizados
        self.categories = ["SOPAS", "BEBIDAS", "PLATOS PRINCIPALES", "GUARNICIONES", "POSTRES", "ENTRADAS"]
        self.menu_items = {
            "SOPAS": [("Sopa a la Criolla", 18), ("Caldo de Gallina", 16), ("Chupe de Camarones", 22),
                      ("Shambar Norteño", 20), ("Sancochado", 24), ("Parihuela", 25), ("Sopa de Quinua", 15),
                      ("Sopa de Pollo", 17), ("Sopa de Verduras", 12)],
            "BEBIDAS": [("Chicha Morada", 8), ("Emoliente", 7), ("Refresco de Maracuyá", 7),
                        ("Jugo de Naranja", 10), ("Pisco Sour", 18), ("Cerveza Artesanal", 12), ("Agua Mineral", 5),
                        ("Café", 4), ("Té de Menta", 6)],
            "PLATOS PRINCIPALES": [("Lomo Saltado", 35), ("Ají de Gallina", 28), ("Seco de Res con Frejoles", 32),
                                   ("Tacu Tacu con Lomo", 38), ("Ceviche Mixto", 40), ("Arroz con Pollo", 30),
                                   ("Pollo a la Brasa", 25), ("Chicharrón de Pollo", 20), ("Parrillada", 45)],
            "GUARNICIONES": [("Arroz Blanco", 6), ("Papas Fritas", 10), ("Yuquitas Fritas", 12),
                             ("Ensalada Criolla", 10), ("Tostones de Plátano", 15), ("Arroz Chaufa", 18),
                             ("Puré de Papas", 8), ("Choclo con Queso", 7), ("Ensalada de Quinoa", 12)],
            "POSTRES": [("Suspiro a la Limeña", 15), ("Mazamorra Morada", 12), ("Arroz con Leche", 10),
                        ("Turrón de Doña Pepa", 18), ("Picarones", 20), ("Crema Volteada", 14),
                        ("Helado de Vainilla", 8), ("Tarta de Manzana", 12), ("Brownie con Helado", 14)],
            "ENTRADAS": [("Papa a la Huancaína", 15), ("Causa Rellena", 18), ("Anticuchos con Papas", 22),
                         ("Choclo con Queso", 14), ("Ocopa Arequipeña", 16), ("Tamales Criollos", 12),
                         ("Empanadas", 8), ("Tequeños", 10), ("Canastitas de Mariscos", 18)]
        }

        self.setup_ui()

    def setup_ui(self):
        # Frame izquierdo (vacío)
        self.left_frame = tk.Frame(self.root, bg="lightgray", width=310)
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Frame derecho (contiene la funcionalidad)
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Botones de categorías en la parte superior del frame derecho
        self.category_buttons_frame = tk.Frame(self.right_frame, bg="white")
        self.category_buttons_frame.pack(pady=10)

        for category in self.categories:
            btn = tk.Button(
                self.category_buttons_frame,
                text=category,
                font=("Arial", 10, "bold"),
                bg="#3b1d14",  # Fondo colorido
                fg="white",  # Texto blanco
                height=2,
                width=17,
                relief="solid",
                command=lambda c=category: self.change_category(c)  # Cambiar categoría al hacer clic
            )
            btn.pack(side=tk.LEFT, padx=1)

        # Categoría de los platos
        self.label_category = tk.Label(
            self.right_frame,
            text=self.categories[self.current_category],
            font=("Arial", 24, "bold"),
            bg="white"
        )
        self.label_category.pack(pady=(20, 10))

        # Frame para los botones de los platos
        self.frame_menu = tk.Frame(self.right_frame, bg="white")
        self.frame_menu.pack(pady=(20, 30))

        self.create_menu_buttons()

        # Cargar el pedido actual automáticamente al iniciar
        self.show_order()  # Agrega esta línea

    def change_category(self, category):
        # Cambiar la categoría actual cuando se hace clic en una de ellas
        if category in self.categories:
            self.current_category = self.categories.index(category)
            self.update_category()

    def update_category(self):
        # Actualizar la categoría y mostrar los platos correspondientes
        self.label_category.config(text=self.categories[self.current_category])
        self.create_menu_buttons()

    def create_menu_buttons(self):
        # Limpiar el frame para evitar superposición de botones
        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        # Crear botones para los platos de la categoría actual
        current_items = self.menu_items[self.categories[self.current_category]]
        row, col = 0, 0
        for idx, (plato, precio) in enumerate(current_items):
            btn = tk.Button(
                self.frame_menu,
                text=f"{plato}\nS/ {precio:.2f}",
                width=20,
                height=4,
                font=("Arial", 18),
                bg="white",
                fg="#3b1d14",
                highlightbackground="#3b1d14",
                highlightthickness=2,
                relief="solid",
                command=lambda p=plato, pr=precio: self.add_to_order(p, pr)
            )
            btn.grid(row=row, column=col, padx=20, pady=15)

            col += 1
            if col == 3:  # Solo tres botones por fila
                col = 0
                row += 1

        # Esto asegura que las filas y columnas tengan el mismo tamaño
        self.frame_menu.grid_rowconfigure(row, weight=1)
        self.frame_menu.grid_columnconfigure(0, weight=1)
        self.frame_menu.grid_columnconfigure(1, weight=1)
        self.frame_menu.grid_columnconfigure(2, weight=1)

    def add_to_order(self, plato, precio, cantidad=1):
        # Llamada al metodo de agregar ítem al pedido
        self.controller.add_item_to_order(self.user_id, plato, precio, cantidad)
        self.load_current_order()

    def remove_selected_item(self):
        selected_item = self.tree_order.selection()
        if not selected_item:
            messagebox.showwarning("Advertencia", "Por favor, selecciona un plato de la orden para eliminar.")
            return

        # Guardar la selección antes de realizar la eliminación
        selected_item_values = self.tree_order.item(selected_item, "values")

        # Obtener el plato seleccionado
        plato_seleccionado = selected_item_values[0]  # Nombre del plato

        # Llamar al metodo para eliminar el plato o decrementar la cantidad
        self.controller.remove_item_from_order(self.user_id, plato_seleccionado)

        # Recargar la orden actual después de la eliminación
        self.load_current_order()

        # Volver a seleccionar el plato que fue seleccionado previamente
        for item in self.tree_order.get_children():
            if self.tree_order.item(item, "values")[0] == plato_seleccionado:
                self.tree_order.selection_set(item)
                break

    def show_order(self):
        for widget in self.left_frame.winfo_children():
            widget.destroy()

        # Crear un estilo para el Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview", font=("Arial", 12))  # Cambiar el tamaño de la fuente para las celdas
        style.configure("Custom.Treeview.Heading",
                        font=("Arial", 13, "bold"))  # Cambiar el tamaño de la fuente para las cabeceras

        # Crear el Treeview con el estilo personalizado
        self.tree_order = ttk.Treeview(self.left_frame, columns=("Platos", "Precio", "Cantidad"), show='headings',
                                       style="Custom.Treeview")
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Precio", text="Prec/Uni")
        self.tree_order.heading("Cantidad", text="Cantidad")

        self.tree_order.column("Platos", width=200)  # Ancho de la columna Platos
        self.tree_order.column("Precio", width=80, anchor='center')  # Ancho de la columna Precio
        self.tree_order.column("Cantidad", width=80, anchor='center')  # Ancho de la columna Cantidad

        self.tree_order.pack(padx=10, pady=5, fill=tk.BOTH, expand=True)
        self.load_current_order()

        self.button_confirm = tk.Button(
            self.left_frame,
            text="Confirmar Pedido",
            command=self.confirm_order,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_confirm.pack(side=tk.LEFT, padx=20, pady=20)

        # Botón para eliminar el plato seleccionado
        self.button_remove = tk.Button(
            self.left_frame,
            text="Eliminar Plato",
            command=self.remove_selected_item,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_remove.pack(side=tk.LEFT, padx=20, pady=20)

    def load_current_order(self):
        self.current_order = self.controller.get_current_order(self.user_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
            platos_lista = [plato.strip() for plato in items.split(',')]
            precios_lista = [float(precio.strip()) for precio in item_prices.split(',') if precio.strip()]
            cantidades_lista = [int(cantidad.strip()) for cantidad in item_amounts.split(',') if cantidad.strip()]
            for plato, precio, cantidad in zip(platos_lista, precios_lista, cantidades_lista):
                self.tree_order.insert("", tk.END, values=(plato, f"S/ {precio:.2f}", f"{cantidad}"))
            self.tree_order.insert("", tk.END, values=("Total", f"S/ {total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedido actual.", "S/ 0.00"))

    def confirm_order(self):
        if self.current_order:
            order_id, items, item_prices, item_amounts, total = self.current_order
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
