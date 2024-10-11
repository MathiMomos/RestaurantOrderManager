-- Crear tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

-- Tabla para guardar configuraciones del sistema, como el número de mesas
CREATE TABLE IF NOT EXISTS settings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    setting_key TEXT UNIQUE NOT NULL,
    setting_value TEXT NOT NULL
);

-- Tabla para almacenar órdenes
CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_number INTEGER NOT NULL,
    order_items TEXT NOT NULL,    -- Lista de ítems en el pedido (JSON)
    total_price REAL NOT NULL,    -- Precio total del pedido
    status TEXT NOT NULL DEFAULT 'pending'  -- Estados: pending, completed
);

-- Tabla para el estado de las mesas
CREATE TABLE IF NOT EXISTS mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mesa_number INTEGER UNIQUE NOT NULL,
    status TEXT NOT NULL DEFAULT 'free'  -- Estados: free, occupied
);
