from data.database import conectar

def observar_pedidos():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE estado = 'pendiente'")
    pedidos = cursor.fetchall()
    conn.close()
    return pedidos

def confirmar_pedido(pedido_id):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = 'confirmado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
