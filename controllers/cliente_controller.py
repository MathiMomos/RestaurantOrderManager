from data.database import conectar

def realizar_reserva(mesa_id, usuario_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO pedidos (mesa_id, usuario_id) VALUES (?, ?)", (mesa_id, usuario_id))
    conn.commit()
    conn.close()
