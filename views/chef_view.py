import tkinter as tk
from tkinter import messagebox
from controllers.chef_controller import ChefController
import json

class ChefView:
    def __init__(self, root):
        self.root = root
        self.root.title("Chef Panel")
        self.root.geometry("1200x600")
        self.controller = ChefController()
        self.root.configure(bg="#DDD6CC")

        self.order_list_frame = tk.Frame(self.root, bg="#DDD6CC")
        self.order_list_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.load_orders()

    def load_orders(self):
        for widget in self.order_list_frame.winfo_children():
            widget.destroy()

        orders = self.controller.get_pending_orders()
        if not orders:
            tk.Label(self.order_list_frame, text="No hay órdenes pendientes.", font=("Arial", 24), bg="#DDD6CC", fg="#19222B").pack(pady=20)
            return

        for order in orders:
            order_id = order[0]
            mesa_number = order[1]
            order_items_json = order[2]
            total_price = order[3]

            order_items = json.loads(order_items_json)

            order_frame = tk.Frame(self.order_list_frame, bg="#DDD6CC", bd=2, relief=tk.RIDGE)
            order_frame.pack(pady=10, padx=20, fill=tk.X)

            tk.Label(order_frame, text=f"Orden #{order_id} - Mesa {mesa_number}", font=("Arial", 18), bg="#DDD6CC", fg="#19222B").pack(anchor='w', padx=10, pady=5)

            for item in order_items:
                item_text = f"{item['item']} x{item['qty']} - S/ {item['price'] * item['qty']}"
                tk.Label(order_frame, text=item_text, font=("Arial", 14), bg="#DDD6CC", fg="#19222B").pack(anchor='w', padx=20)

            tk.Label(order_frame, text=f"Total: S/ {total_price}", font=("Arial", 16, 'bold'), bg="#DDD6CC", fg="#19222B").pack(anchor='w', padx=10, pady=5)

            tk.Button(order_frame, text="Marcar como Completada", command=lambda oid=order_id: self.complete_order(oid),
                      font=("Arial", 14), bg="#19222B", fg="#BD9240").pack(anchor='e', padx=10, pady=10)

    def complete_order(self, order_id):
        self.controller.confirm_order(order_id)
        messagebox.showinfo("Orden Completada", f"La orden #{order_id} ha sido marcada como completada.")
        self.load_orders()

    def close(self):
        self.controller.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChefView(root)
    root.mainloop()
#a