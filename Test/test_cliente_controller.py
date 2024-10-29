import pytest
from unittest.mock import Mock
from controllers.cliente_controller import ClienteController

@pytest.fixture
def cliente_controller():
    #Fixture para crear una instancia del controlador de cliente
    return ClienteController()

def test_get_menu_items(cliente_controller, mocker):
    #Prueba que los ítems del menú se obtengan correctamente
    cursor_mock = mocker.Mock()
    cursor_mock.fetchall.return_value = [(1, 'Chicha Morada', 8.0), (2, 'Pisco Sour', 18.0)]
    cliente_controller.conn.cursor = lambda: cursor_mock

    menu_items = cliente_controller.get_menu_items()
    assert menu_items == [(1, 'Chicha Morada', 8.0), (2, 'Pisco Sour', 18.0)]

def test_add_item_to_order(cliente_controller, mocker):
    #Prueba agregar un ítem al pedido
    cursor_mock = mocker.Mock()
    cliente_controller.conn.cursor = lambda: cursor_mock
    cliente_controller.get_current_order = lambda user_id: (1, "Chicha Morada, ", 8.0)

    cliente_controller.add_item_to_order(1, "Pisco Sour", 18.0)
    cursor_mock.execute.assert_called_with(
        "UPDATE orders SET items = ?, total = ? WHERE id = ?",
        ("Chicha Morada, Pisco Sour, ", 26.0, 1)
    )

def test_confirm_order(cliente_controller, mocker):
    #Prueba confirmar un pedido
    cursor_mock = mocker.Mock()
    cliente_controller.conn.cursor = lambda: cursor_mock

    success = cliente_controller.confirm_order(1)
    assert success is True
    cursor_mock.execute.assert_called_with(
        "UPDATE orders SET status = 'confirmado' WHERE id = ?", (1,)
    )
