from data.database import conectar


def crear_cuenta(nombre, contraseña, tipo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, contraseña, tipo) VALUES (?, ?, ?)", (nombre, contraseña, tipo))
    conn.commit()
    conn.close()


def establecer_mesas(numero_mesas):
    conn = conectar()
    cursor = conn.cursor()

    for i in range(1, numero_mesas + 1):
        # Crear las mesas en la tabla de mesas
        cursor.execute("INSERT INTO mesas (numero) VALUES (?)", (i,))
        # Crear cuentas de cliente con nombre y contraseña predeterminados
        nombre_mesa = f"mesa{i}"
        contraseña_mesa = f"mesa{i}"
        cursor.execute("INSERT INTO usuarios (nombre, contraseña, tipo) VALUES (?, ?, ?)",
                       (nombre_mesa, contraseña_mesa, 'cliente'))

    conn.commit()
    conn.close()
    print(f"{numero_mesas} mesas y sus cuentas de cliente han sido creadas.")


def obtener_cuentas_mesas(numero_mesas):
    cuentas = []
    for i in range(1, numero_mesas + 1):
        nombre_mesa = f"mesa{i}"
        contraseña_mesa = f"mesa{i}"
        cuentas.append((nombre_mesa, contraseña_mesa))
    return cuentas
