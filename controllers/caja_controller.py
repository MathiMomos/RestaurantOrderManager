from data.database import create_connection
from datetime import datetime


class CajaController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_en_caja_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, client.name, orders.items, orders.total, 'cliente' AS role
            FROM orders
            JOIN client ON orders.client_id = client.id
            WHERE orders.status = 'en caja'
        """)
        return cursor.fetchall()

    def generate_bill(self, order_id, method_pay):
        cursor = self.conn.cursor()
        try:
            # Obtener la fecha y hora actual en formato ISO
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Insertar en la tabla caja el método de pago
            cursor.execute("""
                INSERT INTO caja (orders_id, method_pay)
                VALUES (?, ?)
            """, (order_id, method_pay))

            # Actualizar el estado de la orden a 'finalizado' y guardar la hora de salida
            cursor.execute("""
                UPDATE orders
                SET status = 'finalizado', time_out = ?
                WHERE id = ?
            """, (current_time, order_id))

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
                WHERE id = ? AND client_id IN (
                    SELECT id FROM client WHERE id = orders.client_id
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
