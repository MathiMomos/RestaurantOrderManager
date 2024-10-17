# controllers/cliente_controller.py .
from data.database import create_connection

class ClienteController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category , name, price FROM menu")
        return cursor.fetchall()

    def get_current_order(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, items, total FROM orders
            WHERE users_id = ? AND status = 'pendiente'
        """, (user_id,))
        return cursor.fetchone()

    def add_item_to_order(self, user_id, item_name, item_price):
        cursor = self.conn.cursor()
        order = self.get_current_order(user_id)
        if order:
            order_id, items, total = order
            new_items = items + f"{item_name}, "
            new_total = total + item_price
            cursor.execute("""
                UPDATE orders
                SET items = ?, total = ?
                WHERE id = ?
            """, (new_items, new_total, order_id))
        else:
            new_items = f"{item_name}, "
            new_total = item_price
            cursor.execute("""
                INSERT INTO orders (users_id, items, status, total)
                VALUES (?, ?, 'pendiente', ?)
            """, (user_id, new_items, new_total))
        self.conn.commit()

    def confirm_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE orders
                SET status = 'confirmado'
                WHERE id = ?
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()