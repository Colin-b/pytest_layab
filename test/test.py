import os.path
import tempfile

import requests
import responses

from pycommon_test import (
    service_tester,
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
