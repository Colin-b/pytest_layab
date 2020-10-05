<h2 align="center">pytest fixtures and assertions functions for layab</h2>

<p align="center">
<a href="https://pypi.org/project/pytest-layab/"><img alt="pypi version" src="https://img.shields.io/pypi/v/pytest-layab"></a>
<a href="https://travis-ci.com/Colin-b/pytest_layab"><img alt="Build status" src="https://api.travis-ci.com/Colin-b/pytest_layab.svg?branch=master"></a>
<a href="https://travis-ci.com/Colin-b/pytest_layab"><img alt="Coverage" src="https://img.shields.io/badge/coverage-100%25-brightgreen"></a>
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
<a href="https://travis-ci.com/Colin-b/pytest_layab"><img alt="Number of tests" src="https://img.shields.io/badge/tests-18 passed-blue"></a>
<a href="https://pypi.org/project/pytest-layab/"><img alt="Number of downloads" src="https://img.shields.io/pypi/dm/pytest-layab"></a>
</p>

`pytest` fixtures and utility functions that can be used to test [`layab`](https://github.com/Colin-b/layab) based REST API.

- [Flask based API](#flask)
  - [Test client](#test-client)
  - [Sending JSON (as POST)](#posting-json)
  - [Sending file (as POST)](#posting-file)
  - [Sending JSON (as PUT)](#putting-json)
  - [Assert CREATED response](#checking-http-201-created-response)
  - [Compare response content to a file](#checking-response-content)
 
### Flask

#### Test client

You can have access to the `pytest-flask` `client` fixture for your [`layab`](https://github.com/Colin-b/layab) based REST API.

Providing a `service_module_name` `pytest` fixture will give you access to a [Flask test client](https://pytest-flask.readthedocs.io/en/latest/index.html) and ensure `SERVER_ENVIRONMENT` environment variable will be set to `test` in order to load test specific configuration.

`pytest-flask` must be installed for the following sample to work:

```python
import pytest
from pytest_layab.flask import app


@pytest.fixture
def service_module_name():
    # Considering main.py exists within a folder named my_module.
    # And main.py contains a variable named application containing the Flask app.
    return "my_module.main"


def test_get(client):
    # Perform a GET request on your application on /my_endpoint endpoint.
    response = client.get('/my_endpoint')
```

#### Helper functions

The following examples consider that you already have a [test client](#test-client).

##### Posting JSON

```python
from pytest_layab.flask import post_json


def test_json_post(client):
    response = post_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

##### Posting file

```python
from pytest_layab.flask import post_file


def test_file_post(client):
    response = post_file(client, '/my_endpoint', 'file_name', 'file/path')
```

##### Putting JSON

```python
from pytest_layab.flask import put_json


def test_json_put(client):
    response = put_json(client, '/my_endpoint', {
        'my_key': 'my_value',
    })
```

##### Checking HTTP 201 (CREATED) response

`pytest_layab.flask.assert_201` function will ensure that the status code of the response is 201 and that the `location` header contains the expected relative route.

```python
from pytest_layab.flask import assert_201


def test_created_response(client):
    response = None
    assert_201(response, '/my_new_location')
```

##### Checking response content

`pytest_layab.flask.assert_file` function will ensure that the response body will have the same content as in the provided file.

```python
from pytest_layab.flask import assert_file


def test_with_content_in_a_file(client):
    response = None
    assert_file(response, 'path/to/file/with/expected/content')
```

## Mocks

### Date-Time

You can mock current date-time.

```python
import datetime
import module_where_datetime_is_used


_date_time_for_tests = datetime.datetime(2018, 10, 11, 15, 5, 5, 663979)


class DateTimeModuleMock:
    class DateTimeMock(datetime.datetime):
        @classmethod
        def now(cls, tz=None):
            return _date_time_for_tests.replace(tzinfo=tz)
    
    class DateMock(datetime.date):
        @classmethod
        def today(cls):
            return _date_time_for_tests.date()

    timedelta = datetime.timedelta
    timezone = datetime.timezone
    datetime = DateTimeMock
    date = DateMock


def test_date_mock(monkeypatch):
    monkeypatch.setattr(module_where_datetime_is_used, "datetime", DateTimeModuleMock)
```

## How to install
1. [python 3.6+](https://www.python.org/downloads/) must be installed
2. Use pip to install module:
```sh
python -m pip install pytest_layab
```
