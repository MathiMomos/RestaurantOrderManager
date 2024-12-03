-- schema.sql

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
    mesa_id INTEGER NOT NULL,
    client_id INTEGER NOT NULL,
    items TEXT NOT NULL,
    item_prices REAL NOT NULL,
    item_amounts INTEGER NOT NULL,
    status TEXT NOT NULL CHECK(status IN ('pendiente', 'confirmado', 'en caja', 'finalizado')),
    time_in TEXT,
    time_out TEXT,
    total REAL NOT NULL,
    FOREIGN KEY (client_id) REFERENCES client(id),
    FOREIGN KEY (mesa_id) REFERENCES mesa(id)
);

-- Tabla de menú
CREATE TABLE IF NOT EXISTS menu (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT NOT NULL,
    price REAL NOT NULL
);

-- Tabla de clientaes
CREATE TABLE IF NOT EXISTS client (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  documents TEXT NOT NULL,
  visits INTEGER NOT NULL DEFAULT 0
);

-- Tabla de mesas
CREATE TABLE IF NOT EXISTS mesa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cantidad INTEGER NOT NULL,
    state_table INTEGER NOT NULL
);

-- Tabla de caja
CREATE TABLE IF NOT EXISTS caja (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    orders_id INTEGER NOT NULL,
    method_pay TEXT NOT NULL,
    FOREIGN KEY (orders_id) REFERENCES orders(id)
);
