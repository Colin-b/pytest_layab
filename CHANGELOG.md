# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [5.3.1] - 2019-04-25
### Fixed
- Handle the use of SMBConnection mock as a context manager (as it is allowed by SMBConnection).

## [5.3.0] - 2019-04-11
### Added
- version file is now public.

### Changed
- Follow keep a changelog format.
- Update responses to version 0.10.6
- Update coverage to version 4.5.3
- Update celery to version 4.3.0
- Update ldap3 to version 2.6

## [5.2.0] - 2019-03-11
### Added
- Ability to assert excel file content in JSONTestCase.

## [5.1.1] - 2019-02-27
### Fixed
- Celery mock manage exception raised inside celery task.

## [5.1.0] - 2019-02-22
### Added
- Add pytest-cov 2.6.1 as dependency.

## [5.0.1] - 2019-01-29
### Fixed
- Celery mock now allows to call methods decorated as tasks.

## [5.0.0] - 2019-01-14
### Changed
- JSONTestCase.assert_received_* now expect a specific Content-Type (can be overridden).
- JSONTestCase.received_json should not be used anymore (use related assert_* instead).
- JSONTestCase.received_text should not be used anymore (use related assert_* instead).
- JSONTestCase.received_bytes should not be used anymore (use related assert_* instead).

### Added
- JSONTestCase now provides assert_received_text_regex method.
- JSONTestCase.assert_received_* now allow to check headers.

### Fixed
- str body can now be compared to text (it was assumed as bytes).

## [4.10.1] - 2019-01-11
### Fixed
- ADAM mock now simulate the new adamrest health response (standard health).

## [4.10.0] - 2019-01-10
### Added
- Allow LDAP3 mock to send errors in case search is called.
- Allow ADAM mock to mock application groups.

## [4.9.0] - 2019-01-09
### Added
- Add a new mock for ldap3.
- Update responses to latest version (0.10.5)

## [4.8.2] - 2019-01-08
### Fixed
- Serialize date-time attributes provided to Celery mock.
- Avoid warning when providing regex as add_get_response and add_post_response parameter.

## [4.8.1] - 2018-12-20
### Fixed
- Manage services returning empty list or dict.

## [4.8.0] - 2018-12-18
### Added
- Use decorator instead of lambda to add proxy on CeleryApp.
- Initialized server is an attribute of JsonTestCase class.

## [4.7.0] - 2018-12-14
### Added
- service_tester.JSONTestCase now provides handle_202 parameter to avoid specific 202 handling.

## [4.6.0] - 2018-12-14
### Added
- service_tester.JSONTestCase now provides assert_file method.

## [4.5.0] - 2018-12-13
### Added
- service_tester now provides add_get_response and add_post_response methods.

## [4.4.0] - 2018-12-12
### Added
- service_tester.JSONTestCase now provides post_file method.

## [4.3.0] - 2018-12-12
### Added
- service_tester.JSONTestCase can now create the application by itself (default behavior).
- Add async methods for testing asynchronous service.
- Celery mock automatically applied on testing app.

## [4.2.0] - 2018-12-10
### Added
- JSON equality is now discarding order of values in lists within dictionary.

## [4.1.0] - 2018-12-04
### Added
- [ADAM mock] Allow to mock health failure and success.

## [4.0.0] - 2018-12-03
### Changed
- assert_201, assert_202 and assert_303 methods now expects location without http://localhost prefix.

### Added
- assert_201 now return the location as well.

## [3.5.0] - 2018-11-30
### Added
- Add an assert_204 method ensuring that body is empty as well.

## [3.4.1] - 2018-11-30
### Fixed
- assert_202 was expecting 201.

## [3.4.0] - 2018-11-30
### Added
- Add an assert_303_regex method to check location, response status and return relative url at once.
- Add a get_async test method.

## [3.3.0] - 2018-11-30
### Added
- Add an assert_201 method to check location and response status at once.
- Add an assert_202_regex method to check location, response status and return relative url at once.

### Fixed
- Use the exact same method signature from Celery in AsyncTaskProxy#apply_async.
- assert_text_regex is now working properly.

## [3.2.0] - 2018-11-29
### Added
- Add celery mock.

## [3.1.1] - 2018-11-29
### Fixed
- [Samba mock] Allow OperationFailure to be represented as str.
- [Samba mock] pop retrievedFiles.

## [3.1.0] - 2018-11-29
### Added
- [Samba mock] Mock echo.

### Fixed
- [Samba mock] Ensure every expected call was performed on reset.

## [3.0.2] - 2018-11-28
### Fixed
- [datetime mock] Mock datetime.datetime.utcnow().
- [datetime mock] Allow to revert to python datetime.datetime module.
- [datetime mock] Allow to provide micro seconds.

## [3.0.1] - 2018-11-23
### Fixed
- [ADAM mock] Use the default responses mock.

## [3.0.0] - 2018-11-22
### Changed
- [ADAM mock] Remove add and replace methods by a single one: set.

### Added
- [ADAM mock] Add mock_user_groups function.
- [ADAM mock] Add AdamMock class and mock_user_groups functions to __init__.

## [2.1.2] - 2018-11-21
### Fixed
- [Samba mock] Raise OperationFailure if no file was provided and retrieveFile is called.

## [2.1.1] - 2018-11-21
### Fixed
- Allow to check multiple requests sent to the same URL (in the order they were sent).

## [2.1.0] - 2018-11-16
### Added
- Nose and Coverage are now part of dependencies.

## [2.0.0] - 2018-11-16
### Changed
- Adam optional dependency which only contained Responses has been removed.

### Added
- Responses is now a default dependency since it is commonly used for integration testing of API.

## [1.15.2] - 2018-10-30
### Fixed
- Update responses to latest version.

