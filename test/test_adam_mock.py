import requests
import responses
import pytest

from pycommon_test import adam_mock


@pytest.fixture
def adam():
    return adam_mock.AdamMock("http://test")


@responses.activate
def test_add_application_groups(adam):
    adam.set_application_groups(
        "0009", ("0009.00001", "Group 1"), ("0009.00002", "Group 2")
    )
    assert requests.get("http://test/groups?name=0009.*").json() == [
        {"cn": "0009.00001", "description": "Group 1"},
        {"cn": "0009.00002", "description": "Group 2"},
    ]


@responses.activate
def test_update_application_groups(adam):
    adam.set_application_groups(
        "0009", ("0009.00001", "Group 1"), ("0009.00002", "Group 2")
    )
    adam.set_application_groups("0009", ("0009.00002", "Group 2"))
    assert requests.get("http://test/groups?name=0009.*").json() == [{"cn": "0009.00002", "description": "Group 2"}]


@responses.activate
def test_add_user_groups(adam):
    adam.set_user_groups("JS5391", "0009.00001", "0009.00002")
    assert requests.get("http://test/users/JS5391").json() == [{"memberOf": ["0009.00001", "0009.00002"]}]


@responses.activate
def test_update_user_groups(adam):
    adam.set_user_groups("JS5391", "0009.00001", "0009.00002")
    adam.set_user_groups("JS5391", "0009.00002")
    assert requests.get("http://test/users/JS5391").json() == [{"memberOf": ["0009.00002"]}]


@responses.activate
def test_add_user_groups_via_helper():
    adam_mock.mock_user_groups("http://test", "JS5391", "0009.00001", "0009.00002")
    assert requests.get("http://test/users/JS5391").json() == [{"memberOf": ["0009.00001", "0009.00002"]}]


@responses.activate
def test_update_user_groups_via_helper():
    adam_mock.mock_user_groups("http://test", "JS5391", "0009.00001", "0009.00002")
    adam_mock.mock_user_groups("http://test", "JS5391", "0009.00002")
    assert requests.get("http://test/users/JS5391").json() == [{"memberOf": ["0009.00002"]}]


@responses.activate
def test_add_health_pass(adam):
    adam.health_should_succeed()
    assert requests.get("http://test/health").json() == {"status": "pass"}
    assert requests.get("http://test/health").status_code == 200


@responses.activate
def test_add_health_fail(adam):
    adam.health_should_fail()
    assert requests.get("http://test/health").json() == {"status": "fail"}
    assert requests.get("http://test/health").status_code == 400


@responses.activate
def test_update_health_pass(adam):
    adam.health_should_fail()
    adam.health_should_succeed()
    assert requests.get("http://test/health").json() == {"status": "pass"}
    assert requests.get("http://test/health").status_code == 200


@responses.activate
def test_update_health_fail(adam):
    adam.health_should_succeed()
    adam.health_should_fail()
    assert requests.get("http://test/health").json() == {"status": "fail"}
    assert requests.get("http://test/health").status_code == 400
