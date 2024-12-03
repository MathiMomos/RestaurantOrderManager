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
                    ("SOPAS","Sopa a la Criolla", 18),
                    ("SOPAS","Caldo de Gallina", 16),
                    ("SOPAS","Chupe de Camarones", 22),
                    ("SOPAS","Shambar Norteño", 20),
                    ("SOPAS","Sancochado", 24),
                    ("SOPAS","Parihuela", 25),
                    ("SOPAS","Sopa de Choros", 18),
                    ("SOPAS","Aguadito de Pollo", 15),
                    ("SOPAS","Chilcano de Pescado", 17),
                    ("BEBIDAS","Chicha Morada", 8),
                    ("BEBIDAS","Emoliente", 7),
                    ("BEBIDAS","Refresco de Maracuyá", 7),
                    ("BEBIDAS","Jugo de Naranja", 10),
                    ("BEBIDAS","Pisco Sour", 18),
                    ("BEBIDAS","Cerveza Artesanal", 12),
                    ("BEBIDAS","Agua Mineral", 5),
                    ("BEBIDAS","Limonada Clásica", 9),
                    ("BEBIDAS","Chilcano de Pisco", 16),
                    ("PLATOS PRINCIPALES","Lomo Saltado", 35),
                    ("PLATOS PRINCIPALES","Ají de Gallina", 28),
                    ("PLATOS PRINCIPALES","Seco de Res con Frejoles", 32),
                    ("PLATOS PRINCIPALES","Tacu Tacu con Lomo", 38),
                    ("PLATOS PRINCIPALES","Ceviche Mixto", 40),
                    ("PLATOS PRINCIPALES","Arroz con Pollo", 30),
                    ("PLATOS PRINCIPALES","Causa Limeña", 22),
                    ("PLATOS PRINCIPALES","Papa a la Huancaína", 18),
                    ("PLATOS PRINCIPALES","Carapulcra con Sopa Seca", 36),
                    ("GUARNICIONES","Arroz Blanco", 6),
                    ("GUARNICIONES","Papas Fritas", 10),
                    ("GUARNICIONES","Yuquitas Fritas", 12),
                    ("GUARNICIONES","Ensalada Criolla", 10),
                    ("GUARNICIONES","Tostones de Plátano", 15),
                    ("GUARNICIONES","Arroz Chaufa", 18),
                    ("GUARNICIONES","Choclo con Queso", 14),
                    ("GUARNICIONES","Tacu Tacu", 16),
                    ("GUARNICIONES","Camotes Fritos", 10),
                    ("POSTRES", "Suspiro a la Limeña", 15),
                    ("POSTRES","Mazamorra Morada", 12),
                    ("POSTRES","Arroz con Leche", 10),
                    ("POSTRES","Turrón de Doña Pepa", 18),
                    ("POSTRES","Picarones", 20),
                    ("POSTRES","Crema Volteada", 14),
                    ("POSTRES","Alfajores", 8),
                    ("POSTRES","Helado de Lucuma", 16),
                    ("POSTRES","King Kong de Manjar Blanco", 20),
                    ("ENTRADAS","Papa a la Huancaína", 15),
                    ("ENTRADAS","Causa Rellena", 18),
                    ("ENTRADAS","Anticuchos con Papas", 22),
                    ("ENTRADAS","Choclo con Queso", 14),
                    ("ENTRADAS","Ocopa Arequipeña", 16),
                    ("ENTRADAS","Tamales Criollos", 12),
                    ("ENTRADAS","Choros a la Chalaca", 20),
                    ("ENTRADAS","Leche de Tigre", 18),
                    ("ENTRADAS","Papa Rellena", 15)
                ]
                cursor.executemany("INSERT INTO menu (category ,name, price) VALUES (? , ? , ?)", menu_items)
                print("Platos básicos agregados al menú.")
            conn.commit()

            # Insertar mesas en la tabla mesa si está vacía
            cursor.execute("SELECT COUNT(*) FROM mesa")
            if cursor.fetchone()[0] == 0:
                mesas = [(i, 4 if i <= 10 else 6, 0) for i in range(1, 16)]  # Mesas de 1 a 10 con 4 personas, y de 11 a 15 con 6
                cursor.executemany("INSERT INTO mesa (id, cantidad, state_table) VALUES (?, ?, ?)", mesas)
                print("Mesas agregadas a la base de datos.")

            # Eliminadas las cuentas de tipo "mesa"
            # for i in range(1, 16):
            #     username = f"mesa{i}"
            #     password = f"mesa{i}"
            #     hashed_password = hash_password(password)
            #     cursor.execute(
            #         "INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)",
            #         (username, hashed_password, "mesa")
            #     )
            # print("Usuarios de mesas agregados a la base de datos.")

            conn.commit()
            print("Base de datos inicializada correctamente.")

        except Error as e:
            print(f"Error al inicializar la base de datos: {e}")
        finally:
            conn.close()
    else:
        print("No se pudo crear la conexión a la base de datos.")
