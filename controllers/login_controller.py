from data.database import conectar

class Usuario:
    def __init__(self, id, nombre, tipo):
        self.id = id
        self.nombre = nombre
        self.tipo = tipo

def autenticar_usuario(nombre, contraseña):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT id, nombre, tipo FROM usuarios WHERE nombre = ? AND contraseña = ?", (nombre, contraseña))
    user_data = cursor.fetchone()
    conn.close()

    if user_data:
        return Usuario(*user_data)  # Retorna una instancia de Usuario si se encuentra
    return None  # Usuario no encontrado
