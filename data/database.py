import sqlite3

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('data/restaurant.db')
        self.cursor = self.conn.cursor()
        self.create_tables()
        self.create_default_admin()

    def create_tables(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                setting_key TEXT UNIQUE NOT NULL,
                setting_value TEXT NOT NULL
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa_number INTEGER NOT NULL,
                order_items TEXT NOT NULL,
                total_price REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending'
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS mesas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mesa_number INTEGER UNIQUE NOT NULL,
                status TEXT NOT NULL DEFAULT 'free'
            )
        ''')
        self.conn.commit()

    def create_default_admin(self):
        self.cursor.execute("SELECT * FROM users WHERE username = 'admin'")
        if not self.cursor.fetchone():
            self.cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                ('admin', 'admin', 'admin')
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
            return False

    def get_user(self, username, password):
        try:
            self.cursor.execute(
                "SELECT * FROM users WHERE username = ? AND password = ?",
                (username, password)
            )
            return self.cursor.fetchone()
        except Exception as e:
            return None

    def get_user_count(self, role):
        try:
            self.cursor.execute("SELECT COUNT(*) FROM users WHERE role = ?", (role,))
            return self.cursor.fetchone()[0]
        except Exception as e:
            return 0

    def get_mesas_status(self):
        try:
            self.cursor.execute("SELECT mesa_number, status FROM mesas")
            return self.cursor.fetchall()
        except Exception as e:
            return []

    def update_mesa_status(self, mesa_number, new_status):
        try:
            self.cursor.execute(
                "UPDATE mesas SET status = ? WHERE mesa_number = ?",
                (new_status, mesa_number)
            )
            self.conn.commit()
        except Exception as e:
            pass

    def create_order(self, mesa_number, order_items, total_price):
        try:
            self.cursor.execute(
                "INSERT INTO orders (mesa_number, order_items, total_price, status) VALUES (?, ?, ?, ?)",
                (mesa_number, order_items, total_price, 'pending')
            )
            self.conn.commit()
        except Exception as e:
            pass

    def get_orders_by_mesa(self, mesa_number):
        self.cursor.execute("SELECT * FROM orders WHERE mesa_number = ? AND status = 'pending'", (mesa_number,))
        return self.cursor.fetchall()

    def get_all_orders(self):
        self.cursor.execute("SELECT * FROM orders WHERE status = 'pending'")
        return self.cursor.fetchall()

    def confirm_order(self, order_id):
        self.cursor.execute("UPDATE orders SET status = 'completed' WHERE id = ?", (order_id,))
        self.conn.commit()

    def delete_order(self, order_id):
        self.cursor.execute("DELETE FROM orders WHERE id = ?", (order_id,))
        self.conn.commit()

    def get_order_details(self, order_id):
        self.cursor.execute("SELECT order_items FROM orders WHERE id = ?", (order_id,))
        return self.cursor.fetchone()

    def close(self):
        self.conn.close()
