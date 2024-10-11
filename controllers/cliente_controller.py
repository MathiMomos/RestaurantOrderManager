from data.database import Database
import json
#a
class ClienteController:
    def __init__(self, chef_controller):
        self.db = Database()
        self.chef_controller = chef_controller  # Agregar referencia al ChefController

    def start_visit(self, mesa_number):
        self.db.update_mesa_status(mesa_number, 'occupied')

    def add_to_order(self, mesa_number, items, total_price):
        items_json = json.dumps(items)
        self.db.create_order(mesa_number, items_json, total_price)
        self.chef_controller.receive_order(mesa_number, items, total_price)  # Notificar al chef

    def get_order(self, mesa_number):
        return self.db.get_orders_by_mesa(mesa_number)

    def finish_visit(self, mesa_number):
        self.db.update_mesa_status(mesa_number, 'free')

    def close(self):
        self.db.close()
