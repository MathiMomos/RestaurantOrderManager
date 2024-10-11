from data.database import Database

class ClienteController:
    def __init__(self):
        self.db = Database()

    def start_visit(self, mesa_number):
        self.db.cursor.execute("UPDATE mesas SET status = 'occupied' WHERE mesa_number = ?", (mesa_number,))
        self.db.conn.commit()

    def add_to_order(self, mesa_number, items, total_price):
        self.db.create_order(mesa_number, items, total_price)

    def confirm_order(self, mesa_number):
        self.db.cursor.execute("UPDATE orders SET status = 'pending' WHERE mesa_number = ? AND status = 'draft'", (mesa_number,))
        self.db.conn.commit()

    def get_order(self, mesa_number):
        self.db.cursor.execute("SELECT * FROM orders WHERE mesa_number = ? AND status = 'pending'", (mesa_number,))
        return self.db.fetchall()

    def clear_order(self, mesa_number):
        self.db.cursor.execute("DELETE FROM orders WHERE mesa_number = ? AND status = 'pending'", (mesa_number,))
        self.db.conn.commit()

    def finish_visit(self, mesa_number):
        self.db.cursor.execute("UPDATE mesas SET status = 'free' WHERE mesa_number = ?", (mesa_number,))
        self.db.conn.commit()

    def close(self):
        self.db.close()
