# controllers/cliente_controller.py .
import sqlite3

from data.database import create_connection
from datetime import datetime



class ClienteController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_client_by_document(self, document):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, name, documents FROM client
            WHERE documents = ?
        """, (document,))
        return cursor.fetchone()  # Retorna una fila (o None si no existe)

    def add_new_client(self, name, document):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO client (name, documents, visits)
            VALUES (?, ?, 0)
        """, (name, document))
        self.conn.commit()
        return cursor.lastrowid  # Retornar el ID del cliente recién creado


    def apply_discount_and_update_visits(self, client_id):
        """
        Incrementa las visitas del cliente y aplica descuentos basados en el número de visitas.
        """
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT visits FROM client WHERE id = ?
        """, (client_id,))
        visits = cursor.fetchone()[0]

        # Incrementar visitas
        new_visits = visits + 1
        cursor.execute("""
            UPDATE client
            SET visits = ?
            WHERE id = ?
        """, (new_visits, client_id))

        # Calcular descuento
        discount = 0
        if new_visits >= 5:
            discount = 0.10  # 10% de descuento
        elif new_visits >= 10:
            discount = 0.20  # 20% de descuento

        self.conn.commit()
        return discount

    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT category, name, price FROM menu")
        return cursor.fetchall()

    def get_current_order(self, user_id , client_id):
        """Obtiene el pedido actual del usuario si está en estado 'pendiente'."""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT id, items, item_prices, item_amounts, total FROM orders
            WHERE client_id = ? AND status = 'pendiente'
        """, (client_id,))
        return cursor.fetchone()

    def add_item_to_order(self, user_id, client_id, item_name, item_price, item_amount):
        """Agrega un plato al pedido del usuario o actualiza la cantidad si ya está en el pedido."""
        cursor = self.conn.cursor()
        order = self.get_current_order(user_id,client_id)

        if order:
            order_id, items, prices, amounts, total = order

            # Verificar si el plato ya está en el pedido
            item_list = items.split(', ')
            price_list = prices.split(', ')
            amount_list = amounts.split(', ')

            if item_name in item_list:
                # Si el plato ya está, actualizamos la cantidad
                index = item_list.index(item_name)
                current_amount = int(amount_list[index])  # Obtener la cantidad actual
                new_amount = current_amount + item_amount  # Incrementar la cantidad
                amount_list[index] = str(new_amount)  # Actualizar la cantidad en la lista

                # Calcular el nuevo total
                new_total = 0
                for i in range(len(price_list)):
                    try:
                        # Asegurarse de que no haya valores vacíos o inválidos
                        price = float(price_list[i].strip()) if price_list[i].strip() else 0
                        amount = int(amount_list[i].strip()) if amount_list[i].strip() else 0
                        new_total += price * amount
                    except ValueError:
                        # Si hay algún valor inválido, lo ignoramos
                        pass

                # Reconstruir las cadenas con los nuevos valores (sin coma extra al final)
                new_items = ', '.join(item_list)
                new_prices = ', '.join(price_list)
                new_amounts = ', '.join(amount_list)

                cursor.execute("""
                    UPDATE orders
                    SET items = ?, item_prices = ?, item_amounts = ?, total = ?
                    WHERE id = ?
                """, (new_items, new_prices, new_amounts, new_total, order_id))
            else:
                # Si el plato no está en el pedido, agregamos uno nuevo (con la coma al final)
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
            # Si no existe un pedido, creamos uno nuevo (con la coma al final)
            new_items = f"{item_name}, "
            new_prices = f"{item_price}, "
            new_amounts = f"{item_amount}, "
            new_total = item_price * item_amount
            cursor.execute("""
                INSERT INTO orders (mesa_id ,client_id, items, item_prices, item_amounts, status , total)
                VALUES (? , ?, ?, ?, ?, 'pendiente', ?)
            """, (0, client_id, new_items, new_prices, new_amounts, new_total))

        self.conn.commit()

    def remove_item_from_order(self, user_id,client_id, item_name):
        """Elimina un plato del pedido si su cantidad llega a 0, o decrementa su cantidad en 1."""
        cursor = self.conn.cursor()
        order = self.get_current_order(user_id , client_id)

        if order:
            order_id, items, prices, amounts, total = order

            # Convertir las cadenas de items, precios y cantidades a listas
            item_list = items.split(', ')
            price_list = prices.split(', ')
            amount_list = amounts.split(', ')

            if item_name in item_list:
                # Obtener el índice del plato en la lista
                index = item_list.index(item_name)
                current_amount = int(amount_list[index])  # Obtener la cantidad actual

                if current_amount > 1:
                    # Si la cantidad es mayor que 1, decrementamos en 1
                    new_amount = current_amount - 1
                    amount_list[index] = str(new_amount)
                else:
                    # Si la cantidad es 1, eliminamos el plato de las listas
                    item_list.pop(index)
                    price_list.pop(index)
                    amount_list.pop(index)

                # Recalcular el total
                new_total = 0
                for i in range(len(price_list)):
                    try:
                        # Asegurarse de que no haya valores vacíos o inválidos
                        price = float(price_list[i].strip()) if price_list[i].strip() else 0
                        amount = int(amount_list[i].strip()) if amount_list[i].strip() else 0
                        new_total += price * amount
                    except ValueError:
                        pass

                # Reconstruir las cadenas sin la coma extra al final
                new_items = ', '.join(item_list)
                new_prices = ', '.join(price_list)
                new_amounts = ', '.join(amount_list)

                # Actualizar el pedido en la base de datos
                cursor.execute("""
                    UPDATE orders
                    SET items = ?, item_prices = ?, item_amounts = ?, total = ?
                    WHERE id = ?
                """, (new_items, new_prices, new_amounts, new_total, order_id))
            else:
                print("El plato no está en la orden.")
        else:
            print("No hay orden existente.")

        self.conn.commit()

    def confirm_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Obtener la fecha y hora actual en formato ISO
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            # Actualizar el estado del pedido y guardar la fecha y hora de ingreso
            cursor.execute("""
                UPDATE orders
                SET status = 'confirmado', time_in = ?
                WHERE id = ?
            """, (current_time, order_id))

            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    def close_connection(self):
        if self.conn:
            self.conn.close()