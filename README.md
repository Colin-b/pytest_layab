<h2 align="center">PyTest fixtures and assertions functions for layab</h2>

<p align="center">
<a href="https://pypi.org/project/pytest-layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/pytest-layab"></a>
<a href="https://travis-ci.org/Colin-b/pytest_layab"><img alt="Build status" src="https://api.travis-ci.org/Colin-b/pytest_layab.svg?branch=develop"></a>
<a href="https://travis-ci.org/Colin-b/pytest_layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.org/Colin-b/pytest_layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-18 passed-blue"></a>
<a href="https://pypi.org/project/pytest-layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/pytest-layab"></a>
</p>

Provide helper and mocks to ease test cases writing.

## Service testing

You can have access to several REST API assertion functions

If you are using pytest you can import the following fixtures:
 * test_module_name (providing test module name, default to "test")
 * service_module_name (providing service module name, default to the folder containing server.py)
 * service_module (providing server, retrieved thanks to the service module name)
 * async_service_module (providing asynchronous_server)
 * app (providing flask app, default to application within service_module)

### Sending a GET request

```python
from pytest_layab import *


def test_get(client):
    response = client.get('/my_endpoint')
```

### Posting JSON

```python
from pytest_layab import *


def test_json_post(client):
    response = post_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

### Posting file

```python
from pytest_layab import *


def test_file_post(client):
    response = post_file(client, '/my_endpoint', 'file_name', 'file/path')
```

### Posting non JSON

```python
from pytest_layab import *


def test_post(client):
    response = client.post('/my_endpoint', 'data to be sent')
```

### Putting JSON

```python
from pytest_layab import *


def test_json_put(client):
    response = put_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

### Putting non JSON

```python
from pytest_layab import *


def test_put(client):
    response = client.put('/my_endpoint', 'data to be sent')
```

### Sending a DELETE request

```python
from pytest_layab import *


def test_delete(client):
    response = client.delete('/my_endpoint')
```

### Checking response code

```python
from pytest_layab import *


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

### Checking response JSON

```python
from pytest_layab import *


def test_json_exact_content(client):
    response = None
    assert response.json == {'expected_key': 'Expected 13 value'}
```

### Checking response Text

```python
import re

from pytest_layab import *


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

### Checking response bytes

```python
from pytest_layab import *


def test_bytes_with_content_in_a_file(client):
    response = None
    assert_file(response, 'path/to/file/with/expected/content')
```

## Basic Assertions

```python
from pytest_layab import *


def test_without_list_order():
    assert_items_equal({'expected_key': ['First value', 'Second value']}, {'expected_key': ['Second value', 'First value']})
```

## Mocks

### Date-Time

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

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install pytest_layab
```
