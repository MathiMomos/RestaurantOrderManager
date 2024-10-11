# data/database.py

import sqlite3
from sqlite3 import Error
import os
import hashlib

def create_connection(db_file):
    """Crea una conexión a la base de datos SQLite especificada por db_file."""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Conexión establecida a la base de datos {db_file}.")
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    return conn

def hash_password(password):
    """Hash de una contraseña usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def initialize_database():
    """Inicializa la base de datos con las tablas necesarias y crea el admin por defecto."""
    if not os.path.exists('data'):
        os.makedirs('data')
    conn = create_connection('data/restaurant.db')
    if conn is not None:
        with open('data/schema.sql', 'r') as f:
            sql_script = f.read()
        try:
            cursor = conn.cursor()
            cursor.executescript(sql_script)
            # Insertar usuario admin si no existe
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                hashed_password = hash_password("admin")
                cursor.execute(
                    "INSERT INTO users (username, password, role) VALUES (?, ?, ?)",
                    ("admin", hashed_password, "admin")
                )
                print("Cuenta de administrador creada por defecto.")
            # Insertar platos básicos si la tabla está vacía
            cursor.execute("SELECT COUNT(*) FROM menu")
            if cursor.fetchone()[0] == 0:
                menu_items = [
                    ("Hamburguesa", 5.99),
                    ("Pizza", 8.99),
                    ("Ensalada", 4.99),
                    ("Pasta", 7.49),
                    ("Tacos", 6.50)
                ]
                cursor.executemany("INSERT INTO menu (name, price) VALUES (?, ?)", menu_items)
                print("Platos básicos agregados al menú.")
            conn.commit()
            print("Base de datos inicializada correctamente.")
        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()
    else:
        print("No se pudo crear la conexión a la base de datos.")
