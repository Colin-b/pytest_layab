import json
from typing import List, Dict, Union, Pattern

import responses
import pytest


def add_get_response(
    url: Union[str, Pattern],
    data=None,
    file_path: str = None,
    status=200,
    **kwargs,
):
    _add_response(responses.GET, url, data, file_path, status, **kwargs)


def add_post_response(
    url: Union[str, Pattern],
    data=None,
    file_path: str = None,
    status=200,
    **kwargs,
):
    _add_response(responses.POST, url, data, file_path, status, **kwargs)


def _add_response(
    method,
    url: Union[str, Pattern],
    data=None,
    file_path: str = None,
    status=200,
    **kwargs,
):
    if file_path:
        with open(file_path, "rb") as file:
            kwargs["body"] = file.read()

    if data is not None:
        if isinstance(data, dict) or isinstance(data, list):
            kwargs["json"] = data
        else:
            kwargs["body"] = data

    responses.add(method=method, url=url, status=status, **kwargs)


def received_form(
    url: str, expected_headers: Dict[str, Union[str, Pattern]] = None
) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
    """
    Return received form on this URL so that this content can potentially be decoded before assertion.
    In case of a GZIP file for example.
    """
    if not expected_headers:
        expected_headers = {"Content-Type": "application/x-www-form-urlencoded"}
    return _to_form(_received_bytes(url, expected_headers))


def received_json(url: str, expected_headers: Dict[str, Union[str, Pattern]] = None) -> Union[dict, list]:
    if not expected_headers:
        expected_headers = {"Content-Type": "application/json"}
    return json.loads(_to_text(_received_bytes(url, expected_headers)))


def received_text(url: str, expected_headers: Dict[str, Union[str, Pattern]] = None) -> str:
    if not expected_headers:
        expected_headers = {"Content-Type": "text/plain"}
    return _to_text(_received_bytes(url, expected_headers))


def _to_text(body: Union[bytes, str]) -> str:
    return body if isinstance(body, str) else body.decode("utf-8")


def _received_bytes(
    url: str, expected_headers: Dict[str, Union[str, Pattern]]
) -> Union[bytes, str]:
    actual_request = _get_request(url)
    if not actual_request:
        pytest.fail(f"{url} was never called.")

    for expected_header_name, expected_header_value in expected_headers.items():
        if isinstance(expected_header_value, Pattern):
            assert expected_header_value.match(actual_request.headers.get(expected_header_name))
        else:
            assert actual_request.headers.get(expected_header_name) == expected_header_value
    return actual_request.body


def _to_form(body: bytes) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
    """Convert a form string to a dictionary."""
    parts = body.split(b"\r\n")
    index = 0
    form_data = {}
    while index < len(parts):
        if parts[index].startswith(b"Content-Disposition: form-data; name="):
            name = parts[index][38:].split(b'"')[0].decode("utf-8")
            index += 2
            value = parts[index]
            try:
                value = value.decode("utf-8")
            except UnicodeDecodeError:
                pass  # Keep value as bytes if it is not a string value
            form_data.setdefault(name, []).append(value)
            continue
        index += 1
    return {
        name: value if len(value) > 1 else value[0] for name, value in form_data.items()
    }


def _get_request(url: str):
    """Returns the corresponding requests PreparedRequest."""
    for call in responses.calls:
        if call.request.url == url:
            # Pop out verified request (to be able to check multiple requests)
            responses.calls._calls.remove(call)
            return call.request
