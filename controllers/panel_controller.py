import sqlite3
from data.database import create_connection

class PanelController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    # --- Gestión de mesas ---
    def get_tables_status(self):
        """Obtiene el estado de todas las mesas (libres u ocupadas)."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, state_table FROM mesa")
        return cursor.fetchall()

    def get_tables_data(self):
        """Obtener el estado de las mesas desde la base de datos."""
        try:
            cursor = self.conn.cursor()  # Usamos la conexión activa
            cursor.execute("SELECT id, state_table FROM mesa")  # Consulta
            tables = cursor.fetchall()  # Devuelve una lista de tuplas (id, estado)
            return tables

        except sqlite3.Error as e:
            print(f"Error al obtener las mesas: {e}")
            return None




    # --- Gestión de menú ---
    def get_menu_data(self):
        """Obtiene los datos del menú organizados por categorías."""
        cursor = self.conn.cursor()
        query = "SELECT category, name, price FROM menu ORDER BY category"
        cursor.execute(query)
        data = cursor.fetchall()

        menu_data = {}
        for category, name, price in data:
            if category not in menu_data:
                menu_data[category] = []
            menu_data[category].append((name, price))

        cursor.close()
        return menu_data

    # --- Gestión de pedidos ---
    def add_item_to_order(self, user_id, item_name, item_price):
        """Agrega un elemento al pedido actual de un usuario."""
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO orders (client_id, items, status, total)
            VALUES (?, ?, 'pendiente', ?)
            ON CONFLICT(client_id) DO UPDATE SET
            items = items || ', ' || ?,
            total = total + ?
            WHERE client_id = ? AND status = 'pendiente';
        """, (user_id, item_name, item_price, item_name, item_price, user_id))
        self.conn.commit()

    def get_user_order(self, user_id):
        """Obtiene el pedido actual del usuario."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, items, total
            FROM orders
            WHERE client_id = ? AND status = 'pendiente'
        """, (user_id,))
        return cursor.fetchone()

    def confirm_order(self, order_id):
        """Confirma el pedido y lo envía a caja."""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                UPDATE orders
                SET status = 'en caja'
                WHERE id = ? AND status = 'pendiente'
            """, (order_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False



    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()