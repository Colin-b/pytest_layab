import re
import tempfile
import os
import gzip

import requests
import responses
import pytest

from pycommon_test import responses_helper


@responses.activate
def test_add_get_response():
    responses_helper.add_get_response("http://test", {"test": "test value"})
    response = requests.get("http://test")
    assert response.status_code == 200
    assert response.json() == {"test": "test value"}


@responses.activate
def test_add_get_response_with_pattern_url():
    responses_helper.add_get_response(
        re.compile("http://t.*t"), "test value"
    )
    response = requests.get("http://test")
    assert response.status_code == 200
    assert response.text == "test value"


@responses.activate
def test_add_get_response_with_empty_dict():
    responses_helper.add_get_response("http://test", {})
    response = requests.get("http://test")
    assert response.status_code == 200
    assert response.json() == {}


@responses.activate
def test_add_get_response_with_empty_list():
    responses_helper.add_get_response("http://test", [])
    response = requests.get("http://test")
    assert response.status_code == 200
    assert response.json() == []


@responses.activate
def test_add_post_response():
    responses_helper.add_post_response("http://test", {"test": "test value"})
    response = requests.post("http://test", json={})
    assert response.status_code == 200
    assert response.json() == {"test": "test value"}


@responses.activate
def test_add_post_response_with_pattern_url():
    with tempfile.TemporaryDirectory() as temp_dir:
        with open(os.path.join(temp_dir, "test_file"), "w") as file:
            file.write("test value")
        responses_helper.add_post_response(
            re.compile("http://t.*t"), file_path=os.path.join(temp_dir, "test_file")
        )
    response = requests.post("http://test", json={})
    assert response.status_code == 200
    assert response.text == "test value"


@responses.activate
def test_add_post_response_with_empty_dict():
    responses_helper.add_post_response("http://test", {})
    response = requests.post("http://test", json={})
    assert response.status_code == 200
    assert response.json() == {}


@responses.activate
def test_add_post_response_with_empty_list():
    responses_helper.add_post_response("http://test", [])
    response = requests.post("http://test", json={})
    assert response.status_code == 200
    assert response.json() == []


@responses.activate
def test_received_json_without_response():
    with pytest.raises(BaseException):
        responses_helper.received_json("http://test/post")


@responses.activate
def test_received_json():
    responses_helper.add_post_response("http://test/post", {})
    requests.post("http://test/post", json={"key": ["value 1", "value 2"]})
    assert responses_helper.received_json("http://test/post") == {"key": ["value 1", "value 2"]}


@responses.activate
def test_received_json_headers():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post", json={"key": "value"}, headers={"X-Test": "Test"}
    )
    assert responses_helper.received_json("http://test/post", {"X-Test": "Test"}) == {"key": "value"}


@responses.activate
def test_received_json_with_unexpected_headers():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post", json={"key": "value"}, headers={"X-Test": "Test"}
    )
    with pytest.raises(Exception):
        responses_helper.received_json("http://test/post", {"X-Test": "Failing Test"})


@responses.activate
def test_received_form():
    responses_helper.add_post_response("http://test/post", {})

    requests.post(
        "http://test/post",
        data=b"value",
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )

    assert responses_helper.received_form("http://test/post") == {}


@responses.activate
def test_received_form_headers():
    responses_helper.add_post_response("http://test/post", {})

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_file")
        with open(temp_file_path, "wt") as test_file:
            test_file.write("This is the content of the file")

        with open(temp_file_path, "rb") as file:
            requests.post(
                "http://test/post",
                data={"key": "value", b"key2": gzip.compress(b"toto")},
                files={"file1": file.read()},
            )

    form = responses_helper.received_form(
        "http://test/post",
        expected_headers={
            "Content-Type": re.compile("multipart/form-data; boundary=.*")
        },
    )
    assert form["key"] == "value"
    assert form["key2"] == gzip.compress(b"toto")
    assert form["file1"] == "This is the content of the file"
    assert len(form) == 3


@responses.activate
def test_received_form_invalid_header_regex():
    responses_helper.add_post_response("http://test/post", {})

    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_file")
        with open(temp_file_path, "wt") as test_file:
            test_file.write("This is the content of the file")

        with open(temp_file_path, "rb") as file:
            requests.post(
                "http://test/post",
                data={"key": "value"},
                files={"file1": file.read()},
            )

    with pytest.raises(Exception):
        responses_helper.received_form(
            "http://test/post",
            expected_headers={
                "Content-Type": re.compile("multipart/form-data; boundary2=.*")
            },
        )


@responses.activate
def test_received_text():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post", "this is text", headers={"Content-Type": "text/plain"}
    )
    assert responses_helper.received_text("http://test/post") == "this is text"


@responses.activate
def test_received_text_as_bytes():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post",
        b"this is 5 text",
        headers={"Content-Type": "text/plain"},
    )
    assert responses_helper.received_text("http://test/post") == "this is 5 text"


@responses.activate
def test_received_text_headers():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post", "this is text", headers={"Content-Type": "text/csv"}
    )
    assert responses_helper.received_text("http://test/post", {"Content-Type": "text/csv"}) == "this is text"


@responses.activate
def test_received_text_with_unexpected_headers():
    responses_helper.add_post_response("http://test/post", {})
    requests.post(
        "http://test/post", "this is text", headers={"Content-Type": "text/csv"}
    )
    with pytest.raises(Exception):
        responses_helper.received_text("http://test/post", {"Content-Type": "text/csv2"})
