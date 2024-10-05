import sqlite3

class Database:
    def __init__(self):
        # Conexión a la base de datos (se creará si no existe)
        self.conn = sqlite3.connect('ruta_comensal.db')
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):
        # Cargar el archivo schema.sql para crear las tablas
        with open('data/schema.sql', 'r') as schema_file:
            schema = schema_file.read()
            self.cursor.executescript(schema)
        self.conn.commit()

#usuarios del sistema ( admi , chef , caja )
    def add_user(self, username, password, role):
        try:
            self.cursor.execute("INSERT INTO usuarios (username, password, role) VALUES (?, ?, ?)",
                                (username, password, role))
            self.conn.commit()
            print(f"Usuario '{username}' creado exitosamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El nombre de usuario '{username}' ya existe.")

    def get_user(self, username):
        self.cursor.execute("SELECT * FROM usuarios WHERE username = ?", (username,))
        return self.cursor.fetchone()

# las 15 mesas del local
    def add_mesa(self, mesa_number, username, password):
        try:
            self.cursor.execute("INSERT INTO mesas (mesa_number, username, password) VALUES (?, ?, ?)",
                                (mesa_number, username, password))
            self.conn.commit()
            print(f"Mesa {mesa_number} creada exitosamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El nombre de usuario '{username}' ya existe.")

#el cliente con su nombre ,documento de identidad y visitas al local
    def add_cliente(self, nombre, documento , visitas):
        try:
            self.cursor.execute("INSERT INTO clientes (nombre, documento , visitas) VALUES (?, ? , ?)", (nombre, documento , visitas))
            self.conn.commit()
            print(f"Cliente '{nombre}' con DNI '{documento}' agregado exitosamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El cliente con DNI '{documento}' ya existe.")

    def get_cliente_por_dni(self, documento):
        self.cursor.execute("SELECT * FROM clientes WHERE documento = ?", (documento,))
        return self.cursor.fetchone()

    def update_visitas_cliente(self, documento, nuevas_visitas):
        self.cursor.execute("UPDATE clientes SET visitas = ? WHERE documento = ?", (nuevas_visitas, documento))
        self.conn.commit()

#mesas

    def get_mesas(self):
        self.cursor.execute("SELECT * FROM mesas")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
