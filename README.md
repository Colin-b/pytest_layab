<h2 align="center">Python Common Test Module</h2>

<p align="center">
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_test/job/master/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_test/master'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_test/job/master/cobertura/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_test/master&config=testCoverage'></a>
<a href='https://pse.tools.digital.engie.com/drm-all.gem/job/team/view/Python%20modules/job/pycommon_test/job/master/lastSuccessfulBuild/testReport/'><img src='https://pse.tools.digital.engie.com/drm-all.gem/buildStatus/icon?job=team/pycommon_test/master&config=testCount'></a>
</p>

Provide helper and mocks to ease test cases writing.

## Service testing ##

You can have access to several REST API assertion functions within pycommon_test.pytest_flask_helper

If you are using pytest you can import the following fixtures from pycommon_test.pytest_api_helper:
 * service_module_name (providing service module name)
 * service_module (providing server)
 * async_service_module (providing asynchronous_server)
 * app (providing flask app)
 * mock_celery (activate celery mock)
 * mock_huey (activate huey mock)

### Sending a GET request ###

```python
from pycommon_test.pytest_api_helper import *


def test_get(client):
    response = client.get('/my_endpoint')
```

### Posting JSON ###

```python
from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import post_json


def test_json_post(client):
    response = post_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

### Posting file ###

```python
from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import post_file


def test_file_post(client):
    response = post_file(client, '/my_endpoint', 'file_name', 'file/path')
```

### Posting non JSON ###

```python
from pycommon_test.pytest_api_helper import *


def test_post(client):
    response = client.post('/my_endpoint', 'data to be sent')
```

### Putting JSON ###

```python
from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import put_json


def test_json_put(client):
    response = put_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

### Putting non JSON ###

```python
from pycommon_test.pytest_api_helper import *


def test_put(client):
    response = client.put('/my_endpoint', 'data to be sent')
```

### Sending a DELETE request ###

```python
from pycommon_test.pytest_api_helper import *


def test_delete(client):
    response = client.delete('/my_endpoint')
```

### Checking response code ###

```python
from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import assert_201, assert_202_regex, assert_204, assert_303_regex


def test_200_ok(client):
    response = None
    assert response.status_code == 200

def test_201_created(client):
    response = None
    assert_201(response, '/my_new_location')

def test_202_accepted(client):
    response = None
    assert_202_regex(response, '/my_new_location/.*')

def test_204_no_content(client):
    response = None
    assert_204(response)

def test_303_see_other(client):
    response = None
    assert_303_regex(response, '/my_new_location/.*')
```

### Checking response JSON ###

```python
from pycommon_test.pytest_api_helper import *


def test_json_exact_content(client):
    response = None
    assert response.json == {'expected_key': 'Expected 13 value'}
```

### Checking response Text ###

```python
import re

from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import assert_file


def test_text_exact_content(client):
    response = None
    assert response.get_data(as_text=True) == 'Expected 13 value'

def test_text_with_regular_expression(client):
    response = None
    assert re.match('Expected \d\d value', response.get_data(as_text=True))

def test_text_with_content_in_a_file(client):
    response = None
    assert_file(response, 'path/to/file/with/expected/content')
```

### Checking response bytes ###

```python
from pycommon_test.pytest_api_helper import *
from pycommon_test.pytest_flask_helper import assert_file


def test_bytes_with_content_in_a_file(client):
    response = None
    assert_file(response, 'path/to/file/with/expected/content')
```

### Mocking response sent by another service ###

```python
import responses

from pycommon_test.responses_helper import add_get_response, add_post_response


@responses.activate
def test_get_request_mocking():
    add_get_response('http://external_url', {'key': 'value'})

@responses.activate
def test_post_request_mocking():
    add_post_response('http://external_url', {'key': 'value'})
```

### Checking JSON sent to another service ###

```python
import responses

from pycommon_test.responses_helper import received_json


@responses.activate
def test_sent_json_exact_content():
    assert received_json('/called_endpoint') == {'expected_key': 'Expected 13 value'}
```

### Checking text send to another service ###

```python
import responses

from pycommon_test.responses_helper import received_text


@responses.activate
def test_sent_text_exact_content():
    assert received_text('/called_endpoint') == 'Expected 13 value'
```

## Basic Assertions ##

```python
from pycommon_test.pytest_helper import assert_items_equal


def test_without_list_order():
    assert_items_equal({'expected_key': ['First value', 'Second value']}, {'expected_key': ['Second value', 'First value']})
```

## Mocks ##

### Date-Time ###

You can mock current date-time.

```python
import module_where_datetime_is_used


class DateTimeMock:
    @staticmethod
    def utcnow():
        class UTCDateTimeMock:
            @staticmethod
            def isoformat():
                return "2018-10-11T15:05:05.663979"
        return UTCDateTimeMock


def test_date_mock(monkeypatch):
    monkeypatch.setattr(module_where_datetime_is_used, "datetime", DateTimeMock)
```

### LDAP3 ###

You can mock ldap3 python module.

```python
from pycommon_test.ldap_mock import LDAP3ConnectionMock
```

## How to install
1. [python 3.7+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install pycommon_test -i https://all-team-remote:tBa%40W%29tvB%5E%3C%3B2Jm3@artifactory.tools.digital.engie.com/artifactory/api/pypi/all-team-pypi-prod/simple
```
