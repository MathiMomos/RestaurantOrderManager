# controllers/cliente_controller.py .
from data.database import create_connection

class ClienteController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category , name, price FROM menu")
        return cursor.fetchall()

    def get_current_order(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, items, total FROM orders
            WHERE user_id = ? AND status = 'pendiente'
        """, (user_id,))
        return cursor.fetchone()

    def add_item_to_order(self, user_id, item_name, item_price):
        cursor = self.conn.cursor()
        order = self.get_current_order(user_id)
        if order:
            order_id, items, total = order
            new_items = items + f"{item_name}, "
            new_total = total + item_price
            cursor.execute("""
                UPDATE orders
                SET items = ?, total = ?
                WHERE id = ?
            """, (new_items, new_total, order_id))
        else:
            new_items = f"{item_name}, "
            new_total = item_price
            cursor.execute("""
                INSERT INTO orders (user_id, items, status, total)
                VALUES (?, ?, 'pendiente', ?)
            """, (user_id, new_items, new_total))
        self.conn.commit()

    def confirm_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE orders
                SET status = 'confirmado'
                WHERE id = ?
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def get_menu_items1(self):
        cursor = self.conn.cursor()
        query = "SELECT category, name, price FROM menu ORDER BY category"
        cursor.execute(query)
        data = cursor.fetchall()

        menu_items = {}
        for category, name, price in data:
            if category not in menu_items:
                menu_items[category] = []
            menu_items[category].append((name, price))

        cursor.close()
        return menu_items

    def find_client(self, name, document):
        """Verifies if the client exists in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM client WHERE name = ? AND documents = ?", (name, document))
        client = cursor.fetchone()
        cursor.close()
        return client

    def create_client(self, name, document):  # FALTA QUE INGRESE POR PARAMETROS LA ID DE MESA
        """Creates a new client entry in the database."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO client (mesa_id, name, documents, phone, visits, time_in, time_out) VALUES (1, ?, ?, '', 0, '', '')",  # Use a default mesa_id, e.g., 1
            (name, document))
        self.conn.commit()
        cursor.close()

    def close_connection(self):
        if self.conn:
            self.conn.close()