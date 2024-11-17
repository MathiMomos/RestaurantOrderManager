# controllers/caja_controller.py .
from data.database import create_connection

class CajaController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_en_caja_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, users.username, orders.items, orders.total, users.role
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE orders.status = 'en caja'
        """)
        return cursor.fetchall()

    def generate_bill(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Solo actualizar si la cuenta es 'cliente'
            cursor.execute("""
                UPDATE orders
                SET status = 'finalizado'
                WHERE id = ? AND user_id IN (
                    SELECT id FROM users WHERE role = 'cliente'
                )
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al generar la boleta: {e}")
            return False

    def process_panel_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Solo actualizar si la cuenta es 'panel'
            cursor.execute("""
                UPDATE orders
                SET status = 'confirmado'
                WHERE id = ? AND user_id IN (
                    SELECT id FROM users WHERE role = 'panel'
                )
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al procesar el pedido de panel: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()