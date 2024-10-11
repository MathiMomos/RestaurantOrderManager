import tkinter as tk
from tkinter import messagebox
from controllers.chef_controller import ChefController

class ChefView:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef Panel")
        self.root.geometry("1200x600")
        self.controller = ChefController()

        self.order_buttons_frame = tk.Frame(root)
        self.order_buttons_frame.pack(pady=20)

        self.order_listbox = tk.Listbox(root, width=100, height=10)
        self.order_listbox.pack(pady=10)

        self.confirm_button = tk.Button(root, text="Confirmar Pedido", command=self.confirm_order)
        self.confirm_button.pack(side=tk.LEFT, padx=20)

        self.back_button = tk.Button(root, text="Volver", command=self.close)
        self.back_button.pack(side=tk.RIGHT, padx=20)

        self.load_orders()

    def load_orders(self):
        for widget in self.order_buttons_frame.winfo_children():
            widget.destroy()

        orders = self.controller.get_orders()
        for order in orders:
            mesa_number = order[1]
            order_id = order[0]
            button = tk.Button(self.order_buttons_frame, text=f"Mesa {mesa_number} - Pedido {order_id}",
                               command=lambda o=order: self.show_order_details(o))
            button.pack(pady=5)

    def show_order_details(self, order):
        order_id = order[0]
        order_items = order[2]
        self.order_listbox.delete(0, tk.END)
        self.order_listbox.insert(tk.END, f"ID: {order_id}, Items: {order_items}")

    def confirm_order(self):
        selected = self.order_listbox.curselection()
        if selected:
            order_id = self.controller.get_orders()[selected[0]][0]
            self.controller.confirm_order(order_id)
            messagebox.showinfo("Éxito", "Pedido confirmado.")
            self.load_orders()
        else:
            messagebox.showerror("Error", "Selecciona un pedido.")

    def close(self):
        self.controller.close()
        self.root.destroy()
