import tkinter as tk
from tkinter import messagebox


class ClienteView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller
        self.root.geometry("1200x600")
        self.cart = {}

        # Establecer color de fondo de la ventana
        self.root.configure(bg="#DDD6CC")
        self.menu_frame = tk.Frame(self.root, bg="#DDD6CC")
        self.menu_frame.pack(fill=tk.BOTH, expand=True)

        self.show_menu("ENTRADAS")

    def show_menu(self, category="ENTRADAS"):
        self.clear_frame()

        # Aumentar el tamaño del título y ajustar el espacio vertical
        tk.Label(self.menu_frame, text=category.upper(), font=("Arial", 36), bg="#DDD6CC", fg="#19222B").pack(
            pady=(50, 10))

        menu_items = {
            "ENTRADAS": [("Papa a la Huancaína", 15), ("Causa Rellena", 18), ("Anticuchos con Papas", 22),
                         ("Choclo con Queso", 14), ("Ocopa Arequipeña", 16), ("Tamales Criollos", 12),
                         ("Choros a la Chalaca", 20), ("Leche de Tigre", 18), ("Papa Rellena", 15)],

            "SOPAS": [("Sopa a la Criolla", 18), ("Caldo de Gallina", 16), ("Chupe de Camarones", 22),
                      ("Shambar Norteño", 20), ("Sancochado", 24), ("Parihuela", 25),
                      ("Sopa de Choros", 18), ("Aguadito de Pollo", 15), ("Chilcano de Pescado", 17)],

            "PLATOS PRINCIPALES": [("Lomo Saltado", 35), ("Ají de Gallina", 28), ("Seco de Res con Frejoles", 32),
                                   ("Tacu Tacu con Lomo", 38), ("Ceviche Mixto", 40), ("Arroz con Pollo", 30),
                                   ("Causa Limeña", 22), ("Papa a la Huancaína", 18), ("Carapulcra con Sopa Seca", 36)],

            "GUARNICIONES": [("Arroz Blanco", 6), ("Papas Fritas", 10), ("Yuquitas Fritas", 12),
                             ("Ensalada Criolla", 10), ("Tostones de Plátano", 15), ("Arroz Chaufa", 18),
                             ("Choclo con Queso", 14), ("Tacu Tacu", 16), ("Camotes Fritos", 10)],

            "POSTRES": [("Suspiro a la Limeña", 15), ("Mazamorra Morada", 12), ("Arroz con Leche", 10),
                        ("Turrón de Doña Pepa", 18), ("Picarones", 20), ("Crema Volteada", 14),
                        ("Alfajores", 8), ("Helado de Lucuma", 16), ("King Kong de Manjar Blanco", 20)],

            "BEBIDAS": [("Chicha Morada", 8), ("Emoliente", 7), ("Refresco de Maracuyá", 7),
                        ("Jugo de Naranja", 10), ("Pisco Sour", 18), ("Cerveza Artesanal", 12),
                        ("Agua Mineral", 5), ("Limonada Clásica", 9), ("Chilcano de Pisco", 16)]
        }

        items = menu_items[category]

        button_frame = tk.Frame(self.menu_frame, bg="#DDD6CC")
        button_frame.pack(pady=30)

        for i in range(0, min(len(items), 9)):
            item, price = items[i]
            btn = tk.Button(button_frame, text=f"{item} - S/ {price}", font=("Arial", 16),
                            command=lambda item=item, price=price: self.add_to_cart(item, price), width=25, height=3,
                            bg="#19222B", fg="#BD9240", activebackground="#BD9240", activeforeground="#19222B")
            btn.grid(row=i // 3, column=i % 3, padx=20, pady=10)

        # Mantener los botones de navegación en su lugar
        nav_frame = tk.Frame(self.menu_frame, bg="#DDD6CC")
        nav_frame.pack(side=tk.BOTTOM, pady=(10, 30), fill=tk.X)

        # Botón Anterior a la izquierda
        tk.Button(nav_frame, text="<< Anterior", command=lambda: self.navigate_categories(category, -1),
                  font=("Arial", 14), height=2, bg="#19222B", fg="#BD9240", activebackground="#BD9240",
                  activeforeground="#19222B").pack(side=tk.LEFT, padx=(95, 5))

        # Botón Ver Pedido en el medio
        tk.Button(nav_frame, text="Ver Pedido", command=self.show_cart,
                  font=("Arial", 14), height=2, bg="#19222B", fg="#BD9240", activebackground="#BD9240",
                  activeforeground="#19222B").pack(side=tk.LEFT, padx=(10, 10), expand=True)

        # Botón Siguiente a la derecha
        tk.Button(nav_frame, text="Siguiente >>", command=lambda: self.navigate_categories(category, 1),
                  font=("Arial", 14), height=2, bg="#19222B", fg="#BD9240", activebackground="#BD9240",
                  activeforeground="#19222B").pack(side=tk.RIGHT, padx=(5, 95))

    def navigate_categories(self, current_category, direction):
        categories = ["ENTRADAS", "SOPAS", "PLATOS PRINCIPALES", "GUARNICIONES", "POSTRES", "BEBIDAS"]
        current_index = categories.index(current_category)
        new_index = (current_index + direction) % len(categories)
        self.show_menu(categories[new_index])

    def add_to_cart(self, item, price):
        if item in self.cart:
            self.cart[item]['qty'] += 1
        else:
            self.cart[item] = {'qty': 1, 'price': price}
        messagebox.showinfo("Agregado", f"Has agregado {item} a tu pedido.")

    def show_cart(self):
        self.clear_frame()

        tk.Label(self.menu_frame, text="PEDIDO", font=("Arial", 24), bg="#DDD6CC", fg="#19222B").pack(pady=(40, 10))

        # Crear un marco para los platos pedidos, solo con bordes
        cart_frame = tk.Frame(self.menu_frame, bg="#DDD6CC", bd=5, relief=tk.SOLID)
        cart_frame.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        for item, details in self.cart.items():
            frame = tk.Frame(cart_frame, bg="#DDD6CC")
            frame.pack(pady=10)

            tk.Label(frame, text=item, font=("Arial", 16), bg="#DDD6CC", fg="#19222B").pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(frame, text=f"x{details['qty']}", font=("Arial", 16), bg="#DDD6CC", fg="#19222B").pack(
                side=tk.LEFT, padx=(0, 10))
            tk.Button(frame, text="X", command=lambda i=item: self.remove_from_cart(i), bg="#BD9240", fg="#19222B",
                      activebackground="#19222B", activeforeground="#BD9240").pack(side=tk.LEFT, padx=(0, 10))
            tk.Label(frame, text=f"S/ {details['price'] * details['qty']}", font=("Arial", 16), bg="#DDD6CC",
                     fg="#19222B").pack(side=tk.LEFT)

        button_frame = tk.Frame(self.menu_frame, bg="#DDD6CC")
        button_frame.pack(pady=10)

        tk.Button(button_frame, text="Agregar Platos", command=self.show_menu,
                  font=("Arial", 16), height=2, bg="#19222B", fg="#BD9240", activebackground="#BD9240",
                  activeforeground="#19222B").pack(side=tk.LEFT, padx=(50, 10))

        tk.Button(button_frame, text="Confirmar Orden", command=self.confirm_order,
                  font=("Arial", 16), height=2, bg="#19222B", fg="#BD9240", activebackground="#BD9240",
                  activeforeground="#19222B").pack(side=tk.LEFT, padx=(10, 50))

    def remove_from_cart(self, item):
        if item in self.cart:
            del self.cart[item]
            messagebox.showinfo("Eliminado", f"Has eliminado {item} de tu pedido.")
            self.show_cart()

    def confirm_order(self):
        if not self.cart:
            messagebox.showwarning("Sin pedido", "No has agregado platos a tu pedido.")
            return

        total = sum(details['qty'] * details['price'] for details in self.cart.values())
        messagebox.showinfo("Pedido confirmado", f"Has confirmado tu pedido. Total a pagar: S/ {total}")
        self.cart.clear()
        self.show_menu()

    def clear_frame(self):
        for widget in self.menu_frame.winfo_children():
            widget.destroy()
