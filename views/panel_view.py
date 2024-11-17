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

        self.categories = ["SOPAS", "BEBIDAS", "PLATOS PRINCIPALES", "GUARNICIONES", "POSTRES", "ENTRADAS"]
        self.menu_data = {
            "SOPAS": [
                ("Sopa a la Criolla", 18),
                ("Caldo de Gallina", 16),
                ("Chupe de Camarones", 22),
                ("Shambar Norteño", 20),
                ("Sancochado", 24),
                ("Parihuela", 25),
                ("Sopa de Choros", 18),
                ("Aguadito de Pollo", 15),
                ("Chilcano de Pescado", 17),
            ],
            "BEBIDAS": [
                ("Chicha Morada", 8),
                ("Emoliente", 7),
                ("Refresco de Maracuyá", 7),
                ("Jugo de Naranja", 10),
                ("Pisco Sour", 18),
                ("Cerveza Artesanal", 12),
                ("Agua Mineral", 5),
                ("Limonada Clásica", 9),
                ("Chilcano de Pisco", 16),
            ],
            "PLATOS PRINCIPALES": [
                ("Lomo Saltado", 35),
                ("Ají de Gallina", 28),
                ("Seco de Res con Frejoles", 32),
                ("Tacu Tacu con Lomo", 38),
                ("Ceviche Mixto", 40),
                ("Arroz con Pollo", 30),
                ("Causa Limeña", 22),
                ("Papa a la Huancaína", 18),
                ("Carapulcra con Sopa Seca", 36),
            ],
            "GUARNICIONES": [
                ("Arroz Blanco", 6),
                ("Papas Fritas", 10),
                ("Yuquitas Fritas", 12),
                ("Ensalada Criolla", 10),
                ("Tostones de Plátano", 15),
                ("Arroz Chaufa", 18),
                ("Choclo con Queso", 14),
                ("Tacu Tacu", 16),
                ("Camotes Fritos", 10),
            ],
            "POSTRES": [
                ("Suspiro a la Limeña", 15),
                ("Mazamorra Morada", 12),
                ("Arroz con Leche", 10),
                ("Turrón de Doña Pepa", 18),
                ("Picarones", 20),
                ("Crema Volteada", 14),
                ("Alfajores", 8),
                ("Helado de Lucuma", 16),
                ("King Kong de Manjar Blanco", 20),
            ],
            "ENTRADAS": [
                ("Papa a la Huancaína", 15),
                ("Causa Rellena", 18),
                ("Anticuchos con Papas", 22),
                ("Choclo con Queso", 14),
                ("Ocopa Arequipeña", 16),
                ("Tamales Criollos", 12),
                ("Choros a la Chalaca", 20),
                ("Leche de Tigre", 18),
                ("Papa Rellena", 15),
            ],
        }

        # Configuración del fondo
        self.root.configure(bg="white")

        # Canvas para flechas, creado primero para no cubrir otros elementos
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0, width=1200, height=600)

        # Flecha izquierda
        self.canvas.create_text(
            50, 550,  # Coordenadas X, Y
            text="←",
            font=("Arial", 36, "bold"),
            fill="black",
            tags="prev_arrow"
        )
        self.canvas.tag_bind("prev_arrow", "<Button-1>", lambda event: self.show_previous_category())

        # Flecha derecha
        self.canvas.create_text(
            1150, 550,  # Coordenadas X, Y
            text="→",
            font=("Arial", 36, "bold"),
            fill="black",
            tags="next_arrow"
        )
        self.canvas.tag_bind("next_arrow", "<Button-1>", lambda event: self.show_next_category())

        # Título de categoría con texto más grande
        self.label_category = tk.Label(self.root, text=self.categories[self.current_category_index], font=("Arial", 20, 'bold'), bg="white")
        self.label_category.pack(pady=20)

        # Contenedor de botones para los platos
        self.frame_menu_buttons = tk.Frame(self.root, bg="white")
        self.frame_menu_buttons.pack(pady=10)

        self.load_menu_buttons()

        # Botón para ver el pedido con texto más pequeño
        self.button_view_order = tk.Button(self.root, text="Ver Pedido", command=self.view_order, width=18, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
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
                               command=lambda i=item: self.add_to_order(i), width=25, height=5, font=("Arial", 12), bg="white", fg="#3b1d14", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
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
        button_confirm = tk.Button(order_window, text="Confirmar Pedido", command=lambda: self.confirm_order(order_window), width=18, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
        button_confirm.pack(side=tk.LEFT, padx=10, pady=10)

        # Botón para agregar más platos
        button_add_more = tk.Button(order_window, text="Agregar Platos", command=order_window.destroy, width=18, height=2, font=("Arial", 12), bg="#3b1d14", fg="white", highlightbackground="#3b1d14", highlightthickness=2, relief="solid")
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
