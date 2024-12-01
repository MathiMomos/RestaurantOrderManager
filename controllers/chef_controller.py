# controllers/chef_controller.py .
from data.database import create_connection

class ChefController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_confirmed_orders(self):
        """
        Obtiene los pedidos con estado 'confirmado' junto con información del cliente asociado.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT 
                orders.id, 
                client.name AS client_name, 
                orders.items, 
                orders.total, 
                orders.status 
            FROM orders
            JOIN client ON orders.client_id = client.id
            WHERE orders.status = 'confirmado'
        """)
        return cursor.fetchall()

    def confirm_order(self, order_id):
        """
        Cambia el estado de un pedido según el rol del cliente:
        - Si el rol es cliente, pasa el estado a 'en caja'.
        - Si el rol es 'panel' (suponiendo que esto es representado por otro tipo de pedido), pasa el estado a 'finalizado'.
        """
        cursor = self.conn.cursor()
        try:
            # Obtener el estado actual del pedido
            cursor.execute("""
                SELECT orders.status, client.visits 
                FROM orders
                JOIN client ON orders.client_id = client.id
                WHERE orders.id = ?
            """, (order_id,))
            result = cursor.fetchone()

            if not result:
                print("Pedido no encontrado.")
                return False

            current_status, visits = result

            if current_status == 'confirmado':
                # Actualizar estado a 'en caja'
                cursor.execute("""
                    UPDATE orders
                    SET status = 'en caja'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()

                # Actualizar visitas del cliente
                cursor.execute("""
                    UPDATE client
                    SET visits = visits + 1
                    WHERE id = (SELECT client_id FROM orders WHERE id = ?)
                """, (order_id,))
                self.conn.commit()
                return True

            elif current_status == 'en caja':
                # Si ya está 'en caja', pasa a 'finalizado'
                cursor.execute("""
                    UPDATE orders
                    SET status = 'finalizado'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()
                return 'finalizado'

            else:
                print("Estado no válido para confirmar.")
                return False

        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def close_connection(self):
        """
        Cierra la conexión a la base de datos.
        """
        if self.conn:
            self.conn.close()