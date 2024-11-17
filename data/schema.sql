-- data/schema.sql .

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL CHECK(role IN ('admin', 'cliente', 'chef', 'caja', 'panel'))
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    items TEXT NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pendiente', 'confirmado', 'en caja', 'finalizado')),
    total REAL NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

-- Tabla de menú
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    price REAL NOT NULL
);