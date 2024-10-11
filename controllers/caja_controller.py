# controllers/caja_controller.py
from data.database import create_connection

class CajaController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_en_caja_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, users.username, orders.items, orders.total
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE orders.status = 'en caja'
        """)
        return cursor.fetchall()

    def generate_bill(self, order_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE orders
                SET status = 'finalizado'
                WHERE id = ?
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al generar la boleta: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()
