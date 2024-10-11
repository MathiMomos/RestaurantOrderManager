import sqlite3
import json

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/restaurant.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_default_admin()
        self.create_default_mesas()

    def create_tables(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT NOT NULL
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_number INTEGER NOT NULL,
            order_items TEXT NOT NULL,
            total_price REAL NOT NULL,
            status TEXT NOT NULL DEFAULT 'pending'
        )''')
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_number INTEGER UNIQUE NOT NULL,
            status TEXT NOT NULL DEFAULT 'free'
        )''')
        self.conn.commit()

    def create_default_admin(self):
        self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', 'admin', 'admin')
            )
            self.conn.commit()

    def create_default_mesas(self):
        # Crea mesas por defecto si no existen
        self.cursor.execute("SELECT COUNT(*) FROM mesas")
        count = self.cursor.fetchone()[0]
        if count == 0:
            for mesa_number in range(1, 11):  # Suponiendo 10 mesas
                self.cursor.execute(
                    "INSERT INTO mesas (mesa_number, status) VALUES (?, ?)",
                    (mesa_number, 'free')
                )
            self.conn.commit()

    def create_user(self, username, password, role):
        try:
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                (username, password, role)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
        except Exception as e:
            print(f"Error al crear usuario: {e}")  # Imprimir error para depuración
            return False

    def get_user(self, username, password):
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener usuario: {e}")  # Imprimir error para depuración
            return None

    def get_user_count(self, role):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = ?", (role,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            print(f"Error al contar usuarios: {e}")  # Imprimir error para depuración
            return 0

    def get_mesas_status(self):
        try:
            self.cursor.execute("SELECT mesa_number, status FROM mesas")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener estado de mesas: {e}")  # Imprimir error para depuración
            return []

    def update_mesa_status(self, mesa_number, new_status):
        try:
            self.cursor.execute(
                "UPDATE mesas SET status = ? WHERE mesa_number = ?",
                (new_status, mesa_number)
            )
            self.conn.commit()
        except Exception as e:
            print(f"Error al actualizar estado de mesa: {e}")  # Imprimir error para depuración

    def create_order(self, mesa_number, order_items, total_price):
        try:
            self.cursor.execute(
                "INSERT INTO orders (mesa_number, order_items, total_price, status) VALUES (?, ?, ?, ?)",
                (mesa_number, order_items, total_price, 'pending')
            )
            self.conn.commit()
            print(f"Orden creada para la mesa {mesa_number}: {order_items}, Total: {total_price}")
        except Exception as e:
            print(f"Error al crear la orden: {e}")  # Para depuración

    def get_orders_by_mesa(self, mesa_number):
        try:
            self.cursor.execute("SELECT * FROM orders WHERE mesa_number = ? AND status = 'pending'", (mesa_number,))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener órdenes por mesa: {e}")  # Imprimir error para depuración
            return []

    def get_all_pending_orders(self):
        try:
            self.cursor.execute("SELECT * FROM orders WHERE status = 'pending'")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener todas las órdenes pendientes: {e}")  # Imprimir error para depuración
            return []

    def confirm_order(self, order_id):
        try:
            self.cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error al confirmar la orden: {e}")  # Imprimir error para depuración

    def delete_order(self, order_id):
        try:
            self.cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error al eliminar la orden: {e}")  # Imprimir error para depuración

    def get_order_details(self, order_id):
        try:
            self.cursor.execute("SELECT order_items FROM orders WHERE id = ?", (order_id,))
            return self.cursor.fetchone()
        except Exception as e:
            print(f"Error al obtener detalles de la orden: {e}")  # Imprimir error para depuración
            return None

    def close(self):
        self.conn.close()
