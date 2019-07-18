import glob
import os.path
import sys
import importlib

import pytest


@pytest.fixture
def service_module_name() -> str:
    test_file_path = sys.modules["test"].__file__
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
    return service_module.application


@pytest.fixture
def async_service_module(service_module_name):
    # Ensure that test configuration will be loaded
    os.environ["SERVER_ENVIRONMENT"] = "test"
    return importlib.import_module(
        f"{service_module_name}.asynchronous_server"
    )


@pytest.fixture
def mock_celery(async_service_module):
    from flasynk.celery_mock import CeleryMock

    celery_app_func = async_service_module.get_asynchronous_app

    def proxify(func):
        def wrapper(*args, **kwargs):
            return CeleryMock(func(*args, **kwargs))

        return wrapper

    async_service_module.get_asynchronous_app = proxify(celery_app_func)


@pytest.fixture
def mock_huey(async_service_module):
    huey_app_func = async_service_module.get_asynchronous_app

    def proxify(func):
        def wrapper(*args, **kwargs):
            huey_app = func(*args, **kwargs)
            huey_app.immediate = True
            return huey_app

        return wrapper

    async_service_module.get_asynchronous_app = proxify(huey_app_func)
