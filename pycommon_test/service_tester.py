import os
import json
import logging
from flask_testing import TestCase

os.environ['ENVIRONMENT'] = 'test'  # Ensure that test configuration will be loaded
logger = logging.getLogger(__name__)


class JSONTestCase(TestCase):

    def setUp(self):
        self.log_test_start()
        self.maxDiff = None
        self.clear_database()
        self.fill_database()

    def tearDown(self):
        self.clear_database()
        self.log_test_end()

    def clear_database(self):
        # Do nothing by default
        pass

    def fill_database(self):
        # Do nothing by default
        pass

    def log_test_start(self):
        logger.info(f'-------------------------------')
        logger.info(f'Start of {self._testMethodName}')

    def log_test_end(self):
        logger.info(f'End of {self._testMethodName}')
        logger.info(f'-------------------------------')

    def assert_json(self, response, expected):
        """
        Assert that response is containing the following JSON.

        :param response: Received query response.
        :param expected: Expected python structure corresponding to the JSON.
        """
        actual = json.loads(response.data.decode('utf-8'))
        self.assertEqual(expected, actual)

    def post_json(self, url, json_body):
        """
        Send a POST request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.client.post(url, data=json.dumps(json_body), content_type='application/json')

    def put_json(self, url, json_body):
        """
        Send a PUT request to this URL.

        :param url: Relative server URL (starts with /).
        :param json_body: Python structure corresponding to the JSON to be sent.
        :return: Received response.
        """
        return self.client.put(url, data=json.dumps(json_body), content_type='application/json')
