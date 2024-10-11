# controllers/panel_controller.py

from data.database import create_connection

class PanelController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu")
        return cursor.fetchall()

    def get_user_order(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, items, total FROM orders WHERE user_id = ? AND status = 'en caja'", (user_id,))
        return cursor.fetchone()

    def add_item_to_order(self, user_id, item_name, item_price):
        cursor = self.conn.cursor()
        order = self.get_user_order(user_id)
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
                INSERT INTO orders (user_id, items, status, total)
                VALUES (?, ?, 'en caja', ?)
            """, (user_id, new_items, new_total))
        self.conn.commit()

    def confirm_order(self, user_id):
        order = self.get_user_order(user_id)
        return order is not None

    def close_connection(self):
        if self.conn:
            self.conn.close()
