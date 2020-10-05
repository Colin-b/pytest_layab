import os
import shutil

import pytest

from pytest_layab.flask import app


@pytest.fixture
def service_module_name():
    path_to_temp_service_dir = create_temp_service()
    yield "temp_service.server"
    shutil.rmtree(path_to_temp_service_dir)


def create_temp_service():
    path_to_temp_service_dir = os.path.join(
        os.path.dirname(__file__), "..", "temp_service"
    )
    if not os.path.exists(path_to_temp_service_dir):
        os.mkdir(path_to_temp_service_dir)

    with open(os.path.join(path_to_temp_service_dir, "server.py"), "wt") as server_file:
        server_file.writelines(
            ["from flask import Flask\n", "application = Flask(__name__)"]
        )

    return path_to_temp_service_dir


def test_app_fixture(app):
    assert os.environ["SERVER_ENVIRONMENT"] == "test"
    assert app.name == "temp_service.server"
    assert app.testing is True
    assert app.config["PROPAGATE_EXCEPTIONS"] is False
