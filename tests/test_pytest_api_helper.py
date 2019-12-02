import os
import shutil

import pytest

from pytest_layab import service_module_name, service_module, async_service_module, app


@pytest.fixture
def before_service_init():
    path_to_temp_service_dir = create_temp_service()
    yield path_to_temp_service_dir
    shutil.rmtree(path_to_temp_service_dir)


def create_temp_service():
    path_to_temp_service_dir = os.path.join(os.path.dirname(__file__), "..", "temp_service")
    if not os.path.exists(path_to_temp_service_dir):
        os.mkdir(path_to_temp_service_dir)

    with open(os.path.join(path_to_temp_service_dir, "server.py"), "wt") as server_file:
        server_file.writelines(["from flask import Flask\n", "application = Flask(__name__)"])

    with open(os.path.join(path_to_temp_service_dir, "asynchronous_server.py"), "wt") as server_file:
        server_file.write("pass")

    return path_to_temp_service_dir


def test_service_module_name_fixture(service_module_name):
    assert service_module_name == "temp_service"


def test_service_module_fixture(service_module):
    assert service_module.__name__ == "temp_service.server"
    assert os.environ["SERVER_ENVIRONMENT"] == "test"


def test_async_service_module_fixture(async_service_module):
    assert async_service_module.__name__ == "temp_service.asynchronous_server"
    assert os.environ["SERVER_ENVIRONMENT"] == "test"


def test_app_fixture(app):
    assert app.testing is True
    assert app.config["PROPAGATE_EXCEPTIONS"] is False
