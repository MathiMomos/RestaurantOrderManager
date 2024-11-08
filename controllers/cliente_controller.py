# controllers/cliente_controller.py .
from data.database import create_connection

class ClienteController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    #BUSCAR EL CLIENTE EN LA BASE DE DATOS ( FALTA QUE BUSQUE EN LOS DIFERENTES TIPOS DE MESAS)
    def find_client(self, name, document):
        """Verifies if the client exists in the database."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM client WHERE name = ? AND documents = ?", (name, document))
        client = cursor.fetchone()
        cursor.close()
        return client

    def create_client(self, name, document):
        """Creates a new client entry in the database and returns the client id."""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO client (name, documents, visits) VALUES (?, ?, 0)", (name, document)
        )
        self.conn.commit()
        client_id = cursor.lastrowid  # Captura el id del cliente recién insertado
        cursor.close()
        return client_id


    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category , name, price FROM menu")
        return cursor.fetchall()

    #SACAR LOS DATOS DE MENU DE LA BD EN BASE A LA CATEGORIA
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

    def get_current_order(self, mesa_id, client_id):
        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT id, items, total FROM orders
            WHERE client_id = ? AND mesa_id = ? AND status = 'pendiente'
        """, (client_id, mesa_id ))

        order = cursor.fetchone()
        cursor.close()
        return order

    def return_id_mesa(self, user_id):
        """Obtiene el id de la mesa según el patrón del nombre de usuario."""
        cursor = self.conn.cursor()
        # Obtener el nombre de usuario en base al user_id
        cursor.execute("SELECT username FROM users WHERE id = ?", (user_id,))
        result = cursor.fetchone()

        if result:
            username = result[0]
            # Extraer el número de mesa del username, asumiendo el formato "mesaX"
            if username.startswith("mesa"):
                try:
                    mesa_num = int(username[4:]) + 1  # Sumar 1 al número extraído
                    # Verificar que el número de mesa esté dentro del rango de mesas (1 a 15)
                    if 1 <= mesa_num <= 15:
                        cursor.execute("SELECT id FROM mesa WHERE id = ?", (mesa_num,))
                        mesa = cursor.fetchone()
                        if mesa:
                            return mesa[0]
                except ValueError:
                    print("El nombre de usuario no tiene el formato esperado 'mesaX'.")
                    return None
        return None

    def add_item_to_order(self, user_id, client_id, item_name, item_price):
        if client_id is None:
            raise ValueError("El `client_id` no se ha establecido.")

        cursor = self.conn.cursor()
        mesa_id = self.return_id_mesa(user_id)
        order = self.get_current_order(mesa_id, client_id)

        if order:
            # Actualizar pedido existente
            order_id, items, total = order
            new_items = items + f"{item_name}, "
            new_total = total + item_price
            cursor.execute("""
                UPDATE orders
                SET items = ?, total = ?
                WHERE id = ?
            """, (new_items, new_total, order_id))
        else:
            # Crear un nuevo pedido
            new_items = f"{item_name}, "
            new_total = item_price
            cursor.execute("""
                INSERT INTO orders (mesa_id, client_id, items, status, total)
                VALUES (?, ?, ?, 'pendiente', ?)
            """, (mesa_id, client_id, new_items, new_total))

        self.conn.commit()
        cursor.close()

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

    def close_connection(self):
        if self.conn:
            self.conn.close()