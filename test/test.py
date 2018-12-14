import responses
import requests
import tempfile
import os.path

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

        app.testing = True
        return app

    @responses.activate
    def test_add_get_response(self):
        service_tester.add_get_response('http://test', {'test': 'test value'})
        response = self.get('/test_add_get_response')
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    @responses.activate
    def test_add_post_response(self):
        service_tester.add_post_response('http://test', {'test': 'test value'})
        response = self.post_json('/test_add_post_response', {})
        self.assert_200(response)
        self.assert_json(response, {'test': 'test value'})

    def test_assert_file(self):
        response = self.get('/test_assert_file')
        self.assert_200(response)
        with tempfile.TemporaryDirectory() as temp_dir:
            temp_file_path = os.path.join(temp_dir, 'test_file')
            with open(temp_file_path, 'wt') as test_file:
                test_file.write('toto')
            self.assert_file(response, temp_file_path)
