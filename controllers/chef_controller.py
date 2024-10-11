from data.database import Database
#a
class ChefController:
    def __init__(self):
        self.db = Database()

    def get_pending_orders(self):
        orders = self.db.get_all_pending_orders()
        return orders

    def confirm_order(self, order_id):
        self.db.confirm_order(order_id)

    def receive_order(self, mesa_number, items, total_price):
        """Recibir un pedido desde el ClienteController y almacenarlo en la base de datos."""
        items_json = json.dumps(items)
        self.db.create_order(mesa_number, items_json, total_price)  # Método para guardar en la base de datos

    def close(self):
        self.db.close()
