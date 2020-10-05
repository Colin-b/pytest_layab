import os.path

import flask
import pytest

import pytest_layab.flask


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


def test_assert_file(client, tmpdir):
    response = client.get("/test_assert_file")
    temp_file_path = os.path.join(tmpdir, "test_file")
    with open(temp_file_path, "wt") as test_file:
        test_file.write("toto")
    pytest_layab.flask.assert_file(response, temp_file_path)


def test_assert_201(client):
    response = client.get("/test_assert_201")
    pytest_layab.flask.assert_201(response, "http://test")


def test_post_json(client):
    response = pytest_layab.flask.post_json(
        client,
        "/test_post_json",
        {"test": "test value"},
    )
    assert response.json == {"test": "test value"}


def test_post_file_and_assert_file(client, tmpdir):
    temp_file_path = os.path.join(tmpdir, "test_file")
    with open(temp_file_path, "wt") as test_file:
        test_file.write("toto")
    response = pytest_layab.flask.post_file(
        client,
        "/test_post_file_and_assert_file",
        "test_file",
        temp_file_path,
    )
    pytest_layab.flask.assert_file(response, temp_file_path)


def test_post_file_with_additional_json_and_assert_file(client, tmpdir):
    temp_file_path = os.path.join(tmpdir, "test_file")
    with open(temp_file_path, "wt") as test_file:
        test_file.write("toto")
    response = pytest_layab.flask.post_file(
        client,
        "/test_post_file_and_assert_file",
        "test_file",
        temp_file_path,
        additional_json={"key": "value"},
    )
    pytest_layab.flask.assert_file(response, temp_file_path)


def test_put_json(client):
    response = pytest_layab.flask.put_json(
        client,
        "/test_put_json",
        {"test": "test value"},
    )
    assert response.json == {"test": "test value"}
