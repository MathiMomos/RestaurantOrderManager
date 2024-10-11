from data.database import Database
#a
class PanelController:
    def __init__(self):
        self.db = Database()

    def get_mesas_status(self):
        try:
            self.db.cursor.execute("SELECT mesa_number, status FROM mesas")
            mesas = self.db.cursor.fetchall()
            return mesas
        except Exception as e:
            return []

    def update_mesa_status(self, mesa_number, new_status):
        try:
            self.db.cursor.execute("UPDATE mesas SET status = ? WHERE mesa_number = ?", (new_status, mesa_number))
            self.db.conn.commit()
        except Exception as e:
            pass

    def close(self):
        self.db.close()
