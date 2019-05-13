import glob
import json
import logging
import os.path
import sys
import tempfile
from typing import List, Dict, Union, Pattern

import responses
from flask_testing import TestCase

# Ensure that test configuration will be loaded
os.environ["SERVER_ENVIRONMENT"] = "test"
logger = logging.getLogger(__name__)


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


class JSONTestCase(TestCase):
    _service_module_name = None
    server = None

    def _find_service_module_name(self) -> str:
        test_file_path = sys.modules[self.__module__].__file__
        test_folder_path = os.path.dirname(test_file_path)
        root_folder_path = os.path.join(test_folder_path, "..")
        service_files = glob.glob(f"{root_folder_path}/*/server.py")
        if len(service_files) != 1:
            raise Exception(f"Unable to locate the server.py file: {service_files}.")
        service_module_path = os.path.dirname(service_files[0])
        return os.path.basename(service_module_path)

    def create_app(self):
        # Retrieve service module name only once
        if not JSONTestCase._service_module_name:
            JSONTestCase._service_module_name = self._find_service_module_name()

        from importlib import import_module

        self._mock_celery(import_module)
        self._mock_huey(import_module)

        self.server = import_module(f"{JSONTestCase._service_module_name}.server")
        self.server.application.testing = True

        return self.server.application

    @staticmethod
    def _mock_celery(import_module):
        try:
            from flasynk.celery_mock import CeleryMock

            celery_server = import_module(
                f"{JSONTestCase._service_module_name}.asynchronous_server"
            )

            celery_app_func = celery_server.get_asynchronous_app

            def proxify(func):
                def wrapper(*args, **kwargs):
                    return CeleryMock(func(*args, **kwargs))

                return wrapper

            celery_server.get_asynchronous_app = proxify(celery_app_func)
        except ImportError:
            pass  # Celery might not be required by application

    @staticmethod
    def _mock_huey(import_module):
        try:
            huey_server = import_module(
                f"{JSONTestCase._service_module_name}.asynchronous_server"
            )

            huey_app_func = huey_server.get_asynchronous_app

            def proxify(func):
                def wrapper(*args, **kwargs):
                    huey_app = func(*args, **kwargs)
                    huey_app.immediate = True
                    return huey_app

                return wrapper

            huey_server.get_asynchronous_app = proxify(huey_app_func)
        except ImportError:
            pass  # Huey might not be required by application

    def setUp(self):
        self._log_start()
        self.maxDiff = None
        self.clear_database()
        self.fill_database()

    def tearDown(self):
        self.clear_database()
        self._log_end()

    def clear_database(self):
        # Do nothing by default
        pass

    def fill_database(self):
        # Do nothing by default
        pass

    def _log_start(self):
        logger.info(f"-------------------------------")
        logger.info(f"Start of {self._testMethodName}")

    def _log_end(self):
        logger.info(f"End of {self._testMethodName}")
        logger.info(f"-------------------------------")

    def assert_201(self, response, expected_location: str) -> str:
        """
        Assert that status code is 201.
        201 stands for Created, meaning that location header is expected as well.
        Assert that location header is containing the expected location (hostname trimmed for tests)

        :param response: response object from service to be asserted
        :param expected_location: Expected location starting from server root (eg: /xxx)
        :return Location from server root.
        """
        self.assertStatus(response, 201)
        actual_location = response.headers["location"].replace("http://localhost", "")
        self.assertEqual(expected_location, actual_location)
        return actual_location

    def assert_202_regex(self, response, expected_location_regex: str) -> str:
        """
        Assert that status code is 202.
        202 stands for Accepted, meaning that location header is expected as well.
        Assert that location header is containing the expected location (hostname trimmed for tests)

        :param response: response object from service to be asserted
        :param expected_location_regex: Expected location starting from server root (eg: /xxx). Can be a regular exp.
        :return Location from server root.
        """
        self.assertStatus(response, 202)
        actual_location = response.headers["location"].replace("http://localhost", "")
        self.assertRegex(actual_location, expected_location_regex)
        return actual_location

    def assert_204(self, response) -> None:
        """
        Assert that status code is 204.
        204 stands for No Content, meaning that body should be empty.
        Assert that body is empty.
        """
        self.assertStatus(response, 204)
        self.assert_text(response, "")

    def assert_303_regex(self, response, expected_location_regex: str) -> str:
        """
        Assert that status code is 303.
        303 stands for See Other, meaning that location header is expected as well.
        Assert that location header is containing the expected location (hostname trimmed for tests)

        :param response: response object from service to be asserted
        :param expected_location_regex: Expected location starting from server root (eg: /xxx). Can be a regular exp.
        :return Location from server root.
        """
        self.assertStatus(response, 303)
        actual_location = response.location.replace("http://localhost", "")
        self.assertRegex(actual_location, expected_location_regex)
        return actual_location

    def assert_json(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = _to_json(response.data)
        self._assert_json_equal(expected, actual)

    def _assert_json_equal(self, expected, actual):
        if isinstance(actual, list):  # List order does not matter in JSON
            self.assertCountEqual(expected, actual)
        elif isinstance(actual, dict):  # Allow to validate inner lists in JSON dict
            if len(expected) != len(actual):
                self.assertEqual(
                    expected, actual, "Number of elements is not the same."
                )  # Will give a clean comparison
            else:
                for expected_key in expected.keys():
                    self._assert_json_equal(
                        expected[expected_key], actual.get(expected_key)
                    )
        else:
            self.assertEqual(expected, actual)

    def assert_json_regex(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON (with regex in values).
        """
        actual = _to_json(response.data)
        self.assertRegex(f"{actual}", f"{expected}")

    def assert_text(self, response, expected: str):
        """
        Assert that response is containing the following text.

        :param response: Received query response.
        :param expected: Expected text.
        """
        self.assertEqual(expected, _to_text(response.data))

    def assert_text_regex(self, response, expected: str):
        """
        Assert that response is containing the following text.

        :param response: Received query response.
        :param expected: Expected text (with regex in values).
        """
        self.assertRegex(_to_text(response.data), expected)

    def assert_file(self, response, expected_file_path: str):
        """
        Assert that response is containing the bytes contained in expected file.

        :param response: Received query response.
        :param expected_file_path: Path to the file containing expected bytes.
        """
        with open(expected_file_path, "rb") as expected_file:
            self.assertEqual(expected_file.read(), response.data)

    def received_form(
        self, url: str, expected_headers: Dict[str, Union[str, Pattern]] = None
    ) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
        """
        Return received form on this URL so that this content can potentially be decoded before assertion.
        In case of a GZIP file for example.
        """
        if not expected_headers:
            expected_headers = {"Content-Type": "application/x-www-form-urlencoded "}
        return _to_form(self._received_bytes(url, expected_headers))

    def _received_json(self, url: str, expected_headers: Dict[str, Union[str, Pattern]]):
        if not expected_headers:
            expected_headers = {"Content-Type": "application/json"}
        return _to_json(self._received_bytes(url, expected_headers))

    def _received_text(self, url: str, expected_headers: Dict[str, Union[str, Pattern]]):
        if not expected_headers:
            expected_headers = {"Content-Type": "text/plain"}
        return _to_text(self._received_bytes(url, expected_headers))

    def _received_bytes(
        self, url: str, expected_headers: Dict[str, Union[str, Pattern]]
    ) -> Union[bytes, str]:
        actual_request = _get_request(url)
        if not actual_request:
            self.fail(f"{url} was never called.")

        for expected_header_name, expected_header_value in expected_headers.items():
            if isinstance(expected_header_value, Pattern):
                self.assertRegex(
                    actual_request.headers.get(expected_header_name),
                    expected_header_value.pattern,
                )
            else:
                self.assertEqual(
                    expected_header_value,
                    actual_request.headers.get(expected_header_name),
                )
        return actual_request.body

    def assert_received_form(
        self,
        url: str,
        expected_form: Dict[str, Union[bytes, str, List[Union[bytes, str]]]],
        expected_headers: Dict[str, Union[str, Pattern]] = None,
    ):
        self.assertEqual(expected_form, self.received_form(url, expected_headers))

    def assert_received_json(
        self,
        url: str,
        expected: Union[dict, list],
        expected_headers: Dict[str, str] = None,
    ):
        actual = self._received_json(url, expected_headers)
        if isinstance(actual, list):  # List order does not matter in JSON
            self.assertCountEqual(expected, actual)
        else:
            self.assertEqual(expected, actual)

    def assert_received_text(
        self, url: str, expected: str, expected_headers: Dict[str, str] = None
    ):
        self.assertEqual(expected, self._received_text(url, expected_headers))

    def assert_received_text_regex(
        self, url: str, expected: str, expected_headers: Dict[str, str] = None
    ):
        self.assertRegex(self._received_text(url, expected_headers), expected)

    def assert_swagger(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = _to_json(response.data)
        actual_paths = actual["paths"] or {}
        actual["paths"] = None
        expected_paths = expected.get("paths", {})
        expected["paths"] = None
        self.assertEqual(expected, actual)
        self.assertEqual(
            len(expected_paths), len(actual_paths), msg="Different number of paths."
        )
        actual_parameters = actual_paths.pop("parameters", None)
        if actual_parameters:
            self.assertEqual(expected_paths.get("parameters"), actual_parameters)
        for path_key, actual_path in actual_paths.items():
            expected_path = expected_paths.get(path_key, {})
            self.assertEqual(
                len(expected_path),
                len(actual_path),
                msg=f"Different number of {path_key} methods.",
            )
            actual_parameters = actual_path.pop("parameters", None)
            if actual_parameters:
                self.assertEqual(expected_path.get("parameters"), actual_parameters)
            for method_key, actual_method in actual_path.items():
                expected_method = expected_path.get(method_key, {})
                if "parameters" in expected_method:
                    expected_parameters = sorted(
                        expected_method.get("parameters", {}),
                        key=lambda parameter: parameter.get("name", None),
                    )
                else:
                    expected_parameters = None
                expected_method["parameters"] = None
                if "parameters" in actual_method:
                    actual_parameters = sorted(
                        actual_method["parameters"],
                        key=lambda parameter: parameter["name"],
                    )
                else:
                    actual_parameters = None
                actual_method["parameters"] = None
                self.assertEqual(expected_method, actual_method)
                self.assertEqual(expected_parameters, actual_parameters)

    def get(self, url: str, handle_202: bool = True, *args, **kwargs):
        """
        Send a GET request to this URL.

        :param url: Relative server URL (starts with /).
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        response = self.client.get(url, *args, **kwargs)
        return self._async_method(response, handle_202)

    def post(self, url: str, handle_202: bool = True, *args, **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        response = self.client.post(url, *args, **kwargs)
        return self._async_method(response, handle_202)

    def post_json(self, url: str, json_body: Union[Dict, List], **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        return self.post(
            url, data=json.dumps(json_body), content_type="application/json", **kwargs
        )

    def post_file(
        self,
        url: str,
        file_name: str,
        file_path: str,
        additional_json: dict = None,
        **kwargs,
    ):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param file_name: Name of the parameter corresponding to the file to be sent.
        :param file_path: Path to the file that should be sent.
        :param additional_json: Additional JSON to be sent in body.
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        with open(file_path, "rb") as file:
            data = {file_name: (file, file_name)}
            if additional_json:
                data.update(additional_json)
            return self.post(url, data=data, **kwargs)

    def put(self, url: str, handle_202: bool = True, *args, **kwargs):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        response = self.client.put(url, *args, **kwargs)
        return self._async_method(response, handle_202)

    def put_json(self, url: str, json_body: Union[Dict, List], **kwargs):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        return self.put(
            url, data=json.dumps(json_body), content_type="application/json", **kwargs
        )

    def delete(self, url: str, handle_202: bool = True, *args, **kwargs):
        """
        Send a DELETE request to this URL.

        :param url: Relative server URL (starts with /).
        :param handle_202: Handle 202 status code by requesting the corresponding location. Default to True.
        :return: Received response.
        """
        response = self.client.delete(url, *args, **kwargs)
        return self._async_method(response, handle_202)

    def _async_method(self, response, handle_202: bool):
        if response.status_code == 202 and handle_202:
            return self._assert_async(response)
        return response

    def _assert_async(self, response):
        status_url = self.assert_202_regex(response, ".*")
        status_reply = self.client.get(status_url)
        result_url = self.assert_303_regex(status_reply, ".*")
        return self.client.get(result_url)

    def assert_excel_file(self, response, expected_file_path: str):
        self.assert_excel_content(response.data, expected_file_path)

    def assert_excel_content(self, actual_content: bytes, expected_file_path: str):
        import xlrd
        with tempfile.TemporaryDirectory() as temp_dir:
            with open(
                    os.path.join(temp_dir, "actual_excel_file.xlsx"), "wb"
            ) as temp_file:
                temp_file.write(actual_content)

            actual_workbook = xlrd.open_workbook(temp_file.name)

            expected_workbook = xlrd.open_workbook(expected_file_path)

            self.assertCountEqual(actual_workbook.sheet_names(), expected_workbook.sheet_names())

            for sheet_name in actual_workbook.sheet_names():
                self._assert_sheet_content(
                    actual_workbook.sheet_by_name(sheet_name),
                    expected_workbook.sheet_by_name(sheet_name),
                )

    def _assert_sheet_content(self, actual_worksheet, expected_worksheet):
        self.assertEqual(
            actual_worksheet.nrows,
            expected_worksheet.nrows,
            "Different number of rows.",
        )
        self.assertEqual(
            actual_worksheet.ncols,
            expected_worksheet.ncols,
            "Different number of columns.",
        )

        for row_index, actual_row in enumerate(actual_worksheet.get_rows()):
            expected_row = expected_worksheet.row(row_index)
            for cell_index, actual_cell in enumerate(actual_row):
                expected_cell = expected_row[cell_index]
                self.assertEqual(
                    actual_cell.ctype,
                    expected_cell.ctype,
                    f"Different cell type in row {row_index}, column {cell_index}.",
                )
                self.assertEqual(
                    actual_cell.value,
                    expected_cell.value,
                    f"Different cell in row {row_index}, column {cell_index}.",
                )


def _to_form(body: bytes) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
    """Convert a form string to a dictionary."""
    parts = body.split(b"\r\n")
    index = 0
    form_data = {}
    while index < len(parts):
        if parts[index].startswith(b"Content-Disposition: form-data; name="):
            name = _to_text(parts[index][38:].split(b'"')[0])
            index += 2
            value = parts[index]
            try:
                value = _to_text(value)
            except UnicodeDecodeError:
                pass  # Keep value as bytes if it is not a string value
            form_data.setdefault(name, []).append(value)
            continue
        index += 1
    return {
        name: value if len(value) > 1 else value[0] for name, value in form_data.items()
    }


def _to_text(body: Union[bytes, str]) -> str:
    return body if isinstance(body, str) else body.decode("utf-8")


def _to_json(body: bytes):
    return json.loads(_to_text(body))


def _get_request(url: str):
    """Returns the corresponding requests PreparedRequest."""
    for call in responses.calls:
        if call.request.url == url:
            responses.calls._calls.remove(
                call
            )  # Pop out verified request (to be able to check multiple requests)
            return call.request
