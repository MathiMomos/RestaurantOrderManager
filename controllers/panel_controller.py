# controllers/panel_controller.py

import sqlite3
from data.database import create_connection
from datetime import datetime

class PanelController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_or_create_panel_client(self):
        """Obtiene el client_id para 'Panel', creándolo si no existe."""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM client WHERE name = 'Panel'")
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            # Crear el cliente 'Panel'
            cursor.execute("INSERT INTO client (name, documents, visits) VALUES (?, ?, ?)", ("Panel", "N/A", 0))
            self.conn.commit()
            return cursor.lastrowid

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

    def add_item_to_order(self, user_id, item_name, item_price, item_amount=1):
        """Agrega un elemento al pedido actual del panel."""
        cursor = self.conn.cursor()
        try:
            mesa_id = 0  # Indica que es desde el panel
            client_id = self.get_or_create_panel_client()

            # Verificar si ya existe un pedido pendiente para este cliente (panel)
            cursor.execute("""
                SELECT id, items, item_prices, item_amounts, total FROM orders
                WHERE client_id = ? AND status = 'pendiente' AND mesa_id = 0
            """, (client_id,))
            order = cursor.fetchone()

            if order:
                order_id, items, prices, amounts, total = order

                # Verificar si el plato ya está en el pedido
                item_list = items.strip(',').split(', ')
                price_list = prices.strip(',').split(', ')
                amount_list = amounts.strip(',').split(', ')

                if item_name in item_list:
                    index = item_list.index(item_name)
                    current_amount = int(amount_list[index])
                    new_amount = current_amount + item_amount
                    amount_list[index] = str(new_amount)

                    # Calcular el nuevo total
                    new_total = total + (item_price * item_amount)

                    # Reconstruir las cadenas sin comas al final
                    new_items = ', '.join(item_list)
                    new_prices = ', '.join(price_list)
                    new_amounts = ', '.join(amount_list)

                    cursor.execute("""
                        UPDATE orders
                        SET items = ?, item_prices = ?, item_amounts = ?, total = ?
                        WHERE id = ?
                    """, (new_items, new_prices, new_amounts, new_total, order_id))
                else:
                    # Agregar un nuevo plato al pedido
                    new_items = items + f"{item_name}, "
                    new_prices = prices + f"{item_price}, "
                    new_amounts = amounts + f"{item_amount}, "
                    new_total = total + (item_price * item_amount)

                    cursor.execute("""
                        UPDATE orders
                        SET items = ?, item_prices = ?, item_amounts = ?, total = ?
                        WHERE id = ?
                    """, (new_items, new_prices, new_amounts, new_total, order_id))
            else:
                # Crear un nuevo pedido
                new_items = f"{item_name}, "
                new_prices = f"{item_price}, "
                new_amounts = f"{item_amount}, "
                new_total = item_price * item_amount

                cursor.execute("""
                    INSERT INTO orders (mesa_id, client_id, items, item_prices, item_amounts, status, total)
                    VALUES (?, ?, ?, ?, ?, 'pendiente', ?)
                """, (mesa_id, client_id, new_items, new_prices, new_amounts, new_total))

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al agregar el ítem al pedido desde el panel: {e}")
            self.conn.rollback()
            return False

    def get_current_order(self, user_id):
        """Obtiene el pedido actual del panel."""
        cursor = self.conn.cursor()
        client_id = self.get_or_create_panel_client()
        cursor.execute("""
            SELECT id, items, item_prices, item_amounts, total FROM orders
            WHERE client_id = ? AND status = 'pendiente' AND mesa_id = 0
        """, (client_id,))
        return cursor.fetchone()

    def remove_item_from_order(self, user_id, client_id, item_name):
        """Elimina un ítem del pedido del panel."""
        cursor = self.conn.cursor()
        try:
            # Obtener el pedido
            cursor.execute("""
                SELECT id, items, item_prices, item_amounts, total FROM orders
                WHERE client_id = ? AND status = 'pendiente' AND mesa_id = 0
            """, (client_id,))
            order = cursor.fetchone()

            if not order:
                print("No hay pedido pendiente para eliminar.")
                return False

            order_id, items, prices, amounts, total = order

            # Separar los elementos
            item_list = items.strip(',').split(', ')
            price_list = prices.strip(',').split(', ')
            amount_list = amounts.strip(',').split(', ')

            if item_name in item_list:
                index = item_list.index(item_name)
                current_amount = int(amount_list[index])
                if current_amount > 1:
                    amount_list[index] = str(current_amount - 1)
                else:
                    # Eliminar el plato del pedido
                    del item_list[index]
                    del price_list[index]
                    del amount_list[index]

                # Calcular el nuevo total
                new_total = total - float(price_list[index])

                # Reconstruir las cadenas
                if item_list:
                    new_items = ', '.join(item_list) + ', '
                    new_prices = ', '.join(price_list) + ', '
                    new_amounts = ', '.join(amount_list) + ', '
                else:
                    new_items = ''
                    new_prices = ''
                    new_amounts = ''

                cursor.execute("""
                    UPDATE orders
                    SET items = ?, item_prices = ?, item_amounts = ?, total = ?
                    WHERE id = ?
                """, (new_items, new_prices, new_amounts, new_total, order_id))
                self.conn.commit()
                return True
            else:
                print("El plato no está en el pedido.")
                return False
        except Exception as e:
            print(f"Error al eliminar el ítem del pedido desde el panel: {e}")
            self.conn.rollback()
            return False

    def confirm_order(self, order_id):
        """Confirma el pedido del panel y lo envía a caja."""
        cursor = self.conn.cursor()
        try:
            # Actualizar el estado del pedido a 'en caja'
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute("""
                UPDATE orders
                SET status = 'en caja', time_out = ?
                WHERE id = ? AND mesa_id = 0
            """, (current_time, order_id))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido del panel: {e}")
            self.conn.rollback()
            return False

    def close_connection(self):
        """Cierra la conexión a la base de datos."""
        if self.conn:
            self.conn.close()
