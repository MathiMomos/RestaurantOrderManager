from data.database import Database

class ChefController:
    def __init__(self):
        self.db = Database()

    def get_orders(self):
        # Obtener todos los pedidos con estado 'sent' (enviados al chef) o 'pending' (recibidos pero no confirmados)
        self.db.cursor.execute("SELECT * FROM orders WHERE status IN ('pending', 'sent')")
        return self.db.cursor.fetchall()

    def confirm_order(self, order_id):
        # Actualizar el estado del pedido a 'completed' cuando el chef lo confirma
        self.db.cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
        self.db.conn.commit()

    def close(self):
        # Cerrar conexión a la base de datos
        self.db.close()
