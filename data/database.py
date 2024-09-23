import sqlite3

def conectar():
    return sqlite3.connect("data/restaurant.db")

def crear_tablas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contraseña TEXT NOT NULL,
            tipo TEXT NOT NULL  -- admin, cliente, chef, caja
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS mesas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            numero INTEGER NOT NULL,
            estado TEXT NOT NULL DEFAULT 'disponible'
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pedidos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            mesa_id INTEGER,
            usuario_id INTEGER,
            estado TEXT NOT NULL DEFAULT 'pendiente',
            FOREIGN KEY (mesa_id) REFERENCES mesas(id),
            FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
        )
    ''')

    # Agregar usuario por defecto si no existe
    cursor.execute("SELECT COUNT(*) FROM usuarios")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO usuarios (nombre, contraseña, tipo) VALUES (?, ?, ?)", ('admin', 'admin', 'admin'))

    conn.commit()
    conn.close()

if __name__ == "__main__":
    crear_tablas()
    print("Base de datos y tablas creadas exitosamente.")
