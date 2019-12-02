import glob
import os.path
import sys
import importlib

import pytest


@pytest.fixture
def before_service_init():
    pass


@pytest.fixture
def test_module_name():
    return "test"


@pytest.fixture
def service_module_name(before_service_init, test_module_name) -> str:
    test_file_path = sys.modules[test_module_name].__file__
    test_folder_path = os.path.dirname(test_file_path)
    root_folder_path = os.path.join(test_folder_path, "..")
    service_files = glob.glob(f"{root_folder_path}/*/server.py")
    if len(service_files) != 1:
        pytest.fail(f"Unable to locate the server.py file: {service_files}.")
    service_module_path = os.path.dirname(service_files[0])
    return os.path.basename(service_module_path)


@pytest.fixture
def service_module(service_module_name):
    # Ensure that test configuration will be loaded
    os.environ["SERVER_ENVIRONMENT"] = "test"
    return importlib.import_module(f"{service_module_name}.server")


@pytest.fixture
def app(service_module):
    service_module.application.testing = True
    service_module.application.config["PROPAGATE_EXCEPTIONS"] = False
    return service_module.application


@pytest.fixture
def async_service_module(service_module_name):
    # Ensure that test configuration will be loaded
    os.environ["SERVER_ENVIRONMENT"] = "test"
    return importlib.import_module(
        f"{service_module_name}.asynchronous_server"
    )
