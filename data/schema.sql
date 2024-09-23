-- schema.sql

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL UNIQUE,
    contraseña TEXT NOT NULL,
    tipo TEXT NOT NULL
);


-- Tabla de mesas
CREATE TABLE IF NOT EXISTS mesas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    numero INTEGER NOT NULL UNIQUE,
    estado TEXT NOT NULL DEFAULT 'disponible'  -- disponible, ocupada
);

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    mesa_id INTEGER,
    descripcion TEXT NOT NULL,
    estado TEXT NOT NULL,  -- pendiente, confirmado, entregado
    FOREIGN KEY (usuario_id) REFERENCES usuarios (id),
    FOREIGN KEY (mesa_id) REFERENCES mesas (id)
);
