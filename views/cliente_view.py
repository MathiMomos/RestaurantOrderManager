#perdon por la demora :v
import tkinter as tk
from tkinter import messagebox, ttk
from controllers.cliente_controller import ClienteController

class ClienteView:


    def __init__(self, root, user_id):
        self.root = root
        self.root.title("Cliente - Realizar Pedido")
        self.controller = ClienteController()
        self.user_id = user_id
        self.current_order = None
        self.current_category = 0

        # Configuración del fondo y color de los botones
        self.root.configure(bg="#BFD7EA")
        self.button_color = "#0B3954"
        self.button_font = ("Arial", 14)

        # Datos de los platos categorizados
        self.menu_items = self.controller.get_menu_items1()
        self.categories = list(self.menu_items.keys())

        self.setup_ui()

    def setup_ui(self):
        # Categoría de los platos
        self.label_category = tk.Label(self.root, text=self.categories[self.current_category], font=("Arial", 24, "bold"), bg="#BFD7EA")
        self.label_category.pack(pady=(50, 20))

        # Frame para los botones de los platos
        self.frame_menu = tk.Frame(self.root, bg="#BFD7EA")
        self.frame_menu.pack(pady=(20, 30))

        self.create_menu_buttons()

        # Botones de navegación
        self.button_prev = tk.Button(self.root, text="Anterior", command=self.prev_category, bg=self.button_color, fg="white", font=self.button_font)
        self.button_prev.pack(side=tk.LEFT, padx=20, pady=(10, 40))

        self.button_order = tk.Button(self.root, text="Ver Pedido", command=self.show_order, bg=self.button_color, fg="white", font=self.button_font)
        self.button_order.pack(side=tk.LEFT, padx=20, pady=(10, 40))

        self.button_next = tk.Button(self.root, text="Siguiente", command=self.next_category, bg=self.button_color, fg="white", font=self.button_font)
        self.button_next.pack(side=tk.RIGHT, padx=20, pady=(10, 40))

    def create_menu_buttons(self):
        # Limpiar el frame para evitar superposición de botones
        for widget in self.frame_menu.winfo_children():
            widget.destroy()

        # Crear botones para los platos de la categoría actual
        current_items = self.menu_items[self.categories[self.current_category]]
        for idx, (plato, precio) in enumerate(current_items):
            btn = tk.Button(self.frame_menu, text=f"{plato}\nS/ {precio:.2f}", width=18, height=3, font=("Arial", 16),
                            bg=self.button_color, fg="white",
                            command=lambda p=plato, pr=precio: self.add_to_order(p, pr))
            btn.grid(row=idx // 3, column=idx % 3, padx=20, pady=15)

    def prev_category(self):
        if self.current_category > 0:
            self.current_category -= 1
            self.update_category()
        else:
            self.current_category = len(self.categories) - 1
            self.update_category()

    def next_category(self):
        if self.current_category < len(self.categories) - 1:
            self.current_category += 1
            self.update_category()
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
        self.order_window.configure(bg="#BFD7EA")

        self.tree_order = ttk.Treeview(self.order_window, columns=("Platos", "Total"), show='headings')
        self.tree_order.heading("Platos", text="Platos")
        self.tree_order.heading("Total", text="Total")
        self.tree_order.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        self.load_current_order()

        # Botones en la ventana del pedido
        self.button_confirm = tk.Button(self.order_window, text="Confirmar Pedido", command=self.confirm_order, bg=self.button_color, fg="white", font=self.button_font)
        self.button_confirm.pack(side=tk.LEFT, padx=20, pady=20)

        self.button_add_more = tk.Button(self.order_window, text="Agregar Platos", command=self.order_window.destroy, bg=self.button_color, fg="white", font=self.button_font)
        self.button_add_more.pack(side=tk.RIGHT, padx=20, pady=20)

    def load_current_order(self):
        self.current_order = self.controller.get_current_order(self.user_id)
        for row in self.tree_order.get_children():
            self.tree_order.delete(row)
        if self.current_order:
            order_id, items, total = self.current_order
            platos = items.rstrip(", ")
            self.tree_order.insert("", tk.END, values=(platos, f"S/ {total:.2f}"))
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
