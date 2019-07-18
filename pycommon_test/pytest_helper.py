from typing import Union


def assert_items_equal(actual: Union[dict, list], expected: Union[dict, list]):
    if isinstance(actual, list):  # List order does not matter in JSON
        assert sorted(actual) == sorted(expected)
    elif isinstance(actual, dict):  # Allow to validate inner lists in JSON dict
        if len(expected) != len(actual):
            assert actual == expected  # Will give a clean comparison
        else:
            for expected_key in expected.keys():
                assert_items_equal(
                    actual.get(expected_key), expected[expected_key]
                )
    else:
        assert actual == expected
