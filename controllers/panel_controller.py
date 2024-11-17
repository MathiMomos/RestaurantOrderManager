# controllers/panel_controller.py .

from data.database import create_connection

class PanelController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_menu_items(self):
        """Obtiene los elementos del menú para el panel."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, name, price FROM menu")
        return cursor.fetchall()

    def get_user_order(self, user_id):
        """Obtiene el pedido actual del usuario si está en estado 'pendiente'."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, items, total FROM orders
            WHERE user_id = ? AND status = 'pendiente'
        """, (user_id,))
        return cursor.fetchone()

    def add_item_to_order(self, user_id, item_name, item_price):
        """Agrega un plato al pedido del usuario."""
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
            # Crear un nuevo pedido con estado 'pendiente'
            new_items = f"{item_name}, "
            new_total = item_price
            cursor.execute("""
                INSERT INTO orders (user_id, items, status, total)
                VALUES (?, ?, 'pendiente', ?)
            """, (user_id, new_items, new_total))
        self.conn.commit()

    def confirm_order(self, order_id):
        """Confirma el pedido cambiando su estado a 'en caja'."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE orders
                SET status = 'en caja'
                WHERE id = ? AND status = 'pendiente'
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()