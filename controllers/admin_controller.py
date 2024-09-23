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
        cursor.execute("INSERT INTO mesas (numero) VALUES (?)", (i,))
    conn.commit()
    conn.close()
