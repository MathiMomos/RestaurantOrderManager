from data.database import Database

class PanelController:
    def __init__(self):
        self.db = Database()

    def get_mesas_status(self):
        try:
            self.db.cursor.execute("SELECT mesa_number, status FROM mesas")
            mesas = self.db.cursor.fetchall()  # Obtiene todas las filas
            return mesas
        except Exception as e:
            print(f"Error al obtener el estado de las mesas: {str(e)}")
            return []

    def update_mesa_status(self, mesa_number, new_status):
        try:
            self.db.cursor.execute("UPDATE mesas SET status = ? WHERE mesa_number = ?", (new_status, mesa_number))
            self.db.conn.commit()
        except Exception as e:
            print(f"Error al actualizar el estado de la mesa: {str(e)}")

    def close(self):
        self.db.close()
