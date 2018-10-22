import os
import json
import logging
from flask_testing import TestCase
from typing import Dict, List

os.environ['SERVER_ENVIRONMENT'] = 'test'  # Ensure that test configuration will be loaded
logger = logging.getLogger(__name__)


class JSONTestCase(TestCase):

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

    def assert_json(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = json.loads(response.data.decode('utf-8'))
        if isinstance(actual, list):  # List order does not matter in JSON
            self.assertCountEqual(expected, actual)
        else:
            self.assertEqual(expected, actual)

    def assert_json_regex(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON (with regex in values).
        """
        actual = json.loads(response.data.decode('utf-8'))
        self.assertRegex(f'{actual}', f'{expected}')

    def assert_text(self, response, expected: str):
        """
        Assert that response is containing the following text.

        :param response: Received query response.
        :param expected: Expected text.
        """
        actual = response.data.decode('utf-8')
        self.assertEqual(expected, actual)

    def assert_text_regex(self, response, expected: str):
        """
        Assert that response is containing the following text.

        :param response: Received query response.
        :param expected: Expected text (with regex in values).
        """
        actual = response.data.decode('utf-8')
        self.assertRegex(expected, actual)

    def assert_received_form(self, url: str, expected_form: Dict[str, List[str]]):
        actual_request = _get_request(url)
        if not actual_request:
            self.fail(f'{url} was never called.')

        actual_form = _to_form(actual_request.body.decode())
        return self.assertEqual(actual_form, expected_form)

    def assert_swagger(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = json.loads(response.data.decode('utf-8'))
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
                    expected_parameters = sorted(expected_method.get('parameters', {}), key=lambda parameter: parameter.get('name', None))
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

    def post_json(self, url, json_body, **kwargs):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.client.post(url, data=json.dumps(json_body), content_type='application/json', **kwargs)

    def put_json(self, url, json_body, **kwargs):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.client.put(url, data=json.dumps(json_body), content_type='application/json', **kwargs)


def _to_form(body: str) -> Dict[str, List[str]]:
    """Convert a form string to a dictionary."""
    parts = body.split('\r\n')
    index = 0
    form_data = {}
    while index < len(parts):
        if parts[index].startswith('Content-Disposition: form-data; name='):
            name = parts[index][38:].split('"')[0]
            index += 2
            form_data.setdefault(name, []).append(parts[index])
            continue
        index += 1
    return form_data


def _get_request(url: str):
    try:
        import responses
    except ImportError:
        raise Exception('responses python module is required.')

    for call in responses.calls:
        if call.request.url == url:
            return call.request
