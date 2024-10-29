import pytest
from unittest.mock import Mock
from controllers.login_controller import LoginController

@pytest.fixture
def login_controller():
    #Fixture para crear una instancia del controlador de login
    return LoginController()

def test_hash_password(login_controller):
    password = "123456"
    hashed = login_controller.hash_password(password)
    assert hashed == "8d969eef6ecad3c29a3a629280e686cff8fabef61a16fda66d9e91a9279b8cb6"  # SHA256 de '123456'

def test_validate_user_success(login_controller, mocker):
    cursor_mock = mocker.Mock()
    cursor_mock.fetchone.return_value = (1, 'admin')
    login_controller.conn.cursor = lambda: cursor_mock

    result = login_controller.validate_user('admin', 'admin')
    assert result['status'] == 'success'
    assert result['user_id'] == 1
    assert result['role'] == 'admin'

def test_validate_user_failure(login_controller, mocker):
    cursor_mock = mocker.Mock()
    cursor_mock.fetchone.return_value = None
    login_controller.conn.cursor = lambda: cursor_mock

    result = login_controller.validate_user('admin', 'wrongpassword')
    assert result['status'] == 'error'
