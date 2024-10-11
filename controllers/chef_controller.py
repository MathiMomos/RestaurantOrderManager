from data.database import Database

class ChefController:
    def __init__(self):
        self.db = Database()

    def get_orders(self):
        self.db.cursor.execute("SELECT * FROM orders WHERE status IN ('pending', 'sent')")
        return self.db.cursor.fetchall()

    def confirm_order(self, order_id):
        self.db.cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
        self.db.conn.commit()

    def close(self):
        self.db.close()
