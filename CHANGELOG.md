# Python Common Test Changelog #

List all changes in various categories:
* Release notes: Contains all worth noting changes (breaking changes mainly)
* Enhancements
* Bug fixes
* Known issues

## Version 4.4.0 (2018-12-12) ##

### Enhancements ###

- JSONTestCase now provides post_file method.

## Version 4.3.0 (2018-12-12) ##

### Enhancements ###

- JSONTestCase can now create the application by itself (default behavior).
- Add async methods for testing asynchronous service.
- Celery mock automatically applied on testing app.

## Version 4.2.0 (2018-12-10) ##

### Enhancements ###

- JSON equality is now discarding order of values in lists within dictionary.

## Version 4.1.0 (2018-12-04) ##

### Enhancements ###

- [ADAM mock] Allow to mock health failure and success.

## Version 4.0.0 (2018-12-03) ##

### Release notes ###

- assert_201, assert_202 and assert_303 methods now expects location without http://localhost prefix.

### Enhancements ###

- assert_201 now return the location as well.

## Version 3.5.0 (2018-11-30) ##

### Enhancements ###

- Add an assert_204 method ensuring that body is empty as well.

## Version 3.4.1 (2018-11-30) ##

### Bug fixes ###

- assert_202 was expecting 201.

## Version 3.4.0 (2018-11-30) ##

### Enhancements ###

- Add an assert_303_regex method to check location, response status and return relative url at once.
- Add a get_async test method.

## Version 3.3.0 (2018-11-30) ##

### Enhancements ###

- Add an assert_201 method to check location and response status at once.
- Add an assert_202_regex method to check location, response status and return relative url at once.

### Bug fixes ###

- Use the exact same method signature from Celery in AsyncTaskProxy#apply_async.
- assert_text_regex is now working properly.

## Version 3.2.0 (2018-11-29) ##

### Enhancements ###

- Add celery mock.

## Version 3.1.1 (2018-11-29) ##

### Bug fixes ###

- [Samba mock] Allow OperationFailure to be represented as str.
- [Samba mock] pop retrievedFiles.

## Version 3.1.0 (2018-11-29) ##

### Enhancements ###

- [Samba mock] Mock echo.

### Bug fixes ###

- [Samba mock] Ensure every expected call was performed on reset.

## Version 3.0.2 (2018-11-28) ##

### Bug fixes ###

- [datetime mock] Mock datetime.datetime.utcnow().
- [datetime mock] Allow to revert to python datetime.datetime module.
- [datetime mock] Allow to provide micro seconds.

## Version 3.0.1 (2018-11-23) ##

### Bug fixes ###

- [ADAM mock] Use the default responses mock.

## Version 3.0.0 (2018-11-22) ##

### Release notes ###

- [ADAM mock] Remove add and replace methods by a single one: set.

### Enhancements ###

- [ADAM mock] Add mock_user_groups function.
- [ADAM mock] Add AdamMock class and mock_user_groups functions to __init__.

## Version 2.1.2 (2018-11-21) ##

### Bug fixes ###

- [Samba mock] Raise OperationFailure if no file was provided and retrieveFile is called.

## Version 2.1.1 (2018-11-21) ##

### Bug fixes ###

- Allow to check multiple requests sent to the same URL (in the order they were sent).

## Version 2.1.0 (2018-11-16) ##

### Enhancements ###

- Nose and Coverage are now part of dependencies.

## Version 2.0.0 (2018-11-16) ##

### Release notes ###

- Adam optional dependency which only contained Responses has been removed.

### Enhancements ###

- Responses is now a default dependency since it is commonly used for integration testing of API.

## Version 1.15.2 (2018-10-30) ##

### Bug fixes ###

- Update responses to latest version.

## Version 1.15.1 (2018-10-24) ##

### Bug fixes ###

- Handle form containing bytes.

## Version 1.15.0 (2018-10-22) ##

### Enhancements ###

- Allow to assert data sent by service to another API (form only for now).

## Version 1.14.0 (2018-10-15) ##

### Enhancements ###

- Allow to mock datetime.datetime.now().

## Version 1.13.0 (2018-10-15) ##

### Enhancements ###

- Add assert_text and assert_text_regex methods to JSONTestCase.

## Version 1.12.0 (2018-10-05) ##

### Enhancements ###

- Add replace_user_groups method to ADAM Rest mock.

## Version 1.11.0 (2018-10-05) ##

### Enhancements ###

- Add ADAM Rest mock.

## Version 1.10.2 (2018-10-01) ##

### Bug fixes ###

- Update dependencies to latest version.

## Version 1.10.1 (2018-10-01) ##

### Bug fixes ###

- Add return types for Samba Mock functions.

## Version 1.10.0 (2018-09-24) ##

### Enhancements ###

- Samba mock now supports listPath method.

## Version 1.9.1 (2018-08-20) ##

### Bug fixes ###

- Upgrade to last version of dependencies.

## Version 1.9.0 (2018-06-11) ##

### Enhancements ###

- Samba mock stores the content of the files.

## Version 1.8.1 (2018-06-11) ##

### Bug fixes ###

- Samba mock now save remote name.

## Version 1.8.0 (2018-06-11) ##

### Enhancements ###

- Add a Mock for Samba (Windows <-> Linux connections).

## Version 1.7.3 (2018-05-16) ##

### Bug fixes ###

- Proper error message in case user expects None in paths.

## Version 1.7.2 (2018-05-04) ##

### Bug fixes ###

- Handle OpenAPI parameters set at path and paths level.

## Version 1.7.1 (2018-03-24) ##

### Bug fixes ###

- Better error message in case of swagger validation failure.

## Version 1.7.0 (2018-03-05) ##

### Enhancements ###

- Introduce flask_restplus_mock.TestAPI to mock a Flask Rest Plus API.

## Version 1.6.1 (2017-12-13) ##

### Bug fixes ###

- service_tester.assert_json now consider lists as unordered.

## Version 1.6.0 (2017-12-12) ##

### Enhancements ###

- services_handler can be called with more than the port argument.

## Version 1.5.0 (2017-12-07) ##

### Enhancements ###

- Introduce services_handler module to start and stop test services.

## Version 1.4.0 (2017-11-13) ##

### Enhancements ###

- Use SERVER_ENVIRONMENT instead of deprecated ENVIRONMENT variable.

## Version 1.3.1 (2017-10-24) ##

### Bug fixes ###

- Assert Swagger does not manage path without parameters.

## Version 1.3.0 (2017-10-16) ##

### Enhancements ###

- Added kwargs to put/post methods so that headers/auth can be provided.

## Version 1.2.1 (2017-10-16) ##

### Enhancements ###

- Logging start and end of a test case should not be considered as a test by itself.

## Version 1.2.0 (2017-10-16) ##

### Enhancements ###

- Ability to validate a JSON Swagger response.

## Version 1.1.0 (2017-10-16) ##

### Enhancements ###

- Ability to check JSON response with fields as regex.

## Version 1.0.0 (2017-10-16) ##

### Release notes ###

- Initial release.
