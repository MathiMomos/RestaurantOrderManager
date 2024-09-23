from data.database import conectar

def observar_boletas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM pedidos WHERE estado = 'confirmado'")
    boletas = cursor.fetchall()
    conn.close()
    return boletas

def metodo_pago(pedido_id, metodo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("UPDATE pedidos SET estado = 'pagado' WHERE id = ?", (pedido_id,))
    conn.commit()
    conn.close()
