import pytest

from pycommon_test import pytest_helper


def test_assert_items_equal():
    pytest_helper.assert_items_equal(
        {"key1": ["Value 2", "Value 1"], "key2": "Value 3"},
        {"key2": "Value 3", "key1": ["Value 1", "Value 2"]}
    )


def test_assert_items_equal_list_failure():
    with pytest.raises(BaseException):
        pytest_helper.assert_items_equal(
            {"key1": ["Value 2", "Value 1"], "key2": "Value 3"},
            {"key2": "Value 3", "key1": ["Value 1", "Value 2", "Value 3"]}
        )


def test_assert_items_equal_dict_failure():
    with pytest.raises(BaseException):
        pytest_helper.assert_items_equal(
            {"key1": ["Value 2", "Value 1"], "key2": "Value 3"},
            {"key2": "Value 3", "key1": ["Value 1", "Value 2"], "key3": "Value 4"}
        )
