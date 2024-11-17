# controllers/chef_controller.py .
from data.database import create_connection

class ChefController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_confirmed_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, users.username, orders.items, orders.total, users.role
            FROM orders
            JOIN users ON orders.user_id = users.id
            WHERE orders.status = 'confirmado'
        """)
        return cursor.fetchall()

    def confirm_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Obtener el rol del usuario que hizo el pedido
            cursor.execute("""
                SELECT users.role FROM orders
                JOIN users ON orders.user_id = users.id
                WHERE orders.id = ?
            """, (order_id,))
            result = cursor.fetchone()
            if not result:
                return False
            role = result[0]
            if role == 'cliente':
                # Cambiar estado a 'en caja'
                cursor.execute("""
                    UPDATE orders
                    SET status = 'en caja'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()
                return True
            elif role == 'panel':
                # Cambiar estado a 'finalizado' y mostrar mensaje de completado
                cursor.execute("""
                    UPDATE orders
                    SET status = 'finalizado'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()
                return 'panel_finalizado'
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()