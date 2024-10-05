-- Creación de la tabla de usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL -- Puede ser 'admin', 'chef', 'caja', 'mesa'
);

-- Creación de la tabla de mesas
CREATE TABLE IF NOT EXISTS mesas (
    id INTEGER xPRIMARY KEY AUTOINCREMENT,
    mesa_number INTEGER NOT NULL UNIQUE,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    FOREIGN KEY (username) REFERENCES usuarios(username)
);

--clientes guarda nombre , dni y num visitas
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    dni TEXT NOT NULL UNIQUE,
    visitas INTEGER NOT NULL default 0
);

-- Los item de los pedidos
CREATE TABLE IF NOT EXISTS item (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    precio REAL NOT NULL,
    cantidad INTEGER NOT NULL UNIQUE,
    categoria TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS pedidos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    cliente_id INTEGER,
    producto TEXT NOT NULL,
    cantidad INTEGER NOT NULL,
    precio REAL NOT NULL,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
);
