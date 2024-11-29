import tkinter as tk
from tkinter import messagebox, ttk
from controllers.cliente_controller import ClienteController

class ClienteView:
    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Cliente - Realizar Pedido")
        self.root.geometry("1200x600")  # Tamaño fijo de la ventana
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
        self.left_frame = tk.Frame(self.root, bg="lightgray", width=400)  # Cambia el color y el tamaño según sea necesario
        self.left_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Frame derecho (contiene la funcionalidad)
        self.right_frame = tk.Frame(self.root, bg="white")
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # Configuración del canvas y otros elementos en el marco derecho
        self.canvas = tk.Canvas(self.right_frame, bg="white", highlightthickness=0)
        self.canvas.place(x=0, y=0, width=800, height=600)

        # Flecha izquierda
        self.canvas.create_text(
            50, 550,  # Coordenadas X, Y
            text="←",
            font=("Arial", 36, "bold"),
            fill="black",
            tags="prev_arrow"
        )
        self.canvas.tag_bind("prev_arrow", "<Button-1>", lambda event: self.prev_category())

        # Flecha derecha
        self.canvas.create_text(
            750, 550,  # Coordenadas X, Y
            text="→",
            font=("Arial", 36, "bold"),
            fill="black",
            tags="next_arrow"
        )
        self.canvas.tag_bind("next_arrow", "<Button-1>", lambda event: self.next_category())

        # Botón para ver pedido
        self.button_order = tk.Button(
            self.right_frame,
            text="Ver Pedido",
            command=self.show_order,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_order.place(x=300, y=530, width=100, height=40)

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
                width=18,
                height=3,
                font=("Arial", 16),
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

    def prev_category(self):
        if self.current_category > 0:
            self.current_category -= 1
        else:
            self.current_category = len(self.categories) - 1
        self.update_category()

    def next_category(self):
        if self.current_category < len(self.categories) - 1:
            self.current_category += 1
        else:
            self.current_category = 0
        self.update_category()

    def update_category(self):
        self.label_category.config(text=self.categories[self.current_category])
        self.create_menu_buttons()

    def add_to_order(self, plato, precio):
        self.controller.add_item_to_order(self.user_id, plato, precio)
        messagebox.showinfo("Éxito", f"{plato} agregado al pedido.")

    def show_order(self):
        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Pedido Actual")
        self.order_window.configure(bg="white")

        self.tree_order = ttk.Treeview(self.order_window, columns=("Platos", "Total"), show='headings')
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Total", text="Total")
        self.tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.load_current_order()

        self.button_confirm = tk.Button(
            self.order_window,
            text="Confirmar Pedido",
            command=self.confirm_order,
            bg="#3b1d14",
            fg="white",
            font=("Arial",  14)
        )
        self.button_confirm.pack(side=tk.LEFT, padx=20, pady=20)

        self.button_add_more = tk.Button(
            self.order_window,
            text="Agregar Platos",
            command=self.order_window.destroy,
            bg="#3b1d14",
            fg="white",
            font=("Arial", 14)
        )
        self.button_add_more.pack(side=tk.RIGHT, padx=20, pady=20)

    def load_current_order(self):
        self.current_order = self.controller.get_current_order(self.user_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, total = self.current_order
            platos_lista = [plato.strip() for plato in items.split(',')]
            for plato in platos_lista:
                self.tree_order.insert("", tk.END, values=(plato, ""))
            self.tree_order.insert("", tk.END, values=("Total", f"S/ {total:.2f}"))
        else:
            self.tree_order.insert("", tk.END, values=("No hay pedido actual.", "S/ 0.00"))

    def confirm_order(self):
        if self.current_order:
            order_id, items, total = self.current_order
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