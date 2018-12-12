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

    def clear_database(self):
        # TODO You can clear database by overriding this method
        pass

    def fill_database(self):
        # TODO You can fill database by overriding this method
        pass
```

### Sending a GET request ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_get(self):
        response = self.get('/my_endpoint')
```

### Posting JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_json_post(self):
        response = self.post_json('/my_endpoint', {
            'my_key': 'my_value',
        })
```

### Posting file ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_file_post(self):
        response = self.post_file('/my_endpoint', 'file_name', 'file/path')
```

### Posting non JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_post(self):
        response = self.post('/my_endpoint', 'data to be sent')
```

### Putting JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_json_put(self):
        response = self.put_json('/my_endpoint', {
            'my_key': 'my_value',
        })
```

### Putting non JSON ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_put(self):
        response = self.put('/my_endpoint', 'data to be sent')
```

### Sending a DELETE request ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_delete(self):
        response = self.delete('/my_endpoint')
```

### Checking response code ###

```python
from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    def test_201_created(self):
        response = None
        self.assert_201(response, '/my_new_location')
    
    def test_202_accepted(self):
        response = None
        self.assert_202_regex(response, '/my_new_location/.*')
    
    def test_204_no_content(self):
        response = None
        self.assert_204(response)
    
    def test_303_see_other(self):
        response = None
        self.assert_303_regex(response, '/my_new_location/.*')
```

### Checking response JSON ###

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

### Checking response Text ###

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

### Checking JSON sent by service to another service ###

```python
import responses

from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    @responses.activate
    def test_sent_json_exact_content(self):
        self.assert_received_json('/called_endpoint', {'expected_key': 'Expected 13 value'})
```

### Checking text send by service to another service ###

```python
import responses

from pycommon_test.service_tester import JSONTestCase


class ServerTest(JSONTestCase):
    @responses.activate
    def test_sent_text_exact_content(self):
        self.assert_received_text('/called_endpoint', 'Expected 13 value')
```
