from data.database import Database

class CajaController:
    def __init__(self):
        self.db = Database()

    def get_orders(self):
        self.db.cursor.execute("SELECT * FROM orders WHERE status = 'pending'")
        return self.db.cursor.fetchall()

    def delete_order(self, order_id):
        self.db.delete_order(order_id)

    def close(self):
        self.db.close()
