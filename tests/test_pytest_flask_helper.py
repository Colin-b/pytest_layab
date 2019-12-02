import os.path
import tempfile

import flask
import pytest

import pytest_layab


@pytest.fixture
def app():
    application = flask.Flask(__name__)

    @application.route("/test_assert_file")
    def get_test_assert_file():
        return flask.make_response("toto")

    @application.route("/test_assert_201")
    def get_test_assert_201():
        response = flask.make_response("toto", 201)
        response.headers["location"] = "http://test"
        return response

    @application.route("/test_assert_202_regex")
    def get_test_assert_202_regex():
        response = flask.make_response("toto", 202)
        response.headers["location"] = "http://test"
        return response

    @application.route("/test_assert_204")
    def get_test_assert_204():
        return flask.make_response("", 204)

    @application.route("/test_assert_303_regex")
    def get_test_assert_303_regex():
        response = flask.make_response("toto", 303)
        response.headers["location"] = "http://test/result"
        return response

    @application.route("/test_assert_async")
    def get_test_assert_async():
        response = flask.make_response("toto", 202)
        response.headers["location"] = "http://test/test_assert_303_regex"
        return response

    @application.route("/result")
    def get_result():
        return flask.make_response("This is the result")

    @application.route("/test_post_json", methods=["POST"])
    def post_test_post_json():
        return flask.jsonify(flask.request.json)

    @application.route("/test_post_file_and_assert_file", methods=["POST"])
    def post_test_post_file_and_assert_file():
        return flask.make_response(flask.request.files["test_file"].read())

    @application.route("/test_put_json", methods=["PUT"])
    def put_test_put_json():
        return flask.jsonify(flask.request.json)

    application.testing = True
    return application


def test_assert_file(client):
    response = client.get("/test_assert_file")
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_file")
        with open(temp_file_path, "wt") as test_file:
            test_file.write("toto")
        pytest_layab.assert_file(response, temp_file_path)


def test_assert_201(client):
    response = client.get("/test_assert_201")
    pytest_layab.assert_201(response, "http://test")


def test_assert_202_regex(client):
    response = client.get("/test_assert_202_regex")
    pytest_layab.assert_202_regex(response, "http://test")


def test_assert_204(client):
    response = client.get("/test_assert_204")
    pytest_layab.assert_204(response)


def test_assert_303_regex(client):
    response = client.get("/test_assert_303_regex")
    pytest_layab.assert_303_regex(response, "http://test")


def test_assert_async(client):
    response = client.get("/test_assert_async")
    response = pytest_layab.assert_async(client, response)
    assert response.get_data(as_text=True) == "This is the result"


def test_post_json(client):
    response = pytest_layab.post_json(
        client,
        "/test_post_json",
        {"test": "test value"},
    )
    assert response.json == {"test": "test value"}


def test_post_file_and_assert_file(client):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_file")
        with open(temp_file_path, "wt") as test_file:
            test_file.write("toto")
        response = pytest_layab.post_file(
            client,
            "/test_post_file_and_assert_file",
            "test_file",
            temp_file_path,
        )
        pytest_layab.assert_file(response, temp_file_path)


def test_post_file_with_additional_json_and_assert_file(client):
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_file_path = os.path.join(temp_dir, "test_file")
        with open(temp_file_path, "wt") as test_file:
            test_file.write("toto")
        response = pytest_layab.post_file(
            client,
            "/test_post_file_and_assert_file",
            "test_file",
            temp_file_path,
            additional_json={"key": "value"}
        )
        pytest_layab.assert_file(response, temp_file_path)


def test_put_json(client):
    response = pytest_layab.put_json(
        client,
        "/test_put_json",
        {"test": "test value"},
    )
    assert response.json == {"test": "test value"}
