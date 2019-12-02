import pytest
from pytest_layab import service_module_name, before_service_init


# Ensure test will fail because fixture cannot be initialized
@pytest.mark.xfail(reason="Expected failure because server.py file cannot be located.")
def test_service_module_name_fixture(service_module_name):
    pass
