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

    def add_mesa(self, mesa_number, username, password):
        try:
            self.cursor.execute("INSERT INTO mesas (mesa_number, username, password) VALUES (?, ?, ?)",
                                (mesa_number, username, password))
            self.conn.commit()
            print(f"Mesa {mesa_number} creada exitosamente.")
        except sqlite3.IntegrityError:
            print(f"Error: El nombre de usuario '{username}' ya existe.")

    def get_mesas(self):
        self.cursor.execute("SELECT * FROM mesas")
        return self.cursor.fetchall()

    def close(self):
        self.conn.close()
