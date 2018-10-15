# Python Common Test Module #

Provide helper and mocks to ease test cases writing.

## Service testing ##

You can instantiate a service test case by extending pycommon_test.service_tester.JSONTestCase

This test case:
 * Log start and end of test.
 * Provides overridable methods to fill and clear database between each test.
 * Provides various assertion methods (in addition to [http://flask.pocoo.org/docs/1.0/testing/]).

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):

    def create_app(self):
        server.application.testing = True
        return server.application

    def clear_database(self):
        # TODO You can clear database by overriding this method
        pass

    def fill_database(self):
        # TODO You can fill database by overriding this method
        pass
```

### Posting JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_json_post (self):
        response = self.post_json('/my_url',
                                  {
                                      'my_key': 'my_value',
                                  })
```

### Putting JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_json_put(self):
        response = self.put_json('/my_url',
                                  {
                                      'my_key': 'my_value',
                                  })
```

### Checking JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_json_exact_content(self):
        response = None
        self.assert_json(response, {'expected_key': 'Expected 13 value'})

    def test_json_with_regular_expression(self):
        response = None
        self.assert_json_regex(response, {'expected_key': 'Expected \d\d value'})

    def test_open_api_definition(self):
        response = None
        self.assert_swagger(response, {'expected_swagger_key': 'Expected swagger value'})
```

### Checking Text ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_text_exact_content(self):
        response = None
        self.assert_text(response, 'Expected 13 value')

    def test_text_with_regular_expression(self):
        response = None
        self.assert_text_regex(response, 'Expected \d\d value')
```
