import os.path
import tempfile
import re

import requests
import responses
import flask

from pycommon_test import service_tester


class ServiceTesterMock(service_tester.JSONTestCase):
    def create_app(self):
        app = flask.Flask(__name__)

        @app.route("/test_add_get_response")
        def test_add_get_response():
            return flask.jsonify(requests.get("http://test").json())

        @app.route("/test_add_post_response", methods=["POST"])
        def test_add_post_response():
            return flask.jsonify(
                requests.post("http://test", flask.request.json).json()
            )

        @app.route("/test_assert_file")
        def test_assert_file():
            return flask.make_response("toto")

        @app.route("/test_get_without_handle_202")
        def test_get_without_handle_202():
            response = flask.make_response("toto", 202)
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_post_without_handle_202", methods=["POST"])
        def test_post_without_handle_202():
            response = flask.make_response(flask.request.data, 202)
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_post_json_without_handle_202", methods=["POST"])
        def test_post_json_without_handle_202():
            response = flask.jsonify(flask.request.json)
            response.status_code = 202
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_post_file_without_handle_202", methods=["POST"])
        def test_post_file_without_handle_202():
            response = flask.make_response(flask.request.files["test_file"].read(), 202)
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_put_without_handle_202", methods=["PUT"])
        def test_put_without_handle_202():
            response = flask.make_response(flask.request.data, 202)
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_put_json_without_handle_202", methods=["PUT"])
        def test_put_json_without_handle_202():
            response = flask.jsonify(flask.request.json)
            response.status_code = 202
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_delete_without_handle_202", methods=["DELETE"])
        def test_delete_without_handle_202():
            response = flask.make_response("toto", 202)
            response.headers["location"] = "http://test"
            return response

        @app.route("/test_excel_file")
        def test_excel_file():
            this_dir = os.path.abspath(os.path.dirname(__file__))
            with open(os.path.join(this_dir, "resources", "sent_file.xlsx"), "rb") as file:
                response = flask.make_response(file.read())
            response.headers[
                "Content-Type"
            ] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            response.headers[
                "Content-Disposition"
            ] = f'attachment; filename=sent_file.xlsx'
            response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
            return response

        app.testing = True
        return app

    @responses.activate
    def test_add_get_response(self):
        service_tester.add_get_response("http://test", {"test": "test value"})
        response = self.get("/test_add_get_response")
        self.assert_200(response)
        self.assert_json(response, {"test": "test value"})

    @responses.activate
    def test_add_get_response_with_pattern(self):
        service_tester.add_get_response(
            re.compile("http://t.*t"), {"test": "test value"}
        )
        response = self.get("/test_add_get_response")
        self.assert_200(response)
        self.assert_json(response, {"test": "test value"})

    @responses.activate
    def test_add_get_with_empty_dict_response(self):
        service_tester.add_get_response("http://test", {})
        response = self.get("/test_add_get_response")
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_get_empty_list_response(self):
        service_tester.add_get_response("http://test", [])
        response = self.get("/test_add_get_response")
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_post_response(self):
        service_tester.add_post_response("http://test", {"test": "test value"})
        response = self.post_json("/test_add_post_response", {})
        self.assert_200(response)
        self.assert_json(response, {"test": "test value"})

    @responses.activate
    def test_add_post_response_with_pattern(self):
        service_tester.add_post_response(
            re.compile("http://t.*t"), {"test": "test value"}
        )
        response = self.post_json("/test_add_post_response", {})
        self.assert_200(response)
        self.assert_json(response, {"test": "test value"})

    @responses.activate
    def test_add_post_with_empty_dict_response(self):
        service_tester.add_post_response("http://test", {})
        response = self.post_json("/test_add_post_response", {})
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_post_with_empty_list_response(self):
        service_tester.add_post_response("http://test", [])
        response = self.post_json("/test_add_post_response", {})
        self.assert_200(response)
        self.assert_json(response, [])

    def test_assert_file(self):
        response = self.get("/test_assert_file")
        self.assert_200(response)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "test_file")
            with open(temp_file_path, "wt") as test_file:
                test_file.write("toto")
            self.assert_file(response, temp_file_path)

    def test_get_without_handle_202(self):
        response = self.get("/test_get_without_handle_202", handle_202=False)
        self.assert_202_regex(response, "http://test")
        self.assert_text(response, "toto")

    def test_post_without_handle_202(self):
        response = self.post(
            "/test_post_without_handle_202", data="toto", handle_202=False
        )
        self.assert_202_regex(response, "http://test")
        self.assert_text(response, "toto")

    def test_post_json_without_handle_202(self):
        response = self.post_json(
            "/test_post_json_without_handle_202",
            {"test": "test value"},
            handle_202=False,
        )
        self.assert_202_regex(response, "http://test")
        self.assert_json(response, {"test": "test value"})

    @responses.activate
    def test_assert_received_json(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post("http://test/post", json={"key": "value"})
        self.assert_received_json("http://test/post", {"key": "value"})

    @responses.activate
    def test_received_form(self):
        service_tester.add_post_response("http://test/post", {})

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

        form = self.received_form(
            "http://test/post",
            expected_headers={
                "Content-Type": re.compile("multipart/form-data; boundary=.*")
            },
        )
        self.assertEqual(form["key"], "value")
        self.assertEqual(form["file1"], "This is the content of the file")
        self.assertEqual(len(form), 2)

    @responses.activate
    def test_assert_received_form(self):
        service_tester.add_post_response("http://test/post", {})

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

        self.assert_received_form(
            "http://test/post",
            {"key": "value", "file1": "This is the content of the file"},
            expected_headers={
                "Content-Type": re.compile("multipart/form-data; boundary=.*")
            },
        )

    @responses.activate
    def test_assert_received_form_invalid_header_regex(self):
        service_tester.add_post_response("http://test/post", {})

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

        with self.assertRaises(Exception):
            self.assert_received_form(
                "http://test/post",
                {"key": "value", "file1": "This is the content of the file"},
                expected_headers={
                    "Content-Type": re.compile("multipart/form-data; boundary2=.*")
                },
            )

    @responses.activate
    def test_assert_received_form_failure_wrong_value(self):
        service_tester.add_post_response("http://test/post", {})

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

        with self.assertRaises(Exception):
            self.assert_received_form(
                "http://test/post",
                {"wrong key": "value", "file1": "This is the content of the file"},
                expected_headers={
                    "Content-Type": re.compile("multipart/form-data; boundary=.*")
                },
            )

    @responses.activate
    def test_assert_received_form_failure_unexpected_value(self):
        service_tester.add_post_response("http://test/post", {})

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

        with self.assertRaises(Exception):
            self.assert_received_form(
                "http://test/post",
                {
                    "unknown key": "value",
                    "key": "value",
                    "file1": "This is the content of the file",
                },
                expected_headers={
                    "Content-Type": re.compile("multipart/form-data; boundary=.*")
                },
            )

    @responses.activate
    def test_assert_received_form_failure_wrong_value(self):
        service_tester.add_post_response("http://test/post", {})

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

        with self.assertRaises(Exception):
            self.assert_received_form(
                "http://test/post",
                {"key": "wrong value", "file1": "This is the content of the file"},
                expected_headers={
                    "Content-Type": re.compile("multipart/form-data; boundary=.*")
                },
            )

    @responses.activate
    def test_assert_received_form_failure_missing_value(self):
        service_tester.add_post_response("http://test/post", {})

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

        with self.assertRaises(Exception):
            self.assert_received_form(
                "http://test/post",
                {"file1": "This is the content of the file"},
                expected_headers={
                    "Content-Type": re.compile("multipart/form-data; boundary=.*")
                },
            )

    @responses.activate
    def test_assert_received_json_headers(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", json={"key": "value"}, headers={"X-Test": "Test"}
        )
        self.assert_received_json(
            "http://test/post", {"key": "value"}, {"X-Test": "Test"}
        )

    @responses.activate
    def test_assert_received_json_headers_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", json={"key": "value"}, headers={"X-Test": "Test"}
        )
        with self.assertRaises(Exception):
            self.assert_received_json(
                "http://test/post", {"key": "value"}, {"X-Test": "Failing Test"}
            )

    @responses.activate
    def test_assert_received_json_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post("http://test/post", json={"key": "value"})
        with self.assertRaises(Exception):
            self.assert_received_json("http://test/post", {"key": "wrong value"})

    @responses.activate
    def test_assert_received_text(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is text", headers={"Content-Type": "text/plain"}
        )
        self.assert_received_text("http://test/post", "this is text")

    @responses.activate
    def test_assert_received_text_headers(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is text", headers={"Content-Type": "text/csv"}
        )
        self.assert_received_text(
            "http://test/post", "this is text", {"Content-Type": "text/csv"}
        )

    @responses.activate
    def test_assert_received_text_headers_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is text", headers={"Content-Type": "text/csv"}
        )
        with self.assertRaises(Exception):
            self.assert_received_text(
                "http://test/post", "this is text", {"Content-Type": "text/csv2"}
            )

    @responses.activate
    def test_assert_received_text_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is text", headers={"Content-Type": "text/plain"}
        )
        with self.assertRaises(Exception):
            self.assert_received_text("http://test/post", "this is not text")

    @responses.activate
    def test_assert_received_text_regex(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is 5 text", headers={"Content-Type": "text/plain"}
        )
        self.assert_received_text_regex("http://test/post", "this is \d text")

    @responses.activate
    def test_assert_received_text_regex_headers(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is 5 text", headers={"Content-Type": "text/csv"}
        )
        self.assert_received_text_regex(
            "http://test/post", "this is \d text", {"Content-Type": "text/csv"}
        )

    @responses.activate
    def test_assert_received_text_regex_headers_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post", "this is 5 text", headers={"Content-Type": "text/csv"}
        )
        with self.assertRaises(Exception):
            self.assert_received_text_regex(
                "http://test/post", "this is \d text", {"Content-Type": "text/csv2"}
            )

    @responses.activate
    def test_assert_received_bytes_text_regex(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post",
            b"this is 5 text",
            headers={"Content-Type": "text/plain"},
        )
        self.assert_received_text_regex("http://test/post", "this is \d text")

    @responses.activate
    def test_assert_received_text_regex_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post",
            "this is 55 text",
            headers={"Content-Type": "text/plain"},
        )
        with self.assertRaises(Exception):
            self.assert_received_text_regex("http://test/post", "this is \d text")

    @responses.activate
    def test_assert_received_bytes_text_regex_failure(self):
        service_tester.add_post_response("http://test/post", {})
        requests.post(
            "http://test/post",
            b"this is 55 text",
            headers={"Content-Type": "text/plain"},
        )
        with self.assertRaises(Exception):
            self.assert_received_text_regex("http://test/post", "this is \d text")

    def test_post_file_without_handle_202(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, "test_file")
            with open(temp_file_path, "wt") as test_file:
                test_file.write("toto")
            response = self.post_file(
                "/test_post_file_without_handle_202",
                "test_file",
                temp_file_path,
                handle_202=False,
            )
            self.assert_202_regex(response, "http://test")
            self.assert_file(response, temp_file_path)

    def test_put_without_handle_202(self):
        response = self.put(
            "/test_put_without_handle_202", data="toto", handle_202=False
        )
        self.assert_202_regex(response, "http://test")
        self.assert_text(response, "toto")

    def test_put_json_without_handle_202(self):
        response = self.put_json(
            "/test_put_json_without_handle_202",
            {"test": "test value"},
            handle_202=False,
        )
        self.assert_202_regex(response, "http://test")
        self.assert_json(response, {"test": "test value"})

    def test_delete_without_handle_202(self):
        response = self.delete("/test_delete_without_handle_202", handle_202=False)
        self.assert_202_regex(response, "http://test")
        self.assert_text(response, "toto")

    def test_excel_file_content(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        self.assert_excel_content(response.data, os.path.join(this_dir, "resources", "sent_file_copy.xlsx"))

    def test_excel_file_response(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        self.assert_excel_file(response, os.path.join(this_dir, "resources", "sent_file_copy.xlsx"))

    def test_excel_file_content_with_different_format(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with self.assertRaises(Exception) as cm:
            self.assert_excel_content(response.data, os.path.join(this_dir, "resources", "different_format.xlsx"))
        self.assertIn("Different cell type in row 5, column 3.", str(cm.exception))

    def test_excel_file_response_with_different_format(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with self.assertRaises(Exception) as cm:
            self.assert_excel_file(response, os.path.join(this_dir, "resources", "different_format.xlsx"))
        self.assertIn("Different cell type in row 5, column 3.", str(cm.exception))

    def test_excel_file_content_with_different_value(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with self.assertRaises(Exception) as cm:
            self.assert_excel_content(response.data, os.path.join(this_dir, "resources", "different_value.xlsx"))
        self.assertIn("Different cell in row 5, column 1.", str(cm.exception))

    def test_excel_file_response_with_different_value(self):
        response = self.get("/test_excel_file")
        this_dir = os.path.abspath(os.path.dirname(__file__))
        with self.assertRaises(Exception) as cm:
            self.assert_excel_file(response, os.path.join(this_dir, "resources", "different_value.xlsx"))
        self.assertIn("Different cell in row 5, column 1.", str(cm.exception))
