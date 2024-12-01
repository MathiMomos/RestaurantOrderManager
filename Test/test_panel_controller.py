import pytest
from unittest.mock import Mock
from controllers.panel_controller import PanelController

@pytest.fixture
def panel_controller():
    #Fixture para crear una instancia del controlador de panel
    return PanelController()

def test_get_menu_items(panel_controller, mocker):
    #Prueba que los ítems del menú se obtengan correctamente
    cursor_mock = mocker.Mock()
    cursor_mock.fetchall.return_value = [(1, 'Lomo Saltado', 35.0), (2, 'Ceviche Mixto', 40.0)]
    panel_controller.conn.cursor = lambda: cursor_mock

    menu_items = panel_controller.get_menu_items()
    assert menu_items == [(1, 'Lomo Saltado', 35.0), (2, 'Ceviche Mixto', 40.0)]

def test_add_item_to_order_existing(panel_controller, mocker):
    #Prueba agregar un plato a un pedido existente
    cursor_mock = mocker.Mock()
    panel_controller.conn.cursor = lambda: cursor_mock
    panel_controller.get_user_order = lambda user_id: (1, "Lomo Saltado, ", 35.0)

    panel_controller.add_item_to_order(1, "Ceviche Mixto", 40.0)
    cursor_mock.execute.assert_called_with(
        "UPDATE orders SET items = ?, total = ? WHERE id = ?",
        ("Lomo Saltado, Ceviche Mixto, ", 75.0, 1)
    )

def test_confirm_order(panel_controller, mocker):
    #Prueba confirmar un pedido
    cursor_mock = mocker.Mock()
    panel_controller.conn.cursor = lambda: cursor_mock

    success = panel_controller.confirm_order(1)
    assert success is True
    cursor_mock.execute.assert_called_with(
        "UPDATE orders SET status = 'en caja' WHERE id = ? AND status = 'pendiente'", (1,)
    )