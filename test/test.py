import os.path
import tempfile
import re
import unittest

import requests
import responses

from pycommon_test import (
    service_tester,
    adam_mock
)


class ServiceTesterMock(service_tester.JSONTestCase):

    def create_app(self):
        import flask
        app = flask.Flask(__name__)

        @app.route('/test_add_get_response')
        def test_add_get_response():
            return flask.jsonify(requests.get('http://test').json())

        @app.route('/test_add_post_response', methods=['POST'])
        def test_add_post_response():
            return flask.jsonify(requests.post('http://test', flask.request.json).json())

        @app.route('/test_assert_file')
        def test_assert_file():
            return flask.make_response('toto')

        @app.route('/test_get_without_handle_202')
        def test_get_without_handle_202():
            response = flask.make_response('toto', 202)
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_post_without_handle_202', methods=['POST'])
        def test_post_without_handle_202():
            response = flask.make_response(flask.request.data, 202)
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_post_json_without_handle_202', methods=['POST'])
        def test_post_json_without_handle_202():
            response = flask.jsonify(flask.request.json)
            response.status_code = 202
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_post_file_without_handle_202', methods=['POST'])
        def test_post_file_without_handle_202():
            response = flask.make_response(flask.request.files['test_file'].read(), 202)
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_put_without_handle_202', methods=['PUT'])
        def test_put_without_handle_202():
            response = flask.make_response(flask.request.data, 202)
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_put_json_without_handle_202', methods=['PUT'])
        def test_put_json_without_handle_202():
            response = flask.jsonify(flask.request.json)
            response.status_code = 202
            response.headers['location'] = 'http://test'
            return response

        @app.route('/test_delete_without_handle_202', methods=['DELETE'])
        def test_delete_without_handle_202():
            response = flask.make_response('toto', 202)
            response.headers['location'] = 'http://test'
            return response

        app.testing = True
        return app

    @responses.activate
    def test_add_get_response(self):
        service_tester.add_get_response('http://test', {'test': 'test value'})
        response = self.get('/test_add_get_response')
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    @responses.activate
    def test_add_get_response_with_pattern(self):
        service_tester.add_get_response(re.compile('http://t.*t'), {'test': 'test value'})
        response = self.get('/test_add_get_response')
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    @responses.activate
    def test_add_get_with_empty_dict_response(self):
        service_tester.add_get_response('http://test', {})
        response = self.get('/test_add_get_response')
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_get_empty_list_response(self):
        service_tester.add_get_response('http://test', [])
        response = self.get('/test_add_get_response')
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_post_response(self):
        service_tester.add_post_response('http://test', {'test': 'test value'})
        response = self.post_json('/test_add_post_response', {})
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    @responses.activate
    def test_add_post_response_with_pattern(self):
        service_tester.add_post_response(re.compile('http://t.*t'), {'test': 'test value'})
        response = self.post_json('/test_add_post_response', {})
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    @responses.activate
    def test_add_post_with_empty_dict_response(self):
        service_tester.add_post_response('http://test', {})
        response = self.post_json('/test_add_post_response', {})
        self.assert_200(response)
        self.assert_json(response, {})

    @responses.activate
    def test_add_post_with_empty_list_response(self):
        service_tester.add_post_response('http://test', [])
        response = self.post_json('/test_add_post_response', {})
        self.assert_200(response)
        self.assert_json(response, [])

    def test_assert_file(self):
        response = self.get('/test_assert_file')
        self.assert_200(response)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, 'test_file')
            with open(temp_file_path, 'wt') as test_file:
                test_file.write('toto')
            self.assert_file(response, temp_file_path)

    def test_get_without_handle_202(self):
        response = self.get('/test_get_without_handle_202', handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_text(response, 'toto')

    def test_post_without_handle_202(self):
        response = self.post('/test_post_without_handle_202', data='toto', handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_text(response, 'toto')

    def test_post_json_without_handle_202(self):
        response = self.post_json('/test_post_json_without_handle_202', {'test': 'test value'}, handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_json(response, {'test': 'test value'})

    def test_post_file_without_handle_202(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, 'test_file')
            with open(temp_file_path, 'wt') as test_file:
                test_file.write('toto')
            response = self.post_file('/test_post_file_without_handle_202', 'test_file', temp_file_path, handle_202=False)
            self.assert_202_regex(response, 'http://test')
            self.assert_file(response, temp_file_path)

    def test_put_without_handle_202(self):
        response = self.put('/test_put_without_handle_202', data='toto', handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_text(response, 'toto')

    def test_put_json_without_handle_202(self):
        response = self.put_json('/test_put_json_without_handle_202', {'test': 'test value'}, handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_json(response, {'test': 'test value'})

    def test_delete_without_handle_202(self):
        response = self.delete('/test_delete_without_handle_202', handle_202=False)
        self.assert_202_regex(response, 'http://test')
        self.assert_text(response, 'toto')


class ADAMMockTest(unittest.TestCase):
    def setUp(self):
        self.adam = adam_mock.AdamMock('http://test')

    @responses.activate
    def test_add_application_groups(self):
        self.adam.set_application_groups('0009', ('0009.00001', 'Group 1'), ('0009.00002', 'Group 2'))
        self.assertEqual(requests.get('http://test/groups?name=0009.*').json(), [
            {
                'cn': '0009.00001',
                'description': 'Group 1',
            },
            {
                'cn': '0009.00002',
                'description': 'Group 2',
            },
        ])

    @responses.activate
    def test_update_application_groups(self):
        self.adam.set_application_groups('0009', ('0009.00001', 'Group 1'), ('0009.00002', 'Group 2'))
        self.adam.set_application_groups('0009', ('0009.00002', 'Group 2'))
        self.assertEqual(requests.get('http://test/groups?name=0009.*').json(), [
            {
                'cn': '0009.00002',
                'description': 'Group 2',
            },
        ])

    @responses.activate
    def test_add_user_groups(self):
        self.adam.set_user_groups('JS5391', '0009.00001', '0009.00002')
        self.assertEqual(requests.get('http://test/users/JS5391').json(), [
            {
                'memberOf': ['0009.00001', '0009.00002'],
            },
        ])

    @responses.activate
    def test_update_user_groups(self):
        self.adam.set_user_groups('JS5391', '0009.00001', '0009.00002')
        self.adam.set_user_groups('JS5391', '0009.00002')
        self.assertEqual(requests.get('http://test/users/JS5391').json(), [
            {
                'memberOf': ['0009.00002'],
            },
        ])

    @responses.activate
    def test_add_user_groups_via_helper(self):
        adam_mock.mock_user_groups('http://test', 'JS5391', '0009.00001', '0009.00002')
        self.assertEqual(requests.get('http://test/users/JS5391').json(), [
            {
                'memberOf': ['0009.00001', '0009.00002'],
            },
        ])

    @responses.activate
    def test_update_user_groups_via_helper(self):
        adam_mock.mock_user_groups('http://test', 'JS5391', '0009.00001', '0009.00002')
        adam_mock.mock_user_groups('http://test', 'JS5391', '0009.00002')
        self.assertEqual(requests.get('http://test/users/JS5391').json(), [
            {
                'memberOf': ['0009.00002'],
            },
        ])

    @responses.activate
    def test_add_health_pass(self):
        self.adam.health_should_succeed()
        self.assertEqual(requests.get('http://test/health').json(), {
            'status': 'pass'
        })
        self.assertEqual(requests.get('http://test/health').status_code, 200)

    @responses.activate
    def test_add_health_fail(self):
        self.adam.health_should_fail()
        self.assertEqual(requests.get('http://test/health').json(), {
            'status': 'fail'
        })
        self.assertEqual(requests.get('http://test/health').status_code, 400)

    @responses.activate
    def test_update_health_pass(self):
        self.adam.health_should_fail()
        self.adam.health_should_succeed()
        self.assertEqual(requests.get('http://test/health').json(), {
            'status': 'pass'
        })
        self.assertEqual(requests.get('http://test/health').status_code, 200)

    @responses.activate
    def test_update_health_fail(self):
        self.adam.health_should_succeed()
        self.adam.health_should_fail()
        self.assertEqual(requests.get('http://test/health').json(), {
            'status': 'fail'
        })
        self.assertEqual(requests.get('http://test/health').status_code, 400)

