import json
import logging
import os.path
from typing import List, Dict, Union
import sys
import glob

from flask_testing import TestCase
import responses

os.environ['SERVER_ENVIRONMENT'] = 'test'  # Ensure that test configuration will be loaded
logger = logging.getLogger(__name__)


class JSONTestCase(TestCase):
    _service_module_name = None

    def _find_service_module_name(self) -> str:
        test_file_path = sys.modules[self.__module__].__file__
        test_folder_path = os.path.dirname(test_file_path)
        root_folder_path = os.path.join(test_folder_path, '..')
        service_files = glob.glob(f'{root_folder_path}/*/server.py')
        if len(service_files) != 1:
            raise Exception(f'Unable to locate the server.py file: {service_files}.')
        service_module_path = os.path.dirname(service_files[0])
        return os.path.basename(service_module_path)

    def create_app(self):
        # Retrieve service module name only once
        if not JSONTestCase._service_module_name:
            JSONTestCase._service_module_name = self._find_service_module_name()

        from importlib import import_module
        try:
            from pycommon_test.celery_mock import TestCeleryAppProxy

            celery_server = import_module(f'{JSONTestCase._service_module_name}.celery_server')

            celery_app_func = celery_server.get_celery_app

            celery_server.get_celery_app = lambda x: TestCeleryAppProxy(celery_app_func(x))
        except ImportError:
            pass  # Celery might not be required by application

        server = import_module(f'{JSONTestCase._service_module_name}.server')

        server.application.testing = True
        return server.application

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
        logger.info(f'-------------------------------')
        logger.info(f'Start of {self._testMethodName}')

    def _log_end(self):
        logger.info(f'End of {self._testMethodName}')
        logger.info(f'-------------------------------')

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
        actual_location = response.headers['location'].replace('http://localhost', '')
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
        actual_location = response.headers['location'].replace('http://localhost', '')
        self.assertRegex(actual_location, expected_location_regex)
        return actual_location

    def assert_204(self, response) -> None:
        """
        Assert that status code is 204.
        204 stands for No Content, meaning that body should be empty.
        Assert that body is empty.
        """
        self.assertStatus(response, 204)
        self.assert_text(response, '')

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
        actual_location = response.location.replace('http://localhost', '')
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
                self.assertEqual(expected, actual, 'Number of elements is not the same.')  # Will give a clean comparison
            else:
                for expected_key in expected.keys():
                    self._assert_json_equal(expected[expected_key], actual.get(expected_key))
        else:
            self.assertEqual(expected, actual)

    def assert_json_regex(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON (with regex in values).
        """
        actual = _to_json(response.data)
        self.assertRegex(f'{actual}', f'{expected}')

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

    def received_form(self, url: str) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
        return _to_form(self.received_bytes(url))

    def received_json(self, url: str):
        return _to_json(self.received_bytes(url))

    def received_text(self, url: str):
        return _to_text(self.received_bytes(url))

    def received_bytes(self, url: str) -> bytes:
        actual_request = _get_request(url)
        if not actual_request:
            self.fail(f'{url} was never called.')

        return actual_request.body

    def assert_received_form(self, url: str, expected_form: Dict[str, Union[bytes, str, List[Union[bytes, str]]]]):
        return self.assertEqual(expected_form, self.received_form(url))

    def assert_received_json(self, url: str, expected):
        actual = self.received_json(url)
        if isinstance(actual, list):  # List order does not matter in JSON
            self.assertCountEqual(expected, actual)
        else:
            self.assertEqual(expected, actual)

    def assert_received_text(self, url: str, expected: str):
        return self.assertEqual(expected, self.received_text(url))

    def assert_swagger(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = _to_json(response.data)
        actual_paths = actual['paths'] or {}
        actual['paths'] = None
        expected_paths = expected.get('paths', {})
        expected['paths'] = None
        self.assertEqual(expected, actual)
        self.assertEqual(len(expected_paths), len(actual_paths), msg='Different number of paths.')
        actual_parameters = actual_paths.pop('parameters', None)
        if actual_parameters:
            self.assertEqual(expected_paths.get('parameters'), actual_parameters)
        for path_key, actual_path in actual_paths.items():
            expected_path = expected_paths.get(path_key, {})
            self.assertEqual(len(expected_path), len(actual_path), msg=f'Different number of {path_key} methods.')
            actual_parameters = actual_path.pop('parameters', None)
            if actual_parameters:
                self.assertEqual(expected_path.get('parameters'), actual_parameters)
            for method_key, actual_method in actual_path.items():
                expected_method = expected_path.get(method_key, {})
                if 'parameters' in expected_method:
                    expected_parameters = sorted(expected_method.get('parameters', {}),
                                                 key=lambda parameter: parameter.get('name', None))
                else:
                    expected_parameters = None
                expected_method['parameters'] = None
                if 'parameters' in actual_method:
                    actual_parameters = sorted(actual_method['parameters'], key=lambda parameter: parameter['name'])
                else:
                    actual_parameters = None
                actual_method['parameters'] = None
                self.assertEqual(expected_method, actual_method)
                self.assertEqual(expected_parameters, actual_parameters)

    def get(self, url: str, *args, **kwargs):
        """
        Send a GET request to this URL.

        :param url: Relative server URL (starts with /).
        :return: Received response.
        """
        response = self.client.get(url, *args, **kwargs)
        return self._async_method(response)

    def post(self, url: str, *args, **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :return: Received response.
        """
        response = self.client.post(url, *args, **kwargs)
        return self._async_method(response)

    def post_json(self, url: str, json_body: Union[Dict, List], **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.post(url, data=json.dumps(json_body), content_type='application/json', **kwargs)

    def post_file(self, url: str, file_name: str, file_path: str, additional_json: dict=None, **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param file_name: Name of the parameter corresponding to the file to be sent.
        :param file_path: Path to the file that should be sent.
        :param additional_json: Additional JSON to be sent in body.
        :return: Received response.
        """
        with open(file_path, 'rb') as file:
            data = {file_name: (file, file_name)}
            if additional_json:
                data.update(additional_json)
            return self.post(url, data=data, **kwargs)

    def put(self, url: str, *args, **kwargs):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :return: Received response.
        """
        response = self.client.put(url, *args, **kwargs)
        return self._async_method(response)

    def put_json(self, url: str, json_body: Union[Dict, List], **kwargs):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.put(url, data=json.dumps(json_body), content_type='application/json', **kwargs)

    def delete(self, url: str, *args, **kwargs):
        """
        Send a DELETE request to this URL.

        :param url: Relative server URL (starts with /).
        :return: Received response.
        """
        response = self.client.delete(url, *args, **kwargs)
        return self._async_method(response)

    def _async_method(self, response):
        if response.status_code == 202:
            return self._assert_async(response)
        return response

    def _assert_async(self, response):
        status_url = self.assert_202_regex(response, '.*')
        status_reply = self.client.get(status_url)
        result_url = self.assert_303_regex(status_reply, '.*')
        return self.client.get(result_url)


def _to_form(body: bytes) -> Dict[str, Union[bytes, str, List[Union[bytes, str]]]]:
    """Convert a form string to a dictionary."""
    parts = body.split(b'\r\n')
    index = 0
    form_data = {}
    while index < len(parts):
        if parts[index].startswith(b'Content-Disposition: form-data; name='):
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
        name: value if len(value) > 1 else value[0]
        for name, value in form_data.items()
    }


def _to_text(body: bytes) -> str:
    return body.decode('utf-8')


def _to_json(body: bytes):
    return json.loads(_to_text(body))


def _get_request(url: str):
    for call in responses.calls:
        if call.request.url == url:
            responses.calls._calls.remove(call)  # Pop out verified request (to be able to check multiple requests)
            return call.request
