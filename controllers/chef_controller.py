# controllers/chef_controller.py .
from data.database import create_connection

class ChefController:
    def __init__(self):
        self.conn = create_connection('data/restaurant.db')

    def get_confirmed_orders(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT orders.id, users.username, orders.items, orders.total, users.role
            FROM orders
            JOIN users ON orders.users_id = users.id
            WHERE orders.status = 'confirmado'
        """)
        return cursor.fetchall()

    def confirm_order(self, order_id):
        cursor = self.conn.cursor()
        try:
            # Obtener el rol del usuario que hizo el pedido
            cursor.execute("""
                SELECT users.role FROM orders
                JOIN users ON orders.users_id = users.id
                WHERE orders.id = ?
            """, (order_id,))
            result = cursor.fetchone()
            if not result:
                return False
            role = result[0]
            if role == 'cliente':
                # Cambiar estado a 'en caja'
                cursor.execute("""
                    UPDATE orders
                    SET status = 'en caja'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()
                return True
            elif role == 'panel':
                # Cambiar estado a 'finalizado' y mostrar mensaje de completado
                cursor.execute("""
                    UPDATE orders
                    SET status = 'finalizado'
                    WHERE id = ?
                """, (order_id,))
                self.conn.commit()
                return 'panel_finalizado'
        except Exception as e:
            print(f"Error al confirmar el pedido: {e}")
            return False

    #añadir platos al menu
    def anadir_plato(self , category, name, price ):
        cursor = self.conn.cursor()
        try:
            cursor.execute(""" INSERT INTO menu (category, name, price) VALUES (?, ?, ?)""", (category, name, price))
            self.conn.commit()
            print("Plato añadido con éxito.")
            return True
        except Exception as e:
            print(f"Error al leer el pedido: {e}")
            return False

    def eliminar_plato(self, id_plato):
        cursor = self.conn.cursor()
        try:
            # Eliminar el plato con el ID dado
            cursor.execute("DELETE FROM menu WHERE id = ?", (id_plato,))
            self.conn.commit()
            print(f"Plato con ID {id_plato} eliminado exitosamente.")

            # Opcional: Renumerar los ID de los platos
            self.renumerar_menu()
            return True

        except Exception as e:
            print(f"Error al eliminar el plato: {e}")
            return False

    def renumerar_menu(self):
        cursor = self.conn.cursor()
        try:
            # Crear una tabla temporal para renumerar los ID
            cursor.execute("CREATE TEMPORARY TABLE menu_temp AS SELECT * FROM menu")

            # Eliminar la tabla original
            cursor.execute("DELETE FROM menu")

            # Reiniciar los IDs manualmente
            cursor.execute("""
            INSERT INTO menu (category, name, price)
            SELECT category, name, price FROM menu_temp
            """)

            # Eliminar la tabla temporal
            cursor.execute("DROP TABLE menu_temp")

            self.conn.commit()
            print("ID de los platos renumerados correctamente.")

        except Exception as e:
            print(f"Error al renumerar los ID: {e}")

    def get_menu_items(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, category, name, price FROM menu")
        return cursor.fetchall()

    def close_connection(self):
        if self.conn:
            self.conn.close()