## [1.15.1] - 2018-10-24
### Fixed
- Handle form containing bytes.

## [1.15.0] - 2018-10-22
### Added
- Allow to assert data sent by service to another API (form only for now).

## [1.14.0] - 2018-10-15
### Added
- Allow to mock datetime.datetime.now().

## [1.13.0] - 2018-10-15
### Added
- Add assert_text and assert_text_regex methods to JSONTestCase.

## [1.12.0] - 2018-10-05
### Added
- Add replace_user_groups method to ADAM Rest mock.

## [1.11.0] - 2018-10-05
### Added
- Add ADAM Rest mock.

## [1.10.2] - 2018-10-01
### Fixed
- Update dependencies to latest version.

## [1.10.1] - 2018-10-01
### Fixed
- Add return types for Samba Mock functions.

## [1.10.0] - 2018-09-24
### Added
- Samba mock now supports listPath method.

## [1.9.1] - 2018-08-20
### Fixed
- Upgrade to last version of dependencies.

## [1.9.0] - 2018-06-11
### Added
- Samba mock stores the content of the files.

## [1.8.1] - 2018-06-11
### Fixed
- Samba mock now save remote name.

## [1.8.0] - 2018-06-11
### Added
- Add a Mock for Samba (Windows <-> Linux connections).

## [1.7.3] - 2018-05-16
### Fixed
- Proper error message in case user expects None in paths.

## [1.7.2] - 2018-05-04
### Fixed
- Handle OpenAPI parameters set at path and paths level.

## [1.7.1] - 2018-03-24
### Fixed
- Better error message in case of swagger validation failure.

## [1.7.0] - 2018-03-05
### Added
- Introduce flask_restplus_mock.TestAPI to mock a Flask Rest Plus API.

## [1.6.1] - 2017-12-13
### Fixed
- service_tester.assert_json now consider lists as unordered.

## [1.6.0] - 2017-12-12
### Added
- services_handler can be called with more than the port argument.

## [1.5.0] - 2017-12-07
### Added
- Introduce services_handler module to start and stop test services.

## [1.4.0] - 2017-11-13
### Added
- Use SERVER_ENVIRONMENT instead of deprecated ENVIRONMENT variable.

## [1.3.1] - 2017-10-24
### Fixed
- Assert Swagger does not manage path without parameters.

## [1.3.0] - 2017-10-16
### Added
- Added kwargs to put/post methods so that headers/auth can be provided.

## [1.2.1] - 2017-10-16
### Added
- Logging start and end of a test case should not be considered as a test by itself.

## [1.2.0] - 2017-10-16
### Added
- Ability to validate a JSON Swagger response.

## [1.1.0] - 2017-10-16
### Added
- Ability to check JSON response with fields as regex.

## [1.0.0] - 2017-10-16
### Changed
- Initial release.

[Unreleased]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v5.2.0...HEAD
[5.2.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v5.1.1...v5.2.0
[5.1.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v5.1.0...v5.1.1
[5.1.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v5.0.1...v5.1.0
[5.0.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v5.0.0...v5.0.1
[5.0.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.10.1...v5.0.0
[4.10.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.10.0...v4.10.1
[4.10.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.9.0...v4.10.0
[4.9.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.8.2...v4.9.0
[4.8.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.8.1...v4.8.2
[4.8.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.8.0...v4.8.1
[4.8.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.7.0...v4.8.0
[4.7.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.6.0...v4.7.0
[4.6.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.5.0...v4.6.0
[4.5.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.4.0...v4.5.0
[4.4.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.3.0...v4.4.0
[4.3.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.2.0...v4.3.0
[4.2.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.1.0...v4.2.0
[4.1.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v4.0.0...v4.1.0
[4.0.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.5.0...v4.0.0
[3.5.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.4.1...v3.5.0
[3.4.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.4.0...v3.4.1
[3.4.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.3.0...v3.4.0
[3.3.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.2.0...v3.3.0
[3.2.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.1.1...v3.2.0
[3.1.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.1.0...v3.1.1
[3.1.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.0.2...v3.1.0
[3.0.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.0.1...v3.0.2
[3.0.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v3.0.0...v3.0.1
[3.0.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v2.1.2...v3.0.0
[2.1.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v2.1.1...v2.1.2
[2.1.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v2.1.0...v2.1.1
[2.1.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v2.0.0...v2.1.0
[2.0.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.15.2...v2.0.0
[1.15.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.15.1...v1.15.2
[1.15.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.15.0...v1.15.1
[1.15.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.14.0...v1.15.0
[1.14.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.13.0...v1.14.0
[1.13.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.12.0...v1.13.0
[1.12.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.11.0...v1.12.0
[1.11.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.10.2...v1.11.0
[1.10.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.10.1...v1.10.2
[1.10.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.10.0...v1.10.1
[1.10.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.9.1...v1.10.0
[1.9.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.9.0...v1.9.1
[1.9.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.8.1...v1.9.0
[1.8.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.8.0...v1.8.1
[1.8.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.7.3...v1.8.0
[1.7.3]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.7.2...v1.7.3
[1.7.2]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.7.1...v1.7.2
[1.7.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.7.0...v1.7.1
[1.7.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.6.1...v1.7.0
[1.6.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.6.0...v1.6.1
[1.6.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.5.0...v1.6.0
[1.5.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.4.0...v1.5.0
[1.4.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.3.1...v1.4.0
[1.3.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.3.0...v1.3.1
[1.3.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.2.1...v1.3.0
[1.2.1]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/compare/v1.0.0...v1.1.0
[1.0.0]: https://github.tools.digital.engie.com/GEM-Py/pycommon-test/releases/tag/v1.0.0
