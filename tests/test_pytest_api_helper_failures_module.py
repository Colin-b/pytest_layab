import pytest
from pytest_layab import service_module_name, before_service_init, test_module_name


# Ensure test will fail because fixture cannot be initialized
@pytest.mark.xfail(reason="Expected failure because test module cannot be found.")
def test_service_module_name_fixture(service_module_name):
    pass
